import time
from multiprocessing import Process

import pytest
import uvicorn

from mockai.constants import API_KEY, ENDPOINT, PORT
from mockai.server import app


@pytest.fixture(scope="session", autouse=True)
def mockai_server():
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
