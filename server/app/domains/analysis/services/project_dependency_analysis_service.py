from __future__ import annotations

from app.shared.filesystem.scanner import FileSystemScanner

"""Project dependency analysis application service."""
import logging
from pathlib import Path
import uuid

from app.analysis.dependency.base import DependencyCandidate
from app.analysis.dependency.requirements import RequirementsDependencyExtractor
from app.domains.analysis.models.dto.dependency import (
    ProjectDependencyCreate,
    ProjectDependencyPublic,
)
from app.domains.analysis.repository.analysis_ignored_directory_repository import (
    AnalysisIgnoredDirectoryRepository,
)
from app.domains.projects.models.source_type import SourceType
from app.domains.projects.services.project_service import ProjectService
from app.domains.projects.services.snapshot_project_dependency_service import (
    SnapshotProjectDependencyService,
)
from app.domains.projects.services.snapshot_service import SnapshotService
from app.infrastructure.external.source.orchestartor import prepare_source


class ProjectDependencyAnalysisService:
    """Analyze and persist project dependencies."""

    logger = logging.getLogger(__name__)

    def __init__(
        self,
        project_service: ProjectService,
        ignored_directory_repository: AnalysisIgnoredDirectoryRepository,
        snapshot_service: SnapshotService,
        snapshot_dependency_service: SnapshotProjectDependencyService,
    ) -> None:
        self.project_service = project_service
        self.ignored_directory_repository = ignored_directory_repository
        self.snapshot_service = snapshot_service
        self.snapshot_dependency_service = snapshot_dependency_service

    async def analyze_and_store_dependencies(
        self, project_id: uuid.UUID
    ) -> list[ProjectDependencyPublic] | None:
        """Analyze project dependencies, persist snapshot data, and return results."""
        self.logger.info(
            "Analyzing and storing dependencies for project_id=%s", project_id
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
        ignored_directories = await self.ignored_directory_repository.list_active()
        scanner = FileSystemScanner(
            root_path=source_path,
            ignored_directories={entry.name for entry in ignored_directories},
        )

        detected = self._extract_dependencies(scanner, source_path)
        if not detected:
            summary_json = {
                "title": "Dependency analysis snapshot",
                "message": "No dependencies were found in this project.",
            }
            await self.snapshot_service.create_snapshot(
                project_id=project_id,
                summary_json=summary_json,
                commit_hash=None,
            )
            return []

        summary_json = {
            "title": "Dependency analysis snapshot",
            "dependencies": [
                {
                    "name": dependency.name,
                    "version": dependency.version,
                    "ecosystem": dependency.ecosystem,
                    "scope": dependency.scope,
                    "source_file": dependency.source_file,
                }
                for dependency in detected
            ],
            "detected_count": len(detected),
        }
        snapshot = await self.snapshot_service.create_snapshot(
            project_id=project_id,
            summary_json=summary_json,
            commit_hash=None,
        )
        created = await self.snapshot_dependency_service.create_snapshot_dependencies(
            [
                ProjectDependencyCreate(
                    snapshot_id=snapshot.id,
                    name=dependency.name,
                    version=dependency.version,
                    ecosystem=dependency.ecosystem,
                    scope=dependency.scope,
                    source_file=dependency.source_file,
                )
                for dependency in detected
            ]
        )
        return [
            ProjectDependencyPublic(
                id=entry.id,
                snapshot_id=entry.snapshot_id,
                name=entry.name,
                version=entry.version,
                ecosystem=entry.ecosystem,
                scope=entry.scope,
                source_file=entry.source_file,
                created_at=entry.created_at,
            )
            for entry in created
        ]

    async def get_latest_dependencies(
        self, project_id: uuid.UUID
    ) -> list[ProjectDependencyPublic] | None:
        """Return latest stored dependency analysis for a project."""
        self.logger.info("Loading latest dependency analysis project_id=%s", project_id)
        project = await self.project_service.get_project(project_id)
        if not project:
            return None

        snapshot = await self.snapshot_service.get_latest_snapshot(project_id)
        if not snapshot:
            return []

        entries = await self.snapshot_dependency_service.get_snapshot_dependencies(
            snapshot.id
        )
        return [
            ProjectDependencyPublic(
                id=entry.id,
                snapshot_id=entry.snapshot_id,
                name=entry.name,
                version=entry.version,
                ecosystem=entry.ecosystem,
                scope=entry.scope,
                source_file=entry.source_file,
                created_at=entry.created_at,
            )
            for entry in entries
        ]

    def _extract_dependencies(
        self, scanner: FileSystemScanner, root_path: Path
    ) -> list[DependencyCandidate]:
        extractor = RequirementsDependencyExtractor()
        dependencies: list[DependencyCandidate] = []
        for path in scanner.scan_files():
            if path.name != "requirements.txt":
                continue
            dependencies.extend(extractor.extract(path, root_path))
        return dependencies
