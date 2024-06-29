from functools import partial
from importlib.util import find_spec

from fauxai.constants import API_KEY, ENDPOINT, NOT_AVAILABLE

__all__ = ["Client", "AsyncClient"]

Client = NOT_AVAILABLE
AsyncClient = NOT_AVAILABLE

if find_spec("cohere"):
    from cohere import AsyncClient, Client

    Client = partial(Client, base_url=ENDPOINT, api_key=API_KEY)
    AsyncClient = partial(AsyncClient, base_url=ENDPOINT, api_key=API_KEY)
