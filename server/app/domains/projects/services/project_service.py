from __future__ import annotations

from datetime import datetime, timezone

from app.domains.projects.models.dto.project import ProjectCreate, ProjectPublic
from app.domains.projects.models.entities.project import Project
from app.domains.projects.repository.project_repository import ProjectRepository


class ProjectService:
    def __init__(self, project_repository: ProjectRepository) -> None:
        self.project_repository = project_repository

    async def create_project(self, data: ProjectCreate, actor_role: str) -> ProjectPublic:
        if actor_role != "admin":
            raise PermissionError("admin role required")

        project = Project(
            name=data.name,
            description=data.description,
            source_type=data.source_type,
            source_ref=data.source_ref,
            created_at=datetime.now(timezone.utc),
        )
        created = await self.project_repository.create(project)
        return ProjectPublic.model_validate(created)
