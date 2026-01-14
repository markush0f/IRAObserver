from __future__ import annotations

from app.shared.filesystem.scanner import FileSystemScanner

"""Infrastructure analysis application service."""

import logging
import uuid

from app.domains.analysis.models.dto.infrastructure import ProjectInfrastructureAnalysis
from app.domains.projects.models.source_type import SourceType
from app.domains.analysis.repository.analysis_ignored_directory_repository import (
    AnalysisIgnoredDirectoryRepository,
)
from app.domains.analysis.repository.analysis_infra_rule_repository import (
    AnalysisInfraRuleRepository,
)
from app.domains.projects.services.infra_detector import InfraDetector, InfraRule
from app.domains.projects.services.project_service import ProjectService
from app.domains.projects.services.snapshot_infrastructure_service import (
    SnapshotInfrastructureService,
)
from app.domains.projects.services.snapshot_service import SnapshotService
from app.infrastructure.external.source.orchestartor import prepare_source


class InfrastructureAnalysisService:
    """Analyze and persist infrastructure detections for projects."""

    logger = logging.getLogger(__name__)

    def __init__(
        self,
        project_service: ProjectService,
        infra_rule_repository: AnalysisInfraRuleRepository,
        ignored_directory_repository: AnalysisIgnoredDirectoryRepository,
        snapshot_service: SnapshotService,
        snapshot_infrastructure_service: SnapshotInfrastructureService,
    ) -> None:
        self.project_service = project_service
        self.infra_rule_repository = infra_rule_repository
        self.ignored_directory_repository = ignored_directory_repository
        self.snapshot_service = snapshot_service
        self.snapshot_infrastructure_service = snapshot_infrastructure_service

    async def analyze_and_store_infrastructure(
        self, project_id: uuid.UUID
    ) -> ProjectInfrastructureAnalysis | None:
        """Analyze infrastructure, persist snapshot data, and return results."""
        self.logger.info(
            "Analyzing and storing infrastructure for project_id=%s", project_id
        )
        project = await self.project_service.get_project(project_id)
        if not project:
            return None

        source_path = prepare_source(
            source_type=SourceType(project.source_type),
            source_ref=project.source_ref,
            project_id=project.id,
            allow_clone=False,
        )
        rules_with_names = (
            await self.infra_rule_repository.list_active_with_component_name()
        )
        ignored_directories = await self.ignored_directory_repository.list_active()

        detector_rules = [
            InfraRule(
                component=component_name,
                signal_type=rule.signal_type,
                signal_value=rule.signal_value,
                weight=rule.weight,
            )
            for rule, component_name in rules_with_names
        ]

        detector = InfraDetector(detector_rules)
        scanner = FileSystemScanner(
            root_path=source_path,
            ignored_directories={entry.name for entry in ignored_directories},
        )
        components = detector.detect(scanner)
        self.logger.info(
            "Detected infrastructure components project_id=%s count=%s",
            project_id,
            len(components),
        )
        summary_json = {
            "title": "Infrastructure analysis snapshot",
            "components": [{"name": component} for component in components],
            "detected_count": len(components),
        }
        snapshot = await self.snapshot_service.create_snapshot(
            project_id=project_id,
            summary_json=summary_json,
            commit_hash=None,
        )
        await self.snapshot_infrastructure_service.create_snapshot_infrastructure(
            snapshot_id=snapshot.id,
            components=components,
        )
        return ProjectInfrastructureAnalysis(components=components)

    async def get_latest_infrastructure_analysis(
        self, project_id: uuid.UUID
    ) -> ProjectInfrastructureAnalysis | None:
        """Return latest stored infrastructure analysis for a project."""
        self.logger.info(
            "Loading latest infrastructure analysis project_id=%s", project_id
        )
        project = await self.project_service.get_project(project_id)
        if not project:
            return None

        snapshot = await self.snapshot_service.get_latest_snapshot(project_id)
        if not snapshot:
            return ProjectInfrastructureAnalysis(components=[])

        components = (
            await self.snapshot_infrastructure_service.get_snapshot_infrastructure(
                snapshot.id
            )
        )
        return ProjectInfrastructureAnalysis(components=components)
