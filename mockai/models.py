from typing import Literal, TypeAlias

from pydantic import BaseModel, TypeAdapter

ResponseType: TypeAlias = Literal["text", "function"]


class FunctionOutput(BaseModel):
    name: str
    arguments: dict[str, str]


class PreDeterminedResponse(BaseModel):
    type: ResponseType
    input: str
    output: str | FunctionOutput | list[FunctionOutput]


PreDeterminedResponses = TypeAdapter(list[PreDeterminedResponse])
