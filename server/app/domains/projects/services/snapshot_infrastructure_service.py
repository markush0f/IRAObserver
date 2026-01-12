from __future__ import annotations

"""Snapshot infrastructure domain services."""

import uuid
import logging

from app.domains.analysis.models.entities.snapshot_infrastructure import (
    SnapshotInfrastructure,
)
from app.domains.analysis.repository.snapshot_infrastructure_repository import (
    SnapshotInfrastructureRepository,
)


class SnapshotInfrastructureService:
    """Application logic for snapshot infrastructure storage."""

    logger = logging.getLogger(__name__)

    def __init__(
        self,
        snapshot_infrastructure_repository: SnapshotInfrastructureRepository,
    ) -> None:
        self.snapshot_infrastructure_repository = snapshot_infrastructure_repository

    async def create_snapshot_infrastructure(
        self, snapshot_id: uuid.UUID, components: list[str]
    ) -> list[SnapshotInfrastructure]:
        """Create snapshot infrastructure entries for detected components."""
        self.logger.info(
            "Persisting snapshot infrastructure snapshot_id=%s components=%s",
            snapshot_id,
            len(components),
        )
        entries = [
            SnapshotInfrastructure(
                snapshot_id=snapshot_id,
                component=component,
            )
            for component in components
        ]
        if not entries:
            self.logger.debug("No infrastructure components to persist")
            return []
        return await self.snapshot_infrastructure_repository.create_many(entries)

    async def get_snapshot_infrastructure(
        self, snapshot_id: uuid.UUID
    ) -> list[str]:
        """Return infrastructure components for a snapshot."""
        self.logger.info("Loading snapshot infrastructure snapshot_id=%s", snapshot_id)
        entries = await self.snapshot_infrastructure_repository.list_by_snapshot(
            snapshot_id
        )
        return [entry.component for entry in entries]
