"""Core dependency providers."""

import uuid
from datetime import datetime, timezone

from fastapi import Depends, HTTPException, Request, status

from app.api.deps.auth import get_auth_service
from app.api.deps.identity import get_user_repository
from app.core.security import decode_access_token
from app.core.settings import AUTH_TOKEN_ENABLED
from app.domains.auth.services.auth_service import AuthService
from app.domains.identity.models.entities.user import User
from app.domains.identity.repository.user_repository import UserRepository


async def get_current_user(
    request: Request,
    user_repository: UserRepository = Depends(get_user_repository),
) -> User:
    """Resolve the current user from a bearer token or bypass if disabled."""
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
    """Block requests until an admin account has been bootstrapped."""
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
