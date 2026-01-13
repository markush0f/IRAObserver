from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from app.analysis.api_surface.analyzers.fastapi import extract_fastapi_endpoints


class TestFastApiExtractor(unittest.TestCase):
    def test_extracts_fastapi_endpoints_with_prefix_and_symbols(self) -> None:
        source = """
from fastapi import APIRouter

router = APIRouter(prefix="/projects")

@router.get("/{project_id}")
async def get_project():
    return {"ok": True}

@router.post("/items")
def create_item():
    return {"ok": True}

@router.api_route("/ping", methods=["GET", "POST"])
def ping():
    return {"ok": True}
"""
        with tempfile.TemporaryDirectory() as tmp_dir:
            root_path = Path(tmp_dir)
            file_path = root_path / "app" / "api.py"
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(source, encoding="utf-8")

            endpoints = extract_fastapi_endpoints(file_path, root_path)

        payloads = {
            (endpoint.http_method, endpoint.path, endpoint.source_symbol)
            for endpoint in endpoints
        }
        expected = {
            ("GET", "/projects/{project_id}", "get_project"),
            ("POST", "/projects/items", "create_item"),
            ("GET", "/projects/ping", "ping"),
            ("POST", "/projects/ping", "ping"),
        }
        self.assertEqual(payloads, expected)
        for endpoint in endpoints:
            self.assertEqual(endpoint.framework, "fastapi")
            self.assertEqual(endpoint.language, "python")
            self.assertEqual(endpoint.source_file, "app/api.py")


if __name__ == "__main__":
    unittest.main()
