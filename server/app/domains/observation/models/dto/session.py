from __future__ import annotations

"""Observation session DTOs."""

import uuid
from datetime import datetime

from sqlmodel import SQLModel


class ObservationSessionCreate(SQLModel):
    """Payload to create an observation session."""

    project_id: uuid.UUID
    llm_provider: str
    llm_model: str
    started_at: datetime | None = None


class ObservationSessionPublic(SQLModel):
    """Public representation of an observation session."""

    id: uuid.UUID
    project_id: uuid.UUID
    llm_provider: str
    llm_model: str
    started_at: datetime
    ended_at: datetime | None
