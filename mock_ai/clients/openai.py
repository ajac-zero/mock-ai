from functools import partial

from openai import OpenAI as OriginalOpenAI

OpenAI = partial(OriginalOpenAI, base_url="http://localhost:8000", api_key="Mock!")
