import pytest
from openai import OpenAI
from openai.types.chat import (
    ChatCompletion,
    ChatCompletionChunk,
    ChatCompletionMessage,
    ChatCompletionMessageToolCall,
)

from mock_ai.clients.openai import OpenAI as MockOpenAI


@pytest.fixture
def client():
    return OpenAI(base_url="http://localhost:8000", api_key="None")


@pytest.fixture
def mock():
    return MockOpenAI()


def test_openai_chat_completion(client):
    completion = client.chat.completions.create(
        model="mock", messages=[{"role": "user", "content": "Hello!"}]
    )
    assert isinstance(completion, ChatCompletion)
    assert isinstance(completion.choices[0].message, ChatCompletionMessage)
    assert isinstance(completion.choices[0].message.content, str)


def test_openai_function_call(client):
    completion = client.chat.completions.create(
        model="mock", messages=[{"role": "user", "content": "Function!"}]
    )
    assert isinstance(completion, ChatCompletion)
    assert isinstance(completion.choices[0].message, ChatCompletionMessage)
    assert isinstance(
        completion.choices[0].message.tool_calls[0], ChatCompletionMessageToolCall
    )


def test_mock_openai_chat_completion(mock):
    completion = mock.chat.completions.create(
        model="mock", messages=[{"role": "user", "content": "Hello!"}]
    )
    assert isinstance(completion, ChatCompletion)
    assert isinstance(completion.choices[0].message, ChatCompletionMessage)
    assert isinstance(completion.choices[0].message.content, str)


def test_openai_chat_completion_stream(client):
    response = client.chat.completions.create(
        model="mock", messages=[{"role": "user", "content": "Hello!"}], stream=True
    )
    completion = next(response)
    assert isinstance(completion, ChatCompletionChunk)
    assert isinstance(completion.choices[0].delta.content, str)


def test_mock_openai_chat_completion_stream(mock):
    response = mock.chat.completions.create(
        model="mock", messages=[{"role": "user", "content": "Hello!"}], stream=True
    )
    completion = next(response)
    assert isinstance(completion, ChatCompletionChunk)
    assert isinstance(completion.choices[0].delta.content, str)


def test_mock_openai_function_call(mock):
    completion = mock.chat.completions.create(
        model="mock", messages=[{"role": "user", "content": "Function!"}]
    )
    assert isinstance(completion, ChatCompletion)
    assert isinstance(completion.choices[0].message, ChatCompletionMessage)
    assert isinstance(
        completion.choices[0].message.tool_calls[0], ChatCompletionMessageToolCall
    )
