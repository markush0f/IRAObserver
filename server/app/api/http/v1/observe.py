from fastapi import APIRouter, Depends
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.engine.orchestator import ObservationOrchestrator
from app.infrastructure.external.llm.openai_client import OpenAILLMClient
from app.domains.observation.services.observation_service import ObservationService
from app.core.db import get_db
from app.infrastructure.persistence.postgres.observation.repository.observation_conclusion_repository import (
    ObservationConclusionRepository,
)
from app.infrastructure.persistence.postgres.observation.repository.observation_question_repository import (
    ObservationQuestionRepository,
)
from app.infrastructure.persistence.postgres.observation.repository.observation_session_repository import (
    ObservationSessionRepository,
)
from app.infrastructure.persistence.postgres.observation.repository.observation_tool_call_repository import (
    ObservationToolCallRepository,
)

router = APIRouter(prefix="/observe", tags=["observe"])


@router.post("/observe")
async def observe_project(
    project_id: uuid.UUID,
    question: str,
    db: AsyncSession = Depends(get_db),
):
    # Create services
    observation_service = ObservationService(
        session_repository=ObservationSessionRepository(db),
        question_repository=ObservationQuestionRepository(db),
        tool_call_repository=ObservationToolCallRepository(db),
        conclusion_repository=ObservationConclusionRepository(db),
    )

    # Create orchestrator
    orchestrator = ObservationOrchestrator(
        observation_service=observation_service,
    )

    # Create LLM client
    llm_client = OpenAILLMClient(
        api_key="",
        model="gpt-4.1",
    )

    # Start session
    session = await orchestrator.start_session(
        project_id=project_id,
        llm_provider=llm_client.provider,
        llm_model="gpt-4.1",
    )

    # Ask question
    conclusion = await orchestrator.handle_question(
        session_id=session.id,
        question=question,
        llm_client=llm_client,
    )

    return {
        "explanation": conclusion.explanation,
    }
