from __future__ import annotations

"""Infrastructure detection rule persistence model."""

import uuid
from datetime import datetime
from typing import ClassVar

from sqlalchemy import Boolean, Column, DateTime, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import text
from sqlmodel import Field, SQLModel


class AnalysisInfraRule(SQLModel, table=True):
    """Database representation of an infrastructure detection rule."""

    __tablename__: ClassVar[str] = "analysis_infra_rule"

    id: uuid.UUID = Field(  # type: ignore[call-arg]
        default_factory=uuid.uuid4,
        sa_column=Column(
            UUID(as_uuid=True),
            primary_key=True,
            server_default=text("uuid_generate_v4()"),
        ),
    )
    infra_component_id: uuid.UUID = Field(
        sa_column=Column(UUID(as_uuid=True), nullable=False),
    )
    signal_type: str = Field(sa_column=Column(Text, nullable=False))
    signal_value: str = Field(sa_column=Column(Text, nullable=False))
    weight: int = Field(
        default=1,
        sa_column=Column(Integer, nullable=False, server_default=text("1")),
    )
    is_active: bool = Field(
        default=True,
        sa_column=Column(Boolean, nullable=False, server_default=text("true")),
    )
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True), nullable=False, server_default=text("now()")
        ),
    )
