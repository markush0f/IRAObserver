from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")


def get_env(name: str, default: Any | None = None, required: bool = False) -> str:
    value = os.getenv(name)
    if value is None:
        if required:
            raise RuntimeError(f"Missing {name} in environment")
        if default is None:
            return ""
        return str(default)
    return value
