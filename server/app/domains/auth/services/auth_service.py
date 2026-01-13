from __future__ import annotations

from passlib.context import CryptContext

from app.core.security import create_access_token
from app.domains.auth.models.dto.auth import (
    AuthToken,
    AuthUser,
    BootstrapPayload,
    LoginPayload,
    RegisterPayload,
)
from app.domains.identity.models.dto.user import UserCreate
from app.domains.identity.services.user_service import UserService

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, user_service: UserService) -> None:
        self.user_service = user_service

    async def register(self, data: RegisterPayload) -> AuthUser:
        if data.role == "admin":
            raise PermissionError("admin registration is disabled")
        created = await self.user_service.create_user(
            UserCreate(
                display_name=data.display_name,
                password=data.password,
                role=data.role,
            )
        )
        return AuthUser.model_validate(created)

    async def bootstrap_admin(self, data: BootstrapPayload) -> AuthUser:
        if await self.user_service.has_admin():
            raise ValueError("admin already exists")
        created = await self.user_service.create_user(
            UserCreate(
                display_name=data.display_name,
                password=data.password,
                role="admin",
            )
        )
        return AuthUser.model_validate(created)

    async def login(self, data: LoginPayload) -> AuthToken:
        user = await self.user_service.get_by_display_name(data.display_name)
        if not user or not _pwd_context.verify(data.password, user.password_hash):
            raise ValueError("invalid credentials")
        if not user.is_active:
            raise PermissionError("user is inactive")
        token = create_access_token(subject=str(user.id), role=user.role)
        return AuthToken(access_token=token, user=AuthUser.model_validate(user))

    async def bootstrap_needed(self) -> bool:
        return not await self.user_service.has_admin()
