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

import uuid
from datetime import datetime, timezone

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_access_token
from app.core.settings import AUTH_TOKEN_ENABLED
from app.core.db import get_db
from app.domains.auth.services.auth_service import AuthService
from app.domains.identity.models.entities.user import User
from app.domains.identity.repository.membership_repository import MembershipRepository
from app.domains.identity.repository.user_repository import UserRepository
from app.domains.identity.services.membership_service import MembershipService
from app.domains.identity.services.user_service import UserService
from app.domains.projects.repository.project_repository import ProjectRepository
from app.domains.projects.services.project_service import ProjectService


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

def get_project_repository(
    session: AsyncSession = Depends(get_db),
) -> ProjectRepository:
    return ProjectRepository(session)


def get_project_service(
    project_repository: ProjectRepository = Depends(get_project_repository),
) -> ProjectService:
    return ProjectService(project_repository)


def get_membership_service(
    membership_repository: MembershipRepository = Depends(get_membership_repository),
    user_repository: UserRepository = Depends(get_user_repository),
    project_repository: ProjectRepository = Depends(get_project_repository),
) -> MembershipService:
    return MembershipService(
        membership_repository=membership_repository,
        user_repository=user_repository,
        project_repository=project_repository,
    )


async def get_current_user(
    request: Request,
    user_repository: UserRepository = Depends(get_user_repository),
) -> User:
    if not AUTH_TOKEN_ENABLED:
        return User(
            id=uuid.uuid4(),
            display_name="system",
            password_hash="",
            role="admin",
            is_active=True,
            created_at=datetime.now(timezone.utc),
        )

    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="missing bearer token",
        )

    token = auth_header.split(" ", 1)[1].strip()
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="missing bearer token",
        )

    try:
        payload = decode_access_token(token)
        user_id = uuid.UUID(payload.sub)
    except (ValueError, TypeError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token",
        ) from exc

    user = await user_repository.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user is inactive",
        )
    return user


async def require_admin_bootstrap(
    request: Request,
    auth_service: AuthService = Depends(get_auth_service),
) -> None:
    needs_bootstrap = await auth_service.bootstrap_needed()
    if not needs_bootstrap:
        if request.url.path == "/auth/bootstrap":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="bootstrap forbidden",
            )
        return

    allowed_paths = {"/auth/bootstrap", "/auth/bootstrap-status", "/health"}
    if request.url.path in allowed_paths:
        return

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="admin bootstrap required",
    )
