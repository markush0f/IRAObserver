from __future__ import annotations

"""Environment loader and access helpers."""

import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")


def get_env(name: str, default: Any | None = None, required: bool = False) -> str:
    """Return a raw environment value as string, with optional default/required."""
    value = os.getenv(name)
    if value is None:
        if required:
            raise RuntimeError(f"Missing {name} in environment")
        if default is None:
            return ""
        return str(default)
    return value
