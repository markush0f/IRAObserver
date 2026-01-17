import json
from typing import Any, cast

from openai import AsyncOpenAI
from openai.types.chat import (
    ChatCompletionMessageFunctionToolCall,
    ChatCompletionMessageParam,
    ChatCompletionToolUnionParam,
)

from app.engine.llm_types import LLMResponse, ToolCall


class OpenAILLMClient:
    provider = "openai"

    def __init__(self, api_key: str, model: str) -> None:
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model

    async def generate(
        self,
        question: str,
        tools: list[dict[str, Any]],
        tool_results: list[dict[str, Any]] | None = None,
    ) -> LLMResponse:
        messages: list[ChatCompletionMessageParam] = [
            {
                "role": "system",
                "content": (
                    "You are an observer of software projects. "
                    "You do not improve code. "
                    "You do not suggest changes. "
                    "You only explain using factual data returned by tools."
                ),
            },
            {
                "role": "user",
                "content": question,
            },
        ]

        if tool_results:
            for result in tool_results:
                tool_message: dict[str, Any] = {
                    "role": "tool",
                    "content": json.dumps(result["tool_result"]),
                }

                if "tool_call_id" in result:
                    tool_message["tool_call_id"] = result["tool_call_id"]

                messages.append(
                    cast(ChatCompletionMessageParam, tool_message)
                )

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=cast(list[ChatCompletionToolUnionParam], tools),
            tool_choice="auto",
        )

        message = response.choices[0].message

        tool_calls: list[ToolCall] = []

        tool_calls_raw = getattr(message, "tool_calls", None)

        if tool_calls_raw:
            for call in cast(
                list[ChatCompletionMessageFunctionToolCall],
                tool_calls_raw,
            ):
                tool_calls.append(
                    ToolCall(
                        id=call.id,
                        name=call.function.name,
                        arguments=json.loads(call.function.arguments or "{}"),
                    )
                )

        return LLMResponse(
            answer=message.content or "",
            tool_calls=tool_calls,
        )
