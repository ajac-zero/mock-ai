import pytest
from openai.types.chat import (
    ChatCompletion,
    ChatCompletionChunk,
    ChatCompletionMessage,
    ChatCompletionMessageToolCall,
)
from openai.types.chat.chat_completion_chunk import ChoiceDelta, ChoiceDeltaToolCall

from mockai.openai import AsyncClient, AsyncOpenAI, Client, OpenAI


@pytest.mark.parametrize("client", [OpenAI(), Client()])
def test_openai_chat_completion(client):
    completion = client.chat.completions.create(
        model="mock", messages=[{"role": "user", "content": "Hello!"}]
    )
    assert isinstance(completion, ChatCompletion)
    assert isinstance(completion.choices[0].message, ChatCompletionMessage)
    assert isinstance(completion.choices[0].message.content, str)


@pytest.mark.parametrize("client", [OpenAI(), Client()])
def test_openai_chat_programmed_completion(client):
    completion = client.chat.completions.create(
        model="mock", messages=[{"role": "user", "content": "How are ya?"}]
    )
    assert isinstance(completion, ChatCompletion)
    assert isinstance(completion.choices[0].message, ChatCompletionMessage)
    assert (
        completion.choices[0].message.content == "I'm fine, thank u 😊. How about you?"
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("client", [AsyncOpenAI(), AsyncClient()])
async def test_async_openai_chat_completion(client):
    completion = await client.chat.completions.create(
        model="mock", messages=[{"role": "user", "content": "Hello!"}]
    )
    assert isinstance(completion, ChatCompletion)
    assert isinstance(completion.choices[0].message, ChatCompletionMessage)
    assert isinstance(completion.choices[0].message.content, str)


@pytest.mark.asyncio
@pytest.mark.parametrize("client", [AsyncOpenAI(), AsyncClient()])
async def test_async_openai_chat_programmed_completion(client):
    completion = await client.chat.completions.create(
        model="mock",
        messages=[{"role": "user", "content": "Where's my order?"}],
    )
    assert isinstance(completion, ChatCompletion)
    assert isinstance(completion.choices[0].message, ChatCompletionMessage)
    assert (
        completion.choices[0].message.tool_calls[0].function.name == "get_delivery_date"  # type: ignore
    )
    assert (
        completion.choices[0].message.tool_calls[0].function.arguments  # type: ignore
        == {"order_id": "1337"}
    )


@pytest.mark.parametrize("client", [OpenAI(), Client()])
def test_openai_chat_completion_stream(client):
    response = client.chat.completions.create(
        model="mock", messages=[{"role": "user", "content": "Hello!"}], stream=True
    )
    completion = next(response)
    assert isinstance(completion, ChatCompletionChunk)
    assert isinstance(completion.choices[0].delta.content, str)


@pytest.mark.asyncio
@pytest.mark.parametrize("client", [AsyncOpenAI(), AsyncClient()])
async def test_async_openai_chat_completion_stream(client):
    response = await client.chat.completions.create(
        model="mock", messages=[{"role": "user", "content": "Hello!"}], stream=True
    )
    completion = await anext(response)
    assert isinstance(completion, ChatCompletionChunk)
    assert isinstance(completion.choices[0].delta.content, str)


@pytest.mark.parametrize("client", [OpenAI(), Client()])
def test_openai_function_call(client):
    completion = client.chat.completions.create(
        model="mock", messages=[{"role": "user", "content": "Where's my order?"}]
    )
    assert isinstance(completion, ChatCompletion)
    assert isinstance(completion.choices[0].message, ChatCompletionMessage)
    assert isinstance(
        completion.choices[0].message.tool_calls[0],  # type: ignore
        ChatCompletionMessageToolCall,
    )


@pytest.mark.parametrize("client", [OpenAI(), Client()])
def test_openai_programmed_function_call(client):
    completion = client.chat.completions.create(
        model="mock", messages=[{"role": "user", "content": "Where's my order?"}]
    )
    assert isinstance(completion, ChatCompletion)
    assert isinstance(completion.choices[0].message, ChatCompletionMessage)
    assert isinstance(
        completion.choices[0].message.tool_calls[0],  # type: ignore
        ChatCompletionMessageToolCall,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("client", [AsyncOpenAI(), AsyncClient()])
async def test_async_openai_function_call(client):
    completion = await client.chat.completions.create(
        model="mock", messages=[{"role": "user", "content": "Where's my order?"}]
    )
    assert isinstance(completion, ChatCompletion)
    assert isinstance(completion.choices[0].message, ChatCompletionMessage)
    assert isinstance(
        completion.choices[0].message.tool_calls[0],  # type: ignore
        ChatCompletionMessageToolCall,
    )


@pytest.mark.parametrize("client", [OpenAI(), Client()])
def test_openai_function_call_stream(client):
    response = client.chat.completions.create(
        model="mock",
        messages=[{"role": "user", "content": "Where's my order?"}],
        stream=True,
    )
    completion = next(response)
    assert isinstance(completion, ChatCompletionChunk)
    assert isinstance(completion.choices[0].delta, ChoiceDelta)
    assert isinstance(
        completion.choices[0].delta.tool_calls[0],  # type: ignore
        ChoiceDeltaToolCall,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("client", [AsyncOpenAI(), AsyncClient()])
async def test_async_openai_function_call_stream(client):
    response = await client.chat.completions.create(
        model="mock",
        messages=[{"role": "user", "content": "Where's my order?"}],
        stream=True,
    )
    completion = await anext(response)
    assert isinstance(completion, ChatCompletionChunk)
    assert isinstance(completion.choices[0].delta, ChoiceDelta)
    assert isinstance(
        completion.choices[0].delta.tool_calls[0],  # type: ignore
        ChoiceDeltaToolCall,
    )
