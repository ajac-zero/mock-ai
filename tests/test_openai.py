import pytest
from openai import OpenAI
from openai.types.chat import ChatCompletion, ChatCompletionMessage


@pytest.fixture
def client():
    return OpenAI(base_url="http://localhost:8000", api_key="None")


def test_openai_chat_completion(client):
    completion = client.chat.completions.create(
        model="mock", messages=[{"role": "user", "content": "Hello!"}]
    )
    assert isinstance(completion, ChatCompletion)
    assert isinstance(completion.choices[0].message, ChatCompletionMessage)
    assert isinstance(completion.choices[0].message.content, str)
