import sys

from types import ModuleType
from mock_ai.clients import openai, cohere, mistralai

clients = [
    (openai, ["OpenAI", "Client"]),
    (mistralai, ["MistralClient"]),
    (cohere, ["Client"])
]

for sdk, client_classes in clients:
    sdk_name = sdk.__name__.replace("mock_ai.clients.", "")
    mod = ModuleType(f"mock_ai.{sdk_name}")

    sys.modules[mod.__name__] = mod

    for client in client_classes:
        sdk_client = getattr(sdk, client)
        setattr(mod, client, sdk_client)
