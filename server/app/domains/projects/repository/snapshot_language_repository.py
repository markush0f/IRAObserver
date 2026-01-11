from __future__ import annotations

"""Snapshot language repository for persistence access."""

import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.domains.projects.models.entities.snapshot_language import SnapshotLanguage


class SnapshotLanguageRepository:
    """Data access layer for snapshot languages."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_many(
        self, entries: list[SnapshotLanguage]
    ) -> list[SnapshotLanguage]:
        """Persist snapshot language entries."""
        self.session.add_all(entries)
        await self.session.commit()
        for entry in entries:
            await self.session.refresh(entry)
        return entries

    async def list_by_snapshot(
        self, snapshot_id: uuid.UUID
    ) -> list[SnapshotLanguage]:
        """List languages for a snapshot."""
        result = await self.session.execute(
            select(SnapshotLanguage).where(SnapshotLanguage.snapshot_id == snapshot_id)
        )
        return list(result.scalars().all())
