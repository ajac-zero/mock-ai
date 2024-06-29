import json
import os
from warnings import warn

from fastapi import FastAPI, Request
from starlette.exceptions import HTTPException
from starlette.responses import StreamingResponse

from fauxai.server.models import ChatCompletionsRequest
from fauxai.server.responses import (
    _normal_function_call,
    _normal_response,
    _streaming_function_call,
    _streaming_response,
)

app = FastAPI()


@app.post("/chat") # Cohere
@app.post("/v1/messages") # Anthropic
@app.post("/chat/completions") # OpenAI
@app.post("/v1/chat/completions") # Mistral
def chat_completions_create(request: Request, data: ChatCompletionsRequest):
    if data.messages:
        content = data.messages[-1].content
    elif data.message:
        content = data.message
    else:
        raise HTTPException(400, "No message content was found.")

    responses = os.getenv("FAUXAI_RESPONSES")

    FUNCTION_CALL = True if "func" in content.lower() else False
    STREAM = data.stream

    if request.url._url[-4:] == "chat":
        STREAM = False

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

    STRINGIFY_ARGUMENTS = True if request.url._url[-20:] == "/v1/chat/completions" else False

    model = data.model if data.model is not None else "mock-model"
    options = (FUNCTION_CALL, STREAM)

    match options:
        case (True, True):
            return StreamingResponse(_streaming_function_call(name, arguments, model, STRINGIFY_ARGUMENTS))
        case (True, False):
            return _normal_function_call(name, arguments, model, STRINGIFY_ARGUMENTS)
        case (False, True):
            return StreamingResponse(_streaming_response(content, model))
        case (False, False):
            return _normal_response(content, model)
