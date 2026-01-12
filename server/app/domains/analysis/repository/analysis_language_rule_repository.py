from __future__ import annotations

"""Postgres repository for analysis language rules."""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.analysis.models.entities.analysis_language_rule import (
    AnalysisLanguageRule,
)


class AnalysisLanguageRuleRepository:
    """Data access for analysis language rules."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, rule: AnalysisLanguageRule) -> AnalysisLanguageRule:
        """Persist a language rule and return the stored entity."""
        self.session.add(rule)
        await self.session.commit()
        await self.session.refresh(rule)
        return rule

    async def get_by_id(
        self, rule_id: uuid.UUID
    ) -> AnalysisLanguageRule | None:
        """Return a language rule by id or None."""
        result = await self.session.execute(
            select(AnalysisLanguageRule).where(AnalysisLanguageRule.id == rule_id)
        )
        return result.scalar_one_or_none()

    async def list(
        self, limit: int = 100, offset: int = 0
    ) -> list[AnalysisLanguageRule]:
        """List language rules with pagination."""
        result = await self.session.execute(
            select(AnalysisLanguageRule).limit(limit).offset(offset)
        )
        return list(result.scalars().all())

    async def list_active(self) -> list[AnalysisLanguageRule]:
        """List active language rules."""
        result = await self.session.execute(
            select(AnalysisLanguageRule).where(AnalysisLanguageRule.is_active.is_(True))
        )
        return list(result.scalars().all())
