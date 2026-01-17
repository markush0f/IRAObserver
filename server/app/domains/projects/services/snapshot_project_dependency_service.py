from __future__ import annotations

"""Snapshot project dependency domain services."""

import uuid

from app.domains.analysis.models.dto.dependency import ProjectDependencyCreate
from app.infrastructure.persistence.postgres.analysis.entities.project_dependency import ProjectDependency
from app.domains.analysis.repository.project_dependency_repository import (
    ProjectDependencyRepository,
)


class SnapshotProjectDependencyService:
    """Application logic for snapshot dependency storage."""

    def __init__(
        self, project_dependency_repository: ProjectDependencyRepository
    ) -> None:
        self.project_dependency_repository = project_dependency_repository

    async def create_snapshot_dependencies(
        self, dependencies: list[ProjectDependencyCreate]
    ) -> list[ProjectDependency]:
        """Create dependency entries for a snapshot."""
        entries = [
            ProjectDependency(
                snapshot_id=dependency.snapshot_id,
                name=dependency.name,
                version=dependency.version,
                ecosystem=dependency.ecosystem,
                scope=dependency.scope,
                source_file=dependency.source_file,
            )
            for dependency in dependencies
        ]
        if not entries:
            return []
        return await self.project_dependency_repository.create_many(entries)

    async def get_snapshot_dependencies(
        self, snapshot_id: uuid.UUID
    ) -> list[ProjectDependency]:
        """Return dependencies for a snapshot."""
        return await self.project_dependency_repository.list_by_snapshot(snapshot_id)
