from __future__ import annotations

"""Project dependency persistence model."""

import uuid
from datetime import datetime
from typing import ClassVar

from sqlalchemy import Column, DateTime, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import text
from sqlmodel import Field, SQLModel


class ProjectDependency(SQLModel, table=True):
    """Database representation of a project dependency."""

    __tablename__: ClassVar[str] = "project_dependencies"

    id: uuid.UUID = Field(  # type: ignore[call-arg]
        default_factory=uuid.uuid4,
        sa_column=Column(UUID(as_uuid=True), primary_key=True),
    )
    snapshot_id: uuid.UUID = Field(
        sa_column=Column(UUID(as_uuid=True), nullable=False),
    )
    name: str = Field(sa_column=Column(String(128), nullable=False))
    version: str | None = Field(
        default=None, sa_column=Column(String(64), nullable=True)
    )
    ecosystem: str = Field(sa_column=Column(String(32), nullable=False))
    scope: str = Field(sa_column=Column(String(32), nullable=False))
    source_file: str = Field(sa_column=Column(Text, nullable=False))
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=False), nullable=False, server_default=text("now()")
        ),
    )
