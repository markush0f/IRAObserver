from __future__ import annotations

"""Project dependency DTOs."""

import uuid
from datetime import datetime

from sqlmodel import SQLModel


class ProjectDependencyCreate(SQLModel):
    """Payload to create a project dependency entry."""

    snapshot_id: uuid.UUID
    name: str
    version: str | None = None
    ecosystem: str
    scope: str
    source_file: str


class ProjectDependencyPublic(SQLModel):
    """Public representation of a project dependency."""

    id: uuid.UUID
    snapshot_id: uuid.UUID
    name: str
    version: str | None
    ecosystem: str
    scope: str
    source_file: str
    created_at: datetime


class ProjectDependencyPage(SQLModel):
    """Paginated project dependencies response."""

    items: list[ProjectDependencyPublic]
    total: int
    limit: int
    offset: int
