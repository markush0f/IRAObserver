from __future__ import annotations

import uuid
from datetime import datetime

from sqlmodel import SQLModel


class ProjectCreate(SQLModel):
    name: str
    description: str | None = None
    source_type: str
    source_ref: str


class ProjectPublic(SQLModel):
    id: uuid.UUID
    name: str
    description: str | None
    source_type: str
    source_ref: str
    created_at: datetime
    last_analysis_at: datetime | None
