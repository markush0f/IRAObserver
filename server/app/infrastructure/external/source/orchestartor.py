"""Source preparation dispatcher."""

from pathlib import Path

import uuid

from app.domains.projects.models.source_type import SourceType
from app.infrastructure.external.git.clone import clone_repository


def prepare_source(
    source_type: SourceType,
    source_ref: str,
    project_id: uuid.UUID | None = None,
    allow_clone: bool = False,
) -> Path:
    """Prepare a source based on type and return a local path."""
    if source_type == SourceType.GIT:
        return clone_repository(
            source_ref,
            project_id=project_id,
            allow_clone=allow_clone,
        )
    if source_type == SourceType.LOCAL:
        return Path(source_ref)

    raise ValueError(f"Unsupported source_type: {source_type}")
