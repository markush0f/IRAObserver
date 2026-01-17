from __future__ import annotations

"""Snapshot persistence model."""

import uuid
from datetime import datetime
from typing import Any, ClassVar

from sqlalchemy import Column, DateTime, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.sql import text
from sqlmodel import Field, SQLModel


class Snapshot(SQLModel, table=True):
    """Database representation of a project snapshot."""

    __tablename__: ClassVar[str] = "snapshots"

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
    analysis_type: str = Field(
        default="generic",
        sa_column=Column(Text, nullable=False, server_default=text("'generic'")),
    )
    commit_hash: str | None = Field(
        default=None,
        sa_column=Column(Text, nullable=True),
    )
    summary_json: dict[str, Any] = Field(
        sa_column=Column(JSONB, nullable=False),
    )
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True), nullable=False, server_default=text("now()")
        ),
    )
