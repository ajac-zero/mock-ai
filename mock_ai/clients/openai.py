from functools import partial
from importlib.util import find_spec

__all__ = []


if find_spec("openai"):
    from openai import OpenAI as OriginalOpenAI

    OpenAI = partial(OriginalOpenAI, base_url="http://localhost:8000", api_key="Mock!")

    __all__.append("OpenAI")

if find_spec("mistralai"):
    from mistralai.client import MistralClient as OriginalMistralClient

    MistralClient = find_spec(OriginalMistralClient, base_url="http://localhost:8000", api_key="Mock!")

    __all__.append("MistralClient")
