import os
from contextlib import asynccontextmanager

import aiofiles
import anyio
from fastapi import FastAPI, Header, Request
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from starlette_compress import CompressMiddleware

from mockai.anthropic.router import anthropic_router
from mockai.dependencies import ResponseFile, star_watching_responses
from mockai.models.api.openai import (
    EmbeddingPayload as OpenAIEmbeddingPayload,
)
from mockai.models.api.openai import (
    Payload as OpenAIPayload,
)
from mockai.models.json_file.models import PreDeterminedResponse
from mockai.openai.router import (
    _openai_chat_completion,
    _openai_create_embeddings,
    openai_router,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    mockai_embedding_size = os.getenv("MOCKAI_EMBEDDING_SIZE", "1536")
    app.state.embedding_size = int(mockai_embedding_size)

    async with anyio.create_task_group() as tg:
        tg.start_soon(star_watching_responses)
        yield


app = FastAPI(lifespan=lifespan, default_response_class=ORJSONResponse)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.add_middleware(CompressMiddleware)

app.include_router(openai_router)
app.include_router(anthropic_router)

dir = os.path.dirname(os.path.realpath(__file__))
app.mount("/gui", StaticFiles(directory=f"{dir}/gui", html=True), name="gui")


@app.get("/api/responses/create")
async def create_response(responses: ResponseFile):
    if responses is None:
        raise HTTPException(400, "No response file to update.")

    responses.append(PreDeterminedResponse(type="text", input="", output=""))

    if file := os.getenv("MOCKAI_RESPONSES"):
        async with aiofiles.open(file, "w") as f:
            await f.write(responses.model_dump_json(indent=2))
        return responses
    else:
        raise ValueError("No response file set.")


@app.get("/api/responses/read")
async def get_responses(file: ResponseFile):
    return file


class ResponseUpdate(BaseModel):
    number: int
    new_response: PreDeterminedResponse


@app.post("/api/responses/update")
async def update_response(data: ResponseUpdate, responses: ResponseFile):
    if responses is None:
        raise HTTPException(400, "No response file to update.")

    responses[data.number - 1] = data.new_response

    if file := os.getenv("MOCKAI_RESPONSES"):
        async with aiofiles.open(file, "w") as f:
            await f.write(responses.model_dump_json(indent=2))
        return responses
    else:
        raise ValueError("No response file set.")


@app.delete("/api/responses/delete")
async def delete_response(number: int, responses: ResponseFile):
    if responses is None:
        raise HTTPException(400, "No response file to update.")

    responses.pop(number - 1)

    if file := os.getenv("MOCKAI_RESPONSES"):
        async with aiofiles.open(file, "w") as f:
            await f.write(responses.model_dump_json(indent=2))
        return responses
    else:
        raise ValueError("No response file set.")


@app.post("/{path:path}")
async def route_response(
    path: str,
    data: dict,
    request: Request,
    responses: ResponseFile,
    mock_response: str | None = Header(default=None),
    user_agent: str | None = Header(default=None),
):
    if not user_agent:
        return HTTPException(400, "User agent could not be determined")

    if "OpenAI" in user_agent:
        if "completions" in path:
            payload = OpenAIPayload(
                model=data["model"],
                messages=data["messages"],
                stream=data.get("stream"),
            )
            return await _openai_chat_completion(payload, responses, mock_response)
        elif "embeddings" in path:
            payload = OpenAIEmbeddingPayload(model=data["model"], input=data["input"])
            return await _openai_create_embeddings(request, payload)
        else:
            return HTTPException(400, "Invalid path")
