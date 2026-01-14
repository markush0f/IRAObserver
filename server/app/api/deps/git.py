"""Git infrastructure dependency providers."""

from fastapi import Depends

from app.api.deps.projects import get_project_service
from app.domains.projects.services.project_service import ProjectService
from app.infrastructure.external.git.git_info_service import GitInfoService


def get_git_info_service(
    project_service: ProjectService = Depends(get_project_service),
) -> GitInfoService:
    """Provide a git info service instance."""
    return GitInfoService(project_service=project_service)
