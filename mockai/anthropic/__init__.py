import warnings
from functools import partial

from mockai.constants import API_KEY, BASE_ENDPOINT, NOT_AVAILABLE

from .router import anthropic_router as _router
from .services import generate_anthropic_response as _generate_anthropic_response

__all__ = [
    "Anthropic",
    "AsyncAnthropic",
    "AsyncClient",
    "Client",
    "_generate_anthropic_response",
    "_router",
]

ANTHROPIC_ENDPOINT = BASE_ENDPOINT + "/anthropic"

Anthropic = NOT_AVAILABLE
AsyncAnthropic = NOT_AVAILABLE

Client = NOT_AVAILABLE
AsyncClient = NOT_AVAILABLE

try:
    from anthropic import (
        Anthropic,
        AsyncAnthropic,
        AsyncClient,
        Client,
    )

    Anthropic = partial(Anthropic, base_url=ANTHROPIC_ENDPOINT, api_key=API_KEY)
    AsyncAnthropic = partial(
        AsyncAnthropic, base_url=ANTHROPIC_ENDPOINT, api_key=API_KEY
    )

    Client = partial(Client, base_url=ANTHROPIC_ENDPOINT, api_key=API_KEY)
    AsyncClient = partial(AsyncClient, base_url=ANTHROPIC_ENDPOINT, api_key=API_KEY)
except (ImportError, TypeError):
    warnings.warn("Anthropic SDK not installed, anthropic clients are not available")
