from __future__ import annotations

"""Requirements.txt dependency extraction."""

import re
from pathlib import Path

from app.analysis.dependency.base import (
    DependencyCandidate,
    DependencyExtractor,
    extract_version,
    is_ignored_line,
    normalize_name,
    relative_path,
)


class RequirementsDependencyExtractor(DependencyExtractor):
    """Extract dependencies from requirements.txt files."""

    def extract(self, path: Path, root_path: Path) -> list[DependencyCandidate]:
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            return []

        dependencies: list[DependencyCandidate] = []
        source_file = relative_path(path, root_path)
        for line in content.splitlines():
            if "\x00" in line:
                line = line.replace("\x00", "")
            if is_ignored_line(line):
                continue
            line = line.split("#", 1)[0].strip()
            if not line:
                continue
            name = re.split(r"[<=>!~]", line, maxsplit=1)[0]
            name = normalize_name(name)
            if not name:
                continue
            dependencies.append(
                DependencyCandidate(
                    name=name,
                    version=extract_version(line),
                    ecosystem="python",
                    scope="runtime",
                    source_file=source_file,
                )
            )
        return dependencies
