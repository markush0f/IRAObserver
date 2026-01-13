from __future__ import annotations

"""API endpoint DTOs."""

import uuid
from datetime import datetime

from sqlmodel import SQLModel


class ApiEndpointCreate(SQLModel):
    """Payload to create an API endpoint entry."""

    snapshot_id: uuid.UUID
    http_method: str
    path: str
    framework: str
    language: str
    source_file: str
    source_symbol: str | None = None
    confidence: float = 1.0


class ApiEndpointPublic(SQLModel):
    """Public representation of an API endpoint."""

    id: uuid.UUID
    snapshot_id: uuid.UUID
    http_method: str
    path: str
    framework: str
    language: str
    source_file: str
    source_symbol: str | None
    confidence: float
    created_at: datetime


class ProjectApiEndpointAnalysis(SQLModel):
    """API endpoint analysis payload for a project."""

    endpoints: list[ApiEndpointPublic]


class ApiEndpointPage(SQLModel):
    """Paginated API endpoints response."""

    items: list[ApiEndpointPublic]
    total: int
    limit: int
    offset: int
