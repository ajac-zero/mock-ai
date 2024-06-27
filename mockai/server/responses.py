from json import dumps
from time import time

__all__ = [
    "_normal_response",
    "_normal_function_call",
    "_streaming_response",
    "_streaming_function_call",
]


def _normal_response(content: str, model: str):
    response = {
        "id": "Null",
        "text": content,
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


def _normal_function_call(name: str, arguments: dict, model: str):
    response = {
        "id": "Null",
        "text": "None",
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
                                "arguments": dumps(arguments),
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
        "tool_calls": [{"name": "mock", "parameter": {"mock": "mock"}}],
    }
    return response


def _streaming_response(content: str, model: str):
    for char in content:
        chunk = {
            "id": "Null",
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
        }
        yield f"data: {dumps(chunk)}\n\n"
    yield "data: [DONE]\n\n"


def _streaming_function_call(name: str, arguments: dict, model: str):
    for _ in name:
        chunk = {
            "id": "Null",
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
                                    "arguments": dumps(arguments),
                                    "name": name,
                                },
                            }
                        ],
                    },
                    "finish_reason": "tool_calls",
                }
            ],
            "tool_calls": [{"name": "mock", "parameter": {"mock": "mock"}}],
        }
        yield f"data: {dumps(chunk)}\n\n"
    yield "data: [DONE]\n\n"
