from time import time

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Message(BaseModel):
    role: str
    content: str


class ChatCompletionsRequest(BaseModel):
    model: str
    messages: list[Message]


@app.post("/chat/completions")
def chat_completions_create(request: ChatCompletionsRequest):
    content = request.messages[-1].content
    response = {
        "id": "Null",
        "choices": [{"message": {"role": "user", "content": content}}],
        "created": time(),
        "model": request.model,
        "object": "chat.completion",
    }
    return response
