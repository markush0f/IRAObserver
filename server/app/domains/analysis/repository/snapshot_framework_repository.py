from __future__ import annotations

"""Snapshot framework repository for persistence access."""

import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.infrastructure.persistence.postgres.analysis.entities.snapshot_framework import SnapshotFramework


class SnapshotFrameworkRepository:
    """Data access layer for snapshot frameworks."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_many(
        self, entries: list[SnapshotFramework]
    ) -> list[SnapshotFramework]:
        """Persist snapshot framework entries."""
        self.session.add_all(entries)
        await self.session.commit()
        for entry in entries:
            await self.session.refresh(entry)
        return entries

    async def list_by_snapshot(
        self, snapshot_id: uuid.UUID
    ) -> list[SnapshotFramework]:
        """List frameworks for a snapshot."""
        result = await self.session.execute(
            select(SnapshotFramework).where(
                SnapshotFramework.snapshot_id == snapshot_id
            )
        )
        return list(result.scalars().all())
