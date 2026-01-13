from __future__ import annotations

"""Project dependency repository for persistence access."""

import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.domains.analysis.models.entities.project_dependency import ProjectDependency


class ProjectDependencyRepository:
    """Data access layer for project dependencies."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_many(
        self, entries: list[ProjectDependency]
    ) -> list[ProjectDependency]:
        """Persist project dependency entries."""
        self.session.add_all(entries)
        await self.session.commit()
        for entry in entries:
            await self.session.refresh(entry)
        return entries

    async def list_by_snapshot(
        self, snapshot_id: uuid.UUID
    ) -> list[ProjectDependency]:
        """List dependencies for a snapshot."""
        result = await self.session.execute(
            select(ProjectDependency).where(
                ProjectDependency.snapshot_id == snapshot_id
            )
        )
        return list(result.scalars().all())
