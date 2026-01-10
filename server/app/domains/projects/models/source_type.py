from __future__ import annotations

"""Project source types."""

from enum import Enum


class SourceType(str, Enum):
    """Supported source types for project ingestion."""
    GIT = "git"
    LOCAL = "local"
