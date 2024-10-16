import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

from mockai.anthropic.router import anthropic_router
from mockai.models import PreDeterminedResponses
from mockai.openai.router import openai_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    mockai_responses = os.getenv("MOCKAI_RESPONSES", "[]")
    mockai_embedding_size = os.environ["MOCKAI_EMBEDDING_SIZE"]

    app.state.responses = PreDeterminedResponses.validate_json(mockai_responses)
    app.state.embedding_size = int(mockai_embedding_size)

    yield


app = FastAPI(lifespan=lifespan)

app.include_router(openai_router)
app.include_router(anthropic_router)
