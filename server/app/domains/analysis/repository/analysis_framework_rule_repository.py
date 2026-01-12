from __future__ import annotations

"""Postgres repository for analysis framework rules."""

from app.domains.analysis.models.entities.analysis_framework import AnalysisFramework
from app.domains.analysis.models.entities.analysis_framework_rule import (
    AnalysisFrameworkRule,
)

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession



class AnalysisFrameworkRuleRepository:
    """Data access for analysis framework rules."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_active_with_framework_name(
        self,
    ) -> list[tuple[AnalysisFrameworkRule, str]]:
        """List active framework rules with framework name."""
        result = await self.session.execute(
            select(AnalysisFrameworkRule, AnalysisFramework.name)
            .join(
                AnalysisFramework,
                AnalysisFramework.id == AnalysisFrameworkRule.framework_id,
            )
            .where(
                AnalysisFrameworkRule.is_active.is_(True),
                AnalysisFramework.is_active.is_(True),
            )
        )
        return list(result.all())
