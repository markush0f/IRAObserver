from __future__ import annotations

"""Project analysis services."""

import logging
import uuid

from app.analysis.filesystem.scanner import FileSystemScanner
from app.domains.projects.models.dto.project import ProjectLanguageAnalysis
from app.domains.projects.models.source_type import SourceType
from app.domains.projects.repository.analysis_ignored_directory_repository import (
    AnalysisIgnoredDirectoryRepository,
)
from app.domains.projects.repository.analysis_language_rule_repository import (
    AnalysisLanguageRuleRepository,
)
from app.domains.projects.repository.project_repository import ProjectRepository
from app.domains.projects.services.language_detector import LanguageDetector, LanguageRule
from app.infrastructure.external.source.orchestartor import prepare_source


class ProjectAnalysisService:
    """Application logic for project analysis."""

    logger = logging.getLogger(__name__)

    def __init__(
        self,
        project_repository: ProjectRepository,
        language_rule_repository: AnalysisLanguageRuleRepository,
        ignored_directory_repository: AnalysisIgnoredDirectoryRepository,
    ) -> None:
        self.project_repository = project_repository
        self.language_rule_repository = language_rule_repository
        self.ignored_directory_repository = ignored_directory_repository

    async def get_language_analysis(
        self, project_id: uuid.UUID
    ) -> ProjectLanguageAnalysis | None:
        """Return detected languages for a project or None if missing."""
        self.logger.info("Analyzing languages for project_id=%s", project_id)
        project = await self.project_repository.get_by_id(project_id)
        if not project:
            return None

        source_path = prepare_source(
            source_type=SourceType(project.source_type),
            source_ref=project.source_ref,
        )

        rules = await self.language_rule_repository.list_active()
        ignored_directories = await self.ignored_directory_repository.list_active()

        detector_rules = [
            LanguageRule(
                extension=rule.extension,
                language=rule.language,
                weight=rule.weight,
            )
            for rule in rules
        ]

        detector = LanguageDetector(detector_rules)
        scanner = FileSystemScanner(
            root_path=source_path,
            ignored_directories={entry.name for entry in ignored_directories},
        )
        languages = detector.detect(scanner)
        return ProjectLanguageAnalysis(languages=languages)
