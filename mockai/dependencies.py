import os
from typing import Annotated

import aiofiles
from fastapi import Depends

from mockai.models.json_file.models import PreDeterminedResponses


async def read_response_file() -> PreDeterminedResponses | None:
    if file := os.getenv("MOCKAI_RESPONSES"):
        async with aiofiles.open(file, "r") as f:
            contents = await f.read()
        return PreDeterminedResponses.model_validate_json(contents)
    else:
        return None


ResponseFile = Annotated[PreDeterminedResponses | None, Depends(read_response_file)]
