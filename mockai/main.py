import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

from mockai.anthropic.router import anthropic_router
from mockai.openai.router import openai_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    mockai_embedding_size = os.getenv("MOCKAI_EMBEDDING_SIZE", "1536")

    app.state.embedding_size = int(mockai_embedding_size)

    yield


app = FastAPI(lifespan=lifespan)

app.include_router(openai_router)
app.include_router(anthropic_router)
