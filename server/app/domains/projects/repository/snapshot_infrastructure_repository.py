from __future__ import annotations

"""Snapshot infrastructure repository for persistence access."""

import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.domains.projects.models.entities.snapshot_infrastructure import (
    SnapshotInfrastructure,
)


class SnapshotInfrastructureRepository:
    """Data access layer for snapshot infrastructure."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_many(
        self, entries: list[SnapshotInfrastructure]
    ) -> list[SnapshotInfrastructure]:
        """Persist snapshot infrastructure entries."""
        self.session.add_all(entries)
        await self.session.commit()
        for entry in entries:
            await self.session.refresh(entry)
        return entries

    async def list_by_snapshot(
        self, snapshot_id: uuid.UUID
    ) -> list[SnapshotInfrastructure]:
        """List infrastructure components for a snapshot."""
        result = await self.session.execute(
            select(SnapshotInfrastructure).where(
                SnapshotInfrastructure.snapshot_id == snapshot_id
            )
        )
        return list(result.scalars().all())
