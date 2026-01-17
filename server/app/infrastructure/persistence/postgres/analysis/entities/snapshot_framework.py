from __future__ import annotations

"""Snapshot framework persistence model."""

import uuid
from datetime import datetime
from typing import ClassVar

from sqlalchemy import Column, DateTime, Numeric, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import text
from sqlmodel import Field, SQLModel


class SnapshotFramework(SQLModel, table=True):
    """Database representation of snapshot framework confidence."""

    __tablename__: ClassVar[str] = "snapshot_frameworks"

    id: uuid.UUID = Field(  # type: ignore[call-arg]
        default_factory=uuid.uuid4,
        sa_column=Column(
            UUID(as_uuid=True),
            primary_key=True,
            server_default=text("uuid_generate_v4()"),
        ),
    )
    snapshot_id: uuid.UUID = Field(
        sa_column=Column(UUID(as_uuid=True), nullable=False),
    )
    framework: str = Field(sa_column=Column(Text, nullable=False))
    confidence: float = Field(
        sa_column=Column(Numeric(5, 4), nullable=False),
    )
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True), nullable=False, server_default=text("now()")
        ),
    )
