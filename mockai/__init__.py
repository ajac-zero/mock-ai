import sys
from types import ModuleType

from mockai.clients import cohere, mistralai, openai

clients = [
    (openai, ["OpenAI", "Client"]),
    (mistralai, ["MistralClient"]),
    (cohere, ["Client"]),
]

for sdk, client_classes in clients:
    sdk_name = sdk.__name__.replace("mockai.clients.", "")
    mod = ModuleType(f"mockai.{sdk_name}")

    sys.modules[mod.__name__] = mod

    for client in client_classes:
        sdk_client = getattr(sdk, client)
        setattr(mod, client, sdk_client)
