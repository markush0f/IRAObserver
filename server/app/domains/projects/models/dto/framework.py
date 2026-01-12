from __future__ import annotations

"""Framework analysis DTOs."""

from sqlmodel import SQLModel


class ProjectFrameworkAnalysis(SQLModel):
    """Framework analysis payload for a project."""

    frameworks: dict[str, float]
