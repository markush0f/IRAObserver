from __future__ import annotations

"""Infrastructure analysis DTOs."""

from sqlmodel import SQLModel


class ProjectInfrastructureAnalysis(SQLModel):
    """Infrastructure analysis payload for a project."""

    components: list[str]
