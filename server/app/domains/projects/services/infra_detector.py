from __future__ import annotations

"""Infrastructure detection based on filesystem signals."""

from dataclasses import dataclass
import fnmatch
from pathlib import Path

from app.analysis.filesystem.scanner import FileSystemScanner
from app.core.logging import get_logger


@dataclass(frozen=True)
class InfraRule:
    """Rule mapping signals to an infrastructure component."""

    component: str
    signal_type: str
    signal_value: str
    weight: int = 1


class InfraDetector:
    """Detect infrastructure components using signal rules."""

    def __init__(self, rules: list[InfraRule]) -> None:
        self.rules = rules
        self.logger = get_logger(__name__)

    def detect(self, scanner: FileSystemScanner) -> list[str]:
        """Return detected infrastructure components ordered by score."""
        signals = _collect_signals(scanner)
        scores: dict[str, int] = {}

        for rule in self.rules:
            if _signal_matches(rule, signals):
                scores[rule.component] = scores.get(rule.component, 0) + rule.weight

        return [
            name
            for name, _score in sorted(
                scores.items(), key=lambda item: (item[1], item[0].lower()), reverse=True
            )
        ]


def _signal_matches(rule: InfraRule, signals: dict[str, set[str]]) -> bool:
    signal_type = rule.signal_type
    signal_value = rule.signal_value.lower().strip()
    if not signal_value:
        return False
    if signal_type == "glob":
        return _glob_matches(signal_value, signals.get("glob_targets", set()))
    return signal_value in signals.get(signal_type, set())


def _glob_matches(pattern: str, targets: set[str]) -> bool:
    for target in targets:
        if fnmatch.fnmatch(target, pattern):
            return True
    return False


def _collect_signals(scanner: FileSystemScanner) -> dict[str, set[str]]:
    files: set[str] = set()
    directories: set[str] = set()
    glob_targets: set[str] = set()

    for path in scanner.scan_files():
        files.add(path.name.lower())
        relative = _relative_posix(scanner.root_path, path)
        glob_targets.add(relative)
        glob_targets.add(path.name.lower())

    for path in scanner.scan_directories():
        relative = _relative_posix(scanner.root_path, path)
        directories.add(relative)

    return {
        "file": files,
        "directory": directories,
        "glob_targets": glob_targets,
    }


def _relative_posix(root: Path, path: Path) -> str:
    try:
        return path.relative_to(root).as_posix().lower()
    except ValueError:
        return path.as_posix().lower()
