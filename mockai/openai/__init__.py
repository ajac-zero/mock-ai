import warnings
from functools import partial

from mockai.constants import API_KEY, BASE_ENDPOINT, NOT_AVAILABLE

__all__ = [
    "OpenAI",
    "AsyncOpenAI",
    "Client",
    "AsyncClient",
]

OPENAI_ENDPOINT = BASE_ENDPOINT + "/openai"

OpenAI = NOT_AVAILABLE
AsyncOpenAI = NOT_AVAILABLE

Client = NOT_AVAILABLE
AsyncClient = NOT_AVAILABLE

try:
    from openai import (
        AsyncClient,
        AsyncOpenAI,
        Client,
        OpenAI,
    )

    OpenAI = partial(OpenAI, base_url=OPENAI_ENDPOINT, api_key=API_KEY)
    AsyncOpenAI = partial(AsyncOpenAI, base_url=OPENAI_ENDPOINT, api_key=API_KEY)

    Client = partial(Client, base_url=OPENAI_ENDPOINT, api_key=API_KEY)
    AsyncClient = partial(AsyncClient, base_url=OPENAI_ENDPOINT, api_key=API_KEY)
except (ImportError, TypeError):
    warnings.warn("OpenAI SDK not installed, openai clients are not available")
