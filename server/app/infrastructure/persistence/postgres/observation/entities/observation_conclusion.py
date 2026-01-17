from __future__ import annotations

"""Observation conclusion persistence model."""

import uuid
from datetime import datetime
from typing import ClassVar

from sqlalchemy import Column, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import text
from sqlmodel import Field, SQLModel


class ObservationConclusion(SQLModel, table=True):
    """Database representation of an observation conclusion."""

    __tablename__: ClassVar[str] = "observation_conclusion"

    id: uuid.UUID = Field(  # type: ignore[call-arg]
        default_factory=uuid.uuid4,
        sa_column=Column(
            UUID(as_uuid=True),
            primary_key=True,
            server_default=text("uuid_generate_v4()"),
        ),
    )
    question_id: uuid.UUID = Field(
        sa_column=Column(UUID(as_uuid=True), nullable=False),
    )
    explanation: str = Field(sa_column=Column(Text, nullable=False))
    generated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True), nullable=False, server_default=text("now()")
        ),
    )
