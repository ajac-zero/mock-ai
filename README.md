# MockAI

***False LLM endpoints for testing***

MockAI provides a local server that interops with multiple LLM SDKs,
so you can call these APIs as normal but receive mock
or pre-determined responses at no cost!

The package currently provides full support for OpenAI and Anthropic.
It patches these libraries directly under the hood, so it will always be up to date.

## Free Public API

MockAI provides a free API that allows you to make mock calls without any installations!
Behind the scenes, the API is just the mockai server running on a virtual machine
I maintain, so it is the exact same code seen in this repo.

To use it just set the base url of the OpenAI client to `https://mockai.ajac-zero.com/openai`
and the Anthropic client to `https://mockai.ajac-zero.com/anthropic`:

```python
from openai import OpenAI

client = OpenAI(base_url="https://mockai.ajac-zero.com/openai", api_key="anything") # api_key arg can be any string

completion = client.chat.completions.create(
    model="gipiti", # model arg can be any string
    messages=[
      {"role": "user", "content":"hello"}
    ]
  ).choices[0].message

print(completion)
#> ChatCompletionMessage(content='hello', refusal=None, role='assistant', function_call=None, tool_calls=None)
```

You can also set a custom mock response using the extra_headers parameter
in the OpenAI client.

```python
client.chat.completions.create(
    model="gipiti",
    messages=[
      {"role": "user", "content": "Who created MockAI?"}
    ],
    extra_headers={"mock-response": "MockAI was made by ajac-zero"}
  ).choices[0].message

print(completion)
#> ChatCompletionMessage(content='MockAI was made by ajac-zero', refusal=None, role='assistant', function_call=None, tool_calls=None)
```

This also works with function calls, which must be passed as a string
and appended with 'f:', like so:

```python
client.chat.completions.create(
    model="gipiti",
    messages=[
      {"role": "user", "content": "Who created MockAI?"}
    ],
    extra_headers={
      "mock-response":'f:{"name":"my_function","arguments":{"first_arg":"one"}}'
    }
  ).choices[0].message

print(completion)
#> ChatCompletionMessage(content=None, refusal=None, role='assistant', function_call=None, tool_calls=[ChatCompletionMessageToolCall(id='86ae5af5-75ce-43a5-a75b-4cadd864b3b3', function=Function(arguments={'first_arg': 'one'}, name='my_function'), type='function')])
```

Mock function call inputs must always have the 'name' string
parameter and the 'arguments' dict parameter.

## Installation

```bash
# With pip
pip install ai-mock

# With poetry
poetry add ai-mock

# With uv
uv add ai-mock
```

## Usage

### Start the MockAI server

This is the server that the mock clients will communicate with, we'll see later
how we can configure our own pre-determined responses :).

```bash
# After installing MockAI
$ ai-mock server

# Or without installing with uvx
$ uvx ai-mock server
```

### Chat Completions

To use a mock version of these providers, you only have to change a single
line of code (and just barely!):

```diff
- from openai import OpenAI         # Real Client
+ from mockai.openai import OpenAI  # Fake Client
```

```python
# Rest of the code remains the exact same!
client = OpenAI()

response = client.chat.completions.create(
        model="gpt-5",  # Model can be whatever you want
        messages=[
            {
                "role": "user",
                "content": "Hi Mock!"
            }
        ],
        # All other kwargs are accepted, but ignored (except for stream ;))
        temperate = 0.7,
        top_k = 0.95
    )

print(response.choices[0].message.content)
# >> "Hi Mock!"

# By default, the response will be a copy of the
# content of the last message in the conversation
```

Alternatively, you can use the real SDK and
set the base url to the MockAI server address

```python
from openai import OpenAI         # Real Client

# The mockai server runs on port 8100 by default
client = OpenAI(api_key="not used but required", base_url="http://localhost:8100/openai")

response = client.chat.completions.create(
        model="gpt-5",
        messages=[
            {
                "role": "user",
                "content": "Hi Mock!"
            }
        ],
        temperate = 0.7,
        top_k = 0.95
    )

print(response.choices[0].message.content)
# >> "Hi Mock!"
```

MockAI also provides clients for Anthropic:

```python
# from anthropic import Anthropic
from mockai.anthropic import Anthropic

client = Anthropic()

response = client.messages.create(
        model="claude-3.5-opus",
        messages=[{"role": "user", "content": "What's up!"}],
        max_tokens=1024
    )

print(response.content)
# >> "What's up!"
```

And of course the async versions of all clients are supported:

```python
from mockai.openai import AsyncOpenAI
from mockai.anthropic import AsyncAnthropic
```

Streaming is supported as well:

```python
from mockai.openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
        model="gpt-5",
        messages=[{"role": "user", "content": "Hi mock!"}],
        stream = True
    )

# Streaming mock responses will yield one letter per chunk
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

To learn more about the usage of each client, you can look at the docs
of the respective provider, the mock clients are the exact same!

### Tool Calling

All mock clients also work with tool calling! To trigger a tool
call, you must specify it in a pre-determined response.

```python
from mockai.openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
        model="gpt-5",
        messages=[{"role": "user", "content": "Function!"}],
    )

print(response.choices[0].message.tool_calls[0].function.name)
# >> "mock"
print(response.choices[0].message.tool_calls[0].function.arguments)
# >> "{"mock_arg": "mock_val"}"
```

## Configure responses

The MockAI server takes an optional path to a JSON file were we can establish
our responses for both completions and tool calls. The structure of the
json is simple: Each object must have a "type" key of value "text" or "function",
an input key with a value, which is what will be matched against, and an output key,
which is what will be returned if the input key matches the user input.

```json
// mock_responses.json
{
"responses":[
  {
    "type": "text",
    "input": "How are ya?",
    "output": "I'm fine, thank u 😊. How about you?"
  },
  {
    "type": "function",
    "input": "Where's my order?",
    "output": {
      "name": "get_delivery_date",
      "arguments": {
        "order_id": "1337"
      }
    }
  }
]
}
```

When creating your .json file, please follow these rules:

1. Each response must have a `type` key, whose value must be either `text` or `function`,
this will determine the response object of the client.
2. Responses of type `text` must have a `output` key with a string value.
3. Responses of type `function` must have a `name` key with the name of the function,
and a `arguments` key with a dict of args
and values (Example: {"weather": "42 degrees Fahrenheit"}).
4. Responses of type `function` can accept a list of objects,
to simulate parallel tool calls.

### Load the json file

To create a MockAI server with our json file, we just need to
pass it to the mockai command.

```bash
$ ai-mock server mock_responses.json

# The full file path can also be passed
$ ai-mock server ~/home/foo/bar/mock_responses.json
```

With this, our mock clients will have access to our pre-determined responses!

```python
from mockai.openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
        model="gpt-5",
        messages=[{"role": "user", "content": "How are ya?"}],
    )

print(response.choices[0].message.content)
# >> "I'm fine, thank u 😊. How about you?"

response = client.chat.completions.create(
        model="gpt-5",
        messages=[{"role": "user", "content": "Where's my order?"}],
    )

print(response.choices[0].message.tool_calls[0].function.name)
# >> "get_delivery_date"

print(response.choices[0].message.tool_calls[0].function.arguments)
# >> "{'order_id': '1337'}"
```

## Development
### Python
1. Install system dependencies
   * [uv](https://docs.astral.sh/uv/)
   * [docker](https://www.docker.com/)
   * [just](https://github.com/casey/just)
   * then run `just get_started`
and you should be good to go!

### nodejs
TBD
