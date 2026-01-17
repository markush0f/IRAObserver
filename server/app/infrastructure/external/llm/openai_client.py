import json
from typing import Any

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
        tools: list[ChatCompletionToolUnionParam],
        tool_results: list[dict[str, Any]] | None = None,
    ) -> LLMResponse:
        messages: list[ChatCompletionMessageParam] = [
            {
                "role": "system",
                "content": (
                    "You are an observer of software projects. "
                    "You only explain using facts returned by tools."
                ),
            },
            {"role": "user", "content": question},
        ]

        if tool_results:
            for result in tool_results:
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": result["tool_call_id"],
                        "content": json.dumps(result["tool_result"]),
                    }
                )

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=tools,
            tool_choice="auto",
        )

        message = response.choices[0].message

        tool_calls = []
        if message.tool_calls:
            for call in message.tool_calls:
                if not isinstance(call, ChatCompletionMessageFunctionToolCall):
                    continue
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
