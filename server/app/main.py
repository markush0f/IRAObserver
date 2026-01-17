from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from fastmcp import Client

from app.api.http.v1.analysis import router as analysis_router
from app.api.http.v1.auth import router as auth_router
from app.api.http.v1.git import router as git_router
from app.api.http.v1.projects import router as projects_router
from app.api.http.v1.snapshots import router as snapshots_router
from app.api.http.v1.users import router as users_router
from app.api.http.v1.observe import router as observe_router
from app.api.deps import require_admin_bootstrap
from app.core.db import engine
from app.core.logging import configure_logging
from app.core.settings import MCP_SERVER_URL

from app.mcp.schema import FastMCPSchemaExtractor

configure_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- DB bootstrap ---
    async with engine.connect() as conn:
        await conn.execute(text("SELECT 1"))

    # --- MCP client bootstrap ---
    mcp = Client(MCP_SERVER_URL)
    schema_extractor = FastMCPSchemaExtractor(mcp)

    # Expose infrastructure objects via app.state
    app.state.mcp = mcp
    app.state.schema_extractor = schema_extractor

    yield

    # --- Shutdown ---
    await engine.dispose()


app = FastAPI(
    lifespan=lifespan,
    dependencies=[Depends(require_admin_bootstrap)],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(analysis_router)
app.include_router(git_router)
app.include_router(projects_router)
app.include_router(snapshots_router)
app.include_router(users_router)
app.include_router(observe_router)


@app.get("/health")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
