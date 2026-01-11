from __future__ import annotations

"""Snapshot repository for persistence access."""

import logging
import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.domains.projects.models.entities.snapshot import Snapshot


class SnapshotRepository:
    """Data access layer for snapshots."""

    logger = logging.getLogger(__name__)

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, snapshot: Snapshot) -> Snapshot:
        """Persist a snapshot and return the stored entity."""
        self.logger.info("Creating snapshot project_id=%s", snapshot.project_id)
        self.session.add(snapshot)
        await self.session.commit()
        await self.session.refresh(snapshot)
        return snapshot

    async def get_by_id(self, snapshot_id: uuid.UUID) -> Snapshot | None:
        """Return a snapshot by id or None."""
        result = await self.session.execute(
            select(Snapshot).where(Snapshot.id == snapshot_id)
        )
        return result.scalar_one_or_none()

    async def list_by_project(self, project_id: uuid.UUID) -> list[Snapshot]:
        """List snapshots for a project."""
        result = await self.session.execute(
            select(Snapshot).where(Snapshot.project_id == project_id)
        )
        return list(result.scalars().all())

    async def get_latest_by_project(self, project_id: uuid.UUID) -> Snapshot | None:
        """Return the latest snapshot for a project or None."""
        result = await self.session.execute(
            select(Snapshot)
            .where(Snapshot.project_id == project_id)
            .order_by(Snapshot.created_at.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()
