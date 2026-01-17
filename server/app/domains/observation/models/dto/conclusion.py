from __future__ import annotations

"""Observation conclusion DTOs."""

import uuid
from datetime import datetime

from sqlmodel import SQLModel


class ObservationConclusionCreate(SQLModel):
    """Payload to create an observation conclusion."""

    question_id: uuid.UUID
    explanation: str
    generated_at: datetime | None = None


class ObservationConclusionPublic(SQLModel):
    """Public representation of an observation conclusion."""

    id: uuid.UUID
    question_id: uuid.UUID
    explanation: str
    generated_at: datetime
