from fastapi import FastAPI
from starlette.responses import StreamingResponse

from mockai.server.models import ChatCompletionsRequest
from mockai.server.responses import (
    _normal_function_call,
    _normal_response,
    _streaming_function_call,
    _streaming_response,
)

app = FastAPI()


@app.post("/chat")
@app.post("/chat/completions")
@app.post("/v1/chat/completions")
def chat_completions_create(request: ChatCompletionsRequest):
    if request.messages and request.messages[-1]:
        if request.stream:
            if "func" in request.messages[-1].content.lower():
                return StreamingResponse(_streaming_function_call(request))
            else:
                return StreamingResponse(_streaming_response(request))
        else:
            if "func" in request.messages[-1].content.lower():
                return _normal_function_call(request)
            else:
                return _normal_response(request)
    elif request.message:
        if request.stream:
            if "func" in request.message.lower():
                return _normal_function_call(request)
            else:
                return _normal_response(request)
        else:
            if "func" in request.message.lower():
                return _normal_function_call(request)
            else:
                return _normal_response(request)
