from typing import Any, Literal, TypeAlias

from pydantic import BaseModel, RootModel, model_validator

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


class PreDeterminedResponse(BaseModel):
    type: ResponseType
    input: str
    output: str | FunctionOutput | FunctionOutputs

    @model_validator(mode="after")
    def verify_structure(self) -> "PreDeterminedResponse":
        if self.type == "function":
            try:
                if isinstance(self.output, list):
                    checks = [isinstance(f, FunctionOutput) for f in self.output]
                    assert all(checks)
                else:
                    assert isinstance(self.output, FunctionOutput)
            except AssertionError:
                raise ValueError(
                    "When a response is of type 'function', the output must be a single FunctionOutput object or an array of FunctionOutput objects"
                )
        elif self.type == "text":
            if isinstance(self.output, str) is False:
                raise ValueError(
                    "When a response is of type 'text', the output must be a string."
                )
        return self


class PreDeterminedResponses(RootModel):
    root: list[PreDeterminedResponse]

    def __iter__(self):  # type: ignore
        return iter(self.root)

    def __setitem__(self, idx, item):
        self.root[idx] = item
