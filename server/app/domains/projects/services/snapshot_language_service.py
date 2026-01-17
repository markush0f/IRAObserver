from __future__ import annotations

"""Snapshot language domain services."""

import uuid

from app.infrastructure.persistence.postgres.analysis.entities.snapshot_language import SnapshotLanguage
from app.domains.analysis.repository.snapshot_language_repository import (
    SnapshotLanguageRepository,
)


class SnapshotLanguageService:
    """Application logic for snapshot language storage."""

    def __init__(self, snapshot_language_repository: SnapshotLanguageRepository) -> None:
        self.snapshot_language_repository = snapshot_language_repository

    async def create_snapshot_languages(
        self, snapshot_id: uuid.UUID, languages: dict[str, int]
    ) -> list[SnapshotLanguage]:
        """Create snapshot language entries for detected languages."""
        entries = [
            SnapshotLanguage(
                snapshot_id=snapshot_id,
                language=language,
                weight=weight,
            )
            for language, weight in languages.items()
        ]
        if not entries:
            return []
        return await self.snapshot_language_repository.create_many(entries)

    async def get_snapshot_languages(
        self, snapshot_id: uuid.UUID
    ) -> dict[str, int]:
        """Return language weights for a snapshot."""
        entries = await self.snapshot_language_repository.list_by_snapshot(snapshot_id)
        return {entry.language: entry.weight for entry in entries}
