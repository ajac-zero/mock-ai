import warnings
from functools import partial

from mockai.constants import API_KEY, BASE_ENDPOINT, NOT_AVAILABLE

from .router import openai_router as _router
from .services import (
    generate_openai_completion_response as _generate_openai_completion_response,
)
from .services import (
    generate_openai_embeddings_response as _generate_openai_embeddings_response,
)

__all__ = [
    "AsyncClient",
    "AsyncOpenAI",
    "AzureOpenAI",
    "AzureOpenAI",
    "Client",
    "OpenAI",
    "_generate_openai_completion_response",
    "_generate_openai_embeddings_response",
    "_router",
]

OPENAI_ENDPOINT = BASE_ENDPOINT + "/openai"

OpenAI = NOT_AVAILABLE
AsyncOpenAI = NOT_AVAILABLE

Client = NOT_AVAILABLE
AsyncClient = NOT_AVAILABLE

AzureOpenAI = NOT_AVAILABLE
AsyncAzureOpenAI = NOT_AVAILABLE

try:
    from openai import (
        AsyncAzureOpenAI,
        AsyncClient,
        AsyncOpenAI,
        AzureOpenAI,
        Client,
        OpenAI,
    )

    OpenAI = partial(OpenAI, base_url=OPENAI_ENDPOINT, api_key=API_KEY)
    AsyncOpenAI = partial(AsyncOpenAI, base_url=OPENAI_ENDPOINT, api_key=API_KEY)

    Client = partial(Client, base_url=OPENAI_ENDPOINT, api_key=API_KEY)
    AsyncClient = partial(AsyncClient, base_url=OPENAI_ENDPOINT, api_key=API_KEY)

    AzureOpenAI = partial(
        AzureOpenAI, base_url=OPENAI_ENDPOINT, api_key=API_KEY, api_version="None"
    )
    AsyncAzureOpenAI = partial(
        AsyncAzureOpenAI, base_url=OPENAI_ENDPOINT, api_key=API_KEY, api_version="None"
    )
except (ImportError, TypeError):
    warnings.warn("OpenAI SDK not installed, openai clients are not available")
