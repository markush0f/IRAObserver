from __future__ import annotations

"""Membership domain services."""

import logging
import uuid

from app.domains.identity.models.entities.membership import Membership
from app.domains.identity.repository.membership_repository import MembershipRepository
from app.domains.identity.repository.user_repository import UserRepository
from app.domains.projects.models.dto.project import ProjectMemberPublic
from app.domains.projects.repository.project_repository import ProjectRepository


class MembershipService:
    """Application logic for memberships."""
    logger = logging.getLogger(__name__)
    def __init__(
        self,
        membership_repository: MembershipRepository,
        user_repository: UserRepository,
        project_repository: ProjectRepository,
    ) -> None:
        self.membership_repository = membership_repository
        self.user_repository = user_repository
        self.project_repository = project_repository

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

        project = await self.project_repository.get_by_id(project_id)
        if not project:
            raise ValueError("project not found")

        user = await self.user_repository.get_by_id(user_id)
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
