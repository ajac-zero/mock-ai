import json
import os
from warnings import warn

from fastapi import FastAPI
from starlette.exceptions import HTTPException
from starlette.responses import StreamingResponse

from mockai.server.models import ChatCompletionsRequest
from mockai.server.responses import (
    _normal_function_call,
    _normal_response,
    _streaming_function_call,
    _streaming_response,
)

app = FastAPI()


@app.post("/chat")
@app.post("/chat/completions")
@app.post("/v1/chat/completions")
def chat_completions_create(request: ChatCompletionsRequest):
    if request.messages:
        content = request.messages[-1].content
    elif request.message:
        content = request.message
    else:
        raise HTTPException(400, "No message content was found.")

    responses = os.getenv("MOCKAI_RESPONSES")

    FUNCTION_CALL = True if "func" in content.lower() else False
    STREAM = request.stream

    name = "mock_function"
    arguments = {"mock_arg": "mock_var"}

    if responses is not None:
        all_responses_dict = json.loads(responses)
        try:
            response_dict = all_responses_dict[content]
            try:
                response_type = response_dict["type"]
                if response_type == "function":
                    try:
                        name = response_dict["name"]
                        arguments = response_dict["arguments"]
                        FUNCTION_CALL = True
                    except KeyError:
                        raise HTTPException(
                            400, "Mock function call must have name and arguments field"
                        )
                elif response_type == "completion":
                    try:
                        content = response_dict["content"]
                        FUNCTION_CALL = False
                    except KeyError:
                        raise HTTPException(
                            400, "Mock completion must have content field"
                        )
            except KeyError:
                raise HTTPException(400, "Type of mock response must be specified")
        except KeyError:
            warn("No matching response found in JSON file, using default values...")

    model = request.model if request.model is not None else "mock-model"
    options = (FUNCTION_CALL, STREAM)

    match options:
        case (True, True):
            return StreamingResponse(_streaming_function_call(name, arguments, model))
        case (True, False):
            return _normal_function_call(name, arguments, model)
        case (False, True):
            return StreamingResponse(_streaming_response(content, model))
        case (False, False):
            return _normal_response(content, model)
