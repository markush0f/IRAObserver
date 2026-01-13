from __future__ import annotations

"""FastAPI endpoint extraction."""

import re
from pathlib import Path

from app.analysis.api_surface.models.endpoint import EndpointCandidate

HTTP_METHODS = ("get", "post", "put", "delete", "patch", "options", "head")
DECORATOR_RE = re.compile(
    r"@(?P<target>app|router)\.(?P<method>"
    + "|".join(HTTP_METHODS)
    + r")\s*\(\s*[\"'](?P<path>[^\"']+)[\"']",
)
ROUTE_RE = re.compile(
    r"@(?P<target>app|router)\.(?P<route_type>route|api_route)\s*\("
    r"\s*[\"'](?P<path>[^\"']+)[\"']\s*,\s*methods\s*=\s*\[(?P<methods>[^\]]+)\]",
)
ROUTER_PREFIX_RE = re.compile(
    r"APIRouter\([\s\S]*?prefix\s*=\s*[\"'](?P<prefix>[^\"']+)[\"']"
)
DEF_RE = re.compile(r"(async\s+def|def)\s+(?P<name>[A-Za-z_][A-Za-z0-9_]*)")


def extract_fastapi_endpoints(path: Path, root_path: Path) -> list[EndpointCandidate]:
    """Extract FastAPI endpoints from a Python source file."""
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return []

    router_prefix = _parse_router_prefix(text)
    source_file = _relative_path(path, root_path)
    lines = text.splitlines()
    endpoints: list[EndpointCandidate] = []

    for index, line in enumerate(lines):
        decorator_match = DECORATOR_RE.search(line)
        if decorator_match:
            http_method = decorator_match.group("method").upper()
            path_value = decorator_match.group("path")
            path_value = _apply_prefix(
                router_prefix if decorator_match.group("target") == "router" else "",
                path_value,
            )
            source_symbol = _find_python_symbol(lines, index)
            endpoints.append(
                EndpointCandidate(
                    http_method=http_method,
                    path=path_value,
                    framework="fastapi",
                    language="python",
                    source_file=source_file,
                    source_symbol=source_symbol,
                )
            )
            continue

        route_match = ROUTE_RE.search(line)
        if not route_match:
            continue
        path_value = route_match.group("path")
        path_value = _apply_prefix(
            router_prefix if route_match.group("target") == "router" else "",
            path_value,
        )
        methods = _parse_methods(route_match.group("methods"))
        source_symbol = _find_python_symbol(lines, index)
        for method in methods:
            endpoints.append(
                EndpointCandidate(
                    http_method=method,
                    path=path_value,
                    framework="fastapi",
                    language="python",
                    source_file=source_file,
                    source_symbol=source_symbol,
                )
            )

    return endpoints


def _parse_router_prefix(text: str) -> str:
    match = ROUTER_PREFIX_RE.search(text)
    return match.group("prefix") if match else ""


def _parse_methods(methods_raw: str) -> list[str]:
    matches = re.findall(r"[\"'](?P<method>[A-Za-z]+)[\"']", methods_raw)
    return [method.upper() for method in matches] if matches else ["GET"]


def _find_python_symbol(lines: list[str], start_index: int) -> str | None:
    for line in lines[start_index + 1 :]:
        stripped = line.strip()
        if not stripped or stripped.startswith("@"):
            continue
        match = DEF_RE.match(stripped)
        if match:
            return match.group("name")
        break
    return None


def _apply_prefix(prefix: str, path_value: str) -> str:
    if not prefix:
        return path_value
    if not path_value:
        return prefix
    return f"{prefix.rstrip('/')}/{path_value.lstrip('/')}"


def _relative_path(path: Path, root_path: Path) -> str:
    try:
        return path.relative_to(root_path).as_posix()
    except ValueError:
        return path.as_posix()
