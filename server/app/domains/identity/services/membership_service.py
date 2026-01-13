from __future__ import annotations

"""Membership domain services."""

import logging
import uuid

from app.domains.identity.models.entities.membership import Membership
from app.domains.identity.repository.membership_repository import MembershipRepository
from app.domains.identity.services.user_service import UserService
from app.domains.projects.models.dto.project import ProjectMemberPublic
from app.domains.projects.services.project_service import ProjectService


class MembershipService:
    """Application logic for memberships."""
    logger = logging.getLogger(__name__)
    def __init__(
        self,
        membership_repository: MembershipRepository,
        user_service: UserService,
        project_service: ProjectService,
    ) -> None:
        self.membership_repository = membership_repository
        self.user_service = user_service
        self.project_service = project_service

    async def add_user_to_project(
        self,
        project_id: uuid.UUID,
        user_id: uuid.UUID,
        role: str,
        actor_role: str,
    ) -> ProjectMemberPublic:
        """Add a user to a project if the actor has admin privileges."""
        self.logger.info(
            "Adding user to project project_id=%s user_id=%s role=%s",
            project_id,
            user_id,
            role,
        )
        if actor_role != "admin":
            raise PermissionError("admin role required")

        project = await self.project_service.get_project(project_id)
        if not project:
            raise ValueError("project not found")

        user = await self.user_service.get_user(user_id)
        if not user:
            raise ValueError("user not found")

        existing = await self.membership_repository.get_by_user_project(
            user_id=user.id,
            project_id=project.id,
        )
        if existing:
            raise ValueError("membership already exists")

        membership = Membership(
            user_id=user.id,
            project_id=project.id,
            role=role,
        )
        created = await self.membership_repository.create(membership)
        return ProjectMemberPublic.model_validate(created)
