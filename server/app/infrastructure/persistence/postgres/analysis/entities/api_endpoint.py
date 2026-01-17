from __future__ import annotations

"""API endpoint persistence model."""

import uuid
from datetime import datetime
from typing import ClassVar

from sqlalchemy import Column, DateTime, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import text
from sqlmodel import Field, SQLModel


class ApiEndpoint(SQLModel, table=True):
    """Database representation of a detected API endpoint."""

    __tablename__: ClassVar[str] = "api_endpoints"

    id: uuid.UUID = Field(  # type: ignore[call-arg]
        default_factory=uuid.uuid4,
        sa_column=Column(UUID(as_uuid=True), primary_key=True),
    )
    snapshot_id: uuid.UUID = Field(
        sa_column=Column(UUID(as_uuid=True), nullable=False),
    )
    http_method: str = Field(sa_column=Column(String(10), nullable=False))
    path: str = Field(sa_column=Column(Text, nullable=False))
    framework: str = Field(sa_column=Column(String(64), nullable=False))
    language: str = Field(sa_column=Column(String(32), nullable=False))
    source_file: str = Field(sa_column=Column(Text, nullable=False))
    source_symbol: str | None = Field(
        default=None, sa_column=Column(String(128), nullable=True)
    )
    confidence: float = Field(
        default=1.0, sa_column=Column(Numeric(3, 2), nullable=False)
    )
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=False), nullable=False, server_default=text("now()")
        ),
    )
