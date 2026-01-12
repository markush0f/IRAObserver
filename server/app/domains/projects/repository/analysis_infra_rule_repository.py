from __future__ import annotations

"""Postgres repository for analysis infrastructure rules."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.projects.models.entities.analysis_infra_component import (
    AnalysisInfraComponent,
)
from app.domains.projects.models.entities.analysis_infra_rule import AnalysisInfraRule


class AnalysisInfraRuleRepository:
    """Data access for analysis infrastructure rules."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_active_with_component_name(
        self,
    ) -> list[tuple[AnalysisInfraRule, str]]:
        """List active infra rules with component name."""
        result = await self.session.execute(
            select(AnalysisInfraRule, AnalysisInfraComponent.name)
            .join(
                AnalysisInfraComponent,
                AnalysisInfraComponent.id == AnalysisInfraRule.infra_component_id,
            )
            .where(
                AnalysisInfraRule.is_active.is_(True),
                AnalysisInfraComponent.is_active.is_(True),
            )
        )
        return list(result.all())
