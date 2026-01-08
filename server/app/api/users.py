from __future__ import annotations

from fastapi import APIRouter, Depends

from app.api.deps import get_user_service
from app.domains.identity.services.UserService import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/health")
def healthcheck(_service: UserService = Depends(get_user_service)) -> dict[str, str]:
    return {"status": "ok"}


@router.post("")
def create_user(user_service: UserService = Depends(get_user_service)):
    return user_service.create_user()
