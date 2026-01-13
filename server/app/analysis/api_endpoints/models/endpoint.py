from __future__ import annotations

"""Endpoint extraction model."""

from dataclasses import dataclass


@dataclass(frozen=True)
class EndpointCandidate:
    """Represents an extracted API endpoint candidate."""

    http_method: str
    path: str
    framework: str
    language: str
    source_file: str
    source_symbol: str | None = None
    confidence: float = 1.0
