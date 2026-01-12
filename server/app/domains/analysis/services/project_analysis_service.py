from __future__ import annotations

"""Project analysis orchestration service."""

import uuid

from app.domains.analysis.models.dto.framework import ProjectFrameworkAnalysis
from app.domains.analysis.models.dto.infrastructure import ProjectInfrastructureAnalysis
from app.domains.analysis.models.dto.language import ProjectLanguageAnalysis
from app.domains.analysis.services.framework_analysis_service import (
    FrameworkAnalysisService,
)
from app.domains.analysis.services.infrastructure_analysis_service import (
    InfrastructureAnalysisService,
)
from app.domains.analysis.services.language_analysis_service import (
    LanguageAnalysisService,
)


class ProjectAnalysisService:
    """Compose language, framework, and infrastructure analysis services."""

    def __init__(
        self,
        language_analysis_service: LanguageAnalysisService,
        framework_analysis_service: FrameworkAnalysisService,
        infrastructure_analysis_service: InfrastructureAnalysisService,
    ) -> None:
        self.language_analysis_service = language_analysis_service
        self.framework_analysis_service = framework_analysis_service
        self.infrastructure_analysis_service = infrastructure_analysis_service

    async def analyze_and_store_languages(
        self, project_id: uuid.UUID
    ) -> ProjectLanguageAnalysis | None:
        """Analyze and persist detected languages for a project."""
        return await self.language_analysis_service.analyze_and_store_languages(
            project_id
        )

    async def get_latest_language_analysis(
        self, project_id: uuid.UUID
    ) -> ProjectLanguageAnalysis | None:
        """Get stored languages for a project."""
        return await self.language_analysis_service.get_latest_language_analysis(
            project_id
        )

    async def analyze_and_store_frameworks(
        self, project_id: uuid.UUID
    ) -> ProjectFrameworkAnalysis | None:
        """Analyze and persist detected frameworks for a project."""
        return await self.framework_analysis_service.analyze_and_store_frameworks(
            project_id
        )

    async def get_latest_framework_analysis(
        self, project_id: uuid.UUID
    ) -> ProjectFrameworkAnalysis | None:
        """Get stored frameworks for a project."""
        return await self.framework_analysis_service.get_latest_framework_analysis(
            project_id
        )

    async def analyze_and_store_infrastructure(
        self, project_id: uuid.UUID
    ) -> ProjectInfrastructureAnalysis | None:
        """Analyze and persist detected infrastructure for a project."""
        return (
            await self.infrastructure_analysis_service.analyze_and_store_infrastructure(
                project_id
            )
        )

    async def get_latest_infrastructure_analysis(
        self, project_id: uuid.UUID
    ) -> ProjectInfrastructureAnalysis | None:
        """Get stored infrastructure for a project."""
        return (
            await self.infrastructure_analysis_service.get_latest_infrastructure_analysis(
                project_id
            )
        )
