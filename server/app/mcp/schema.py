"""
Extract tool schemas from FastMCP at runtime and expose them as LLM-compatible schemas.

Design rationale:
- FastMCP is the single source of truth for tool definitions.
- Tool schemas must be generated dynamically to avoid JSON duplication.
- The output schema is LLM-agnostic (not tied to OpenAI).
"""

import inspect
from typing import Any, Dict, List, cast

from fastmcp import FastMCP

from app.mcp._typing import _FastMCPInternal


class FastMCPSchemaExtractor:
    def __init__(self, mcp: FastMCP) -> None:
        # FastMCP does not expose its internal tool registry via public type hints.
        # We explicitly cast to an internal Protocol to keep static type checkers satisfied
        # while isolating this dependency to a single location.
        self._mcp = cast(_FastMCPInternal, mcp)

    def llm_tool_schemas(self) -> List[Dict[str, Any]]:
        """
        Generate LLM-compatible tool schemas from FastMCP-registered tools.

        - Schemas are derived from FastMCP runtime metadata.
        - No tool definitions or JSON schemas are duplicated manually.
        - The resulting format can be consumed by any LLM supporting tool/function calling.
        """
        tools: List[Dict[str, Any]] = []

        # FastMCP keeps registered tools in an internal registry.
        # Each tool contains the handler function and its metadata.
        for tool in self._mcp._tools.values():
            fn = tool.func
            sig = inspect.signature(fn)

            properties: Dict[str, Any] = {}
            required: List[str] = []

            # Parameters are inferred from the handler function signature.
            # A simple default mapping is used to keep schemas generic and provider-agnostic.
            for name, param in sig.parameters.items():
                properties[name] = {"type": "string"}
                if param.default is inspect._empty:
                    required.append(name)

            tools.append(
                {
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description or "",
                        "parameters": {
                            "type": "object",
                            "properties": properties,
                            "required": required,
                        },
                    },
                }
            )

        return tools
