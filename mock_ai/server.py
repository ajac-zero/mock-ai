from json import dumps
from time import time
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import StreamingResponse

app = FastAPI()


class Message(BaseModel):
    role: str
    content: str


class ChatCompletionsRequest(BaseModel):
    model: str
    messages: list[Message]
    stream: Optional[bool] = False
    tools: Optional[dict] = None
    tool_choice: Optional[str] = None


def _normal_response(request: ChatCompletionsRequest):
    content = request.messages[-1].content
    response = {
        "id": "Null",
        "choices": [{"message": {"role": "assistant", "content": content}}],
        "created": time(),
        "model": request.model,
        "object": "chat.completion",
    }
    return response


def _normal_function_call(request: ChatCompletionsRequest):
    response = {
        "id": "Null",
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": None,
                    "tool_calls": [
                        {
                            "id": "Null",
                            "type": "function",
                            "function": {
                                "arguments": {"mock": "mock"},
                                "name": "mock",
                            },
                        }
                    ],
                }
            }
        ],
        "created": time(),
        "model": request.model,
        "object": "chat.completion",
    }
    return response


def _streaming_response(request: ChatCompletionsRequest):
    content = request.messages[-1].content
    for char in content:
        chunk = {
            "id": "Null",
            "object": "chat.completion.chunk",
            "created": time(),
            "model": request.model,
            "choices": [{"delta": {"content": char, "role": "assistant"}}],
        }
        yield f"data: {dumps(chunk)}\n\n"
    yield "data: [DONE]\n\n"


def _streaming_function_call(request: ChatCompletionsRequest):
    for char in "mock":
        chunk = {
            "id": "Null",
            "object": "chat.completion.chunk",
            "created": time(),
            "model": request.model,
            "choices": [
                {
                    "delta": {
                        "role": "assistant",
                        "content": None,
                        "tool_calls": [
                            {
                                "id": "Null",
                                "type": "function",
                                "function": {
                                    "arguments": {"mock": char},
                                    "name": "mock",
                                },
                            }
                        ],
                    }
                }
            ],
        }
        yield f"data: {dumps(chunk)}\n\n"
    yield "data: [DONE]\n\n"


@app.post("/chat/completions")
def chat_completions_create(request: ChatCompletionsRequest):
    if request.messages and request.messages[-1]:
        if request.stream:
            return StreamingResponse(_streaming_response(request))
        else:
            if "func" in request.messages[-1].content.lower():
                return _normal_function_call(request)
            else:
                return _normal_response(request)
