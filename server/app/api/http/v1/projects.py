from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

import uuid

from app.api.deps import (
    get_current_user,
    get_membership_service,
    get_project_service,
)
from app.domains.identity.models.entities.user import User
from app.domains.projects.models.dto.project import (
    ProjectCreate,
    ProjectMemberCreate,
    ProjectMemberPublic,
    ProjectPublic,
)
from app.domains.identity.services.membership_service import MembershipService
from app.domains.projects.services.project_service import ProjectService

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("", response_model=ProjectPublic, status_code=status.HTTP_201_CREATED)
async def create_project(
    payload: ProjectCreate,
    project_service: ProjectService = Depends(get_project_service),
    current_user: User = Depends(get_current_user),
) -> ProjectPublic:
    try:
        return await project_service.create_project(
            payload,
            actor_role=current_user.role,
        )
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc


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
