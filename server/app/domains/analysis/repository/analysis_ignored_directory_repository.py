from __future__ import annotations

"""Postgres repository for analysis ignored directories."""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.analysis.models.entities.analysis_ignored_directory import (
    AnalysisIgnoredDirectory,
)


class AnalysisIgnoredDirectoryRepository:
    """Data access for analysis ignored directories."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(
        self, directory: AnalysisIgnoredDirectory
    ) -> AnalysisIgnoredDirectory:
        """Persist an ignored directory and return the stored entity."""
        self.session.add(directory)
        await self.session.commit()
        await self.session.refresh(directory)
        return directory

    async def get_by_id(
        self, directory_id: uuid.UUID
    ) -> AnalysisIgnoredDirectory | None:
        """Return an ignored directory by id or None."""
        result = await self.session.execute(
            select(AnalysisIgnoredDirectory).where(
                AnalysisIgnoredDirectory.id == directory_id
            )
        )
        return result.scalar_one_or_none()

    async def get_by_name(self, name: str) -> AnalysisIgnoredDirectory | None:
        """Return an ignored directory by name or None."""
        result = await self.session.execute(
            select(AnalysisIgnoredDirectory).where(
                AnalysisIgnoredDirectory.name == name
            )
        )
        return result.scalar_one_or_none()

    async def list(
        self, limit: int = 100, offset: int = 0
    ) -> list[AnalysisIgnoredDirectory]:
        """List ignored directories with pagination."""
        result = await self.session.execute(
            select(AnalysisIgnoredDirectory).limit(limit).offset(offset)
        )
        return list(result.scalars().all())

    async def list_active(self) -> list[AnalysisIgnoredDirectory]:
        """List active ignored directories."""
        result = await self.session.execute(
            select(AnalysisIgnoredDirectory).where(
                AnalysisIgnoredDirectory.is_active.is_(True)
            )
        )
        return list(result.scalars().all())
