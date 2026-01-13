"""
Dependency composition module.

This module acts as the composition root of the application.
Its responsibility is to wire together infrastructure implementations
with domain services and expose them to the API layer via dependency injection.

Rules:
- No business logic must live here.
- No validation or domain decisions must be performed here.
- This module only creates and connects dependencies.

The API layer requests fully constructed services from this module,
without knowing which concrete implementations are used underneath.

All technical decisions (e.g. database choice, external providers)
are centralized here to keep the domain isolated and testable.
"""

import uuid
from datetime import datetime, timezone

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_access_token
from app.core.settings import AUTH_TOKEN_ENABLED
from app.core.db import get_db
from app.domains.auth.services.auth_service import AuthService
from app.domains.identity.models.entities.user import User
from app.domains.identity.repository.membership_repository import MembershipRepository
from app.domains.identity.repository.user_repository import UserRepository
from app.domains.identity.services.membership_service import MembershipService
from app.domains.identity.services.user_service import UserService
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
from app.domains.projects.repository.project_repository import ProjectRepository
from app.domains.analysis.repository.snapshot_framework_repository import (
    SnapshotFrameworkRepository,
)
from app.domains.analysis.repository.snapshot_infrastructure_repository import (
    SnapshotInfrastructureRepository,
)
from app.domains.analysis.repository.snapshot_language_repository import (
    SnapshotLanguageRepository,
)
from app.domains.projects.repository.snapshot_repository import SnapshotRepository
from app.domains.analysis.services.framework_analysis_service import (
    FrameworkAnalysisService,
)
from app.domains.analysis.services.api_endpoint_analysis_service import (
    ApiEndpointAnalysisService,
)
from app.domains.analysis.services.infrastructure_analysis_service import (
    InfrastructureAnalysisService,
)
from app.domains.analysis.services.language_analysis_service import (
    LanguageAnalysisService,
)
from app.domains.analysis.services.project_analysis_service import (
    ProjectAnalysisService,
)
from app.domains.projects.services.project_service import ProjectService
from app.domains.projects.services.snapshot_api_endpoint_service import (
    SnapshotApiEndpointService,
)
from app.domains.projects.services.snapshot_framework_service import SnapshotFrameworkService
from app.domains.projects.services.snapshot_infrastructure_service import (
    SnapshotInfrastructureService,
)
from app.domains.projects.services.snapshot_language_service import SnapshotLanguageService
from app.domains.projects.services.snapshot_service import SnapshotService


def get_user_repository(
    session: AsyncSession = Depends(get_db),
) -> UserRepository:
    """Provide a user repository instance."""
    return UserRepository(session)


def get_membership_repository(
    session: AsyncSession = Depends(get_db),
) -> MembershipRepository:
    """Provide a membership repository instance."""
    return MembershipRepository(session)


def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository),
) -> UserService:
    """Provide a user service instance."""
    return UserService(user_repository)


def get_auth_service(
    user_service: UserService = Depends(get_user_service),
) -> AuthService:
    """Provide an auth service instance."""
    return AuthService(user_service)


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


def get_api_endpoint_repository(
    session: AsyncSession = Depends(get_db),
) -> ApiEndpointRepository:
    """Provide an API endpoint repository instance."""
    return ApiEndpointRepository(session)


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


def get_snapshot_service(
    snapshot_repository: SnapshotRepository = Depends(get_snapshot_repository),
    project_service: ProjectService = Depends(get_project_service),
) -> SnapshotService:
    """Provide a snapshot service instance."""
    return SnapshotService(
        snapshot_repository=snapshot_repository,
        project_service=project_service,
    )


def get_snapshot_api_endpoint_service(
    api_endpoint_repository: ApiEndpointRepository = Depends(
        get_api_endpoint_repository
    ),
) -> SnapshotApiEndpointService:
    """Provide a snapshot API endpoint service instance."""
    return SnapshotApiEndpointService(
        api_endpoint_repository=api_endpoint_repository,
    )


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


def get_language_analysis_service(
    project_service: ProjectService = Depends(get_project_service),
    language_rule_repository: AnalysisLanguageRuleRepository = Depends(
        get_analysis_language_rule_repository
    ),
    ignored_directory_repository: AnalysisIgnoredDirectoryRepository = Depends(
        get_analysis_ignored_directory_repository
    ),
    snapshot_service: SnapshotService = Depends(get_snapshot_service),
    snapshot_language_service: SnapshotLanguageService = Depends(
        get_snapshot_language_service
    ),
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
    project_service: ProjectService = Depends(get_project_service),
    ignored_directory_repository: AnalysisIgnoredDirectoryRepository = Depends(
        get_analysis_ignored_directory_repository
    ),
    snapshot_service: SnapshotService = Depends(get_snapshot_service),
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


def get_framework_analysis_service(
    project_service: ProjectService = Depends(get_project_service),
    framework_rule_repository: AnalysisFrameworkRuleRepository = Depends(
        get_analysis_framework_rule_repository
    ),
    ignored_directory_repository: AnalysisIgnoredDirectoryRepository = Depends(
        get_analysis_ignored_directory_repository
    ),
    snapshot_service: SnapshotService = Depends(get_snapshot_service),
    snapshot_framework_service: SnapshotFrameworkService = Depends(
        get_snapshot_framework_service
    ),
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
    project_service: ProjectService = Depends(get_project_service),
    infra_rule_repository: AnalysisInfraRuleRepository = Depends(
        get_analysis_infra_rule_repository
    ),
    ignored_directory_repository: AnalysisIgnoredDirectoryRepository = Depends(
        get_analysis_ignored_directory_repository
    ),
    snapshot_service: SnapshotService = Depends(get_snapshot_service),
    snapshot_infrastructure_service: SnapshotInfrastructureService = Depends(
        get_snapshot_infrastructure_service
    ),
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
) -> ProjectAnalysisService:
    """Provide a project analysis service instance."""
    return ProjectAnalysisService(
        language_analysis_service=language_analysis_service,
        framework_analysis_service=framework_analysis_service,
        infrastructure_analysis_service=infrastructure_analysis_service,
        api_endpoint_analysis_service=api_endpoint_analysis_service,
    )


def get_membership_service(
    membership_repository: MembershipRepository = Depends(get_membership_repository),
    user_service: UserService = Depends(get_user_service),
    project_service: ProjectService = Depends(get_project_service),
) -> MembershipService:
    """Provide a membership service instance."""
    return MembershipService(
        membership_repository=membership_repository,
        user_service=user_service,
        project_service=project_service,
    )


async def get_current_user(
    request: Request,
    user_repository: UserRepository = Depends(get_user_repository),
) -> User:
    """Resolve the current user from a bearer token or bypass if disabled."""
    if not AUTH_TOKEN_ENABLED:
        return User(
            id=uuid.uuid4(),
            display_name="system",
            password_hash="",
            role="admin",
            is_active=True,
            created_at=datetime.now(timezone.utc),
        )

    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="missing bearer token",
        )

    token = auth_header.split(" ", 1)[1].strip()
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="missing bearer token",
        )

    try:
        payload = decode_access_token(token)
        user_id = uuid.UUID(payload.sub)
    except (ValueError, TypeError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token",
        ) from exc

    user = await user_repository.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user is inactive",
        )
    return user


async def require_admin_bootstrap(
    request: Request,
    auth_service: AuthService = Depends(get_auth_service),
) -> None:
    """Block requests until an admin account has been bootstrapped."""
    needs_bootstrap = await auth_service.bootstrap_needed()
    if not needs_bootstrap:
        if request.url.path == "/auth/bootstrap":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="bootstrap forbidden",
            )
        return

    allowed_paths = {"/auth/bootstrap", "/auth/bootstrap-status", "/health"}
    if request.url.path in allowed_paths:
        return

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="admin bootstrap required",
    )
