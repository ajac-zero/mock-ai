import pytest
from mistralai.models.chat_completion import (
    ChatCompletionResponse,
    ChatCompletionResponseChoice,
    ChatCompletionResponseStreamChoice,
    ChatCompletionStreamResponse,
    ChatMessage,
    DeltaMessage,
    ToolCall,
)

from mockai.clients.mistralai import MistralAsyncClient, MistralClient


@pytest.fixture
def client():
    return MistralClient()


@pytest.fixture
def mock():
    return MistralAsyncClient()


def test_mistral_chat_completion(client):
    completion = client.chat(
        model="mock", messages=[{"role": "user", "content": "Hello!"}]
    )
    assert isinstance(completion, ChatCompletionResponse)
    assert isinstance(completion.choices[0], ChatCompletionResponseChoice)
    assert isinstance(completion.choices[0].message, ChatMessage)
    assert isinstance(completion.choices[0].message.content, str)


def test_mistral_chat_programmed_completion(client):
    completion = client.chat(
        model="mock", messages=[{"role": "user", "content": "Hello?"}]
    )
    assert isinstance(completion, ChatCompletionResponse)
    assert isinstance(completion.choices[0], ChatCompletionResponseChoice)
    assert isinstance(completion.choices[0].message, ChatMessage)
    assert completion.choices[0].message.content == "How are ya!"


@pytest.mark.asyncio
async def test_mock_mistral_chat_completion(mock):
    completion = await mock.chat(
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


@pytest.mark.asyncio
async def test_mock_mistral_chat_completion_stream(mock):
    response = mock.chat_stream(
        model="mock",
        messages=[{"role": "user", "content": "Hello!"}],
    )
    completion = await anext(response)
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


def test_mistral_programmed_function_call(client):
    completion = client.chat(
        model="mock",
        messages=[{"role": "user", "content": "What's the weather in San Fran"}],
    )
    assert isinstance(completion, ChatCompletionResponse)
    assert isinstance(completion.choices[0], ChatCompletionResponseChoice)
    assert isinstance(completion.choices[0].message, ChatMessage)
    assert completion.choices[0].message.tool_calls[0].function.name == "get_weather"  # type: ignore
    assert (
        completion.choices[0].message.tool_calls[0].function.arguments  # type: ignore
        == """{"weather": "42 degrees Fahrenheit"}"""
    )


@pytest.mark.asyncio
async def test_mock_mistralai_function_call(mock):
    completion = await mock.chat(
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


@pytest.mark.asyncio
async def test_mock_mistral_function_call_stream(mock):
    response = mock.chat_stream(
        model="mock",
        messages=[{"role": "user", "content": "Function!"}],
    )
    completion = await anext(response)
    assert isinstance(completion, ChatCompletionStreamResponse)
    assert isinstance(completion.choices[0], ChatCompletionResponseStreamChoice)
    assert isinstance(completion.choices[0].delta, DeltaMessage)
    assert isinstance(
        completion.choices[0].delta.tool_calls[0],  # type: ignore
        ToolCall,
    )
