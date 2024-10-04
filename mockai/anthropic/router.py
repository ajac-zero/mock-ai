import json
from uuid import uuid4

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, StreamingResponse
from starlette.exceptions import HTTPException

from mockai.anthropic.models import Payload, anthropic_tool
from mockai.models import FunctionOutput, PreDeterminedResponse

anthropic_router = APIRouter(prefix="/anthropic")


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
        except Exception as e:
            print(e)
            print(event)

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
def anthropic_messages(request: Request, payload: Payload):
    model = payload.model
    stream = payload.stream
    # Get content from last message
    content = payload.messages[-1].content

    # If content is list of objects, get text from first object where type == text
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

    # Set initial response_array
    response_array = [{"type": "text", "text": content}]

    # Check predetermined responses for matching inputs
    responses: list[PreDeterminedResponse] = request.app.state.responses
    for response in responses:
        if content == response.input:
            if response.type == "text":
                response_array = [{"type": "text", "text": response.output}]

            elif response.type == "function":
                output = response.output

                if type(output) == list:
                    response_array = [anthropic_tool(m) for m in output]
                elif type(output) is FunctionOutput:
                    response_array = [anthropic_tool(output)]
                else:
                    raise ValueError("Invalid function")
            break

    if stream is None or stream is False:
        response = json_response(response_array, model)
        return JSONResponse(response)
    else:
        response = streaming_response(response_array, model)
        return StreamingResponse(response)
