from __future__ import annotations

"""Shared LLM response types for orchestration."""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ToolCall:
    id: str
    name: str
    arguments: dict[str, Any]


@dataclass(frozen=True)
class LLMResponse:
    answer: str
    tool_calls: list[ToolCall]
