from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import AsyncGenerator

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlmodel import SQLModel

BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")

logger = logging.getLogger(__name__)

def _env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("Missing DATABASE_URL in environment")

_safe_url = DATABASE_URL
if "@" in DATABASE_URL and "://" in DATABASE_URL:
    scheme, rest = DATABASE_URL.split("://", 1)
    if "@" in rest:
        creds, hostpart = rest.split("@", 1)
        if ":" in creds:
            user, _password = creds.split(":", 1)
            _safe_url = f"{scheme}://{user}:***@{hostpart}"

logger.info("Database URL loaded: %s", _safe_url)

engine = create_async_engine(
    DATABASE_URL,
    echo=_env_bool("DB_ECHO"),
    pool_pre_ping=True,
)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Base(SQLModel):
    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
