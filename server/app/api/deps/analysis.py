"""Analysis domain dependency providers."""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.domains.analysis.repository.analysis_ignored_directory_repository import (
    AnalysisIgnoredDirectoryRepository,
)
from app.domains.analysis.repository.analysis_framework_rule_repository import (
    AnalysisFrameworkRuleRepository,
)
from app.domains.analysis.repository.analysis_infra_rule_repository import (
    AnalysisInfraRuleRepository,
)
from app.domains.analysis.repository.analysis_language_rule_repository import (
    AnalysisLanguageRuleRepository,
)
from app.domains.analysis.repository.api_endpoint_repository import (
    ApiEndpointRepository,
)
from app.domains.analysis.repository.project_dependency_repository import (
    ProjectDependencyRepository,
)
from app.domains.analysis.services.api_endpoint_analysis_service import (
    ApiEndpointAnalysisService,
)
from app.domains.analysis.services.framework_analysis_service import (
    FrameworkAnalysisService,
)
from app.domains.analysis.services.infrastructure_analysis_service import (
    InfrastructureAnalysisService,
)
from app.domains.analysis.services.language_analysis_service import (
    LanguageAnalysisService,
)
from app.domains.analysis.services.project_dependency_analysis_service import (
    ProjectDependencyAnalysisService,
)
from app.domains.analysis.services.project_analysis_service import (
    ProjectAnalysisService,
)
from app.domains.projects.services.snapshot_api_endpoint_service import (
    SnapshotApiEndpointService,
)
from app.domains.projects.services.snapshot_project_dependency_service import (
    SnapshotProjectDependencyService,
)
from app.api.deps.projects import (
    get_project_service,
    get_snapshot_framework_service,
    get_snapshot_infrastructure_service,
    get_snapshot_language_service,
    get_snapshot_service,
)


def get_api_endpoint_repository(
    session: AsyncSession = Depends(get_db),
) -> ApiEndpointRepository:
    """Provide an API endpoint repository instance."""
    return ApiEndpointRepository(session)


def get_project_dependency_repository(
    session: AsyncSession = Depends(get_db),
) -> ProjectDependencyRepository:
    """Provide a project dependency repository instance."""
    return ProjectDependencyRepository(session)


def get_analysis_language_rule_repository(
    session: AsyncSession = Depends(get_db),
) -> AnalysisLanguageRuleRepository:
    """Provide a language rule repository instance."""
    return AnalysisLanguageRuleRepository(session)


def get_analysis_framework_rule_repository(
    session: AsyncSession = Depends(get_db),
) -> AnalysisFrameworkRuleRepository:
    """Provide a framework rule repository instance."""
    return AnalysisFrameworkRuleRepository(session)


def get_analysis_infra_rule_repository(
    session: AsyncSession = Depends(get_db),
) -> AnalysisInfraRuleRepository:
    """Provide an infrastructure rule repository instance."""
    return AnalysisInfraRuleRepository(session)


def get_analysis_ignored_directory_repository(
    session: AsyncSession = Depends(get_db),
) -> AnalysisIgnoredDirectoryRepository:
    """Provide an ignored directory repository instance."""
    return AnalysisIgnoredDirectoryRepository(session)


def get_snapshot_api_endpoint_service(
    api_endpoint_repository: ApiEndpointRepository = Depends(
        get_api_endpoint_repository
    ),
) -> SnapshotApiEndpointService:
    """Provide a snapshot API endpoint service instance."""
    return SnapshotApiEndpointService(
        api_endpoint_repository=api_endpoint_repository,
    )


def get_snapshot_project_dependency_service(
    project_dependency_repository: ProjectDependencyRepository = Depends(
        get_project_dependency_repository
    ),
) -> SnapshotProjectDependencyService:
    """Provide a snapshot dependency service instance."""
    return SnapshotProjectDependencyService(
        project_dependency_repository=project_dependency_repository,
    )


def get_language_analysis_service(
    language_rule_repository: AnalysisLanguageRuleRepository = Depends(
        get_analysis_language_rule_repository
    ),
    ignored_directory_repository: AnalysisIgnoredDirectoryRepository = Depends(
        get_analysis_ignored_directory_repository
    ),
    project_service=Depends(get_project_service),
    snapshot_service=Depends(get_snapshot_service),
    snapshot_language_service=Depends(get_snapshot_language_service),
) -> LanguageAnalysisService:
    """Provide a language analysis service instance."""
    return LanguageAnalysisService(
        project_service=project_service,
        language_rule_repository=language_rule_repository,
        ignored_directory_repository=ignored_directory_repository,
        snapshot_service=snapshot_service,
        snapshot_language_service=snapshot_language_service,
    )


def get_api_endpoint_analysis_service(
    ignored_directory_repository: AnalysisIgnoredDirectoryRepository = Depends(
        get_analysis_ignored_directory_repository
    ),
    project_service=Depends(get_project_service),
    snapshot_service=Depends(get_snapshot_service),
    snapshot_api_endpoint_service: SnapshotApiEndpointService = Depends(
        get_snapshot_api_endpoint_service
    ),
) -> ApiEndpointAnalysisService:
    """Provide an API endpoint analysis service instance."""
    return ApiEndpointAnalysisService(
        project_service=project_service,
        ignored_directory_repository=ignored_directory_repository,
        snapshot_service=snapshot_service,
        snapshot_api_endpoint_service=snapshot_api_endpoint_service,
    )


def get_project_dependency_analysis_service(
    ignored_directory_repository: AnalysisIgnoredDirectoryRepository = Depends(
        get_analysis_ignored_directory_repository
    ),
    project_service=Depends(get_project_service),
    snapshot_service=Depends(get_snapshot_service),
    snapshot_dependency_service: SnapshotProjectDependencyService = Depends(
        get_snapshot_project_dependency_service
    ),
) -> ProjectDependencyAnalysisService:
    """Provide a project dependency analysis service instance."""
    return ProjectDependencyAnalysisService(
        project_service=project_service,
        ignored_directory_repository=ignored_directory_repository,
        snapshot_service=snapshot_service,
        snapshot_dependency_service=snapshot_dependency_service,
    )


def get_framework_analysis_service(
    framework_rule_repository: AnalysisFrameworkRuleRepository = Depends(
        get_analysis_framework_rule_repository
    ),
    ignored_directory_repository: AnalysisIgnoredDirectoryRepository = Depends(
        get_analysis_ignored_directory_repository
    ),
    project_service=Depends(get_project_service),
    snapshot_service=Depends(get_snapshot_service),
    snapshot_framework_service=Depends(get_snapshot_framework_service),
) -> FrameworkAnalysisService:
    """Provide a framework analysis service instance."""
    return FrameworkAnalysisService(
        project_service=project_service,
        framework_rule_repository=framework_rule_repository,
        ignored_directory_repository=ignored_directory_repository,
        snapshot_service=snapshot_service,
        snapshot_framework_service=snapshot_framework_service,
    )


def get_infrastructure_analysis_service(
    infra_rule_repository: AnalysisInfraRuleRepository = Depends(
        get_analysis_infra_rule_repository
    ),
    ignored_directory_repository: AnalysisIgnoredDirectoryRepository = Depends(
        get_analysis_ignored_directory_repository
    ),
    project_service=Depends(get_project_service),
    snapshot_service=Depends(get_snapshot_service),
    snapshot_infrastructure_service=Depends(get_snapshot_infrastructure_service),
) -> InfrastructureAnalysisService:
    """Provide an infrastructure analysis service instance."""
    return InfrastructureAnalysisService(
        project_service=project_service,
        infra_rule_repository=infra_rule_repository,
        ignored_directory_repository=ignored_directory_repository,
        snapshot_service=snapshot_service,
        snapshot_infrastructure_service=snapshot_infrastructure_service,
    )


def get_project_analysis_service(
    language_analysis_service: LanguageAnalysisService = Depends(
        get_language_analysis_service
    ),
    framework_analysis_service: FrameworkAnalysisService = Depends(
        get_framework_analysis_service
    ),
    infrastructure_analysis_service: InfrastructureAnalysisService = Depends(
        get_infrastructure_analysis_service
    ),
    api_endpoint_analysis_service: ApiEndpointAnalysisService = Depends(
        get_api_endpoint_analysis_service
    ),
    project_dependency_analysis_service: ProjectDependencyAnalysisService = Depends(
        get_project_dependency_analysis_service
    ),
) -> ProjectAnalysisService:
    """Provide a project analysis service instance."""
    return ProjectAnalysisService(
        language_analysis_service=language_analysis_service,
        framework_analysis_service=framework_analysis_service,
        infrastructure_analysis_service=infrastructure_analysis_service,
        api_endpoint_analysis_service=api_endpoint_analysis_service,
        project_dependency_analysis_service=project_dependency_analysis_service,
    )
