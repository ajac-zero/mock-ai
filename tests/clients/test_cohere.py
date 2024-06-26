import pytest
from cohere.types import (
    NonStreamedChatResponse,
    StreamedChatResponse_StreamStart,
    ToolCall,
)

from mockai.clients.cohere import AsyncClient, Client


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def async_client():
    return AsyncClient()


def test_cohere_chat_completion(client):
    completion = client.chat(
        model="mock",
        message="helloooo",
    )
    assert isinstance(completion, NonStreamedChatResponse)
    assert isinstance(completion.text, str)


@pytest.mark.asyncio
async def test_async_cohere_chat_completion(async_client):
    completion = await async_client.chat(model="mock", message="helloooo")
    assert isinstance(completion, NonStreamedChatResponse)
    assert isinstance(completion.text, str)


def test_cohere_chat_completion_stream(client):
    response = client.chat_stream(model="mock", message="Hello")
    completion = next(response)
    assert isinstance(completion, StreamedChatResponse_StreamStart)
    assert isinstance(completion.text, str)  # type: ignore


@pytest.mark.asyncio
async def test_async_cohere_chat_completion_stream(async_client):
    response = async_client.chat_stream(model="mock", message="Hello")
    completion = await anext(response)
    assert isinstance(completion, StreamedChatResponse_StreamStart)
    assert isinstance(completion.text, str)  # type: ignore


def test_cohere_function_call(client):
    completion = client.chat(
        model="mock",
        message="function!",
    )
    assert isinstance(completion, NonStreamedChatResponse)
    assert isinstance(completion.tool_calls[0], ToolCall)  # type: ignore


@pytest.mark.asyncio
async def test_async_cohere_function_call(async_client):
    completion = await async_client.chat(
        model="mock",
        message="function!",
    )
    assert isinstance(completion, NonStreamedChatResponse)
    assert isinstance(completion.tool_calls[0], ToolCall)  # type: ignore


def test_cohere_function_call_stream(client):
    response = client.chat_stream(
        model="mock",
        message="function!",
    )
    completion = next(response)
    assert isinstance(completion, StreamedChatResponse_StreamStart)
    assert isinstance(completion.tool_calls[0], dict)  # type: ignore


@pytest.mark.asyncio
async def test_mock_cohere_function_call_stream(async_client):
    response = async_client.chat_stream(model="mock", message="func!")
    completion = await anext(response)
    assert isinstance(completion, StreamedChatResponse_StreamStart)
    assert isinstance(completion.tool_calls[0], dict)  # type: ignore
