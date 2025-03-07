import pytest
from openai.types import CreateEmbeddingResponse
from openai.types.chat import (
    ChatCompletion,
    ChatCompletionChunk,
    ChatCompletionMessage,
    ChatCompletionMessageToolCall,
)
from openai.types.chat.chat_completion_chunk import ChoiceDelta, ChoiceDeltaToolCall

from mockai.openai import (
    AsyncAzureOpenAI,
    AsyncClient,
    AsyncOpenAI,
    AzureOpenAI,
    Client,
    OpenAI,
)

clients = [OpenAI(), Client(), AzureOpenAI()]

aclients = [AsyncOpenAI(), AsyncClient(), AsyncAzureOpenAI()]


# Fixtures
@pytest.fixture(params=clients, scope="module")
def client(request):
    return request.param


@pytest.fixture(params=aclients, scope="module")
def aclient(request):
    return request.param


def test_openai_chat_completion(client):
    completion = client.chat.completions.create(
        model="mock", messages=[{"role": "user", "content": "Hello!"}]
    )
    assert isinstance(completion, ChatCompletion)
    assert isinstance(completion.choices[0].message, ChatCompletionMessage)
    assert isinstance(completion.choices[0].message.content, str)


def test_openai_complex_chat_completion(client):
    completion = client.chat.completions.create(
        model="mock",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Hello!"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png"
                        },
                    },
                ],
            }
        ],
    )
    assert isinstance(completion, ChatCompletion)
    assert isinstance(completion.choices[0].message, ChatCompletionMessage)
    assert isinstance(completion.choices[0].message.content, str)


def test_openai_chat_programmed_completion(client):
    completion = client.chat.completions.create(
        model="mock", messages=[{"role": "user", "content": "How are ya?"}]
    )
    assert isinstance(completion, ChatCompletion)
    assert isinstance(completion.choices[0].message, ChatCompletionMessage)
    assert (
        completion.choices[0].message.content == "I'm fine, thank u 😊. How about you?"
    )


async def test_async_openai_chat_completion(aclient):
    completion = await aclient.chat.completions.create(
        model="mock", messages=[{"role": "user", "content": "Hello!"}]
    )
    assert isinstance(completion, ChatCompletion)
    assert isinstance(completion.choices[0].message, ChatCompletionMessage)
    assert isinstance(completion.choices[0].message.content, str)


async def test_async_openai_chat_programmed_completion(aclient):
    completion = await aclient.chat.completions.create(
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
        == {"order_id": "1337", "order_loc": ["New York", "Mexico City"]}
    )


def test_openai_chat_completion_stream(client):
    response = client.chat.completions.create(
        model="mock", messages=[{"role": "user", "content": "Hello!"}], stream=True
    )
    completion = next(response)
    assert isinstance(completion, ChatCompletionChunk)
    assert isinstance(completion.choices[0].delta.content, str)


async def test_async_openai_chat_completion_stream(aclient):
    response = await aclient.chat.completions.create(
        model="mock", messages=[{"role": "user", "content": "Hello!"}], stream=True
    )
    completion = await anext(response)
    assert isinstance(completion, ChatCompletionChunk)
    assert isinstance(completion.choices[0].delta.content, str)


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


def test_openai_function_call_followup(client):
    completion = client.chat.completions.create(
        model="mock",
        messages=[
            {"role": "user", "content": "Where's my order?"},
            {
                "role": "assistant",
                "tool_calls": [
                    {
                        "id": "call_123",
                        "type": "function",
                        "function": {
                            "name": "get_delivery_date",
                            "arguments": "{'order_id': '1337'}",
                        },
                    }
                ],
            },
            {
                "role": "tool",
                "content": "{'order_id': '1337', 'delivery_date': '25/10/2024'}",
                "tool_call_id": "call_123",
            },
        ],
    )
    assert isinstance(completion, ChatCompletion)

    message = completion.choices[0].message
    assert isinstance(message, ChatCompletionMessage)
    assert message.content == "Your order will arrive the 25th of October."


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


async def test_async_openai_function_call(aclient):
    completion = await aclient.chat.completions.create(
        model="mock", messages=[{"role": "user", "content": "Where's my order?"}]
    )
    assert isinstance(completion, ChatCompletion)
    assert isinstance(completion.choices[0].message, ChatCompletionMessage)
    assert isinstance(
        completion.choices[0].message.tool_calls[0],  # type: ignore
        ChatCompletionMessageToolCall,
    )


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


async def test_async_openai_function_call_stream(aclient):
    response = await aclient.chat.completions.create(
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


# Embeddings


def test_openai_embedding(client):
    response = client.embeddings.create(model="mock", input="hello")
    assert isinstance(response, CreateEmbeddingResponse)
    assert len(response.data) == 1
    assert len(response.data[0].embedding) == 1536


async def test_async_embedding(aclient):
    response = await aclient.embeddings.create(model="mock", input="hello")
    assert isinstance(response, CreateEmbeddingResponse)
    assert len(response.data) == 1
    assert len(response.data[0].embedding) == 1536


def test_openai_embedding_list(client):
    input_list = ["hiii", "my", "name", "is", "joe"]

    response = client.embeddings.create(model="mock", input=input_list)
    assert isinstance(response, CreateEmbeddingResponse)
    assert len(response.data) == 5

    for i, data in enumerate(response.data):
        assert data.index == i
        assert len(data.embedding) == 1536


async def test_async_embedding_list(aclient):
    input_list = ["hiii", "my", "name", "is", "joe"]

    response = await aclient.embeddings.create(model="mock", input=input_list)
    assert isinstance(response, CreateEmbeddingResponse)
    assert len(response.data) == 5

    for i, data in enumerate(response.data):
        assert data.index == i
        assert len(data.embedding) == 1536


async def test_async_openai_user_message_is_not_last_not_matched(aclient):
    completion = await aclient.chat.completions.create(
        model="mock",
        messages=[
            {"role": "user", "content": "Where's my json you do not know?"},
            {"role": "assistant", "content": "your json is here:"},
        ],
    )

    assert isinstance(completion, ChatCompletion)

    message = completion.choices[0].message
    assert isinstance(message, ChatCompletionMessage)
    assert message.content == "Where's my json you do not know?"


async def test_async_openai_user_message_is_not_last_matched(aclient):
    completion = await aclient.chat.completions.create(
        model="mock",
        messages=[
            {"role": "user", "content": "Where's my json you know?"},
            {"role": "assistant", "content": "your json is here:"},
        ],
    )

    assert isinstance(completion, ChatCompletion)

    message = completion.choices[0].message
    assert isinstance(message, ChatCompletionMessage)
    assert message.content == "{'fake': 'json'}"
