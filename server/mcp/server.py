from __future__ import annotations

import asyncio
import os

from fastmcp import FastMCP


def _get_env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default


def _get_env_str(name: str, default: str) -> str:
    value = os.getenv(name)
    return value if value else default


mcp = FastMCP("IRAObserver MCP")
app = mcp.http_app(transport="http")


async def main() -> None:
    host = _get_env_str("MCP_HOST", "0.0.0.0")
    port = _get_env_int("MCP_PORT", 8100)
    path = _get_env_str("MCP_PATH", "mcp")

    await mcp.run_http_async(
        host=host,
        port=port,
        path=path,
        transport="http",
    )


if __name__ == "__main__":
    asyncio.run(main())
