from __future__ import annotations

"""Git commit helpers."""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from git import InvalidGitRepositoryError, NoSuchPathError, Repo


@dataclass(frozen=True)
class GitCommitInfo:
    """Lightweight commit info."""

    commit_hash: str
    message: str
    author_name: str
    authored_at: datetime


def list_recent_commits(repo_path: Path, limit: int = 20) -> list[GitCommitInfo]:
    """Return recent commits for a repository path."""
    try:
        repo = Repo(repo_path)
    except (InvalidGitRepositoryError, NoSuchPathError) as exc:
        raise ValueError("git repository not found") from exc

    commits = []
    for commit in repo.iter_commits(max_count=limit):
        commits.append(
            GitCommitInfo(
                commit_hash=commit.hexsha,
                message=commit.message.strip().splitlines()[0] if commit.message else "",
                author_name=commit.author.name if commit.author else "",
                authored_at=commit.authored_datetime,
            )
        )
    return commits
