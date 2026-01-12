from __future__ import annotations

"""Framework detection based on dependency and config signals."""

from dataclasses import dataclass
import json
import re
from pathlib import Path
import tomllib

from app.analysis.filesystem.scanner import FileSystemScanner
from app.core.logging import get_logger


@dataclass(frozen=True)
class FrameworkRule:
    """Rule mapping signals to a framework and weight."""

    framework: str
    signal_type: str
    signal_value: str
    weight: int = 1


class FrameworkDetector:
    """Detect frameworks using signal rules and weighted scores."""

    def __init__(self, rules: list[FrameworkRule]) -> None:
        self.rules = rules
        self.logger = get_logger(__name__)

    def detect(self, scanner: FileSystemScanner) -> dict[str, float]:
        """Return confidence scores for frameworks based on signals."""
        signals = _collect_signals(scanner)
        scores: dict[str, int] = {}

        for rule in self.rules:
            if _signal_matches(rule, signals):
                scores[rule.framework] = scores.get(rule.framework, 0) + rule.weight

        total = sum(scores.values())
        if total <= 0:
            return {}
        return {name: score / total for name, score in scores.items()}


def _signal_matches(rule: FrameworkRule, signals: dict[str, set[str]]) -> bool:
    signal_type = rule.signal_type
    signal_value = rule.signal_value.lower().strip()
    if not signal_value:
        return False
    return signal_value in signals.get(signal_type, set())


def _collect_signals(scanner: FileSystemScanner) -> dict[str, set[str]]:
    python_deps: set[str] = set()
    node_deps: set[str] = set()
    java_deps: set[str] = set()
    config_files: set[str] = set()
    import_tokens: set[str] = set()

    for path in scanner.scan_files():
        name = path.name
        config_files.add(name.lower())

        if name == "requirements.txt":
            python_deps.update(_parse_requirements(path))
        elif name == "pyproject.toml":
            python_deps.update(_parse_pyproject(path))
        elif name == "package.json":
            node_deps.update(_parse_package_json(path))
        elif name == "pom.xml":
            java_deps.update(_parse_pom(path))
        elif name in {"build.gradle", "build.gradle.kts"}:
            java_deps.update(_parse_gradle(path))

        if path.suffix.lower() in {".py", ".js", ".ts", ".jsx", ".tsx", ".java"}:
            import_tokens.update(_parse_imports(path))

    return {
        "python_dependency": python_deps,
        "node_dependency": node_deps,
        "java_dependency": java_deps,
        "config_file": config_files,
        "import": import_tokens,
    }


def _parse_requirements(path: Path) -> set[str]:
    deps: set[str] = set()
    try:
        content = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return deps
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        name = re.split(r"[<=>!~]", line, maxsplit=1)[0]
        name = name.split("[", 1)[0].strip().lower()
        if name:
            deps.add(name)
    return deps


def _parse_pyproject(path: Path) -> set[str]:
    deps: set[str] = set()
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError):
        return deps

    project_deps = data.get("project", {}).get("dependencies", [])
    for dep in project_deps:
        name = re.split(r"[<=>!~]", dep, maxsplit=1)[0]
        name = name.split("[", 1)[0].strip().lower()
        if name:
            deps.add(name)

    poetry_deps = data.get("tool", {}).get("poetry", {}).get("dependencies", {})
    for name in poetry_deps.keys():
        if name.lower() == "python":
            continue
        deps.add(name.lower())

    return deps


def _parse_package_json(path: Path) -> set[str]:
    deps: set[str] = set()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return deps

    for section in (
        "dependencies",
        "devDependencies",
        "peerDependencies",
        "optionalDependencies",
    ):
        items = data.get(section, {})
        if isinstance(items, dict):
            deps.update({name.lower() for name in items.keys()})

    return deps


def _parse_pom(path: Path) -> set[str]:
    deps: set[str] = set()
    try:
        content = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return deps
    for match in re.findall(r"<artifactId>([^<]+)</artifactId>", content):
        deps.add(match.strip().lower())
    return deps


def _parse_gradle(path: Path) -> set[str]:
    deps: set[str] = set()
    try:
        content = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return deps
    for match in re.findall(r"['\"]([^'\"]+)['\"]", content):
        token = match.strip()
        if ":" in token:
            token = token.split(":")[-1]
        token = token.strip().lower()
        if token:
            deps.add(token)
    return deps


def _parse_imports(path: Path) -> set[str]:
    tokens: set[str] = set()
    try:
        content = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return tokens

    for line in content.splitlines():
        line = line.strip()
        if not line:
            continue
        if path.suffix.lower() == ".py":
            match = re.match(r"import\s+([a-zA-Z0-9_\\.]+)", line)
            if match:
                tokens.add(match.group(1).split(".")[0].lower())
            match = re.match(r"from\s+([a-zA-Z0-9_\\.]+)\s+import", line)
            if match:
                tokens.add(match.group(1).split(".")[0].lower())
        elif path.suffix.lower() in {".js", ".ts", ".jsx", ".tsx"}:
            match = re.search(r"from\s+['\"]([^'\"]+)['\"]", line)
            if match:
                tokens.add(match.group(1).split("/")[0].lower())
            match = re.search(r"require\(['\"]([^'\"]+)['\"]\)", line)
            if match:
                tokens.add(match.group(1).split("/")[0].lower())
        elif path.suffix.lower() == ".java":
            match = re.match(r"import\s+([a-zA-Z0-9_\\.]+);", line)
            if match:
                tokens.add(match.group(1).split(".")[-1].lower())
    return tokens
