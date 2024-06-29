import os
import time
from multiprocessing import Process

import pytest
import uvicorn

from fauxai.constants import API_KEY, ENDPOINT, PORT
from fauxai.server import app

DIR = os.path.dirname(os.path.realpath(__file__))


@pytest.fixture(scope="session", autouse=True)
def mockai_server():
    with open(f"{DIR}/mock_responses.json", "r") as json_responses:
        os.environ["FAUXAI_RESPONSES"] = json_responses.read()

    process = Process(target=lambda: uvicorn.run(app, port=PORT), daemon=True)
    process.start()

    time.sleep(2)

    yield

    process.terminate()


@pytest.fixture
def endpoint():
    return ENDPOINT


@pytest.fixture
def api_key():
    return API_KEY
