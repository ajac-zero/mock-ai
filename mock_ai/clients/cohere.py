from functools import partial
from importlib.util import find_spec

from mock_ai.constants import API_KEY, ENDPOINT, NOT_AVAILABLE

__all__ = ["Client"]

Client = NOT_AVAILABLE

if find_spec("cohere"):
    from cohere import Client as OriginalCohereClient

    Client = partial(OriginalCohereClient, base_url=ENDPOINT, api_key=API_KEY)
