import pytest
from mistralai.client import MistralClient
from mistralai.models.chat_completion import (
    ChatCompletionResponse,
    ChatCompletionResponseChoice,
    ChatCompletionResponseStreamChoice,
    ChatCompletionStreamResponse,
    ChatMessage,
    DeltaMessage,
    ToolCall,
)

from mockai.clients.mistralai import MistralClient as MockMistral


@pytest.fixture
def client(endpoint, api_key):
    return MistralClient(endpoint=endpoint, api_key=api_key)


@pytest.fixture
def mock():
    return MockMistral()


def test_mistral_chat_completion(client):
    completion = client.chat(
        model="mock", messages=[{"role": "user", "content": "Hello!"}]
    )
    assert isinstance(completion, ChatCompletionResponse)
    assert isinstance(completion.choices[0], ChatCompletionResponseChoice)
    assert isinstance(completion.choices[0].message, ChatMessage)
    assert isinstance(completion.choices[0].message.content, str)


def test_mock_mistral_chat_completion(mock):
    completion = mock.chat(
        model="mock", messages=[{"role": "user", "content": "Hello!"}]
    )
    assert isinstance(completion, ChatCompletionResponse)
    assert isinstance(completion.choices[0], ChatCompletionResponseChoice)
    assert isinstance(completion.choices[0].message, ChatMessage)
    assert isinstance(completion.choices[0].message.content, str)


def test_mistral_chat_completion_stream(client):
    response = client.chat_stream(
        model="mock",
        messages=[{"role": "user", "content": "Hello!"}],
    )
    completion = next(response)
    assert isinstance(completion, ChatCompletionStreamResponse)
    assert isinstance(completion.choices[0], ChatCompletionResponseStreamChoice)
    assert isinstance(completion.choices[0].delta, DeltaMessage)
    assert isinstance(completion.choices[0].delta.content, str)


def test_mock_mistral_chat_completion_stream(mock):
    response = mock.chat_stream(
        model="mock",
        messages=[{"role": "user", "content": "Hello!"}],
    )
    completion = next(response)
    assert isinstance(completion, ChatCompletionStreamResponse)
    assert isinstance(completion.choices[0], ChatCompletionResponseStreamChoice)
    assert isinstance(completion.choices[0].delta, DeltaMessage)
    assert isinstance(completion.choices[0].delta.content, str)


def test_mistral_function_call(client):
    completion = client.chat(
        model="mock", messages=[{"role": "user", "content": "Function!"}]
    )
    assert isinstance(completion, ChatCompletionResponse)
    assert isinstance(completion.choices[0], ChatCompletionResponseChoice)
    assert isinstance(completion.choices[0].message, ChatMessage)
    assert isinstance(completion.choices[0].message.tool_calls[0], ToolCall)  # type: ignore


def test_mock_mistralai_function_call(mock):
    completion = mock.chat(
        model="mock", messages=[{"role": "user", "content": "Function!"}]
    )
    assert isinstance(completion, ChatCompletionResponse)
    assert isinstance(completion.choices[0], ChatCompletionResponseChoice)
    assert isinstance(completion.choices[0].message, ChatMessage)
    assert isinstance(completion.choices[0].message.tool_calls[0], ToolCall)  # type: ignore


def test_mistral_function_call_stream(client):
    response = client.chat_stream(
        model="mock",
        messages=[{"role": "user", "content": "Function!"}],
    )
    completion = next(response)
    assert isinstance(completion, ChatCompletionStreamResponse)
    assert isinstance(completion.choices[0], ChatCompletionResponseStreamChoice)
    assert isinstance(completion.choices[0].delta, DeltaMessage)
    assert isinstance(
        completion.choices[0].delta.tool_calls[0],  # type: ignore
        ToolCall,
    )


def test_mock_mistral_function_call_stream(mock):
    response = mock.chat_stream(
        model="mock",
        messages=[{"role": "user", "content": "Function!"}],
    )
    completion = next(response)
    assert isinstance(completion, ChatCompletionStreamResponse)
    assert isinstance(completion.choices[0], ChatCompletionResponseStreamChoice)
    assert isinstance(completion.choices[0].delta, DeltaMessage)
    assert isinstance(
        completion.choices[0].delta.tool_calls[0],  # type: ignore
        ToolCall,
    )
