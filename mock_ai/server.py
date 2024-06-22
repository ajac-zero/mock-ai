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
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": content},
                "finish_reason": "stop",
            }
        ],
        "created": int(time()),
        "model": request.model,
        "object": "chat.completion",
        "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
    }
    return response


def _normal_function_call(request: ChatCompletionsRequest):
    response = {
        "id": "Null",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "None",
                    "tool_calls": [
                        {
                            "id": "Null",
                            "type": "function",
                            "function": {
                                "arguments": str({"mock": "mock"}),
                                "name": "mock",
                            },
                        }
                    ],
                },
                "finish_reason": "tool_calls",
            }
        ],
        "created": int(time()),
        "model": request.model,
        "object": "chat.completion",
        "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
    }
    return response


def _streaming_response(request: ChatCompletionsRequest):
    content = request.messages[-1].content
    for char in content:
        chunk = {
            "id": "Null",
            "object": "chat.completion.chunk",
            "created": int(time()),
            "model": request.model,
            "choices": [
                {
                    "index": 0,
                    "delta": {"content": char, "role": "assistant"},
                    "finish_reason": "stop",
                }
            ],
        }
        yield f"data: {dumps(chunk)}\n\n"
    yield "data: [DONE]\n\n"


def _streaming_function_call(request: ChatCompletionsRequest):
    for char in "mock":
        chunk = {
            "id": "Null",
            "object": "chat.completion.chunk",
            "created": int(time()),
            "model": request.model,
            "choices": [
                {
                    "index": 0,
                    "delta": {
                        "role": "assistant",
                        "content": None,
                        "tool_calls": [
                            {
                                "id": "Null",
                                "type": "function",
                                "function": {
                                "arguments": str({"mock": "mock"}),
                                    "name": "mock",
                                },
                            }
                        ],
                    },
                    "finish_reason": "tool_calls",
                }
            ],
        }
        yield f"data: {dumps(chunk)}\n\n"
    yield "data: [DONE]\n\n"


@app.post("/chat/completions")
@app.post("/v1/chat/completions")
def chat_completions_create(request: ChatCompletionsRequest):
    if request.messages and request.messages[-1]:
        if request.stream:
            if "func" in request.messages[-1].content.lower():
                return StreamingResponse(_streaming_function_call(request))
            else:
                return StreamingResponse(_streaming_response(request))
        else:
            if "func" in request.messages[-1].content.lower():
                return _normal_function_call(request)
            else:
                return _normal_response(request)
