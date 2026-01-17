from __future__ import annotations

import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.infrastructure.persistence.postgres.observation.entities.observation_session import (
    ObservationSession,
)


class ObservationSessionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, session_entry: ObservationSession) -> ObservationSession:
        self.session.add(session_entry)
        await self.session.commit()
        await self.session.refresh(session_entry)
        return session_entry

    async def get_by_id(self, session_id: uuid.UUID) -> ObservationSession | None:
        result = await self.session.execute(
            select(ObservationSession).where(ObservationSession.id == session_id)
        )
        return result.scalar_one_or_none()

    async def list_by_project(
        self, project_id: uuid.UUID, limit: int = 100, offset: int = 0
    ) -> list[ObservationSession]:
        result = await self.session.execute(
            select(ObservationSession)
            .where(ObservationSession.project_id == project_id)
            .order_by(ObservationSession.started_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())
