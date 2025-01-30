from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, model_validator


class Content(BaseModel):
    type: Literal["text", "image_url"]
    text: str | None = None
    image_url: dict | None = None

    @model_validator(mode="after")
    def check_fields(self) -> Content:
        if self.type == "text":
            if self.text is None:
                raise ValueError("text field required")
        elif self.type == "image_url":
            if self.image_url is None:
                raise ValueError("image_url field required")
            url = self.image_url.get("url", None)
            if isinstance(url, str):
                raise ValueError('image_url dict must contain "url" key of type string')
        return self


class Message(BaseModel):
    role: Literal["system", "user", "assistant", "tool"]
    content: str | list[Content] | None = None

    model_config = ConfigDict(extra="allow")


class Payload(BaseModel):
    model: str
    messages: list[Message]
    stream: bool | None = None

    model_config = ConfigDict(extra="allow")

    @model_validator(mode="after")
    def check_messages(self) -> Payload:
        if len(self.messages) == 0:
            raise ValueError("messages array can't be empty.")
        return self


class EmbeddingPayload(BaseModel):
    model: str
    input: str | list[str]

    model_config = ConfigDict(extra="allow")

    @property
    def input_list(self) -> list[str]:
        if isinstance(self.input, str):
            return [self.input]
        else:
            return self.input
