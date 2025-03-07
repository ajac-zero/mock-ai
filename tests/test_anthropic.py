import json

import pytest
from anthropic import AsyncStream, Stream
from anthropic.types import Message, TextBlock, ToolUseBlock

from mockai.anthropic import Anthropic, AsyncAnthropic, AsyncClient, Client


# Fixtures
@pytest.fixture(params=[Anthropic(), Client()], scope="module")
def client_x(request):
    return request.param


@pytest.fixture(params=[AsyncAnthropic(), AsyncClient()], scope="module")
def async_client_x(request):
    return request.param


# Tests
def test_message(client_x):
    completion = client_x.messages.create(
        model="mock", messages=[{"role": "user", "content": "Hello!"}], max_tokens=1024
    )
    content = completion.content[0]
    assert isinstance(content, TextBlock)
    assert content.text == "Hello!"


def test_predefined_message(client_x):
    completion = client_x.messages.create(
        model="mock",
        messages=[{"role": "user", "content": "How are ya?"}],
        max_tokens=1024,
    )
    content = completion.content[0]
    assert isinstance(content, TextBlock)
    assert content.text == "I'm fine, thank u 😊. How about you?"


def test_message_stream(client_x):
    generator = client_x.messages.create(
        model="mock",
        messages=[{"role": "user", "content": "How are ya?"}],
        max_tokens=1024,
        stream=True,
    )
    assert isinstance(generator, Stream)
    buffer = ""
    for chunk in generator:
        if chunk.type == "content_block_delta":
            buffer += chunk.delta.text
    assert buffer == "I'm fine, thank u 😊. How about you?"


def test_tool_call(client_x):
    response = client_x.messages.create(
        model="mock",
        messages=[{"role": "user", "content": "Where's my order?"}],
        max_tokens=1024,
    )
    tool = response.content[0]
    assert isinstance(tool, ToolUseBlock)
    assert tool.name == "get_delivery_date"
    assert tool.input == {"order_id": "1337", "order_loc": ["New York", "Mexico City"]}


def test_tool_call_stream(client_x):
    generator = client_x.messages.create(
        model="mock",
        messages=[{"role": "user", "content": "Where's my order?"}],
        max_tokens=1024,
        stream=True,
    )
    assert isinstance(generator, Stream)
    buffer = ""
    for chunk in generator:
        if chunk.type == "content_block_delta":
            buffer += chunk.delta.partial_json
    assert json.loads(buffer) == {
        "order_id": "1337",
        "order_loc": ["New York", "Mexico City"],
    }


async def test_async_message(async_client_x):
    completion = await async_client_x.messages.create(
        model="mock", messages=[{"role": "user", "content": "Hello!"}], max_tokens=1024
    )
    assert isinstance(completion, Message)
    content = completion.content[0]
    assert isinstance(content, TextBlock)
    assert content.text == "Hello!"


async def test_predefined_async_message(async_client_x):
    completion = await async_client_x.messages.create(
        model="mock",
        messages=[{"role": "user", "content": "Where's my order?"}],
        max_tokens=1024,
    )
    assert isinstance(completion, Message)
    assert isinstance(completion.content[0], ToolUseBlock)
    assert completion.content[0].name == "get_delivery_date"
    assert completion.content[0].input == {
        "order_id": "1337",
        "order_loc": ["New York", "Mexico City"],
    }


async def test_async_message_stream(async_client_x):
    generator = await async_client_x.messages.create(
        model="mock",
        messages=[{"role": "user", "content": "How are ya?"}],
        max_tokens=1024,
        stream=True,
    )
    assert isinstance(generator, AsyncStream)
    buffer = ""
    async for chunk in generator:
        if chunk.type == "content_block_delta":
            buffer += chunk.delta.text
    assert buffer == "I'm fine, thank u 😊. How about you?"


async def test_async_tool_call(async_client_x):
    response = await async_client_x.messages.create(
        model="mock",
        messages=[{"role": "user", "content": "Where's my order?"}],
        max_tokens=1024,
    )
    tool = response.content[0]
    assert isinstance(tool, ToolUseBlock)
    assert tool.name == "get_delivery_date"
    assert tool.input == {"order_id": "1337", "order_loc": ["New York", "Mexico City"]}


async def test_async_tool_call_stream(async_client_x):
    generator = await async_client_x.messages.create(
        model="mock",
        messages=[{"role": "user", "content": "Where's my order?"}],
        max_tokens=1024,
        stream=True,
    )
    assert isinstance(generator, AsyncStream)
    buffer = ""
    async for chunk in generator:
        if chunk.type == "content_block_delta":
            buffer += chunk.delta.partial_json
    assert json.loads(buffer) == {
        "order_id": "1337",
        "order_loc": ["New York", "Mexico City"],
    }


async def test_user_message_is_not_last_no_match(async_client_x):
    completion = await async_client_x.messages.create(
        model="mock",
        messages=[
            {"role": "user", "content": "Where's my json you do not know?"},
            {"role": "assistant", "content": "your json is here:"},
        ],
        max_tokens=1024,
    )
    content = completion.content[0]
    assert isinstance(content, TextBlock)
    assert content.text == "Where's my json you do not know?"


async def test_user_message_is_not_last_and_is_matched():
    async_client = AsyncAnthropic()
    completion = await async_client.messages.create(
        model="mock",
        messages=[
            {"role": "user", "content": "Where's my json you know?"},
            {"role": "assistant", "content": "your json is here:"},
        ],
        max_tokens=1024,
    )
    content = completion.content[0]
    assert isinstance(content, TextBlock)
    assert content.text == "{'fake': 'json'}"


async def test_cached_system_prompt_allowed(async_client_x):
    # https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching
    response = await async_client_x.messages.create(
        model="mock",
        system=[
            {
                "type": "text",
                "text": "test_system_prompt",
                "cache_control": {
                    "type": "ephemeral"
                },  # Cache the static system prompt
            }
        ],
        messages=[{"role": "user", "content": "Where's my orda?"}],
        max_tokens=1024,
    )
    content = response.content[0]
    assert isinstance(content, TextBlock)
    assert content.text == "ORDER MATCHED BASED ON SYSTEM PROMPT"
