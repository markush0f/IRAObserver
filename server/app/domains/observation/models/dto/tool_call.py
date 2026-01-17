from __future__ import annotations

"""Observation tool call DTOs."""

import uuid
from datetime import datetime
from typing import Any

from sqlmodel import SQLModel


class ObservationToolCallCreate(SQLModel):
    """Payload to create an observation tool call."""

    question_id: uuid.UUID
    tool_name: str
    tool_arguments: dict[str, Any]
    tool_result: dict[str, Any]
    executed_at: datetime | None = None


class ObservationToolCallPublic(SQLModel):
    """Public representation of an observation tool call."""

    id: uuid.UUID
    question_id: uuid.UUID
    tool_name: str
    tool_arguments: dict[str, Any]
    tool_result: dict[str, Any]
    executed_at: datetime
