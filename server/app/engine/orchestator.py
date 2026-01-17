from __future__ import annotations

"""Observation orchestration for LLM + MCP tools + persistence."""

from typing import Any, Protocol
import uuid

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
from openai.types.chat import ChatCompletionToolUnionParam

from app.engine.llm_types import LLMResponse, ToolCall


class LLMClient(Protocol):
    async def generate(
        self,
        question: str,
        tools: list[ChatCompletionToolUnionParam],
        tool_results: list[dict[str, Any]] | None = None,
    ) -> LLMResponse:
        """Generate an answer and optional tool calls for a question."""
        ...


class ToolRegistry(Protocol):
    def list(self) -> list[ChatCompletionToolUnionParam]:
        """Return available tool specs for the LLM."""
        ...

    async def call(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute a tool and return its structured result."""
        ...


class ObservationOrchestrator:
    """Coordinate questions, LLM responses, MCP tools, and persistence."""

    def __init__(self, observation_service: ObservationService) -> None:
        self.observation_service = observation_service

    async def start_session(
        self,
        project_id: uuid.UUID,
        llm_provider: str,
        llm_model: str,
    ) -> ObservationSessionPublic:
        session = await self.observation_service.create_session(
            ObservationSessionCreate(
                project_id=project_id,
                llm_provider=llm_provider,
                llm_model=llm_model,
            )
        )
        return session

    async def handle_question(
        self,
        session_id: uuid.UUID,
        question: str,
        llm_client: LLMClient,
        tool_registry: ToolRegistry,
    ) -> ObservationConclusionPublic:
        question_entry = await self.observation_service.create_question(
            ObservationQuestionCreate(session_id=session_id, raw_question=question)
        )

        tool_specs = tool_registry.list()
        initial = await llm_client.generate(question=question, tools=tool_specs)

        tool_results: list[dict[str, Any]] = []
        for tool_call in initial.tool_calls:
            result = await tool_registry.call(tool_call.name, tool_call.arguments)
            tool_results.append(
                {
                    "tool_call_id": tool_call.id,
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

        if tool_results:
            final = await llm_client.generate(
                question=question, tools=tool_specs, tool_results=tool_results
            )
        else:
            final = initial

        return await self.observation_service.create_conclusion(
            ObservationConclusionCreate(
                question_id=question_entry.id,
                explanation=final.answer,
            )
        )
