from __future__ import annotations

"""Centralized application settings loaded from .env."""

from pathlib import Path

from app.core.config import get_env

DATABASE_URL = get_env("DATABASE_URL", required=True)
DB_ECHO = get_env("DB_ECHO", default="").strip().lower() in {"1", "true", "yes", "on"}

JWT_SECRET_KEY = get_env("JWT_SECRET_KEY", default="")
JWT_ALGORITHM = get_env("JWT_ALGORITHM", default="HS256")
JWT_EXPIRE_MINUTES = int(get_env("JWT_EXPIRE_MINUTES", default="60"))
AUTH_TOKEN_ENABLED = (
    get_env("AUTH_TOKEN_ENABLED", default="true").strip().lower()
    in {"1", "true", "yes", "on"}
)

IRAOBSERVER_REPOS_DIR = Path(get_env("IRAOBSERVER_REPOS_DIR", required=True))
MCP_SERVER_URL = get_env("MCP_SERVER_URL", required=True)
