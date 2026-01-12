from __future__ import annotations

"""Project analysis endpoints."""

import logging
import uuid

from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import get_current_user, get_project_analysis_service
from app.domains.identity.models.entities.user import User
from app.domains.projects.models.dto.framework import ProjectFrameworkAnalysis
from app.domains.projects.models.dto.infrastructure import ProjectInfrastructureAnalysis
from app.domains.projects.models.dto.project import ProjectLanguageAnalysis
from app.domains.projects.services.project_analysis_service import ProjectAnalysisService

router = APIRouter(prefix="/projects", tags=["analysis"])
logger = logging.getLogger(__name__)


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
    "/{project_id}/analysis/frameworks", response_model=ProjectFrameworkAnalysis
)
async def analyze_project_frameworks(
    project_id: uuid.UUID,
    project_analysis_service: ProjectAnalysisService = Depends(
        get_project_analysis_service
    ),
    current_user: User = Depends(get_current_user),
) -> ProjectFrameworkAnalysis:
    """Analyze and persist detected frameworks for a project."""
    logger.info(
        "POST /projects/%s/analysis/frameworks by user_id=%s",
        project_id,
        current_user.id,
    )
    analysis = await project_analysis_service.analyze_and_store_frameworks(project_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="project not found")
    return analysis


@router.get(
    "/{project_id}/analysis/frameworks", response_model=ProjectFrameworkAnalysis
)
async def get_project_framework_analysis(
    project_id: uuid.UUID,
    project_analysis_service: ProjectAnalysisService = Depends(
        get_project_analysis_service
    ),
    current_user: User = Depends(get_current_user),
) -> ProjectFrameworkAnalysis:
    """Get stored frameworks for a project."""
    logger.info(
        "GET /projects/%s/analysis/frameworks by user_id=%s",
        project_id,
        current_user.id,
    )
    analysis = await project_analysis_service.get_latest_framework_analysis(project_id)
    if analysis is None:
        raise HTTPException(status_code=404, detail="project not found")
    return analysis


@router.post(
    "/{project_id}/analysis/infrastructure",
    response_model=ProjectInfrastructureAnalysis,
)
async def analyze_project_infrastructure(
    project_id: uuid.UUID,
    project_analysis_service: ProjectAnalysisService = Depends(
        get_project_analysis_service
    ),
    current_user: User = Depends(get_current_user),
) -> ProjectInfrastructureAnalysis:
    """Analyze and persist detected infrastructure for a project."""
    logger.info(
        "POST /projects/%s/analysis/infrastructure by user_id=%s",
        project_id,
        current_user.id,
    )
    analysis = await project_analysis_service.analyze_and_store_infrastructure(
        project_id
    )
    if not analysis:
        raise HTTPException(status_code=404, detail="project not found")
    return analysis


@router.get(
    "/{project_id}/analysis/infrastructure",
    response_model=ProjectInfrastructureAnalysis,
)
async def get_project_infrastructure_analysis(
    project_id: uuid.UUID,
    project_analysis_service: ProjectAnalysisService = Depends(
        get_project_analysis_service
    ),
    current_user: User = Depends(get_current_user),
) -> ProjectInfrastructureAnalysis:
    """Get stored infrastructure for a project."""
    logger.info(
        "GET /projects/%s/analysis/infrastructure by user_id=%s",
        project_id,
        current_user.id,
    )
    analysis = await project_analysis_service.get_latest_infrastructure_analysis(
        project_id
    )
    if analysis is None:
        raise HTTPException(status_code=404, detail="project not found")
    return analysis
