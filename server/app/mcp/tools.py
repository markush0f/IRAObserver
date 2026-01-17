from typing import Dict, List
from pathlib import Path
import re
from fastmcp import FastMCP


mcp = FastMCP()


@mcp.tool(
    name="search_project_ocurrences",
    description="Searches for ocurrences of a term across the project and returns objective ocurrence data.",
)
def search_project_ocurrences(term: str) -> Dict:
    project_root = Path("/project")
    pattern = re.compile(re.escape(term), re.IGNORECASE)

    # Obtain files in the project directory
    files: List[Dict] = []

    for file_path in project_root.rglob("*"):
        if not file_path.is_file():
            continue

        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        count = len(pattern.findall(content))
        if count > 0:
            files.append(
                {
                    "path": str(file_path.relative_to(project_root)),
                    "occurrences": count,
                }
            )
    return {
        "term": term,
        "files": files,
        "total_files": len(files),
        "total_occurrences": sum(f["occurrences"] for f in files),
    }
