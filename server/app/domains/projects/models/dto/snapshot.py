from __future__ import annotations

"""Snapshot DTOs."""

import uuid
from datetime import datetime
from typing import Any

from sqlmodel import SQLModel


class SnapshotPublic(SQLModel):
    """Public representation of a snapshot."""

    id: uuid.UUID
    project_id: uuid.UUID
    commit_hash: str | None
    summary_json: dict[str, Any]
    created_at: datetime


class SnapshotPage(SQLModel):
    """Paginated snapshots response."""

    items: list[SnapshotPublic]
    total: int
    limit: int
    offset: int
