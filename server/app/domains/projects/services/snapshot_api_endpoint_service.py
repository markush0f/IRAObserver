from __future__ import annotations

"""Snapshot API endpoint domain services."""

import uuid

from app.domains.analysis.models.dto.api_endpoint import ApiEndpointCreate
from app.infrastructure.persistence.postgres.analysis.entities.api_endpoint import ApiEndpoint
from app.domains.analysis.repository.api_endpoint_repository import (
    ApiEndpointRepository,
)


class SnapshotApiEndpointService:
    """Application logic for snapshot API endpoint storage."""

    def __init__(self, api_endpoint_repository: ApiEndpointRepository) -> None:
        self.api_endpoint_repository = api_endpoint_repository

    async def create_snapshot_api_endpoints(
        self, endpoints: list[ApiEndpointCreate]
    ) -> list[ApiEndpoint]:
        """Create API endpoint entries for a snapshot."""
        entries = [
            ApiEndpoint(
                snapshot_id=endpoint.snapshot_id,
                http_method=endpoint.http_method,
                path=endpoint.path,
                framework=endpoint.framework,
                language=endpoint.language,
                source_file=endpoint.source_file,
                source_symbol=endpoint.source_symbol,
                confidence=endpoint.confidence,
            )
            for endpoint in endpoints
        ]
        if not entries:
            return []
        return await self.api_endpoint_repository.create_many(entries)

    async def get_snapshot_api_endpoints(
        self, snapshot_id: uuid.UUID
    ) -> list[ApiEndpoint]:
        """Return API endpoints for a snapshot."""
        return await self.api_endpoint_repository.list_by_snapshot(snapshot_id)

    async def get_project_api_endpoints(
        self,
        project_id: uuid.UUID,
        limit: int = 100,
        offset: int = 0,
        http_method: str | None = None,
    ) -> list[ApiEndpoint]:
        """Return API endpoints for a project."""
        return await self.api_endpoint_repository.list_by_project(
            project_id=project_id,
            limit=limit,
            offset=offset,
            http_method=http_method,
        )

    async def count_project_api_endpoints(
        self, project_id: uuid.UUID, http_method: str | None = None
    ) -> int:
        """Count API endpoints for a project."""
        return await self.api_endpoint_repository.count_by_project(
            project_id=project_id,
            http_method=http_method,
        )
