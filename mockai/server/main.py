import json
import os
from typing import cast
from enum import Enum
from typing_extensions import Text
from warnings import warn

from fastapi import FastAPI, Request
from pydantic import ValidationError
from pydantic.dataclasses import dataclass
from starlette.exceptions import HTTPException
from starlette.responses import StreamingResponse

from mockai.schemas import PreDeterminedResponse, FunctionOutput, ResponseConfig
from mockai.server.models import ChatCompletionsRequest
from mockai.server.responses import (
    text_response,
    streaming_text_response,
    function_response,
    streaming_function_response,
)


def load_predetermined_responses() -> list[PreDeterminedResponse]:
    responses = os.environ.get("MOCKAI_RESPONSES", "[]")

    if responses is not None:
        all_responses = json.loads(responses)
        responses = [
            PreDeterminedResponse.model_validate(response) for response in all_responses
        ]

    return responses


def search_predetermined_responses(
    config: ResponseConfig, responses: list[PreDeterminedResponse]
):
    found = False

    for response in responses:
        if response.input == config.content:
            found = True
            if response.type == "text":
                config.content = cast(str, response.output)
            else:
                config.function_params = cast(FunctionOutput, response.output)

    if not found:
        warn("No matching response found in response JSON file.")

    return config


def generate_response(config: ResponseConfig):
    if config.type == "text":
        if config.streaming:
            return streaming_text_response(config)
        else:
            return text_response(config)
    else:
        if config.streaming:
            return streaming_function_response(config)
        else:
            return function_response(config)


predetermined_responses = load_predetermined_responses()

app = FastAPI()


@app.post("/v1/chat")  # Cohere
@app.post("/v1/messages")  # Anthropic
@app.post("/chat/completions")  # OpenAI
@app.post("/v1/chat/completions")  # Mistral
def chat_completions_create(request: Request, data: ChatCompletionsRequest):
    if data.messages:
        content = data.messages[-1].content
    elif data.message:
        content = data.message
    else:
        raise HTTPException(400, "No message content was found.")

    # Default response config
    config = ResponseConfig(content)

    if "func" in content.lower():
        config.type = "function"

    if request.url._url[-4:] == "chat":
        config.streaming = False

    if request.url._url[-20:] == "/v1/chat/completions":
        config.stringify_args = True

    if data.model is not None:
        config.model = data.model

    config = search_predetermined_responses(config, predetermined_responses)

    response = generate_response(config)

    if config.streaming:
        return StreamingResponse(response)
    else:
        return response
