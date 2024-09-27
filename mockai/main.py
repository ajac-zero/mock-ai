import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

from mockai.models import PreDeterminedResponses
from mockai.openai.router import openai_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    mockai_responses = os.getenv("MOCKAI_RESPONSES", "[]")

    app.state.responses = PreDeterminedResponses.validate_json(mockai_responses)

    yield


app = FastAPI(lifespan=lifespan)

app.include_router(openai_router)
