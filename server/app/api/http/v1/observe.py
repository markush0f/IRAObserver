from fastapi import APIRouter, Depends, Request
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
    request: Request,
    project_id: uuid.UUID,
    question: str,
    db: AsyncSession = Depends(get_db),
):
    # Get infrastructure from app.state
    mcp = request.app.state.mcp
    schema_extractor = request.app.state.schema_extractor

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
        mcp=mcp,
        schema_extractor=schema_extractor,
    )

    # Create LLM client
    llm_client = OpenAILLMClient(
        api_key="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",
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
