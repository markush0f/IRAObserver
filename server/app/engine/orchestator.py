from __future__ import annotations

"""Observation orchestration for LLM + MCP tools + persistence."""

from typing import Any, Protocol, cast
import uuid
from app.mcp._typing import _FastMCPInternal


from app.domains.observation.models.dto.conclusion import (
    ObservationConclusionCreate,
    ObservationConclusionPublic,
)
from app.domains.observation.models.dto.question import ObservationQuestionCreate
from app.domains.observation.models.dto.session import (
    ObservationSessionCreate,
    ObservationSessionPublic,
)
from app.domains.observation.models.dto.tool_call import ObservationToolCallCreate
from app.domains.observation.services.observation_service import ObservationService

from app.engine.llm_types import LLMResponse
from app.mcp.schema import FastMCPSchemaExtractor
from fastmcp import FastMCP


class LLMClient(Protocol):
    async def generate(
        self,
        question: str,
        tools: list[dict[str, Any]],
        tool_results: list[dict[str, Any]] | None = None,
    ) -> LLMResponse:
        """Generate an answer and optional tool calls for a question."""
        ...


class ObservationOrchestrator:
    """Coordinate questions, LLM responses, MCP tools, and persistence."""

    def __init__(
        self,
        observation_service: ObservationService,
        mcp: FastMCP,
        schema_extractor: FastMCPSchemaExtractor,
    ) -> None:
        self.observation_service = observation_service
        self.mcp = cast(_FastMCPInternal, mcp)

        self.schema_extractor = schema_extractor

    async def start_session(
        self,
        project_id: uuid.UUID,
        llm_provider: str,
        llm_model: str,
    ) -> ObservationSessionPublic:
        return await self.observation_service.create_session(
            ObservationSessionCreate(
                project_id=project_id,
                llm_provider=llm_provider,
                llm_model=llm_model,
            )
        )

    async def handle_question(
        self,
        session_id: uuid.UUID,
        question: str,
        llm_client: LLMClient,
    ) -> ObservationConclusionPublic:
        # Persist the incoming question
        question_entry = await self.observation_service.create_question(
            ObservationQuestionCreate(
                session_id=session_id,
                raw_question=question,
            )
        )

        # Expose available MCP tools to the LLM
        tool_schemas = self.schema_extractor.llm_tool_schemas()

        # First LLM pass: decide whether tools are needed
        initial = await llm_client.generate(
            question=question,
            tools=tool_schemas,
        )

        tool_results: list[dict[str, Any]] = []

        # Execute requested MCP tools
        for tool_call in initial.tool_calls:
            result = await self.mcp.call_tool(
                tool_call.name,
                tool_call.arguments,
            )

            tool_results.append(
                {
                    "tool_name": tool_call.name,
                    "tool_arguments": tool_call.arguments,
                    "tool_result": result,
                }
            )

            await self.observation_service.create_tool_call(
                ObservationToolCallCreate(
                    question_id=question_entry.id,
                    tool_name=tool_call.name,
                    tool_arguments=tool_call.arguments,
                    tool_result=result,
                )
            )

        # Second LLM pass only if tools were executed
        final = (
            await llm_client.generate(
                question=question,
                tools=tool_schemas,
                tool_results=tool_results,
            )
            if tool_results
            else initial
        )

        return await self.observation_service.create_conclusion(
            ObservationConclusionCreate(
                question_id=question_entry.id,
                explanation=final.answer,
            )
        )
