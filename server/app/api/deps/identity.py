"""Identity domain dependency providers."""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.domains.identity.repository.membership_repository import MembershipRepository
from app.domains.identity.repository.user_repository import UserRepository
from app.domains.identity.services.membership_service import MembershipService
from app.domains.identity.services.user_service import UserService
from app.api.deps.projects import get_project_service
from app.domains.projects.services.project_service import ProjectService


def get_user_repository(
    session: AsyncSession = Depends(get_db),
) -> UserRepository:
    """Provide a user repository instance."""
    return UserRepository(session)


def get_membership_repository(
    session: AsyncSession = Depends(get_db),
) -> MembershipRepository:
    """Provide a membership repository instance."""
    return MembershipRepository(session)


def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository),
) -> UserService:
    """Provide a user service instance."""
    return UserService(user_repository)


def get_membership_service(
    membership_repository: MembershipRepository = Depends(get_membership_repository),
    user_service: UserService = Depends(get_user_service),
    project_service: ProjectService = Depends(get_project_service),
) -> MembershipService:
    """Provide a membership service instance."""
    return MembershipService(
        membership_repository=membership_repository,
        user_service=user_service,
        project_service=project_service,
    )
