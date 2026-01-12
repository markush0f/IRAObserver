from __future__ import annotations

"""Snapshot domain services."""

from datetime import datetime, timezone
import logging
import uuid
from typing import Any

from app.domains.projects.models.dto.snapshot import SnapshotPage, SnapshotPublic
from app.domains.projects.models.entities.snapshot import Snapshot
from app.domains.projects.repository.snapshot_repository import SnapshotRepository
from app.domains.projects.services.project_service import ProjectService


class SnapshotService:
    """Application logic for snapshots."""

    logger = logging.getLogger(__name__)

    def __init__(
        self,
        snapshot_repository: SnapshotRepository,
        project_service: ProjectService,
    ) -> None:
        self.snapshot_repository = snapshot_repository
        self.project_service = project_service

    async def create_snapshot(
        self,
        project_id: uuid.UUID,
        summary_json: dict[str, Any],
        commit_hash: str | None = None,
    ) -> Snapshot:
        """Create a snapshot for an existing project."""
        self.logger.info("Creating snapshot project_id=%s", project_id)
        project = await self.project_service.get_project(project_id)
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

    async def list_snapshots(
        self,
        project_id: uuid.UUID,
        limit: int = 100,
        offset: int = 0,
        start_at: datetime | None = None,
        end_at: datetime | None = None,
    ) -> SnapshotPage | None:
        """List snapshots for a project with pagination and date filters."""
        self.logger.info("Listing snapshots project_id=%s", project_id)
        project = await self.project_service.get_project(project_id)
        if not project:
            return None

        snapshots = await self.snapshot_repository.list_by_project(
            project_id=project_id,
            limit=limit,
            offset=offset,
            start_at=start_at,
            end_at=end_at,
        )
        total = await self.snapshot_repository.count_by_project(
            project_id=project_id,
            start_at=start_at,
            end_at=end_at,
        )
        items = [
            SnapshotPublic(
                id=snapshot.id,
                project_id=snapshot.project_id,
                commit_hash=snapshot.commit_hash,
                summary_json=snapshot.summary_json,
                created_at=snapshot.created_at,
            )
            for snapshot in snapshots
        ]
        return SnapshotPage(items=items, total=total, limit=limit, offset=offset)
