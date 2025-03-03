import os

import aiofiles
from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from mockai.dependencies import ResponseFile
from mockai.models.json_file.models import PreDeterminedResponse

gui_router = APIRouter(prefix="/api/responses")

gui_router.mount(
    "/gui",
    StaticFiles(
        directory=f"{os.path.dirname(os.path.realpath(__file__))}/static", html=True
    ),
    name="gui",
)


@gui_router.get("/create")
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


@gui_router.get("/read")
async def get_responses(file: ResponseFile):
    return file


class ResponseUpdate(BaseModel):
    number: int
    new_response: PreDeterminedResponse


@gui_router.post("/update")
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


@gui_router.delete("/delete")
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
