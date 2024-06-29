from functools import partial
from importlib.util import find_spec

from fauxai.constants import API_KEY, ENDPOINT, NOT_AVAILABLE

__all__ = [
    "Anthropic",
    "AsyncAnthropic",
    "Client",
    "AsyncClient",
]

Anthropic = NOT_AVAILABLE
AsyncAnthropic = NOT_AVAILABLE

Client = NOT_AVAILABLE
AsyncClient = NOT_AVAILABLE

if find_spec("anthropic"):
    from anthropic import Anthropic, AsyncAnthropic, AsyncClient, Client

    Anthropic = partial(Anthropic, base_url=ENDPOINT, api_key=API_KEY)
    AsyncAnthropic = partial(AsyncAnthropic, base_url=ENDPOINT, api_key=API_KEY)

    Client = partial(Client, base_url=ENDPOINT, api_key=API_KEY)
    AsyncClient = partial(AsyncClient, base_url=ENDPOINT, api_key=API_KEY)
