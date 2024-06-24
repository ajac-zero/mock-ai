from typing import Optional

from pydantic import BaseModel, ConfigDict


class Message(BaseModel):
    role: str
    content: str


class ChatCompletionsRequest(BaseModel):
    model: str
    message: Optional[str] = None
    messages: Optional[list[Message]] = None
    chat_history: Optional[list[Message]] = None
    stream: Optional[bool] = False
    tools: Optional[dict] = None
    tool_choice: Optional[str] = None

    model_config = ConfigDict(extra="allow")
