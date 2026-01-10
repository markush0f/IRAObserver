from __future__ import annotations

"""Project domain services."""

from datetime import datetime, timezone
import logging
import uuid

from app.domains.projects.models.dto.project import ProjectCreate, ProjectPublic
from app.domains.projects.models.entities.project import Project
from app.domains.projects.models.source_type import SourceType
from app.domains.projects.repository.project_repository import ProjectRepository
from app.infrastructure.external.source.orchestartor import prepare_source


class ProjectService:
    """Application logic for projects."""
    logger = logging.getLogger(__name__)

    def __init__(
        self,
        project_repository: ProjectRepository,
    ) -> None:
        self.project_repository = project_repository

    async def create_project(
        self, data: ProjectCreate, actor_role: str
    ) -> ProjectPublic:
        """Create a project if the actor has admin privileges."""
        self.logger.info("Creating project name=%s source_type=%s", data.name, data.source_type)
        if actor_role != "admin":
            raise PermissionError("admin role required")
        if data.source_type not in {SourceType.GIT, SourceType.LOCAL}:
            raise ValueError("invalid source_type")

        if data.source_type == SourceType.GIT:
            try:
                local_path = prepare_source(
                    source_type=data.source_type,
                    source_ref=data.source_ref,
                )
                self.logger.info("Cloned git source to %s", local_path)
            except Exception as exc:
                self.logger.warning("Git clone failed source_ref=%s error=%s", data.source_ref, exc)
                raise ValueError("git repository not found or unreachable") from exc

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
        self.logger.info("Preparing project source project_id=%s", project_id)
        if actor_role != "admin":
            raise PermissionError("admin role required")

        project = await self.project_repository.get_by_id(project_id)
        if not project:
            raise ValueError("project not found")

        prepare_source(
            source_type=SourceType(project.source_type),
            source_ref=project.source_ref,
        )
