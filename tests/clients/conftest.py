import subprocess
import time

import pytest

from mock_ai.constants import API_KEY, ENDPOINT


@pytest.fixture(scope="session")
def mockai_server():
    process = subprocess.Popen("mock-ai")
    time.sleep(2)

    yield

    process.terminate()


@pytest.fixture
def endpoint():
    return ENDPOINT


@pytest.fixture
def api_key():
    return API_KEY
