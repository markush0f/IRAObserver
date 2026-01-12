from __future__ import annotations

"""Language analysis DTOs."""

from sqlmodel import SQLModel


class ProjectLanguageAnalysis(SQLModel):
    """Language analysis payload for a project."""

    languages: dict[str, int]
