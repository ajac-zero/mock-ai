import os
from typing import Annotated

import aiofiles
from fastapi import Depends

from mockai import models


async def read_response_file():
    if file := os.getenv("MOCKAI_RESPONSES"):
        async with aiofiles.open(file, "r") as f:
            contents = await f.read()
        return models.PreDeterminedResponses.validate_json(contents)
    else:
        return None


ResponseFile = Annotated[
    list[models.PreDeterminedResponse] | None, Depends(read_response_file)
]
