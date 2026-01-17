from typing import Protocol, Dict, Any


class _FastMCPInternal(Protocol):
    _tools: Dict[str, Any]