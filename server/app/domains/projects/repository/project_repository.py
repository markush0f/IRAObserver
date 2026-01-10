from __future__ import annotations

"""Project repository for persistence access."""

import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.domains.projects.models.entities.project import Project


class ProjectRepository:
    """Data access layer for projects."""
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, project: Project) -> Project:
        """Persist a project and return the stored entity."""
        self.session.add(project)
        await self.session.commit()
        await self.session.refresh(project)
        return project

    async def get_by_id(self, project_id: uuid.UUID) -> Project | None:
        """Return a project by id or None."""
        result = await self.session.execute(
            select(Project).where(Project.id == project_id)
        )
        return result.scalar_one_or_none()

    async def list(self, limit: int = 100, offset: int = 0) -> list[Project]:
        """List projects with pagination."""
        result = await self.session.execute(
            select(Project).limit(limit).offset(offset)
        )
        return list(result.scalars().all())
