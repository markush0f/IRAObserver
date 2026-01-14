from __future__ import annotations

"""Project tree extraction utilities."""

from pathlib import Path
from typing import Any, Iterable


def build_project_tree(
    root_path: Path, ignored_directories: Iterable[str] | None = None
) -> dict[str, Any]:
    """Build a nested tree representation for a project path."""
    root = Path(root_path)
    if not root.exists():
        raise FileNotFoundError(f"Path not found: {root}")

    ignored = set(ignored_directories or [])
    return _build_node(root, root, ignored)


def _build_node(root: Path, current: Path, ignored: set[str]) -> dict[str, Any]:
    node: dict[str, Any] = {
        "name": current.name or current.as_posix(),
        "path": _relative_path(root, current),
        "type": "dir" if current.is_dir() else "file",
    }

    if current.is_dir():
        children = []
        for child in _iter_children(current, ignored):
            children.append(_build_node(root, child, ignored))
        node["children"] = children

    return node


def _iter_children(path: Path, ignored: set[str]) -> Iterable[Path]:
    for child in sorted(path.iterdir(), key=_sort_key):
        if _should_skip(child, ignored):
            continue
        yield child


def _should_skip(path: Path, ignored: set[str]) -> bool:
    return any(part in ignored for part in path.parts)


def _sort_key(path: Path) -> tuple[bool, str]:
    return (path.is_file(), path.name.lower())


def _relative_path(root: Path, current: Path) -> str:
    try:
        relative = current.relative_to(root)
    except ValueError:
        return current.as_posix()
    if relative.parts:
        return relative.as_posix()
    return "."
