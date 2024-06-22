from functools import partial
from importlib.util import find_spec

__all__ = []

ENDPOINT = "http://localhost:8000"
API_KEY = "mock!"

if find_spec("openai"):
    from openai import OpenAI as OriginalOpenAI

    OpenAI = partial(OriginalOpenAI, base_url=ENDPOINT, api_key=API_KEY)

    __all__.append("OpenAI")

if find_spec("mistralai"):
    from mistralai.client import MistralClient as OriginalMistral

    MistralClient = partial(OriginalMistral, endpoint=ENDPOINT, api_key=API_KEY)

    __all__.append("MistralClient")

if find_spec("cohere"):
    from cohere import Client as OriginalCohereClient

    Client = partial(OriginalCohereClient, base_url=ENDPOINT, api_key=API_KEY)

    __all__.append("Client")
