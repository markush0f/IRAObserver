from __future__ import annotations

from passlib.context import CryptContext

from app.domains.auth.models.dto.auth import AuthUser, LoginPayload, RegisterPayload
from app.domains.identity.models.dto.user import UserCreate
from app.domains.identity.services.user_service import UserService

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, user_service: UserService) -> None:
        self.user_service = user_service

    async def register(self, data: RegisterPayload) -> AuthUser:
        created = await self.user_service.create_user(
            UserCreate(
                display_name=data.display_name,
                password=data.password,
                role=data.role,
            )
        )
        return AuthUser.model_validate(created)

    async def login(self, data: LoginPayload) -> AuthUser:
        user = await self.user_service.user_repository.get_by_display_name(
            data.display_name
        )
        if not user or not _pwd_context.verify(data.password, user.password_hash):
            raise ValueError("invalid credentials")
        if not user.is_active:
            raise PermissionError("user is inactive")
        return AuthUser.model_validate(user)
