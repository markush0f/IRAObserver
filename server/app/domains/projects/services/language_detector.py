from __future__ import annotations

from app.shared.filesystem.scanner import FileSystemScanner

"""Language detection based on file extensions."""

from dataclasses import dataclass
from typing import Iterable

from app.core.logging import get_logger


@dataclass(frozen=True)
class LanguageRule:
    """Rule mapping file extensions to a language and weight."""

    extension: str
    language: str
    weight: int = 1


class LanguageDetector:
    """Detect languages using extension rules and weighted counts."""

    def __init__(self, rules: Iterable[LanguageRule]) -> None:
        self.rules = list(rules)
        self.logger = get_logger(__name__)

    def detect(self, scanner: FileSystemScanner) -> dict[str, int]:
        """Return a weighted language count based on scanned files."""
        self.logger.info("Detecting languages using %s rules", len(self.rules))
        rule_map: dict[str, LanguageRule] = {}
        for rule in self.rules:
            extension = rule.extension.lower().lstrip(".")
            if not extension:
                continue
            rule_map[extension] = rule

        counts: dict[str, int] = {}
        for path in scanner.scan_files():
            extension = path.suffix.lower().lstrip(".")
            if not extension:
                continue
            rule = rule_map.get(extension)
            if not rule:
                continue
            counts[rule.language] = counts.get(rule.language, 0) + rule.weight

        self.logger.info("Language detection complete languages=%s", len(counts))
        return counts
