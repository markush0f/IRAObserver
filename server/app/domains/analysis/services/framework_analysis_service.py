from __future__ import annotations

"""Framework analysis application service."""

import logging
import uuid

from app.analysis.filesystem.scanner import FileSystemScanner
from app.domains.analysis.models.dto.framework import ProjectFrameworkAnalysis
from app.domains.projects.models.source_type import SourceType
from app.domains.analysis.repository.analysis_framework_rule_repository import (
    AnalysisFrameworkRuleRepository,
)
from app.domains.analysis.repository.analysis_ignored_directory_repository import (
    AnalysisIgnoredDirectoryRepository,
)
from app.domains.projects.services.framework_detector import (
    FrameworkDetector,
    FrameworkRule,
)
from app.domains.projects.services.project_service import ProjectService
from app.domains.projects.services.snapshot_framework_service import (
    SnapshotFrameworkService,
)
from app.domains.projects.services.snapshot_service import SnapshotService
from app.infrastructure.external.source.orchestartor import prepare_source


class FrameworkAnalysisService:
    """Analyze and persist framework detections for projects."""

    logger = logging.getLogger(__name__)

    def __init__(
        self,
        project_service: ProjectService,
        framework_rule_repository: AnalysisFrameworkRuleRepository,
        ignored_directory_repository: AnalysisIgnoredDirectoryRepository,
        snapshot_service: SnapshotService,
        snapshot_framework_service: SnapshotFrameworkService,
    ) -> None:
        self.project_service = project_service
        self.framework_rule_repository = framework_rule_repository
        self.ignored_directory_repository = ignored_directory_repository
        self.snapshot_service = snapshot_service
        self.snapshot_framework_service = snapshot_framework_service

    async def analyze_and_store_frameworks(
        self, project_id: uuid.UUID
    ) -> ProjectFrameworkAnalysis | None:
        """Analyze frameworks, persist snapshot data, and return results."""
        self.logger.info(
            "Analyzing and storing frameworks for project_id=%s", project_id
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
            await self.framework_rule_repository.list_active_with_framework_name()
        )
        ignored_directories = await self.ignored_directory_repository.list_active()

        detector_rules = [
            FrameworkRule(
                framework=framework_name,
                signal_type=rule.signal_type,
                signal_value=rule.signal_value,
                weight=rule.weight,
            )
            for rule, framework_name in rules_with_names
        ]

        detector = FrameworkDetector(detector_rules)
        scanner = FileSystemScanner(
            root_path=source_path,
            ignored_directories={entry.name for entry in ignored_directories},
        )
        frameworks = detector.detect(scanner)
        self.logger.info(
            "Detected frameworks project_id=%s count=%s",
            project_id,
            len(frameworks),
        )
        summary_json = {
            "title": "Framework analysis snapshot",
            "frameworks": [
                {"name": name, "confidence": confidence}
                for name, confidence in sorted(
                    frameworks.items(), key=lambda item: item[1], reverse=True
                )
            ],
            "detected_count": len(frameworks),
        }
        snapshot = await self.snapshot_service.create_snapshot(
            project_id=project_id,
            summary_json=summary_json,
            commit_hash=None,
        )
        await self.snapshot_framework_service.create_snapshot_frameworks(
            snapshot_id=snapshot.id,
            frameworks=frameworks,
        )
        return ProjectFrameworkAnalysis(frameworks=frameworks)

    async def get_latest_framework_analysis(
        self, project_id: uuid.UUID
    ) -> ProjectFrameworkAnalysis | None:
        """Return latest stored framework analysis for a project."""
        self.logger.info("Loading latest framework analysis project_id=%s", project_id)
        project = await self.project_service.get_project(project_id)
        if not project:
            return None

        snapshot = await self.snapshot_service.get_latest_snapshot(project_id)
        if not snapshot:
            return ProjectFrameworkAnalysis(frameworks={})

        frameworks = await self.snapshot_framework_service.get_snapshot_frameworks(
            snapshot.id
        )
        return ProjectFrameworkAnalysis(frameworks=frameworks)
