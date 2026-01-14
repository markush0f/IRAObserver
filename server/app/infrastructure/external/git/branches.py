from __future__ import annotations

"""Git branch helpers."""

from pathlib import Path

from git import InvalidGitRepositoryError, NoSuchPathError, Repo


def list_local_branches(repo_path: Path) -> list[str]:
    """Return local git branch names for a repository path."""
    try:
        repo = Repo(repo_path)
    except (InvalidGitRepositoryError, NoSuchPathError) as exc:
        raise ValueError("git repository not found") from exc

    return sorted([head.name for head in repo.branches])
