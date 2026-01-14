from __future__ import annotations

"""Git DTOs."""

from datetime import datetime

from sqlmodel import SQLModel


class GitCommitPublic(SQLModel):
    """Public representation of a git commit."""

    commit_hash: str
    message: str
    author_name: str
    authored_at: datetime
