from typing import Literal, TypedDict
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, model_validator

from mockai.models import FunctionOutput

roles = Literal["user", "assistant"]

content_types = Literal["text", "image", "tool_result", "tool_use"]


class Content(BaseModel):
    type: content_types
    text: str | None = None
    source: dict | None = None
    tool_use_id: str | None = None
    content: str | None = None

    @model_validator(mode="after")
    def check_fields(self) -> "Content":
        match self.type:
            case "text":
                if self.text is None:
                    raise ValueError("text field required")
            case "image":
                if self.source is None:
                    raise ValueError("image field required")
            case "tool_result":
                if self.tool_use_id is None or self.content is None:
                    raise ValueError(
                        "tool_use_id and content field required for content of type 'tool_result'"
                    )
        return self


class Message(BaseModel):
    role: roles
    content: str | list[Content]


class Payload(BaseModel):
    model: str
    max_tokens: int
    messages: list[Message]
    stream: bool | None = None

    model_config = ConfigDict(extra="allow")


class AnthropicTool(TypedDict):
    id: str
    type: str
    input: dict
    name: str


def anthropic_tool(function: FunctionOutput):
    return AnthropicTool(
        {
            "id": f"toolu_{uuid4().hex}",
            "type": "tool_use",
            "input": function.arguments,
            "name": function.name,
        }
    )
