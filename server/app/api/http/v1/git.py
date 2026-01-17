from __future__ import annotations

"""Git metadata endpoints."""

from datetime import datetime
import logging
import uuid

from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.deps import get_current_user, get_git_info_service
from app.infrastructure.persistence.postgres.identity.entities.user import User
from app.domains.projects.models.dto.git import GitCommitPublic
from app.infrastructure.external.git.git_info_service import GitInfoService

router = APIRouter(prefix="/projects", tags=["git"])
logger = logging.getLogger(__name__)


@router.get("/{project_id}/git/branches", response_model=list[str])
async def list_project_branches(
    project_id: uuid.UUID,
    git_info_service: GitInfoService = Depends(get_git_info_service),
    current_user: User = Depends(get_current_user),
) -> list[str]:
    """List local git branches for a project."""
    logger.info(
        "GET /projects/%s/git/branches by user_id=%s", project_id, current_user.id
    )
    try:
        branches = await git_info_service.list_branches(project_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    if branches is None:
        raise HTTPException(status_code=404, detail="project not found")
    return branches


@router.get("/{project_id}/git/commits", response_model=list[GitCommitPublic])
async def list_project_commits(
    project_id: uuid.UUID,
    git_info_service: GitInfoService = Depends(get_git_info_service),
    current_user: User = Depends(get_current_user),
    limit: int = Query(default=20, ge=1, le=200),
    since: datetime | None = Query(default=None),
    until: datetime | None = Query(default=None),
) -> list[GitCommitPublic]:
    """List recent git commits for a project."""
    logger.info(
        "GET /projects/%s/git/commits by user_id=%s", project_id, current_user.id
    )
    try:
        commits = await git_info_service.list_commits(
            project_id, limit=limit, since=since, until=until
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    if commits is None:
        raise HTTPException(status_code=404, detail="project not found")
    return [
        GitCommitPublic(
            commit_hash=commit.commit_hash,
            message=commit.message,
            author_name=commit.author_name,
            authored_at=commit.authored_at,
        )
        for commit in commits
    ]


@router.get("/{project_id}/git/branch")
async def get_project_current_branch(
    project_id: uuid.UUID,
    git_info_service: GitInfoService = Depends(get_git_info_service),
    current_user: User = Depends(get_current_user),
) -> dict[str, str]:
    """Get current git branch for a project."""
    logger.info(
        "GET /projects/%s/git/branch by user_id=%s", project_id, current_user.id
    )
    try:
        branch = await git_info_service.get_current_branch(project_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    if branch is None:
        raise HTTPException(status_code=404, detail="project not found")
    return {"branch": branch}
