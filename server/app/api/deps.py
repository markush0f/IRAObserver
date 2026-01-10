"""
Dependency composition module.

This module acts as the composition root of the application.
Its responsibility is to wire together infrastructure implementations
with domain services and expose them to the API layer via dependency injection.

Rules:
- No business logic must live here.
- No validation or domain decisions must be performed here.
- This module only creates and connects dependencies.

The API layer requests fully constructed services from this module,
without knowing which concrete implementations are used underneath.

All technical decisions (e.g. database choice, external providers)
are centralized here to keep the domain isolated and testable.
"""

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.domains.auth.services.auth_service import AuthService
from app.domains.identity.repository.membership_repository import MembershipRepository
from app.domains.identity.repository.user_repository import UserRepository
from app.domains.identity.services.user_service import UserService


def get_user_repository(
    session: AsyncSession = Depends(get_db),
) -> UserRepository:
    return UserRepository(session)


def get_membership_repository(
    session: AsyncSession = Depends(get_db),
) -> MembershipRepository:
    return MembershipRepository(session)


def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository),
) -> UserService:
    return UserService(user_repository)


def get_auth_service(
    user_service: UserService = Depends(get_user_service),
) -> AuthService:
    return AuthService(user_service)


async def require_admin_bootstrap(
    request: Request,
    auth_service: AuthService = Depends(get_auth_service),
) -> None:
    needs_bootstrap = await auth_service.bootstrap_needed()
    if not needs_bootstrap:
        if request.url.path == "/auth/bootstrap":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="not found",
            )
        return

    allowed_paths = {"/auth/bootstrap", "/auth/bootstrap-status", "/health"}
    if request.url.path in allowed_paths:
        return

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="admin bootstrap required",
    )
