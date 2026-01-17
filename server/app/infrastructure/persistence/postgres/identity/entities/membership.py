from __future__ import annotations

import uuid
from datetime import datetime
from typing import ClassVar

from sqlalchemy import Column, DateTime, ForeignKey, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import text
from sqlmodel import Field, SQLModel


class Membership(SQLModel, table=True):
    __tablename__: ClassVar[str] = "memberships"
    __table_args__ = (UniqueConstraint("user_id", "project_id", name="uq_memberships_user_project"),)

    id: uuid.UUID = Field(  # type: ignore[call-arg]
        default_factory=uuid.uuid4,
        sa_column=Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()")),
    )
    user_id: uuid.UUID = Field(  # type: ignore[call-arg]
        sa_column=Column(
            UUID(as_uuid=True),
            ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        )
    )
    project_id: uuid.UUID = Field(  # type: ignore[call-arg]
        sa_column=Column(
            UUID(as_uuid=True),
            ForeignKey("projects.id", ondelete="CASCADE"),
            nullable=False,
        )
    )
    role: str = Field(sa_column=Column(Text, nullable=False))
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False, server_default=text("now()")),
    )
    revoked_at: datetime | None = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), nullable=True),
    )
