from __future__ import annotations

"""Snapshot infrastructure domain services."""

import uuid

from app.domains.projects.models.entities.snapshot_infrastructure import (
    SnapshotInfrastructure,
)
from app.domains.projects.repository.snapshot_infrastructure_repository import (
    SnapshotInfrastructureRepository,
)


class SnapshotInfrastructureService:
    """Application logic for snapshot infrastructure storage."""

    def __init__(
        self,
        snapshot_infrastructure_repository: SnapshotInfrastructureRepository,
    ) -> None:
        self.snapshot_infrastructure_repository = snapshot_infrastructure_repository

    async def create_snapshot_infrastructure(
        self, snapshot_id: uuid.UUID, components: list[str]
    ) -> list[SnapshotInfrastructure]:
        """Create snapshot infrastructure entries for detected components."""
        entries = [
            SnapshotInfrastructure(
                snapshot_id=snapshot_id,
                component=component,
            )
            for component in components
        ]
        if not entries:
            return []
        return await self.snapshot_infrastructure_repository.create_many(entries)

    async def get_snapshot_infrastructure(
        self, snapshot_id: uuid.UUID
    ) -> list[str]:
        """Return infrastructure components for a snapshot."""
        entries = await self.snapshot_infrastructure_repository.list_by_snapshot(
            snapshot_id
        )
        return [entry.component for entry in entries]
