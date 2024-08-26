from typing import Literal, TypeAlias

from pydantic import BaseModel
from pydantic.dataclasses import dataclass

ResponseType: TypeAlias = Literal["text", "function"]


class FunctionOutput(BaseModel):
    name: str = "mock_function"
    arguments: dict[str, str] = {"mock_arg": "mock_var"}


class PreDeterminedResponse(BaseModel):
    type: ResponseType
    input: str
    output: str | FunctionOutput


@dataclass
class ResponseConfig:
    content: str

    type: ResponseType = "text"
    streaming: bool = False
    model: str = "mock-model"
    stringify_args: bool = False
    function_params: FunctionOutput = FunctionOutput()
