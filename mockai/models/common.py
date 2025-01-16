from typing import Any

from pydantic import BaseModel, RootModel
from typing_extensions import Literal, TypeAlias

ResponseType: TypeAlias = Literal["text", "function"]


class FunctionOutput(BaseModel):
    name: str
    arguments: dict[str, Any]

    def _to_dict_list(self):
        return [self.model_dump()]

    def _to_list(self):
        return [self]


class FunctionOutputs(RootModel):
    root: list[FunctionOutput]

    def __iter__(self):  # type: ignore
        return iter(self.root)

    def _to_dict_list(self):
        return self.model_dump()

    def _to_list(self):
        return self.root