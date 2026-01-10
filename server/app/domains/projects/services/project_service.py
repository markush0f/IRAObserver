from __future__ import annotations

"""Project domain services."""

from datetime import datetime, timezone
import uuid

from app.domains.projects.models.dto.project import ProjectCreate, ProjectPublic
from app.domains.projects.models.entities.project import Project
from app.domains.projects.models.source_type import SourceType
from app.domains.projects.repository.project_repository import ProjectRepository
from app.infrastructure.external.source.orchestartor import prepare_source


class ProjectService:
    """Application logic for projects."""
    def __init__(
        self,
        project_repository: ProjectRepository,
    ) -> None:
        self.project_repository = project_repository

    async def create_project(
        self, data: ProjectCreate, actor_role: str
    ) -> ProjectPublic:
        """Create a project if the actor has admin privileges."""
        if actor_role != "admin":
            raise PermissionError("admin role required")
        if data.source_type not in {SourceType.GIT, SourceType.LOCAL}:
            raise ValueError("invalid source_type")

        project = Project(
            name=data.name,
            description=data.description,
            source_type=data.source_type.value,
            source_ref=data.source_ref,
            created_at=datetime.now(timezone.utc),
        )

        created = await self.project_repository.create(project)
        return ProjectPublic.model_validate(created)

    async def prepare_project_source(
        self, project_id: uuid.UUID, actor_role: str
    ) -> None:
        """Prepare project source content based on its configured type."""
        if actor_role != "admin":
            raise PermissionError("admin role required")

        project = await self.project_repository.get_by_id(project_id)
        if not project:
            raise ValueError("project not found")

        prepare_source(
            source_type=SourceType(project.source_type),
            source_ref=project.source_ref,
        )
