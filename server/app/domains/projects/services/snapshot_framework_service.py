from __future__ import annotations

"""Snapshot framework domain services."""

import uuid

from app.domains.analysis.models.entities.snapshot_framework import SnapshotFramework
from app.domains.analysis.repository.snapshot_framework_repository import (
    SnapshotFrameworkRepository,
)


class SnapshotFrameworkService:
    """Application logic for snapshot framework storage."""

    def __init__(self, snapshot_framework_repository: SnapshotFrameworkRepository) -> None:
        self.snapshot_framework_repository = snapshot_framework_repository

    async def create_snapshot_frameworks(
        self, snapshot_id: uuid.UUID, frameworks: dict[str, float]
    ) -> list[SnapshotFramework]:
        """Create snapshot framework entries for detected frameworks."""
        entries = [
            SnapshotFramework(
                snapshot_id=snapshot_id,
                framework=framework,
                confidence=confidence,
            )
            for framework, confidence in frameworks.items()
        ]
        if not entries:
            return []
        return await self.snapshot_framework_repository.create_many(entries)

    async def get_snapshot_frameworks(
        self, snapshot_id: uuid.UUID
    ) -> dict[str, float]:
        """Return framework confidences for a snapshot."""
        entries = await self.snapshot_framework_repository.list_by_snapshot(snapshot_id)
        return {entry.framework: float(entry.confidence) for entry in entries}
