from __future__ import annotations

"""Base types for dependency extraction."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
import re


@dataclass(frozen=True)
class DependencyCandidate:
    """Represents an extracted dependency candidate."""

    name: str
    version: str | None
    ecosystem: str
    scope: str
    source_file: str


class DependencyExtractor(ABC):
    """Base class for dependency extractors."""

    @abstractmethod
    def extract(self, path: Path, root_path: Path) -> list[DependencyCandidate]:
        """Extract dependency candidates from a file."""


def normalize_name(raw: str) -> str:
    return raw.split("[", 1)[0].strip()


def is_ignored_line(line: str) -> bool:
    stripped = line.strip()
    return not stripped or stripped.startswith("#") or stripped.startswith("-")


def extract_version(line: str) -> str | None:
    match = re.search(r"(==|>=|<=|~=|!=|>|<)\s*([^;\\s]+)", line)
    if not match:
        return None
    return match.group(2).strip()


def relative_path(path: Path, root_path: Path) -> str:
    try:
        return path.relative_to(root_path).as_posix()
    except ValueError:
        return path.as_posix()
