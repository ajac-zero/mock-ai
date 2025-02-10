from fastapi import APIRouter, Header, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse

from mockai.dependencies import ResponseFile

from .models import Payload
from .services import generate_anthropic_response

anthropic_router = APIRouter(prefix="/anthropic")


@anthropic_router.post("/v1/messages")
async def anthropic_messages(
    payload: Payload,
    file: ResponseFile,
    mock_response: str | None = Header(default=None),
):
    try:
        response = await generate_anthropic_response(
            payload.model_dump(), file, mock_response
        )

        if payload.stream is True:
            return StreamingResponse(response)
        else:
            return JSONResponse(response)

    except ValueError as e:
        raise HTTPException(400, str(e))
