from __future__ import annotations

"""Git branch helpers."""

from pathlib import Path

from git import InvalidGitRepositoryError, NoSuchPathError, RemoteReference, Repo


def list_local_branches(repo_path: Path) -> list[str]:
    """Return local and remote git branch names for a repository path."""
    try:
        repo = Repo(repo_path)
    except (InvalidGitRepositoryError, NoSuchPathError) as exc:
        raise ValueError("git repository not found") from exc

    branches = {head.name for head in repo.branches}
    branches.update(ref.name for ref in repo.references if isinstance(ref, RemoteReference))
    return sorted(branches)


def get_current_branch(repo_path: Path) -> str:
    """Return current branch name for a repository path."""
    try:
        repo = Repo(repo_path)
    except (InvalidGitRepositoryError, NoSuchPathError) as exc:
        raise ValueError("git repository not found") from exc

    if repo.head.is_detached:
        return "DETACHED"
    return repo.active_branch.name
