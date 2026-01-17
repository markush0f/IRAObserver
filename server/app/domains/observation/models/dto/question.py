from __future__ import annotations

"""Observation question DTOs."""

import uuid
from datetime import datetime

from sqlmodel import SQLModel


class ObservationQuestionCreate(SQLModel):
    """Payload to create an observation question."""

    session_id: uuid.UUID
    raw_question: str
    normalized_intent: str | None = None
    created_at: datetime | None = None


class ObservationQuestionPublic(SQLModel):
    """Public representation of an observation question."""

    id: uuid.UUID
    session_id: uuid.UUID
    raw_question: str
    normalized_intent: str | None
    created_at: datetime
