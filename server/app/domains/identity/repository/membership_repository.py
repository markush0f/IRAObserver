from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.infrastructure.persistence.postgres.identity.entities.membership import Membership


class MembershipRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, membership: Membership) -> Membership:
        self.session.add(membership)
        await self.session.commit()
        await self.session.refresh(membership)
        return membership

    async def get_by_id(self, membership_id: uuid.UUID) -> Membership | None:
        result = await self.session.execute(
            select(Membership).where(Membership.id == membership_id)
        )
        return result.scalar_one_or_none()

    async def get_by_user_project(
        self, user_id: uuid.UUID, project_id: uuid.UUID
    ) -> Membership | None:
        result = await self.session.execute(
            select(Membership).where(
                (Membership.user_id == user_id)
                & (Membership.project_id == project_id)
            )
        )
        return result.scalar_one_or_none()

    async def list_by_user(self, user_id: uuid.UUID) -> list[Membership]:
        result = await self.session.execute(
            select(Membership).where(Membership.user_id == user_id)
        )
        return list(result.scalars().all())

    async def list_by_project(self, project_id: uuid.UUID) -> list[Membership]:
        result = await self.session.execute(
            select(Membership).where(Membership.project_id == project_id)
        )
        return list(result.scalars().all())

    async def revoke(self, membership: Membership) -> Membership:
        membership.revoked_at = datetime.utcnow()
        self.session.add(membership)
        await self.session.commit()
        await self.session.refresh(membership)
        return membership
