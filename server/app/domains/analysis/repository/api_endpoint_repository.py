from __future__ import annotations

"""API endpoint repository for persistence access."""

import uuid

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.infrastructure.persistence.postgres.analysis.entities.api_endpoint import ApiEndpoint
from app.infrastructure.persistence.postgres.projects.entities.snapshot import Snapshot


class ApiEndpointRepository:
    """Data access layer for API endpoints."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_many(
        self, entries: list[ApiEndpoint]
    ) -> list[ApiEndpoint]:
        """Persist API endpoint entries."""
        self.session.add_all(entries)
        await self.session.commit()
        for entry in entries:
            await self.session.refresh(entry)
        return entries

    async def list_by_snapshot(self, snapshot_id: uuid.UUID) -> list[ApiEndpoint]:
        """List API endpoints for a snapshot."""
        result = await self.session.execute(
            select(ApiEndpoint).where(ApiEndpoint.snapshot_id == snapshot_id)
        )
        return list(result.scalars().all())

    async def list_by_project(
        self,
        project_id: uuid.UUID,
        limit: int = 100,
        offset: int = 0,
        http_method: str | None = None,
    ) -> list[ApiEndpoint]:
        """List API endpoints for a project."""
        query = (
            select(ApiEndpoint)
            .join(Snapshot, ApiEndpoint.snapshot_id == Snapshot.id)
            .where(Snapshot.project_id == project_id)
        )
        if http_method:
            query = query.where(ApiEndpoint.http_method == http_method)
        result = await self.session.execute(
            query.order_by(ApiEndpoint.created_at.desc()).limit(limit).offset(offset)
        )
        return list(result.scalars().all())

    async def count_by_project(
        self, project_id: uuid.UUID, http_method: str | None = None
    ) -> int:
        """Count API endpoints for a project."""
        query = (
            select(func.count())
            .select_from(ApiEndpoint)
            .join(Snapshot, ApiEndpoint.snapshot_id == Snapshot.id)
            .where(Snapshot.project_id == project_id)
        )
        if http_method:
            query = query.where(ApiEndpoint.http_method == http_method)
        result = await self.session.execute(query)
        return int(result.scalar_one())
