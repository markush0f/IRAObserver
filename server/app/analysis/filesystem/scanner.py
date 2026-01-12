from __future__ import annotations

"""Filesystem scanner utilities."""
from pathlib import Path
from typing import Iterable, Set

from app.core.logging import get_logger

class FileSystemScanner:
    """Filesystem scanner with ignored directories support."""
    def __init__(self, root_path: Path, ignored_directories: Set[str]) -> None:
        self.root_path = root_path
        self.ignored_directories = ignored_directories
        self.logger = get_logger(__name__)

    def scan_files(self) -> Iterable[Path]:
        self.logger.debug("Scanning files root_path=%s", self.root_path)
        for path in self.root_path.rglob("*"):
            if not path.is_file():
                continue

            if any(part in self.ignored_directories for part in path.parts):
                self.logger.debug("Skipping ignored path=%s", path)
                continue

            yield path

    def scan_directories(self) -> Iterable[Path]:
        """Yield directories under the root, excluding ignored paths."""
        self.logger.debug("Scanning directories root_path=%s", self.root_path)
        for path in self.root_path.rglob("*"):
            if not path.is_dir():
                continue

            if any(part in self.ignored_directories for part in path.parts):
                self.logger.debug("Skipping ignored path=%s", path)
                continue

            yield path
