from __future__ import annotations

import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.infrastructure.persistence.postgres.observation.entities.observation_tool_call import (
    ObservationToolCall,
)


class ObservationToolCallRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, tool_call: ObservationToolCall) -> ObservationToolCall:
        self.session.add(tool_call)
        await self.session.commit()
        await self.session.refresh(tool_call)
        return tool_call

    async def get_by_id(self, tool_call_id: uuid.UUID) -> ObservationToolCall | None:
        result = await self.session.execute(
            select(ObservationToolCall).where(ObservationToolCall.id == tool_call_id)
        )
        return result.scalar_one_or_none()

    async def list_by_question(
        self, question_id: uuid.UUID, limit: int = 100, offset: int = 0
    ) -> list[ObservationToolCall]:
        result = await self.session.execute(
            select(ObservationToolCall)
            .where(ObservationToolCall.question_id == question_id)
            .order_by(ObservationToolCall.executed_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())
