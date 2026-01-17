from typing import Protocol, Dict, Any


class _FastMCPInternal(Protocol):
    _tools: Dict[str, Any]

    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        ...
