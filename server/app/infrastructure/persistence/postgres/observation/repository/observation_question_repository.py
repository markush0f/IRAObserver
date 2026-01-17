from __future__ import annotations

import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.infrastructure.persistence.postgres.observation.entities.observation_question import (
    ObservationQuestion,
)


class ObservationQuestionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, question: ObservationQuestion) -> ObservationQuestion:
        self.session.add(question)
        await self.session.commit()
        await self.session.refresh(question)
        return question

    async def get_by_id(self, question_id: uuid.UUID) -> ObservationQuestion | None:
        result = await self.session.execute(
            select(ObservationQuestion).where(ObservationQuestion.id == question_id)
        )
        return result.scalar_one_or_none()

    async def list_by_session(
        self, session_id: uuid.UUID, limit: int = 100, offset: int = 0
    ) -> list[ObservationQuestion]:
        result = await self.session.execute(
            select(ObservationQuestion)
            .where(ObservationQuestion.session_id == session_id)
            .order_by(ObservationQuestion.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())
