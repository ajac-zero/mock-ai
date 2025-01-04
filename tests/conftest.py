import subprocess
import time

import pytest


@pytest.fixture(scope="session", autouse=True)
def mockai_server():
    process = subprocess.Popen(
        ["poetry", "run", "ai-mock", "server", "./tests/responses.json"]
    )
    time.sleep(3)

    yield

    process.terminate()
    process.wait()
