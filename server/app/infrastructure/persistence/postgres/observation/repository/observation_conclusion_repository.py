from __future__ import annotations

import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.infrastructure.persistence.postgres.observation.entities.observation_conclusion import (
    ObservationConclusion,
)


class ObservationConclusionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(
        self, conclusion: ObservationConclusion
    ) -> ObservationConclusion:
        self.session.add(conclusion)
        await self.session.commit()
        await self.session.refresh(conclusion)
        return conclusion

    async def get_by_id(self, conclusion_id: uuid.UUID) -> ObservationConclusion | None:
        result = await self.session.execute(
            select(ObservationConclusion).where(
                ObservationConclusion.id == conclusion_id
            )
        )
        return result.scalar_one_or_none()

    async def list_by_question(
        self, question_id: uuid.UUID, limit: int = 100, offset: int = 0
    ) -> list[ObservationConclusion]:
        result = await self.session.execute(
            select(ObservationConclusion)
            .where(ObservationConclusion.question_id == question_id)
            .order_by(ObservationConclusion.generated_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())
