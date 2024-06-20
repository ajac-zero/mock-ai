import pytest

from mock_ai.clients.openai import OpenAI
from mock_ai.types.openai.completions import (
    ChatCompletion,
    ChatCompletionMessage,
    Choice,
)
from mock_ai.types.openai.stream import (
    ChatCompletionChunk,
    ChoiceDelta,
)
from mock_ai.types.openai.stream import (
    Choice as StreamChoice,
)


@pytest.fixture
def client():
    return OpenAI()


def test_openai_chat_completion(client):
    completion = client.chat.completions.create(model="mock", messages=[{"role": "user", "content": "Hello!"}])
    assert isinstance(completion, ChatCompletion)
    assert isinstance(completion.choices[0], Choice)
    assert isinstance(completion.choices[0].message, ChatCompletionMessage)
    assert isinstance(completion.choices[0].message.content, str)


def test_openai_chat_stream_completion(client):
    generator = client.chat.completions.create(
        model="mock", messages=[{"role": "user", "content": "Hello!"}], stream=True
    )
    completion = next(generator)
    assert isinstance(completion, ChatCompletionChunk)
    assert isinstance(completion.choices[0], StreamChoice)
    assert isinstance(completion.choices[0].delta, ChoiceDelta)
    assert isinstance(completion.choices[0].delta.content, str)
