from __future__ import annotations

"""Project endpoints."""

import logging
import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.deps import (
    get_current_user,
    get_membership_service,
    get_project_analysis_service,
    get_project_service,
)
from app.domains.identity.models.entities.user import User
from app.domains.projects.models.dto.project import (
    ProjectCreate,
    ProjectLanguageAnalysis,
    ProjectMemberCreate,
    ProjectMemberPublic,
    ProjectPublic,
)
from app.domains.identity.services.membership_service import MembershipService
from app.domains.projects.services.project_analysis_service import ProjectAnalysisService
from app.domains.projects.services.project_service import ProjectService

router = APIRouter(prefix="/projects", tags=["projects"])
logger = logging.getLogger(__name__)


@router.post("", response_model=ProjectPublic, status_code=status.HTTP_201_CREATED)
async def create_project(
    payload: ProjectCreate,
    project_service: ProjectService = Depends(get_project_service),
    current_user: User = Depends(get_current_user),
) -> ProjectPublic:
    """Create a new project."""
    logger.info("POST /projects by user_id=%s", current_user.id)
    try:
        return await project_service.create_project(
            payload,
            actor_role=current_user.role,
        )
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("", response_model=list[ProjectPublic])
async def list_projects(
    project_service: ProjectService = Depends(get_project_service),
    current_user: User = Depends(get_current_user),
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
) -> list[ProjectPublic]:
    """List projects."""
    logger.info("GET /projects by user_id=%s", current_user.id)
    return await project_service.list_projects(limit=limit, offset=offset)


@router.get("/{project_id}", response_model=ProjectPublic)
async def get_project(
    project_id: uuid.UUID,
    project_service: ProjectService = Depends(get_project_service),
    current_user: User = Depends(get_current_user),
) -> ProjectPublic:
    """Get a project by id."""
    logger.info("GET /projects/%s by user_id=%s", project_id, current_user.id)
    project = await project_service.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="project not found")
    return project


@router.post(
    "/{project_id}/analysis/languages", response_model=ProjectLanguageAnalysis
)
async def analyze_project_languages(
    project_id: uuid.UUID,
    project_analysis_service: ProjectAnalysisService = Depends(
        get_project_analysis_service
    ),
    current_user: User = Depends(get_current_user),
) -> ProjectLanguageAnalysis:
    """Analyze and persist detected languages for a project."""
    logger.info(
        "POST /projects/%s/analysis/languages by user_id=%s",
        project_id,
        current_user.id,
    )
    try:
        analysis = await project_analysis_service.analyze_and_store_languages(
            project_id
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if not analysis:
        raise HTTPException(status_code=404, detail="project not found")
    return analysis


@router.get("/{project_id}/analysis/languages", response_model=ProjectLanguageAnalysis)
async def get_project_language_analysis(
    project_id: uuid.UUID,
    project_analysis_service: ProjectAnalysisService = Depends(
        get_project_analysis_service
    ),
    current_user: User = Depends(get_current_user),
) -> ProjectLanguageAnalysis:
    """Get stored languages for a project."""
    logger.info(
        "GET /projects/%s/analysis/languages by user_id=%s",
        project_id,
        current_user.id,
    )
    analysis = await project_analysis_service.get_latest_language_analysis(project_id)
    if analysis is None:
        raise HTTPException(status_code=404, detail="project not found")
    return analysis


@router.post(
    "/{project_id}/members",
    response_model=ProjectMemberPublic,
    status_code=status.HTTP_201_CREATED,
)
async def add_project_member(
    project_id: uuid.UUID,
    payload: ProjectMemberCreate,
    membership_service: MembershipService = Depends(get_membership_service),
    current_user: User = Depends(get_current_user),
) -> ProjectMemberPublic:
    """Add a user to a project."""
    logger.info("POST /projects/%s/members by user_id=%s", project_id, current_user.id)
    try:
        return await membership_service.add_user_to_project(
            project_id=project_id,
            user_id=payload.user_id,
            role=payload.role,
            actor_role=current_user.role,
        )
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
