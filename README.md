# Mock AI
***False LLM endpoints for testing***

Mock AI provides a local server that interops with many LLM SDKs, so you can call these APIs as normal, but receive pre-determined or fake responses at no cost!

### Installation

```bash
# With pip
pip install mockai

# With poetry
poetry add mockai
```

## Usage
Mock AI currently provides clients for OpenAI, MistralAI, and Cohere. It patches these libraries directly under the hood, so it will always be up to date.

### Start the server
This is the server that the mock clients will communicate with, we'll see later how we can configure our own predetermined responses :).

```bash
# After installing mock-ai
$ mock-ai
```

### Chat Completions
To use a mock version of these providers, you only have to change a single line of code (and just barely!):

```python
# from openai import OpenAI - Original Client
from mockai.openai import OpenAI # Fake Client!

# Rest of the code remains the exact same

client = OpenAI()

response = client.chat.completions.create(
        model="gpt-5",  # Model can be whatever you want
        messages=[
            {
                "role": "user",
                "content": "Hi mock!"
            }
        ],
        # All other kwargs are accepted, but ignored (except for stream ;)) 
        temperate = 0.7,
        top_k = 0.95
    )

print(response.choices[0].message.content)
# >> "Hi mock!"

# By default, the response will be a copy of the
# content of the last message in the conversation
```

Mock AI also provides clients for Cohere and Mistral:
```python
# from mistralai.client import MistralClient
from mockai.mistralai import MistralClient

client = MistralClient()

response = client.chat(model="mistral-turbo", messages=[{"role": "user", "content": "Hi!"}])

print(response.choices[0].message.content)
# >> "Hi!"

# from cohere import Client
from mockai.cohere import Client

client = Client()

response = client.chat(model="Command-X", message="Hello!")

print(response.text)
# >> "Hello!"
```
And of couse the async versions of all clients:
```python
from mockai.openai import AsyncOpenAI
from mockai.mistralai import MistralAsyncClient
from mockai.cohere import AsynClient
```
Streaming is supported as well for all clients:
```python
from mockai.openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
        model="gpt-5",  # Model can be whatever you want
        messages=[
            {
                "role": "user",
                "content": "Hi mock!"
            }
        ],
        stream = True
    )

# Streaming mock responses will one letter per chunk
for chunk in response:
    if chunk.choices:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content)
# >> H
# >> i
# >>  
# >> m
# >> o
# >> c
# >> k
# >> !
```

To learn more about the usage of each client, you can look at the docs of the respective provider, the mock clients are the exact same!

### Tool Calling
All mock clients also work with tool calling! By default, a function call will be triggered if the subtring "func" is found in the most recent message contents.

```python
from mockai.openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
        model="gpt-5",
        messages=[
            {
                "role": "user",
                "content": "Function!"
            }
        ],
    )

print(response.choices[0].message.tool_calls[0].function.name)
# >> "mock"
print(response.choices[0].message.tool_calls[0].function.arguments)
# >> "{"mock": "mock"}"
```
However, the default function is not useful at all, so let's see how to set up our own pre-determined responses!

## Configure responses
The mock-ai cli takes an optional path to a JSON file were we can establish our responses for both completions and tool calls.

The structure of the json is simple. Each key should be the the **content** of a user message, and the value is a dict with the wanted response.
```json
# mock_responses.json
{
  "Hello?": {
    "type": "completion",
    "content": "How are ya!"
  },
  "What's the weather in San Fran": {
    "type": "function",
    "name": "get_weather",
    "arguments": {
      "weather": "42 degrees Fahrenheit"
    }
  }
}
```
When creating your .json file, please follow these rules:

1. Each response must have a `type` key, whose value must be either `completion` or `function`, this will determine the response object of the client.
2. Responses of type `completion` must have a `content` key with the string response.
3. Responses of type `function` must have a `name` key with the name of the function, and a `arguments` key with a dict of args and values (Example: {"weather": "42 degrees Fahrenheit"}).

### Load the json file
To create a mock-ai server with our json file, we just need to pass it to the mockai cli.
```bash
$ mock-ai mock_responses.json

# The full file path can also be passed
$ mock-ai ~/home/foo/bar/mock_responses.json
```

With this, our clients will have access to our pre-determined respones.

```python
from mockai.openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
        model="gpt-5",
        messages=[{"role": "user", "content": "Hello?"}],
    )

print(response.choices[0].message.content)
# >> "How are ya!"

response = client.chat.completions.create(
        model="gpt-5",
        messages=[{"role": "user", "content": "What's the weather in San Fran"}],
    )

print(response.choices[0].message.tool_calls[0].function.name)
# >> "get_weather"

print(response.choices[0].message.tool_calls[0].function.arguments)
# >> "{'weather': '42 degrees Fahrenheit'}"
```
