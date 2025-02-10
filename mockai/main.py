import os
from contextlib import asynccontextmanager

import anyio
from fastapi import FastAPI, Header, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import ORJSONResponse
from starlette_compress import CompressMiddleware

import mockai.anthropic.services as anthropic_services
import mockai.openai.services as openai_services
from mockai.anthropic.router import anthropic_router
from mockai.dependencies import ResponseFile, star_watching_responses
from mockai.gui.router import gui_router
from mockai.openai.router import openai_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    mockai_embedding_size = os.getenv("MOCKAI_EMBEDDING_SIZE", "1536")
    app.state.embedding_size = int(mockai_embedding_size)

    async with anyio.create_task_group() as tg:
        tg.start_soon(star_watching_responses)
        yield


app = FastAPI(lifespan=lifespan, default_response_class=ORJSONResponse)

app.add_middleware(CompressMiddleware)

app.include_router(openai_router)
app.include_router(anthropic_router)
app.include_router(gui_router)


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
        raise HTTPException(400, "User agent could not be determined")

    if "OpenAI" in user_agent:
        if "completions" in path:
            return await openai_services.generate_openai_completion_response(
                data, responses, mock_response
            )
        elif "embeddings" in path:
            return await openai_services.generate_openai_embeddings_response(
                request.app.state.embedding_size, data
            )
        else:
            return HTTPException(400, "Invalid path")
    elif "Anthropic" in user_agent:
        return await anthropic_services.generate_anthropic_response(
            data, responses, mock_response
        )
    else:
        raise HTTPException(400, "Invalid user agent")
