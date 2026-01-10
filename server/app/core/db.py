from __future__ import annotations

"""Database configuration and session factory."""

import logging
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlmodel import SQLModel

from app.core.settings import DATABASE_URL, DB_ECHO

logger = logging.getLogger(__name__)

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
    echo=DB_ECHO,
    pool_pre_ping=True,
)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Base(SQLModel):
    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
