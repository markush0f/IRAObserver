import hashlib
import subprocess
import uuid
from pathlib import Path

from app.core.settings import IRAOBSERVER_REPOS_DIR


def clone_repository(
    repo_url: str,
    project_id: uuid.UUID | None = None,
    allow_clone: bool = False,
) -> Path:
    # Return deterministic local path, optionally cloning if missing.
    if project_id:
        target_path = IRAOBSERVER_REPOS_DIR / str(project_id)
    else:
        repo_hash = hashlib.sha1(repo_url.encode("utf-8")).hexdigest()
        target_path = IRAOBSERVER_REPOS_DIR / repo_hash

    IRAOBSERVER_REPOS_DIR.mkdir(parents=True, exist_ok=True)

    if target_path.exists():
        return target_path

    if not allow_clone:
        raise FileNotFoundError(
            f"Repository not found at {target_path}. Clone is disabled."
        )

    subprocess.run(
        ["git", "clone", repo_url, str(target_path)],
        check=True,
    )

    return target_path
