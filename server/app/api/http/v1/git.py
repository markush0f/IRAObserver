from __future__ import annotations

"""Git metadata endpoints."""

import logging
import uuid

from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import get_current_user, get_git_info_service
from app.domains.identity.models.entities.user import User
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
    limit: int = 20,
) -> list[GitCommitPublic]:
    """List recent git commits for a project."""
    logger.info(
        "GET /projects/%s/git/commits by user_id=%s", project_id, current_user.id
    )
    if limit < 1 or limit > 200:
        raise HTTPException(
            status_code=400, detail="limit must be between 1 and 200"
        )
    try:
        commits = await git_info_service.list_commits(project_id, limit=limit)
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
