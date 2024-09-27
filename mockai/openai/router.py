import json
from itertools import zip_longest
from time import time
from typing import cast
from uuid import uuid4

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, StreamingResponse
from starlette.exceptions import HTTPException

from .models import Payload

openai_router = APIRouter(prefix="/openai")


def json_response(content: str | None, model: str, tool_calls: list[dict] | None):
    response = {
        "id": f"chatcmpl-{uuid4().hex}",
        "object": "chat.completion",
        "created": int(time()),
        "model": model,
        "system_fingerprint": "mock",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": content,
                    "tool_calls": tool_calls,
                },
                "logprobs": None,
                "finish_reason": "stop",
            }
        ],
        "usage": {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
            "completion_tokens_details": {"reasoning_tokens": 0},
        },
    }
    return response


def streaming_response(content: str | None, model: str, tool_calls: list[dict] | None):
    id = f"chatcmpl-{uuid4().hex}"

    if content is not None:
        iterator = content
    elif tool_calls is not None:
        iterator = zip_longest(
            *[
                list(json.dumps(tool_call["function"]["arguments"]))
                for tool_call in tool_calls
            ]
        )
    else:
        raise ValueError("Either content or tool_calls must not be None")

    for i in iterator:
        chunk = {
            "id": id,
            "object": "chat.completion.chunk",
            "created": int(time()),
            "model": model,
            "system_fingerprint": "mock",
            "choices": [
                {
                    "index": 0,
                    "delta": {
                        "role": "assistant",
                        "content": i if content is not None else None,
                        "tool_calls": [
                            {
                                "id": tool_call["id"],
                                "type": tool_call["type"],
                                "function": {
                                    "name": tool_call["function"]["name"],
                                    "arguments": i[n],
                                },
                            }
                            for n, tool_call in enumerate(tool_calls)
                        ]
                        if tool_calls is not None
                        else None,
                    },
                    "logprobs": None,
                    "finish_reason": None,
                }
            ],
        }
        yield f"data: {json.dumps(chunk)}\n\n"


@openai_router.post("/chat/completions")
def openai_chat_completion(request: Request, payload: Payload):
    model = payload.model
    stream = payload.stream
    content = payload.messages[-1].content
    tool_calls = None

    if type(content) == list:
        for obj in content:
            if obj.type == "text":
                content = obj.text
                break
        else:
            raise HTTPException(
                400,
                "Content array must include at least one object with 'type' = 'text'",
            )

    content = cast(str, content)

    for response in request.app.state.responses:
        if content == response.input:
            if response.type == "text":
                content = response.output
            elif response.type == "function":
                content = None
                output = response.output
                if type(output) == list:
                    tool_calls = [m.model_dump() for m in output]
                else:
                    tool_calls = [output.model_dump()]
                for tool_call in tool_calls:
                    tool_call["id"] = str(uuid4())
                    tool_call["type"] = "function"
                    function = {
                        "name": tool_call.pop("name"),
                        "arguments": tool_call.pop("arguments"),
                    }
                    tool_call["function"] = function
            break

    if stream is None or stream is False:
        response = json_response(content, model, tool_calls)
        return JSONResponse(response)
    else:
        response = streaming_response(content, model, tool_calls)
        return StreamingResponse(response)
