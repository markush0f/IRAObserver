"""
HTTP API for identity domain.
"""

from fastapi import APIRouter, Depends, status

from app.domains.identity.services.user import UserService

router = APIRouter(prefix="/identity", tags=["identity"])


def get_user_service():
    return UserService()


@router.get("/health", status_code=status.HTTP_200_OK)
def health_check() -> dict:
    return {"status": "ok"}


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(
    create_user: CreateUserDTO,
    user_service: UserService = Depends(get_user_service),
) -> UserResponse:
    return user_service.create_user()
