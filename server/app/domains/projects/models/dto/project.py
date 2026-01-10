from __future__ import annotations

import uuid
from datetime import datetime

from sqlmodel import SQLModel

from app.domains.projects.models.source_type import SourceType


class ProjectCreate(SQLModel):
    name: str
    description: str | None = None
    source_type: SourceType
    source_ref: str


class ProjectPublic(SQLModel):
    id: uuid.UUID
    name: str
    description: str | None
    source_type: SourceType
    source_ref: str
    created_at: datetime
    last_analysis_at: datetime | None


class ProjectMemberCreate(SQLModel):
    user_id: uuid.UUID
    role: str = "member"


class ProjectMemberPublic(SQLModel):
    id: uuid.UUID
    user_id: uuid.UUID
    project_id: uuid.UUID
    role: str
    created_at: datetime
    revoked_at: datetime | None
