from __future__ import annotations

from passlib.context import CryptContext

from app.domains.auth.models.dto.auth import AuthUser, LoginPayload, RegisterPayload
from app.domains.identity.models.entities.user import User
from app.domains.identity.repository.user_repository import UserRepository

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    async def register(self, data: RegisterPayload) -> AuthUser:
        existing = await self.user_repository.get_by_display_name(data.display_name)
        if existing:
            raise ValueError("display_name already exists")

        user = User(
            display_name=data.display_name,
            password_hash=_pwd_context.hash(data.password),
            role=data.role,
        )
        created = await self.user_repository.create(user)
        return AuthUser.model_validate(created)

    async def login(self, data: LoginPayload) -> AuthUser:
        user = await self.user_repository.get_by_display_name(data.display_name)
        if not user or not _pwd_context.verify(data.password, user.password_hash):
            raise ValueError("invalid credentials")
        if not user.is_active:
            raise PermissionError("user is inactive")
        return AuthUser.model_validate(user)
