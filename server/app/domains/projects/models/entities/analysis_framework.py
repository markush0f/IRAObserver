from __future__ import annotations

"""Analysis framework catalog persistence model."""

import uuid
from datetime import datetime
from typing import ClassVar

from sqlalchemy import Column, DateTime, Text, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import text
from sqlmodel import Field, SQLModel


class AnalysisFramework(SQLModel, table=True):
    """Database representation of a framework catalog entry."""

    __tablename__: ClassVar[str] = "analysis_framework"

    id: uuid.UUID = Field(  # type: ignore[call-arg]
        default_factory=uuid.uuid4,
        sa_column=Column(
            UUID(as_uuid=True),
            primary_key=True,
            server_default=text("gen_random_uuid()"),
        ),
    )
    name: str = Field(sa_column=Column(Text, nullable=False, unique=True))
    category: str = Field(sa_column=Column(Text, nullable=False))
    website: str | None = Field(sa_column=Column(Text, nullable=True))
    is_active: bool = Field(
        default=True,
        sa_column=Column(Boolean, nullable=False, server_default=text("true")),
    )
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True), nullable=False, server_default=text("now()")
        ),
    )
