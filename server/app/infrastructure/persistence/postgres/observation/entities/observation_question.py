from __future__ import annotations

"""Observation question persistence model."""

import uuid
from datetime import datetime
from typing import ClassVar

from sqlalchemy import Column, DateTime, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import text
from sqlmodel import Field, SQLModel


class ObservationQuestion(SQLModel, table=True):
    """Database representation of an observation question."""

    __tablename__: ClassVar[str] = "observation_question"

    id: uuid.UUID = Field(  # type: ignore[call-arg]
        default_factory=uuid.uuid4,
        sa_column=Column(
            UUID(as_uuid=True),
            primary_key=True,
            server_default=text("uuid_generate_v4()"),
        ),
    )
    session_id: uuid.UUID = Field(
        sa_column=Column(UUID(as_uuid=True), nullable=False),
    )
    raw_question: str = Field(sa_column=Column(Text, nullable=False))
    normalized_intent: str | None = Field(
        default=None,
        sa_column=Column(String(255), nullable=True),
    )
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True), nullable=False, server_default=text("now()")
        ),
    )
