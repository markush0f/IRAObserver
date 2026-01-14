"""Projects domain dependency providers."""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.domains.projects.repository.project_repository import ProjectRepository
from app.domains.projects.repository.snapshot_repository import SnapshotRepository
from app.domains.projects.services.project_service import ProjectService
from app.domains.projects.services.snapshot_service import SnapshotService
from app.domains.analysis.repository.analysis_ignored_directory_repository import (
    AnalysisIgnoredDirectoryRepository,
)
from app.domains.projects.services.project_tree_service import ProjectTreeService
from app.domains.analysis.repository.snapshot_framework_repository import (
    SnapshotFrameworkRepository,
)
from app.domains.analysis.repository.snapshot_infrastructure_repository import (
    SnapshotInfrastructureRepository,
)
from app.domains.analysis.repository.snapshot_language_repository import (
    SnapshotLanguageRepository,
)
from app.domains.projects.services.snapshot_framework_service import (
    SnapshotFrameworkService,
)
from app.domains.projects.services.snapshot_infrastructure_service import (
    SnapshotInfrastructureService,
)
from app.domains.projects.services.snapshot_language_service import (
    SnapshotLanguageService,
)


def get_project_repository(
    session: AsyncSession = Depends(get_db),
) -> ProjectRepository:
    """Provide a project repository instance."""
    return ProjectRepository(session)


def get_project_service(
    project_repository: ProjectRepository = Depends(get_project_repository),
) -> ProjectService:
    """Provide a project service instance."""
    return ProjectService(project_repository)


def get_snapshot_repository(
    session: AsyncSession = Depends(get_db),
) -> SnapshotRepository:
    """Provide a snapshot repository instance."""
    return SnapshotRepository(session)


def get_snapshot_service(
    snapshot_repository: SnapshotRepository = Depends(get_snapshot_repository),
    project_service: ProjectService = Depends(get_project_service),
) -> SnapshotService:
    """Provide a snapshot service instance."""
    return SnapshotService(
        snapshot_repository=snapshot_repository,
        project_service=project_service,
    )


def get_analysis_ignored_directory_repository(
    session: AsyncSession = Depends(get_db),
) -> AnalysisIgnoredDirectoryRepository:
    """Provide an ignored directory repository instance."""
    return AnalysisIgnoredDirectoryRepository(session)


def get_project_tree_service(
    project_service: ProjectService = Depends(get_project_service),
    ignored_directory_repository: AnalysisIgnoredDirectoryRepository = Depends(
        get_analysis_ignored_directory_repository
    ),
) -> ProjectTreeService:
    """Provide a project tree service instance."""
    return ProjectTreeService(
        project_service=project_service,
        ignored_directory_repository=ignored_directory_repository,
    )


def get_snapshot_framework_repository(
    session: AsyncSession = Depends(get_db),
) -> SnapshotFrameworkRepository:
    """Provide a snapshot framework repository instance."""
    return SnapshotFrameworkRepository(session)


def get_snapshot_infrastructure_repository(
    session: AsyncSession = Depends(get_db),
) -> SnapshotInfrastructureRepository:
    """Provide a snapshot infrastructure repository instance."""
    return SnapshotInfrastructureRepository(session)


def get_snapshot_language_repository(
    session: AsyncSession = Depends(get_db),
) -> SnapshotLanguageRepository:
    """Provide a snapshot language repository instance."""
    return SnapshotLanguageRepository(session)


def get_snapshot_framework_service(
    snapshot_framework_repository: SnapshotFrameworkRepository = Depends(
        get_snapshot_framework_repository
    ),
) -> SnapshotFrameworkService:
    """Provide a snapshot framework service instance."""
    return SnapshotFrameworkService(
        snapshot_framework_repository=snapshot_framework_repository,
    )


def get_snapshot_infrastructure_service(
    snapshot_infrastructure_repository: SnapshotInfrastructureRepository = Depends(
        get_snapshot_infrastructure_repository
    ),
) -> SnapshotInfrastructureService:
    """Provide a snapshot infrastructure service instance."""
    return SnapshotInfrastructureService(
        snapshot_infrastructure_repository=snapshot_infrastructure_repository,
    )


def get_snapshot_language_service(
    snapshot_language_repository: SnapshotLanguageRepository = Depends(
        get_snapshot_language_repository
    ),
) -> SnapshotLanguageService:
    """Provide a snapshot language service instance."""
    return SnapshotLanguageService(
        snapshot_language_repository=snapshot_language_repository,
    )
