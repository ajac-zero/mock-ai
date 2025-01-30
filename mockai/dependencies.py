import logging
import os
from typing import Annotated

import aiofiles
import watchfiles
from fastapi import Depends
from pydantic_core._pydantic_core import ValidationError

from mockai.models.json_file.models import PreDeterminedResponses

logger = logging.getLogger(__name__)
responses = None


async def save_reload(path: str, change: watchfiles.Change):
    global responses

    try:
        async with aiofiles.open(path) as f:
            responses = PreDeterminedResponses.model_validate_json(await f.read())
        logger.info(
            "Predetermined responses reloaded after %s",
            "modification" if change == watchfiles.Change.modified else "recreation",
        )
    except ValidationError as e:
        error = e.errors()[0]
        logger.error(
            f"Error reloading responses\n"
            f"Problematic input: {error['input']}\n"
            f"Fix: {error['msg']}\n"
            f"Keeping old responses"
        )


async def star_watching_responses():
    global responses
    if file := os.getenv("MOCKAI_RESPONSES"):
        async with aiofiles.open(file) as f:
            contents = await f.read()
        responses = PreDeterminedResponses.model_validate_json(contents)

        try:
            async for changes in watchfiles.awatch(file):
                change = changes.pop()
                change, _ = change
                if (
                    change == watchfiles.Change.modified
                    or change == watchfiles.Change.added
                ):
                    await save_reload(file, change)
                else:
                    logger.info(
                        "Predetirmened response file deleted. Clearing responses"
                    )
                    responses = None
        except Exception:
            logger.exception("Unexpected Error watching responses file")
            raise


async def get_responses() -> PreDeterminedResponses | None:
    return responses


ResponseFile = Annotated[PreDeterminedResponses | None, Depends(get_responses)]
