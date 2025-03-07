from __future__ import annotations

from typing import Annotated, Literal, TypeAlias

from pydantic import BaseModel, Field, model_validator

from .common import FunctionOutput, FunctionOutputs

ResponseType: TypeAlias = Literal["text", "function"]


class InputMatcher(BaseModel):
    system_prompt_name: Annotated[str | None, Field(default=None)]
    role: Annotated[str | None, Field(default=None)]
    content: str
    offset: Annotated[int, Field(default=-1)]

    def is_matching_payload(
        self, origin: str, payload: dict, system_prompts: dict[str, str]
    ) -> bool:
        msg_count = len(messages := payload["messages"])
        if not -msg_count <= self.offset < msg_count:
            return False
        message = messages[self.offset]
        if origin == "anthropic":
            if isinstance(message["content"], list):
                found = False
                for content in message["content"]:
                    if self.content == content["text"]:
                        found = True
                        break
                if not found:
                    return False
            elif self.content != message["content"]:
                return False

            if self.role is not None and self.role != message["role"]:
                return False
            if self.system_prompt_name is not None:
                if isinstance(system := payload["system"], list):
                    prompt = system_prompts[self.system_prompt_name]
                    return any(sys_prompt["text"] == prompt for sys_prompt in system)
                return system == system_prompts[self.system_prompt_name]
            return True
        else:
            if isinstance(message["content"], list):
                found = False
                for content in message["content"]:
                    if self.content == content["text"]:
                        found = True
                        break
                if not found:
                    return False
            elif self.content != message["content"]:
                return False
            if self.role is not None and self.role != message["role"]:
                return False
            return True


class PreDeterminedResponse(BaseModel):
    type: ResponseType
    input: InputMatcher | str
    output: str | FunctionOutput | FunctionOutputs

    @model_validator(mode="after")
    def verify_structure(self) -> PreDeterminedResponse:
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

    def response_matches(
        self, origin: str, payload: dict, system_prompts: dict[str, str]
    ) -> bool:
        if isinstance(self.input, str):
            return self.input == payload["messages"][-1]["content"]
        else:
            return self.input.is_matching_payload(origin, payload, system_prompts)


class PreDeterminedResponses(BaseModel):
    responses: Annotated[list[PreDeterminedResponse], Field(default=[])]
    system_prompts: Annotated[dict[str, str], Field(default={})]

    @model_validator(mode="after")
    def _verify_responses(self) -> PreDeterminedResponses:
        glob_errors = []
        temp_errors = [
            response.input.system_prompt_name
            for response in self.responses
            if (
                isinstance(response.input, InputMatcher)
                and response.input.system_prompt_name is not None
                and response.input.system_prompt_name not in self.system_prompts
            )
        ]
        if len(temp_errors) > 0:
            glob_errors.append(
                f"Following system prompt missing for the following system_prompt_names: {temp_errors}"
            )
            temp_errors = []

        if len(glob_errors) > 0:
            raise ValueError(
                "found following errors in file:\n" + "\n".join(glob_errors)
            )
        return self

    def find_matching_or_none(
        self, origin: str, payload: dict
    ) -> PreDeterminedResponse | None:
        for response in self.responses:
            if response.response_matches(origin, payload, self.system_prompts):
                return response
        return None

    # todo add chaching that will be flushed when file changes
