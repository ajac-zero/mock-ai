from functools import partial
from importlib.util import find_spec

from mock_ai.constants import API_KEY, ENDPOINT, NOT_AVAILABLE

__all__ = ["OpenAI", "Client"]

OpenAI = NOT_AVAILABLE
Client = NOT_AVAILABLE

if find_spec("openai"):
    from openai import Client as OpenAIClient
    from openai import OpenAI as OriginalOpenAI

    OpenAI = partial(OriginalOpenAI, base_url=ENDPOINT, api_key=API_KEY)
    Client = partial(OpenAIClient, base_url=ENDPOINT, api_key=API_KEY)
