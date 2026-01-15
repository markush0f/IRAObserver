from __future__ import annotations

from enum import Enum


class SnapshotType(str, Enum):
    LANGUAGES = "languages"
    FRAMEWORKS = "frameworks"
    INFRASTRUCTURE = "infrastructure"
    API_ENDPOINTS = "api_endpoints"
    DEPENDENCIES = "dependencies"
