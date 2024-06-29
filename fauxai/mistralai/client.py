from functools import partial
from importlib.util import find_spec

from fauxai.constants import API_KEY, ENDPOINT, NOT_AVAILABLE

__all__ = ["MistralClient", "MistralAsyncClient"]

MistralClient = NOT_AVAILABLE

if find_spec("mistralai"):
    from mistralai.async_client import MistralAsyncClient
    from mistralai.client import MistralClient

    MistralClient = partial(MistralClient, endpoint=ENDPOINT, api_key=API_KEY)
    MistralAsyncClient = partial(MistralAsyncClient, endpoint=ENDPOINT, api_key=API_KEY)
