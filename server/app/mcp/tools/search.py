from pathlib import Path
import re
from typing import Dict, List

from app.mcp.instance import mcp


@mcp.tool(
    name="search_project_ocurrences",
    description=(
        "Search for occurrences of a term across the project source code "
        "and return objective occurrence data."
    ),
)
def search_project_ocurrences(term: str) -> Dict:
    project_root = Path("/project")
    pattern = re.compile(re.escape(term), re.IGNORECASE)

    files: List[Dict] = []

    for file_path in project_root.rglob("*"):
        if not file_path.is_file():
            continue

        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        matches = pattern.findall(content)
        if matches:
            files.append(
                {
                    "path": str(file_path.relative_to(project_root)),
                    "occurrences": len(matches),
                }
            )

    return {
        "term": term,
        "total_files": len(files),
        "total_occurrences": sum(f["occurrences"] for f in files),
        "files": files,
    }
