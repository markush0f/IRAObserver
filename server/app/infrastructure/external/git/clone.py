from pathlib import Path
import hashlib
import subprocess

from app.core.settings import IRAOBSERVER_REPOS_DIR


def clone_repository(repo_url: str) -> Path:
    # Change implemented:
    # - Clone git repository into a deterministic local path
    repo_hash = hashlib.sha1(repo_url.encode("utf-8")).hexdigest()
    target_path = IRAOBSERVER_REPOS_DIR / repo_hash

    IRAOBSERVER_REPOS_DIR.mkdir(parents=True, exist_ok=True)

    if target_path.exists():
        return target_path

    subprocess.run(
        ["git", "clone", repo_url, str(target_path)],
        check=True,
    )

    return target_path
