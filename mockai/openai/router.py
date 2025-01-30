import json
import logging
import random
from itertools import zip_longest
from time import time
from typing import cast
from uuid import uuid4

from fastapi import APIRouter, Header, Request
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import ValidationError
from starlette.exceptions import HTTPException

from mockai.dependencies import ResponseFile
from mockai.models.api.openai import EmbeddingPayload, Payload
from mockai.models.json_file.models import PreDeterminedResponse

openai_router = APIRouter(prefix="/openai")

_log = logging.getLogger(__name__)


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

    yield "data: [DONE]\n\n"


def response_struct_to_openai_format(response: PreDeterminedResponse):
    if response.type == "text":
        content = response.output
        tool_calls = None
    elif response.type == "function":
        content = None

        if isinstance(response.output, str):
            raise ValueError("Impossible state")

        tool_calls = response.output._to_dict_list()

        for tool_call in tool_calls:
            tool_call["id"] = str(uuid4())
            tool_call["type"] = "function"
            function = {
                "name": tool_call.pop("name"),
                "arguments": tool_call.pop("arguments"),
            }
            tool_call["function"] = function
    else:
        raise ValueError("unreachable")

    return content, tool_calls


@openai_router.post("/chat/completions")  # OpenAI Endpoint
@openai_router.post("/deployments/{path}/chat/completions")  # AzureOpenAI Endpoint
async def openai_chat_completion(
    payload: Payload,
    responses: ResponseFile,
    mock_response: str | None = Header(default=None),
):
    model = payload.model
    stream = payload.stream
    content = None
    for message in payload.messages[::-1]:
        if message.role == "user":
            content = message.content
            break
    if content is None:
        content = payload.messages[-1].content

    if content is None:
        raise ValueError("Content from last message cannot be None")
    tool_calls = None

    if isinstance(content, list):
        for obj in content:
            if obj.type == "text":
                content = obj.text
                break
        else:
            raise HTTPException(
                400,
                "Content array must include at least one object with 'type' = 'text'",
            )
    found_predetermined_response = False
    if responses is not None:
        response = responses.find_matching_or_none(payload)
        if response is not None:
            content, tool_calls = response_struct_to_openai_format(response)
            found_predetermined_response = True

    _log.info(
        "predetermined response %s found",
        "not" if not found_predetermined_response else "",
    )

    if mock_response is not None:
        if found_predetermined_response:
            _log.info(
                "Overriding predetermined response with mock response from header"
            )
        else:
            _log.info("Using mock response from header")
        try:
            is_function = mock_response[:2] == "f:"

            r_type = "function" if is_function else "text"

            if is_function:
                output = json.loads(mock_response[2:])
            else:
                output = mock_response

            header_mock_response = PreDeterminedResponse(
                type=r_type, input="None", output=output
            )
            content, tool_calls = response_struct_to_openai_format(header_mock_response)
        except (ValidationError, json.JSONDecodeError) as e:
            content = str(e)

    content = cast(str, content)

    if stream is None or stream is False:
        response = json_response(content, model, tool_calls)
        return JSONResponse(response)
    else:
        response = streaming_response(content, model, tool_calls)
        return StreamingResponse(response)


@openai_router.post("/embeddings")  # OpenAI Endpoint
@openai_router.post("/deployments/{path}/embeddings")  # AzureOpenAI Endpoint
async def openai_create_embeddings(request: Request, payload: EmbeddingPayload):
    embedding_range = range(request.app.state.embedding_size)
    input_range = range(len(payload.input_list))
    return {
        "object": "list",
        "data": [
            {
                "object": "embedding",
                "embedding": [random.uniform(-1, 1) for _ in embedding_range],
                "index": number,
            }
            for number in input_range
        ],
        "model": payload.model,
        "usage": {
            "prompt_tokens": 0,
            "total_tokens": 0,
        },
    }
