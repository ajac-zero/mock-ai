from typing import Any, Literal, TypeAlias

from pydantic import BaseModel, TypeAdapter, model_validator

ResponseType: TypeAlias = Literal["text", "function"]


class FunctionOutput(BaseModel):
    name: str
    arguments: dict[str, Any]


class PreDeterminedResponse(BaseModel):
    type: ResponseType
    input: str
    output: str | FunctionOutput | list[FunctionOutput]

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


PreDeterminedResponses = TypeAdapter(list[PreDeterminedResponse])
