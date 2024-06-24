import pytest
from cohere import Client
from cohere.types import (
    NonStreamedChatResponse,
    StreamedChatResponse_StreamStart,
    ToolCall,
)

from mockai.clients.cohere import Client as MockClient


@pytest.fixture
def client(endpoint, api_key):
    return Client(base_url=endpoint, api_key=api_key)


@pytest.fixture
def mock():
    return MockClient()


def test_cohere_chat_completion(client):
    completion = client.chat(
        model="mock",
        message="helloooo",
        preamble=None,
        chat_history=None,
        conversation_id=None,
        prompt_truncation=None,
        connectors=None,
        search_queries_only=None,
        documents=None,
        citation_quality=None,
        temperature=None,
        max_tokens=None,
        max_input_tokens=None,
        k=None,
        p=None,
        seed=None,
        stop_sequences=None,
        frequency_penalty=None,
        presence_penalty=None,
        raw_prompting=None,
        return_prompt=None,
        tools=None,
        tool_results=None,
        force_single_step=None,
        request_options=None,
    )
    assert isinstance(completion, NonStreamedChatResponse)
    assert isinstance(completion.text, str)


def test_mock_openai_chat_completion(mock):
    completion = mock.chat(model="mock", message="helloooo")
    assert isinstance(completion, NonStreamedChatResponse)
    assert isinstance(completion.text, str)


def test_cohere_chat_completion_stream(client):
    response = client.chat_stream(model="mock", message="Hello")
    completion = next(response)
    assert isinstance(completion, StreamedChatResponse_StreamStart)
    assert isinstance(completion.text, str)  # type: ignore


def test_mock_cohere_chat_completion_stream(mock):
    response = mock.chat_stream(model="mock", message="Hello")
    completion = next(response)
    assert isinstance(completion, StreamedChatResponse_StreamStart)
    assert isinstance(completion.text, str)  # type: ignore


def test_cohere_function_call(client):
    completion = client.chat(
        model="mock",
        message="function!",
    )
    assert isinstance(completion, NonStreamedChatResponse)
    assert isinstance(completion.tool_calls[0], ToolCall)  # type: ignore


def test_mock_cohere_function_call(mock):
    completion = mock.chat(
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


def test_mock_cohere_function_call_stream(mock):
    response = mock.chat_stream(model="mock", message="func!")
    completion = next(response)
    assert isinstance(completion, StreamedChatResponse_StreamStart)
    assert isinstance(completion.tool_calls[0], dict)  # type: ignore
