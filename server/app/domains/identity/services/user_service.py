from passlib.context import CryptContext

from app.domains.identity.models.dto.user import UserCreate, UserPublic
from app.domains.identity.models.entities.user import User
from app.domains.identity.repository.user_repository import UserRepository

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    async def create_user(self, data: UserCreate) -> UserPublic:
        existing = await self.user_repository.get_by_display_name(data.display_name)
        if existing:
            raise ValueError("display_name already exists")

        user = User(
            display_name=data.display_name,
            password_hash=_pwd_context.hash(data.password),
            role=data.role,
        )
        created = await self.user_repository.create(user)
        return UserPublic.model_validate(created)

    async def has_admin(self) -> bool:
        return await self.user_repository.has_role("admin")
