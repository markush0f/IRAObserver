from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_user_service
from app.domains.identity.models.dto.user import UserCreate, UserPublic
from app.domains.identity.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/health")
def healthcheck(_service: UserService = Depends(get_user_service)) -> dict[str, str]:
    return {"status": "ok"}


@router.post("", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def create_user(
    payload: UserCreate,
    user_service: UserService = Depends(get_user_service),
) -> UserPublic:
    try:
        return await user_service.create_user(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
