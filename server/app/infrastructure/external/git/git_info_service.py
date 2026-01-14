from __future__ import annotations

"""Git information service."""

import uuid

from app.domains.projects.models.source_type import SourceType
from app.domains.projects.services.project_service import ProjectService
from app.infrastructure.external.source.orchestartor import prepare_source
from app.infrastructure.external.git.branches import list_local_branches
from app.infrastructure.external.git.commits import GitCommitInfo, list_recent_commits


class GitInfoService:
    """Application logic for git metadata retrieval."""

    def __init__(self, project_service: ProjectService) -> None:
        self.project_service = project_service

    async def list_branches(self, project_id: uuid.UUID) -> list[str] | None:
        """Return local git branches for a project."""
        project = await self.project_service.get_project(project_id)
        if not project:
            return None

        source_path = prepare_source(
            source_type=SourceType(project.source_type),
            source_ref=project.source_ref,
            project_id=project.id,
            allow_clone=False,
        )
        return list_local_branches(source_path)

    async def list_commits(
        self, project_id: uuid.UUID, limit: int = 20
    ) -> list[GitCommitInfo] | None:
        """Return recent commits for a project."""
        project = await self.project_service.get_project(project_id)
        if not project:
            return None

        source_path = prepare_source(
            source_type=SourceType(project.source_type),
            source_ref=project.source_ref,
            project_id=project.id,
            allow_clone=False,
        )
        return list_recent_commits(source_path, limit=limit)
