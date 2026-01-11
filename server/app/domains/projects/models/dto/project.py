from __future__ import annotations

"""Project-related DTOs."""

import uuid
from datetime import datetime

from sqlmodel import SQLModel

from app.domains.projects.models.source_type import SourceType


class ProjectCreate(SQLModel):
    """Payload to create a project."""
    name: str
    description: str | None = None
    source_type: SourceType
    source_ref: str


class ProjectPublic(SQLModel):
    """Public representation of a project."""
    id: uuid.UUID
    name: str
    description: str | None
    source_type: SourceType
    source_ref: str
    created_at: datetime
    last_analysis_at: datetime | None


class ProjectMemberCreate(SQLModel):
    """Payload to add a user to a project."""
    user_id: uuid.UUID
    role: str = "member"


class ProjectMemberPublic(SQLModel):
    """Public representation of a project membership."""
    id: uuid.UUID
    user_id: uuid.UUID
    project_id: uuid.UUID
    role: str
    created_at: datetime
    revoked_at: datetime | None


class ProjectLanguageAnalysis(SQLModel):
    """Language analysis payload for a project."""

    languages: dict[str, int]
