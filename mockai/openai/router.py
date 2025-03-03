from fastapi import APIRouter, Header, HTTPException, Request
from fastapi.responses import JSONResponse, StreamingResponse

from mockai.dependencies import ResponseFile

from . import models, services

openai_router = APIRouter(prefix="/openai")


@openai_router.post("/chat/completions")  # OpenAI Endpoint
@openai_router.post("/deployments/{path}/chat/completions")  # AzureOpenAI Endpoint
async def openai_chat_completion(
    payload: models.Payload,
    responses: ResponseFile,
    mock_response: str | None = Header(default=None),
):
    try:
        response = await services.generate_openai_completion_response(
            payload.model_dump(), responses, mock_response
        )

        if payload.stream is True:
            return StreamingResponse(response)
        else:
            return JSONResponse(response)
    except ValueError as e:
        raise HTTPException(400, str(e))


@openai_router.post("/embeddings")  # OpenAI Endpoint
@openai_router.post("/deployments/{path}/embeddings")  # AzureOpenAI Endpoint
async def openai_create_embeddings(request: Request, payload: models.EmbeddingPayload):
    return await services.generate_openai_embeddings_response(
        request.app.state.embedding_size, payload.model_dump()
    )
