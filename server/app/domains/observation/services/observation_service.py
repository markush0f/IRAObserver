from __future__ import annotations

"""Observation domain services."""

import uuid

from app.domains.observation.models.dto.conclusion import (
    ObservationConclusionCreate,
    ObservationConclusionPublic,
)
from app.domains.observation.models.dto.question import (
    ObservationQuestionCreate,
    ObservationQuestionPublic,
)
from app.domains.observation.models.dto.session import (
    ObservationSessionCreate,
    ObservationSessionPublic,
)
from app.domains.observation.models.dto.tool_call import (
    ObservationToolCallCreate,
    ObservationToolCallPublic,
)
from app.infrastructure.persistence.postgres.observation.entities.observation_conclusion import (
    ObservationConclusion,
)
from app.infrastructure.persistence.postgres.observation.entities.observation_question import (
    ObservationQuestion,
)
from app.infrastructure.persistence.postgres.observation.entities.observation_session import (
    ObservationSession,
)
from app.infrastructure.persistence.postgres.observation.entities.observation_tool_call import (
    ObservationToolCall,
)
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


class ObservationService:
    """Application logic for observation sessions and related records."""

    def __init__(
        self,
        session_repository: ObservationSessionRepository,
        question_repository: ObservationQuestionRepository,
        tool_call_repository: ObservationToolCallRepository,
        conclusion_repository: ObservationConclusionRepository,
    ) -> None:
        self.session_repository = session_repository
        self.question_repository = question_repository
        self.tool_call_repository = tool_call_repository
        self.conclusion_repository = conclusion_repository

    async def create_session(
        self, data: ObservationSessionCreate
    ) -> ObservationSessionPublic:
        payload: dict[str, object] = {
            "project_id": data.project_id,
            "llm_provider": data.llm_provider,
            "llm_model": data.llm_model,
        }
        if data.started_at is not None:
            payload["started_at"] = data.started_at
        session_entry = ObservationSession(**payload)
        created = await self.session_repository.create(session_entry)
        return ObservationSessionPublic.model_validate(created)

    async def get_session(
        self, session_id: uuid.UUID
    ) -> ObservationSessionPublic | None:
        session_entry = await self.session_repository.get_by_id(session_id)
        if not session_entry:
            return None
        return ObservationSessionPublic.model_validate(session_entry)

    async def list_sessions_by_project(
        self, project_id: uuid.UUID, limit: int = 100, offset: int = 0
    ) -> list[ObservationSessionPublic]:
        sessions = await self.session_repository.list_by_project(
            project_id=project_id,
            limit=limit,
            offset=offset,
        )
        return [ObservationSessionPublic.model_validate(session) for session in sessions]

    async def create_question(
        self, data: ObservationQuestionCreate
    ) -> ObservationQuestionPublic:
        payload: dict[str, object] = {
            "session_id": data.session_id,
            "raw_question": data.raw_question,
            "normalized_intent": data.normalized_intent,
        }
        if data.created_at is not None:
            payload["created_at"] = data.created_at
        question = ObservationQuestion(**payload)
        created = await self.question_repository.create(question)
        return ObservationQuestionPublic.model_validate(created)

    async def get_question(
        self, question_id: uuid.UUID
    ) -> ObservationQuestionPublic | None:
        question = await self.question_repository.get_by_id(question_id)
        if not question:
            return None
        return ObservationQuestionPublic.model_validate(question)

    async def list_questions_by_session(
        self, session_id: uuid.UUID, limit: int = 100, offset: int = 0
    ) -> list[ObservationQuestionPublic]:
        questions = await self.question_repository.list_by_session(
            session_id=session_id,
            limit=limit,
            offset=offset,
        )
        return [
            ObservationQuestionPublic.model_validate(question)
            for question in questions
        ]

    async def create_tool_call(
        self, data: ObservationToolCallCreate
    ) -> ObservationToolCallPublic:
        payload: dict[str, object] = {
            "question_id": data.question_id,
            "tool_name": data.tool_name,
            "tool_arguments": data.tool_arguments,
            "tool_result": data.tool_result,
        }
        if data.executed_at is not None:
            payload["executed_at"] = data.executed_at
        tool_call = ObservationToolCall(**payload)
        created = await self.tool_call_repository.create(tool_call)
        return ObservationToolCallPublic.model_validate(created)

    async def get_tool_call(
        self, tool_call_id: uuid.UUID
    ) -> ObservationToolCallPublic | None:
        tool_call = await self.tool_call_repository.get_by_id(tool_call_id)
        if not tool_call:
            return None
        return ObservationToolCallPublic.model_validate(tool_call)

    async def list_tool_calls_by_question(
        self, question_id: uuid.UUID, limit: int = 100, offset: int = 0
    ) -> list[ObservationToolCallPublic]:
        tool_calls = await self.tool_call_repository.list_by_question(
            question_id=question_id,
            limit=limit,
            offset=offset,
        )
        return [
            ObservationToolCallPublic.model_validate(tool_call)
            for tool_call in tool_calls
        ]

    async def create_conclusion(
        self, data: ObservationConclusionCreate
    ) -> ObservationConclusionPublic:
        payload: dict[str, object] = {
            "question_id": data.question_id,
            "explanation": data.explanation,
        }
        if data.generated_at is not None:
            payload["generated_at"] = data.generated_at
        conclusion = ObservationConclusion(**payload)
        created = await self.conclusion_repository.create(conclusion)
        return ObservationConclusionPublic.model_validate(created)

    async def get_conclusion(
        self, conclusion_id: uuid.UUID
    ) -> ObservationConclusionPublic | None:
        conclusion = await self.conclusion_repository.get_by_id(conclusion_id)
        if not conclusion:
            return None
        return ObservationConclusionPublic.model_validate(conclusion)

    async def list_conclusions_by_question(
        self, question_id: uuid.UUID, limit: int = 100, offset: int = 0
    ) -> list[ObservationConclusionPublic]:
        conclusions = await self.conclusion_repository.list_by_question(
            question_id=question_id,
            limit=limit,
            offset=offset,
        )
        return [
            ObservationConclusionPublic.model_validate(conclusion)
            for conclusion in conclusions
        ]
