from __future__ import annotations

"""Infrastructure catalog persistence model."""

import uuid
from datetime import datetime
from typing import ClassVar

from sqlalchemy import Boolean, Column, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import text
from sqlmodel import Field, SQLModel


class AnalysisInfraComponent(SQLModel, table=True):
    """Database representation of an infrastructure component."""

    __tablename__: ClassVar[str] = "analysis_infra_component"

    id: uuid.UUID = Field(  # type: ignore[call-arg]
        default_factory=uuid.uuid4,
        sa_column=Column(
            UUID(as_uuid=True),
            primary_key=True,
            server_default=text("uuid_generate_v4()"),
        ),
    )
    name: str = Field(sa_column=Column(Text, nullable=False, unique=True))
    category: str = Field(sa_column=Column(Text, nullable=False))
    is_active: bool = Field(
        default=True,
        sa_column=Column(Boolean, nullable=False, server_default=text("true")),
    )
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True), nullable=False, server_default=text("now()")
        ),
    )
