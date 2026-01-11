from __future__ import annotations

"""Snapshot domain services."""

from datetime import datetime, timezone
import logging
import uuid
from typing import Any

from app.domains.projects.models.entities.snapshot import Snapshot
from app.domains.projects.repository.project_repository import ProjectRepository
from app.domains.projects.repository.snapshot_repository import SnapshotRepository


class SnapshotService:
    """Application logic for snapshots."""

    logger = logging.getLogger(__name__)

    def __init__(
        self,
        snapshot_repository: SnapshotRepository,
        project_repository: ProjectRepository,
    ) -> None:
        self.snapshot_repository = snapshot_repository
        self.project_repository = project_repository

    async def create_snapshot(
        self,
        project_id: uuid.UUID,
        summary_json: dict[str, Any],
        commit_hash: str | None = None,
    ) -> Snapshot:
        """Create a snapshot for an existing project."""
        self.logger.info("Creating snapshot project_id=%s", project_id)
        project = await self.project_repository.get_by_id(project_id)
        if not project:
            raise ValueError("project not found")

        snapshot = Snapshot(
            project_id=project_id,
            commit_hash=commit_hash,
            summary_json=summary_json,
            created_at=datetime.now(timezone.utc),
        )
        return await self.snapshot_repository.create(snapshot)

    async def get_latest_snapshot(self, project_id: uuid.UUID) -> Snapshot | None:
        """Return the latest snapshot for a project."""
        return await self.snapshot_repository.get_latest_by_project(project_id)
