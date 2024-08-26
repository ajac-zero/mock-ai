from json import dumps
from time import time

from mockai.schemas import ResponseConfig


def text_response(config: ResponseConfig):
    content = config.content
    model = config.model

    response = {
        "id": "Null",
        "text": content,
        "content": content,
        "role": "assistant",
        "generation_id": "Null",
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": content},
                "finish_reason": "stop",
            }
        ],
        "created": int(time()),
        "model": model,
        "object": "chat.completion",
        "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
    }
    return response


def function_response(config: ResponseConfig):
    name = config.function_params.name
    arguments = config.function_params.arguments
    stringify = config.stringify_args
    model = config.model

    response = {
        "id": "Null",
        "text": "None",
        "content": [
            {"type": "tool_use", "id": "None", "name": name, "input": arguments}
        ],
        "role": "assistant",
        "generation_id": "Null",
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
                                "arguments": dumps(arguments)
                                if stringify
                                else arguments,
                                "name": name,
                            },
                        }
                    ],
                },
                "finish_reason": "tool_calls",
            }
        ],
        "created": int(time()),
        "model": model,
        "object": "chat.completion",
        "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
        "tool_calls": [{"name": name, "parameters": arguments}],
    }
    return response


def streaming_text_response(config: ResponseConfig):
    content = config.content
    model = config.model

    for char in content:
        chunk = {
            "id": "Null",
            "text": char,
            "content": None,
            "role": "assistant",
            "object": "chat.completion.chunk",
            "created": int(time()),
            "model": model,
            "choices": [
                {
                    "index": 0,
                    "delta": {"content": char, "role": "assistant"},
                    "finish_reason": "stop",
                }
            ],
            "type": "content_block_delta",
            "index": 0,
            "delta": {"type": "text_delta", "text": char},
        }
        yield f"data: {dumps(chunk)}\n\n"
    yield "data: [DONE]\n\n"


def streaming_function_response(config: ResponseConfig):
    name = config.function_params.name
    arguments = config.function_params.arguments
    stringify = config.stringify_args
    model = config.model

    for _ in name:
        chunk = {
            "id": "Null",
            "role": "assistant",
            "content": [
                {"type": "tool_use", "id": "None", "name": name, "input": arguments}
            ],
            "object": "chat.completion.chunk",
            "created": int(time()),
            "model": model,
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
                                    "arguments": dumps(arguments)
                                    if stringify
                                    else arguments,
                                    "name": name,
                                },
                            }
                        ],
                    },
                    "finish_reason": "tool_calls",
                }
            ],
            "tool_calls": [{"name": name, "parameters": arguments}],
        }
        yield f"data: {dumps(chunk)}\n\n"
    yield "data: [DONE]\n\n"
