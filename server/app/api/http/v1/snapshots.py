from __future__ import annotations

"""Snapshot endpoints."""

import logging
import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.deps import get_current_user, get_snapshot_service
from app.domains.identity.models.entities.user import User
from app.domains.projects.models.dto.snapshot import SnapshotPage, SnapshotPageNoSummary
from app.domains.projects.services.snapshot_service import SnapshotService

router = APIRouter(prefix="/projects", tags=["snapshots"])
logger = logging.getLogger(__name__)


@router.get("/{project_id}/snapshots", response_model=SnapshotPage)
async def list_project_snapshots(
    project_id: uuid.UUID,
    snapshot_service: SnapshotService = Depends(get_snapshot_service),
    current_user: User = Depends(get_current_user),
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    start_at: datetime | None = Query(default=None),
    end_at: datetime | None = Query(default=None),
) -> SnapshotPage:
    """List snapshots for a project with pagination and date filters."""
    logger.info(
        "GET /projects/%s/snapshots by user_id=%s", project_id, current_user.id
    )
    page = await snapshot_service.list_snapshots(
        project_id=project_id,
        limit=limit,
        offset=offset,
        start_at=start_at,
        end_at=end_at,
    )
    if page is None:
        raise HTTPException(status_code=404, detail="project not found")
    return page


@router.get(
    "/{project_id}/snapshots/compact",
    response_model=SnapshotPageNoSummary,
)
async def list_project_snapshots_compact(
    project_id: uuid.UUID,
    snapshot_service: SnapshotService = Depends(get_snapshot_service),
    current_user: User = Depends(get_current_user),
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    start_at: datetime | None = Query(default=None),
    end_at: datetime | None = Query(default=None),
) -> SnapshotPageNoSummary:
    """List snapshots for a project without summary_json."""
    logger.info(
        "GET /projects/%s/snapshots/compact by user_id=%s",
        project_id,
        current_user.id,
    )
    page = await snapshot_service.list_snapshots_without_summary(
        project_id=project_id,
        limit=limit,
        offset=offset,
        start_at=start_at,
        end_at=end_at,
    )
    if page is None:
        raise HTTPException(status_code=404, detail="project not found")
    return page
