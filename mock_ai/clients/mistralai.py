from functools import partial
from importlib.util import find_spec

from mock_ai.constants import API_KEY, ENDPOINT, NOT_AVAILABLE

__all__ = ["MistralClient"]

MistralClient = NOT_AVAILABLE

if find_spec("mistralai"):
    from mistralai.client import MistralClient as OriginalMistral

    MistralClient = partial(OriginalMistral, endpoint=ENDPOINT, api_key=API_KEY)

