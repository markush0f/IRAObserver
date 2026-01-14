from __future__ import annotations

"""Project tree domain services."""

from app.analysis.structure.tree import build_project_tree
from app.domains.analysis.repository.analysis_ignored_directory_repository import (
    AnalysisIgnoredDirectoryRepository,
)
from app.domains.projects.services.project_service import ProjectService
from app.infrastructure.external.source.orchestartor import prepare_source
from app.domains.projects.models.source_type import SourceType
import uuid


class ProjectTreeService:
    """Application logic for project tree retrieval."""

    def __init__(
        self,
        project_service: ProjectService,
        ignored_directory_repository: AnalysisIgnoredDirectoryRepository,
    ) -> None:
        self.project_service = project_service
        self.ignored_directory_repository = ignored_directory_repository

    async def get_project_tree(self, project_id: uuid.UUID):
        """Return the tree for a project."""
        project = await self.project_service.get_project(project_id)
        if not project:
            return None

        source_path = prepare_source(
            source_type=SourceType(project.source_type),
            source_ref=project.source_ref,
            project_id=project.id,
            allow_clone=False,
        )
        ignored_directories = await self.ignored_directory_repository.list_active()
        return build_project_tree(
            source_path, ignored_directories={entry.name for entry in ignored_directories}
        )
