from __future__ import annotations

"""API endpoint repository for persistence access."""

import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.domains.analysis.models.entities.api_endpoint import ApiEndpoint


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
