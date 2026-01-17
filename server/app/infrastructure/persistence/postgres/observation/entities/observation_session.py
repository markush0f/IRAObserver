from __future__ import annotations

"""Observation session persistence model."""

import uuid
from datetime import datetime
from typing import ClassVar

from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import text
from sqlmodel import Field, SQLModel


class ObservationSession(SQLModel, table=True):
    """Database representation of an observation session."""

    __tablename__: ClassVar[str] = "observation_session"

    id: uuid.UUID = Field(  # type: ignore[call-arg]
        default_factory=uuid.uuid4,
        sa_column=Column(
            UUID(as_uuid=True),
            primary_key=True,
            server_default=text("uuid_generate_v4()"),
        ),
    )
    project_id: uuid.UUID = Field(
        sa_column=Column(UUID(as_uuid=True), nullable=False),
    )
    llm_provider: str = Field(sa_column=Column(String(50), nullable=False))
    llm_model: str = Field(sa_column=Column(String(100), nullable=False))
    started_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True), nullable=False, server_default=text("now()")
        ),
    )
    ended_at: datetime | None = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), nullable=True),
    )
