"""Source preparation dispatcher."""

from pathlib import Path

from app.domains.projects.models.source_type import SourceType
from app.infrastructure.external.git.clone import clone_repository


def prepare_source(source_type: SourceType, source_ref: str) -> Path:
    """Prepare a source based on type and return a local path."""
    if source_type == SourceType.GIT:
        return clone_repository(source_ref)
    if source_type == SourceType.LOCAL:
        return Path(source_ref)

    raise ValueError(f"Unsupported source_type: {source_type}")
