"""Auth domain dependency providers."""

from fastapi import Depends

from app.domains.auth.services.auth_service import AuthService
from app.api.deps.identity import get_user_service
from app.domains.identity.services.user_service import UserService


def get_auth_service(
    user_service: UserService = Depends(get_user_service),
) -> AuthService:
    """Provide an auth service instance."""
    return AuthService(user_service)
