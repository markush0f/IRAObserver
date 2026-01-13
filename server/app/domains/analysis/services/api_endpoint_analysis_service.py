from __future__ import annotations

"""API endpoint analysis application service."""

from dataclasses import dataclass
import logging
from pathlib import Path
import re
import uuid

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

HTTP_METHODS = ("get", "post", "put", "delete", "patch", "options", "head")
PY_DECORATOR_RE = re.compile(
    r"@(?P<target>app|router)\.(?P<method>"
    + "|".join(HTTP_METHODS)
    + r")\s*\(\s*[\"'](?P<path>[^\"']+)[\"']",
)
PY_ROUTE_RE = re.compile(
    r"@(?P<target>app|router)\.(?P<route_type>route|api_route)\s*\("
    r"\s*[\"'](?P<path>[^\"']+)[\"']\s*,\s*methods\s*=\s*\[(?P<methods>[^\]]+)\]",
)
PY_ROUTER_PREFIX_RE = re.compile(
    r"APIRouter\([\s\S]*?prefix\s*=\s*[\"'](?P<prefix>[^\"']+)[\"']"
)
PY_DEF_RE = re.compile(r"(async\s+def|def)\s+(?P<name>[A-Za-z_][A-Za-z0-9_]*)")
JS_ROUTE_RE = re.compile(
    r"\b(?P<target>app|router)\.(?P<method>"
    + "|".join(HTTP_METHODS)
    + r")\s*\(\s*(?P<quote>[\"'])(?P<path>[^\"']+)(?P=quote)"
)
JS_HANDLER_RE = re.compile(
    r"\b(?:app|router)\.(?:"
    + "|".join(HTTP_METHODS)
    + r")\s*\(\s*[\"'][^\"']+[\"']\s*,\s*(?P<handler>[A-Za-z_$][A-Za-z0-9_$]*)"
)


@dataclass(frozen=True)
class _DetectedEndpoint:
    http_method: str
    path: str
    framework: str
    language: str
    source_file: str
    source_symbol: str | None
    confidence: float = 1.0


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
        )
        ignored_directories = await self.ignored_directory_repository.list_active()
        scanner = FileSystemScanner(
            root_path=source_path,
            ignored_directories={entry.name for entry in ignored_directories},
        )

        detected = self._extract_endpoints(scanner, source_path)
        if not detected:
            summary_json = {
                "title": "API endpoint analysis snapshot",
                "message": "No endpoints were found in this project.",
            }
            await self.snapshot_service.create_snapshot(
                project_id=project_id,
                summary_json=summary_json,
                commit_hash=None,
            )
            return ProjectApiEndpointAnalysis(endpoints=[])

        summary_json = {
            "title": "API endpoint analysis snapshot",
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

    def _extract_endpoints(
        self, scanner: FileSystemScanner, root_path: Path
    ) -> list[_DetectedEndpoint]:
        endpoints: list[_DetectedEndpoint] = []
        for path in scanner.scan_files():
            if path.suffix.lower() == ".py":
                endpoints.extend(self._extract_from_python(path, root_path))
            elif path.suffix.lower() in {".js", ".jsx", ".ts", ".tsx"}:
                endpoints.extend(self._extract_from_js(path, root_path))
        return endpoints

    def _extract_from_python(
        self, path: Path, root_path: Path
    ) -> list[_DetectedEndpoint]:
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            return []

        router_prefix = self._parse_router_prefix(text)
        framework = self._detect_python_framework(text)
        language = "python"
        source_file = self._relative_path(path, root_path)

        lines = text.splitlines()
        endpoints: list[_DetectedEndpoint] = []
        for index, line in enumerate(lines):
            decorator_match = PY_DECORATOR_RE.search(line)
            if decorator_match:
                http_method = decorator_match.group("method").upper()
                path_value = decorator_match.group("path")
                path_value = self._apply_prefix(
                    router_prefix if decorator_match.group("target") == "router" else "",
                    path_value,
                )
                source_symbol = self._find_python_symbol(lines, index)
                endpoints.append(
                    _DetectedEndpoint(
                        http_method=http_method,
                        path=path_value,
                        framework=framework,
                        language=language,
                        source_file=source_file,
                        source_symbol=source_symbol,
                    )
                )
                continue

            route_match = PY_ROUTE_RE.search(line)
            if not route_match:
                continue
            path_value = route_match.group("path")
            path_value = self._apply_prefix(
                router_prefix if route_match.group("target") == "router" else "",
                path_value,
            )
            methods = self._parse_methods(route_match.group("methods"))
            source_symbol = self._find_python_symbol(lines, index)
            for method in methods:
                endpoints.append(
                    _DetectedEndpoint(
                        http_method=method,
                        path=path_value,
                        framework=framework,
                        language=language,
                        source_file=source_file,
                        source_symbol=source_symbol,
                    )
                )
        return endpoints

    def _extract_from_js(self, path: Path, root_path: Path) -> list[_DetectedEndpoint]:
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            return []

        framework = self._detect_js_framework(text)
        language = self._language_from_suffix(path.suffix.lower())
        source_file = self._relative_path(path, root_path)
        endpoints: list[_DetectedEndpoint] = []
        for line in text.splitlines():
            match = JS_ROUTE_RE.search(line)
            if not match:
                continue
            http_method = match.group("method").upper()
            path_value = match.group("path")
            handler_match = JS_HANDLER_RE.search(line)
            source_symbol = handler_match.group("handler") if handler_match else None
            endpoints.append(
                _DetectedEndpoint(
                    http_method=http_method,
                    path=path_value,
                    framework=framework,
                    language=language,
                    source_file=source_file,
                    source_symbol=source_symbol,
                )
            )
        return endpoints

    @staticmethod
    def _parse_router_prefix(text: str) -> str:
        match = PY_ROUTER_PREFIX_RE.search(text)
        return match.group("prefix") if match else ""

    @staticmethod
    def _parse_methods(methods_raw: str) -> list[str]:
        matches = re.findall(r"[\"'](?P<method>[A-Za-z]+)[\"']", methods_raw)
        return [method.upper() for method in matches] if matches else ["GET"]

    @staticmethod
    def _find_python_symbol(lines: list[str], start_index: int) -> str | None:
        for line in lines[start_index + 1 :]:
            stripped = line.strip()
            if not stripped or stripped.startswith("@"):
                continue
            match = PY_DEF_RE.match(stripped)
            if match:
                return match.group("name")
            break
        return None

    @staticmethod
    def _apply_prefix(prefix: str, path_value: str) -> str:
        if not prefix:
            return path_value
        if not path_value:
            return prefix
        return f"{prefix.rstrip('/')}/{path_value.lstrip('/')}"

    @staticmethod
    def _detect_python_framework(text: str) -> str:
        lowered = text.lower()
        if "fastapi" in lowered or "apirouter" in lowered:
            return "fastapi"
        if "flask" in lowered:
            return "flask"
        return "unknown"

    @staticmethod
    def _detect_js_framework(text: str) -> str:
        lowered = text.lower()
        if "express" in lowered:
            return "express"
        if "fastify" in lowered:
            return "fastify"
        return "unknown"

    @staticmethod
    def _language_from_suffix(suffix: str) -> str:
        if suffix in {".ts", ".tsx"}:
            return "typescript"
        return "javascript"

    @staticmethod
    def _relative_path(path: Path, root_path: Path) -> str:
        try:
            return path.relative_to(root_path).as_posix()
        except ValueError:
            return path.as_posix()
