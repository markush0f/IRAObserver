from __future__ import annotations

"""API endpoint analysis application service."""

import logging
from pathlib import Path
import uuid

from app.analysis.api_surface.analyzers.fastapi import extract_fastapi_endpoints
from app.analysis.api_surface.models.endpoint import EndpointCandidate
from app.analysis.filesystem.scanner import FileSystemScanner
from app.domains.analysis.models.dto.api_endpoint import (
    ApiEndpointCreate,
    ApiEndpointPublic,
    ProjectApiEndpointAnalysis,
)
from app.domains.analysis.repository.analysis_ignored_directory_repository import (
    AnalysisIgnoredDirectoryRepository,
)
from app.domains.projects.models.source_type import SourceType
from app.domains.projects.services.project_service import ProjectService
from app.domains.projects.services.snapshot_api_endpoint_service import (
    SnapshotApiEndpointService,
)
from app.domains.projects.services.snapshot_service import SnapshotService
from app.infrastructure.external.source.orchestartor import prepare_source


class ApiEndpointAnalysisService:
    """Analyze and persist API endpoints for projects."""

    logger = logging.getLogger(__name__)

    def __init__(
        self,
        project_service: ProjectService,
        ignored_directory_repository: AnalysisIgnoredDirectoryRepository,
        snapshot_service: SnapshotService,
        snapshot_api_endpoint_service: SnapshotApiEndpointService,
    ) -> None:
        self.project_service = project_service
        self.ignored_directory_repository = ignored_directory_repository
        self.snapshot_service = snapshot_service
        self.snapshot_api_endpoint_service = snapshot_api_endpoint_service

    async def analyze_and_store_api_endpoints(
        self, project_id: uuid.UUID
    ) -> ProjectApiEndpointAnalysis | None:
        """Analyze API endpoints, persist snapshot data, and return results."""
        self.logger.info(
            "Analyzing and storing API endpoints for project_id=%s", project_id
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

        detected = self._extract_fastapi_endpoints(scanner, source_path)
        return await self._store_detected_endpoints(
            project_id=project_id,
            detected=detected,
            title="API endpoint analysis snapshot",
        )

    async def analyze_and_store_fastapi_endpoints(
        self, project_id: uuid.UUID
    ) -> ProjectApiEndpointAnalysis | None:
        """Analyze FastAPI endpoints, persist snapshot data, and return results."""
        self.logger.info(
            "Analyzing and storing FastAPI endpoints for project_id=%s", project_id
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

        detected = self._extract_fastapi_endpoints(scanner, source_path)
        return await self._store_detected_endpoints(
            project_id=project_id,
            detected=detected,
            title="FastAPI endpoint analysis snapshot",
        )

    async def get_latest_api_endpoint_analysis(
        self, project_id: uuid.UUID
    ) -> ProjectApiEndpointAnalysis | None:
        """Return latest stored API endpoint analysis for a project."""
        self.logger.info(
            "Loading latest API endpoint analysis project_id=%s", project_id
        )
        project = await self.project_service.get_project(project_id)
        if not project:
            return None

        snapshot = await self.snapshot_service.get_latest_snapshot(project_id)
        if not snapshot:
            return ProjectApiEndpointAnalysis(endpoints=[])

        entries = await self.snapshot_api_endpoint_service.get_snapshot_api_endpoints(
            snapshot.id
        )
        return ProjectApiEndpointAnalysis(
            endpoints=[
                ApiEndpointPublic(
                    id=entry.id,
                    snapshot_id=entry.snapshot_id,
                    http_method=entry.http_method,
                    path=entry.path,
                    framework=entry.framework,
                    language=entry.language,
                    source_file=entry.source_file,
                    source_symbol=entry.source_symbol,
                    confidence=float(entry.confidence),
                    created_at=entry.created_at,
                )
                for entry in entries
            ]
        )

    def _extract_fastapi_endpoints(
        self, scanner: FileSystemScanner, root_path: Path
    ) -> list[EndpointCandidate]:
        endpoints: list[EndpointCandidate] = []
        for path in scanner.scan_files():
            if path.suffix.lower() != ".py":
                continue
            endpoints.extend(extract_fastapi_endpoints(path, root_path))
        return endpoints

    async def _store_detected_endpoints(
        self,
        project_id: uuid.UUID,
        detected: list[EndpointCandidate],
        title: str,
    ) -> ProjectApiEndpointAnalysis:
        if not detected:
            summary_json = {
                "title": title,
                "message": "No endpoints were found in this project.",
            }
            await self.snapshot_service.create_snapshot(
                project_id=project_id,
                summary_json=summary_json,
                commit_hash=None,
            )
            return ProjectApiEndpointAnalysis(endpoints=[])

        summary_json = {
            "title": title,
            "endpoints": [
                {
                    "method": endpoint.http_method,
                    "path": endpoint.path,
                    "framework": endpoint.framework,
                    "language": endpoint.language,
                }
                for endpoint in detected
            ],
            "detected_count": len(detected),
        }
        snapshot = await self.snapshot_service.create_snapshot(
            project_id=project_id,
            summary_json=summary_json,
            commit_hash=None,
        )
        created = await self.snapshot_api_endpoint_service.create_snapshot_api_endpoints(
            [
                ApiEndpointCreate(
                    snapshot_id=snapshot.id,
                    http_method=endpoint.http_method,
                    path=endpoint.path,
                    framework=endpoint.framework,
                    language=endpoint.language,
                    source_file=endpoint.source_file,
                    source_symbol=endpoint.source_symbol,
                    confidence=endpoint.confidence,
                )
                for endpoint in detected
            ]
        )
        return ProjectApiEndpointAnalysis(
            endpoints=[
                ApiEndpointPublic(
                    id=entry.id,
                    snapshot_id=entry.snapshot_id,
                    http_method=entry.http_method,
                    path=entry.path,
                    framework=entry.framework,
                    language=entry.language,
                    source_file=entry.source_file,
                    source_symbol=entry.source_symbol,
                    confidence=float(entry.confidence),
                    created_at=entry.created_at,
                )
                for entry in created
            ]
        )
