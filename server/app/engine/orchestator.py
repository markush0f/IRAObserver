from __future__ import annotations

"""Observation orchestration for LLM + persistence."""

from typing import Any, Protocol
import uuid
from openai.types.chat import ChatCompletionToolUnionParam

from app.domains.observation.models.dto.conclusion import (
    ObservationConclusionCreate,
    ObservationConclusionPublic,
)
from app.domains.observation.models.dto.question import ObservationQuestionCreate
from app.domains.observation.models.dto.session import (
    ObservationSessionCreate,
    ObservationSessionPublic,
)
from app.domains.observation.services.observation_service import ObservationService

from app.engine.llm_types import LLMResponse


class LLMClient(Protocol):
    async def generate(
        self,
        question: str,
        tools: list[ChatCompletionToolUnionParam],
        tool_results: list[dict[str, Any]] | None = None,
    ) -> LLMResponse:
        """Generate an answer and optional tool calls for a question."""
        ...


class ObservationOrchestrator:
    """Coordinate questions, LLM responses, MCP tools, and persistence."""

    def __init__(
        self,
        observation_service: ObservationService,
    ) -> None:
        self.observation_service = observation_service

    async def start_session(
        self,
        project_id: uuid.UUID,
        llm_provider: str,
        llm_model: str,
    ) -> ObservationSessionPublic:
        return await self.observation_service.create_session(
            ObservationSessionCreate(
                project_id=project_id,
                llm_provider=llm_provider,
                llm_model=llm_model,
            )
        )

    async def handle_question(
        self,
        session_id: uuid.UUID,
        question: str,
        llm_client: LLMClient,
    ) -> ObservationConclusionPublic:
        # Persist the incoming question
        question_entry = await self.observation_service.create_question(
            ObservationQuestionCreate(
                session_id=session_id,
                raw_question=question,
            )
        )

        initial = await llm_client.generate(
            question=question,
            tools=[],
        )

        return await self.observation_service.create_conclusion(
            ObservationConclusionCreate(
                question_id=question_entry.id,
                explanation=initial.answer,
            )
        )
