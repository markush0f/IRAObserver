from __future__ import annotations

"""Observation tool call persistence model."""

import uuid
from datetime import datetime
from typing import ClassVar

from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.sql import text
from sqlmodel import Field, SQLModel


class ObservationToolCall(SQLModel, table=True):
    """Database representation of an observation tool call."""

    __tablename__: ClassVar[str] = "observation_tool_call"

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
    tool_name: str = Field(sa_column=Column(String(100), nullable=False))
    tool_arguments: dict = Field(sa_column=Column(JSONB, nullable=False))
    tool_result: dict = Field(sa_column=Column(JSONB, nullable=False))
    executed_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True), nullable=False, server_default=text("now()")
        ),
    )
