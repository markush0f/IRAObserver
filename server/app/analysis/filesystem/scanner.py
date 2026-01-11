from pathlib import Path
from typing import Iterable

IGNORED_DIRECTORIES = {
    "__pycache__",
    ".git",
    ".idea",
    ".vscode",
    "node_modules",
    ".venv",
    "venv",
    "dist",
    "build",
}


class FileSystemScanner:
    def __init__(self, root_path: Path) -> None:
        self.root_path = root_path

    def scan_files(self) -> Iterable[Path]:
        for path in self.root_path.rglob("*"):
            if not path.is_file():
                continue

            if any(part in IGNORED_DIRECTORIES for part in path.parts):
                continue

            yield path
