from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_auth_service
from app.domains.auth.models.dto.auth import (
    AuthToken,
    AuthUser,
    LoginPayload,
    RegisterPayload,
)
from app.domains.auth.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=AuthUser, status_code=status.HTTP_201_CREATED)
async def register(
    payload: RegisterPayload,
    auth_service: AuthService = Depends(get_auth_service),
) -> AuthUser:
    try:
        return await auth_service.register(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc


@router.post("/bootstrap", response_model=AuthUser, status_code=status.HTTP_201_CREATED)
async def bootstrap_admin(
    payload: RegisterPayload,
    auth_service: AuthService = Depends(get_auth_service),
) -> AuthUser:
    try:
        return await auth_service.bootstrap_admin(payload)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.post("/login", response_model=AuthToken)
async def login(
    payload: LoginPayload,
    auth_service: AuthService = Depends(get_auth_service),
) -> AuthToken:
    try:
        return await auth_service.login(payload)
    except ValueError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc


@router.get("/bootstrap-status")
async def bootstrap_status(
    auth_service: AuthService = Depends(get_auth_service),
) -> dict[str, bool]:
    return {"needs_bootstrap": await auth_service.bootstrap_needed()}
