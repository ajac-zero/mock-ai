from typing import Literal

from pydantic import BaseModel


class FunctionOutput(BaseModel):
    name: str
    arguments: dict[str, str]


class PreDeterminedResponse(BaseModel):
    type: Literal["completion", "function"]
    input: str
    output: str | FunctionOutput
