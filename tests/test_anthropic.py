import pytest
from anthropic.types import Message, ToolUseBlock

from fauxai.anthropic import Anthropic, AsyncAnthropic, AsyncClient, Client


@pytest.mark.parametrize("client", [Anthropic(), Client()])
def test_anthropic_chat_completion(client):
    completion = client.messages.create(
        model="mock", messages=[{"role": "user", "content": "Hello!"}], max_tokens=1024
    )
    assert isinstance(completion, Message)
    assert isinstance(completion.content, str)


@pytest.mark.parametrize("client", [Anthropic(), Client()])
def test_anthropic_programmed_chat_completion(client):
    completion = client.messages.create(
        model="mock", messages=[{"role": "user", "content": "Hello?"}], max_tokens=1024
    )
    assert isinstance(completion, Message)
    assert completion.content == "How are ya!"


@pytest.mark.asyncio
@pytest.mark.parametrize("client", [AsyncAnthropic(), AsyncClient()])
async def test_async_anthropic_chat_completion(client):
    completion = await client.messages.create(
        model="mock", messages=[{"role": "user", "content": "Hello!"}], max_tokens=1024
    )
    assert isinstance(completion, Message)
    assert isinstance(completion.content, str)


@pytest.mark.asyncio
@pytest.mark.parametrize("client", [AsyncAnthropic(), AsyncClient()])
async def test_async_anthropic_chat_programmed_completion(client):
    completion = await client.messages.create(
        model="mock",
        messages=[{"role": "user", "content": "What's the weather in San Fran"}],
        max_tokens=1024,
    )
    assert isinstance(completion, Message)
    assert isinstance(completion.content[0], ToolUseBlock)
    assert completion.content[0].name == "get_weather"
    assert completion.content[0].input == {"weather": "42 degrees Fahrenheit"}


# pytest.mark.parametrize("client", [Anthropic(), Client()])
# ef test_anthropic_chat_completion_stream(client):
#   response = client.messages.create(
#       model="mock",
#       messages=[{"role": "user", "content": "Hello!"}],
#       stream=True,
#       max_tokens=1024,
#   )
#   completion = next(response)
#   assert isinstance(completion, MessageStreamEvent)


# pytest.mark.asyncio
# pytest.mark.parametrize("client", [AsyncOpenAI(), AsyncClient()])
# sync def test_async_openai_chat_completion_stream(client):
#   response = await client.chat.completions.create(
#       model="mock", messages=[{"role": "user", "content": "Hello!"}], stream=True
#   )
#   completion = await anext(response)
#   assert isinstance(completion, ChatCompletionChunk)
#   assert isinstance(completion.choices[0].delta.content, str)


# pytest.mark.parametrize("client", [OpenAI(), Client()])
# ef test_openai_function_call(client):
#   completion = client.chat.completions.create(
#       model="mock", messages=[{"role": "user", "content": "Function!"}]
#   )
#   assert isinstance(completion, ChatCompletion)
#   assert isinstance(completion.choices[0].message, ChatCompletionMessage)
#   assert isinstance(
#       completion.choices[0].message.tool_calls[0],  # type: ignore
#       ChatCompletionMessageToolCall,
#   )


# pytest.mark.parametrize("client", [OpenAI(), Client()])
# ef test_openai_programmed_function_call(client):
#   completion = client.chat.completions.create(
#       model="mock", messages=[{"role": "user", "content": "Function!"}]
#   )
#   assert isinstance(completion, ChatCompletion)
#   assert isinstance(completion.choices[0].message, ChatCompletionMessage)
#   assert isinstance(
#       completion.choices[0].message.tool_calls[0],  # type: ignore
#       ChatCompletionMessageToolCall,
#   )


# pytest.mark.asyncio
# pytest.mark.parametrize("client", [AsyncOpenAI(), AsyncClient()])
# sync def test_async_openai_function_call(client):
#   completion = await client.chat.completions.create(
#       model="mock", messages=[{"role": "user", "content": "Function!"}]
#   )
#   assert isinstance(completion, ChatCompletion)
#   assert isinstance(completion.choices[0].message, ChatCompletionMessage)
#   assert isinstance(
#       completion.choices[0].message.tool_calls[0],  # type: ignore
#       ChatCompletionMessageToolCall,
#   )


# pytest.mark.parametrize("client", [OpenAI(), Client()])
# ef test_openai_function_call_stream(client):
#   response = client.chat.completions.create(
#       model="mock", messages=[{"role": "user", "content": "Function!"}], stream=True
#   )
#   completion = next(response)
#   assert isinstance(completion, ChatCompletionChunk)
#   assert isinstance(completion.choices[0].delta, ChoiceDelta)
#   assert isinstance(
#       completion.choices[0].delta.tool_calls[0],  # type: ignore
#       ChoiceDeltaToolCall,
#   )


# pytest.mark.asyncio
# pytest.mark.parametrize("client", [AsyncOpenAI(), AsyncClient()])
# sync def test_async_openai_function_call_stream(client):
#   response = await client.chat.completions.create(
#       model="mock", messages=[{"role": "user", "content": "Function!"}], stream=True
#   )
#   completion = await anext(response)
#   assert isinstance(completion, ChatCompletionChunk)
#   assert isinstance(completion.choices[0].delta, ChoiceDelta)
#   assert isinstance(
#       completion.choices[0].delta.tool_calls[0],  # type: ignore
#       ChoiceDeltaToolCall,
#   )
