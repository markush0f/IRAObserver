"""
Dependency composition package.

This package wires infrastructure implementations with domain services and
exposes them to the API layer via dependency injection.
"""

from app.api.deps.analysis import (
    get_analysis_framework_rule_repository,
    get_analysis_ignored_directory_repository,
    get_analysis_infra_rule_repository,
    get_analysis_language_rule_repository,
    get_api_endpoint_analysis_service,
    get_api_endpoint_repository,
    get_framework_analysis_service,
    get_infrastructure_analysis_service,
    get_language_analysis_service,
    get_project_analysis_service,
    get_project_dependency_analysis_service,
    get_project_dependency_repository,
    get_snapshot_api_endpoint_service,
    get_snapshot_project_dependency_service,
)
from app.api.deps.auth import get_auth_service
from app.api.deps.core import get_current_user, require_admin_bootstrap
from app.api.deps.git import get_git_info_service
from app.api.deps.identity import (
    get_membership_repository,
    get_membership_service,
    get_user_repository,
    get_user_service,
)
from app.api.deps.projects import (
    get_project_repository,
    get_project_service,
    get_project_tree_service,
    get_snapshot_framework_repository,
    get_snapshot_framework_service,
    get_snapshot_infrastructure_repository,
    get_snapshot_infrastructure_service,
    get_snapshot_language_repository,
    get_snapshot_language_service,
    get_snapshot_repository,
    get_snapshot_service,
)

__all__ = [
    "get_analysis_framework_rule_repository",
    "get_analysis_ignored_directory_repository",
    "get_analysis_infra_rule_repository",
    "get_analysis_language_rule_repository",
    "get_api_endpoint_analysis_service",
    "get_api_endpoint_repository",
    "get_auth_service",
    "get_current_user",
    "get_git_info_service",
    "get_framework_analysis_service",
    "get_infrastructure_analysis_service",
    "get_language_analysis_service",
    "get_membership_repository",
    "get_membership_service",
    "get_project_analysis_service",
    "get_project_dependency_analysis_service",
    "get_project_dependency_repository",
    "get_project_repository",
    "get_project_service",
    "get_project_tree_service",
    "get_snapshot_api_endpoint_service",
    "get_snapshot_framework_repository",
    "get_snapshot_framework_service",
    "get_snapshot_infrastructure_repository",
    "get_snapshot_infrastructure_service",
    "get_snapshot_language_repository",
    "get_snapshot_language_service",
    "get_snapshot_project_dependency_service",
    "get_snapshot_repository",
    "get_snapshot_service",
    "get_user_repository",
    "get_user_service",
    "require_admin_bootstrap",
]
