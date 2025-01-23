import json
import logging
from uuid import uuid4

from fastapi import APIRouter, Header
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import ValidationError
from starlette.exceptions import HTTPException

from mockai.dependencies import ResponseFile
from mockai.models.api.anthropic import Payload, anthropic_tool
from mockai.models.common import FunctionOutput

anthropic_router = APIRouter(prefix="/anthropic")
_logger = logging.getLogger(__name__)


def json_response(response_array, model: str):
    response = {
        "id": f"msg_{uuid4().hex}",
        "type": "message",
        "model": model,
        "role": "assistant",
        "content": response_array,
        "stop_reason": "end_turn",
        "stop_sequence": None,
        "usage": {
            "input_tokens": 0,
            "output_tokens": 0,
        },
    }
    return response


def stream_chunk(event: str, data: dict):
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"


def streaming_response(response_array, model: str):
    id = f"msg_{uuid4().hex}"

    message_start = {
        "type": "message_start",
        "message": {
            "id": id,
            "type": "message",
            "role": "assistant",
            "content": [],
            "model": model,
            "stop_reason": None,
            "stop_sequence": None,
            "usage": {"input_tokens": 0, "output_tokens": 0},
        },
    }
    yield stream_chunk("message_start", message_start)

    yield stream_chunk("ping", {"type": "ping"})

    is_function = False

    for idx, event in enumerate(response_array):
        try:
            is_function = True if event["type"] == "tool_use" else False
        except Exception:
            _logger.exception("unexpected error: durring streaming response")

        block_start = {
            "type": "content_block_start",
            "index": idx,
            "content_block": {
                "type": event["type"],
                "id": event["id"],
                "name": event["name"],
                "input": {},
            }
            if is_function
            else {"type": "text", "text": ""},
        }
        yield stream_chunk("content_block_start", block_start)

        if is_function:
            iterator = json.dumps(event["input"])
        else:
            iterator = event["text"]

        for char in iterator:
            chunk = {"type": "content_block_delta", "index": idx}

            if is_function:
                chunk["delta"] = {"type": "input_json_delta", "partial_json": char}
            else:
                chunk["delta"] = {"type": "text_delta", "text": char}

            yield stream_chunk("content_block_delta", chunk)

        block_stop = {"type": "content_block_stop", "index": idx}
        yield stream_chunk("content_block_stop", block_stop)

    message_delta = {
        "type": "message_delta",
        "delta": {"stop_reason": "tool_use" if is_function else "end_turn"},
        "usage": {"output_tokens": 0},
    }
    yield stream_chunk("message_delta", message_delta)

    yield stream_chunk("message_stop", {"type": "message_stop"})


@anthropic_router.post("/v1/messages")
async def anthropic_messages(
    payload: Payload,
    file: ResponseFile,
    mock_response: str | None = Header(default=None),
):
    model = payload.model
    stream = payload.stream
    # Get content from last message
    content = None
    for message in payload.messages[::-1]:
        if message.role == "user":
            content = message.content
            break

    if content is None:
        content = payload.messages[-1].content

    # If content is list of objects, get text from first object where type == text
    if content is list:
        for obj in content:
            if obj.type == "text":
                content = obj.text
                break
        else:
            raise HTTPException(
                400,
                "Content array must include at least one object with 'type' = 'text'",
            )

    # Set initial response_array
    response_array = [{"type": "text", "text": content}]

    # Check predetermined responses for matching inputs
    found_predetermined = False
    if file is not None:
        response = file.find_matching_or_none(payload)
        if response is not None:
            if response.type == "text":
                response_array = [{"type": "text", "text": response.output}]
                found_predetermined = True

            elif response.type == "function":
                if isinstance(output := response.output, str):
                    raise ValueError("Impossible state")

                response_array = [anthropic_tool(m) for m in output._to_list()]
                found_predetermined = True
    _logger.info(
        "Predetermined response %s found", "not" if not found_predetermined else ""
    )

    # Check if a mock response was passed in header
    if mock_response is not None:
        if found_predetermined:
            _logger.info(
                "Overriding predetermined response with mock response from header"
            )
        else:
            _logger.info("Using mock response from header")
        try:
            if mock_response[:2] == "f:":
                function_output = FunctionOutput.model_validate_json(mock_response[2:])
                response_array = [anthropic_tool(function_output)]
            else:
                response_array = [{"type": "text", "text": mock_response}]

        except (ValidationError, json.JSONDecodeError) as e:
            response_array = [{"type": "text", "text": str(e)}]

    if stream is None or stream is False:
        response = json_response(response_array, model)
        return JSONResponse(response)
    else:
        response = streaming_response(response_array, model)
        return StreamingResponse(response)
