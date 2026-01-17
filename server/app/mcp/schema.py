from typing import Any

from fastmcp import Client
from mcp.types import Tool as MCPTool
from openai.types.chat import ChatCompletionToolParam, ChatCompletionToolUnionParam
from openai.types.shared_params import FunctionDefinition


class FastMCPSchemaExtractor:
    def __init__(self, mcp: Client) -> None:
        self._mcp = mcp

    @staticmethod
    def _to_openai_tool(tool: MCPTool) -> ChatCompletionToolUnionParam:
        parameters = dict(tool.inputSchema) if tool.inputSchema else {}
        if "type" not in parameters:
            parameters["type"] = "object"
        return ChatCompletionToolParam(
            type="function",
            function=FunctionDefinition(
                name=tool.name,
                description=tool.description or "",
                parameters=parameters,
            ),
        )

    async def tool_schemas(self) -> list[ChatCompletionToolUnionParam]:
        """Return LLM-compatible tool schemas from a remote FastMCP server."""
        async with self._mcp:
            tools = await self._mcp.list_tools()
        return [self._to_openai_tool(tool) for tool in tools]
