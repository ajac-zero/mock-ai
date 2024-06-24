import pytest
import subprocess
import time


@pytest.fixture(scope="session")
def mockai_server():
    process = subprocess.Popen("mock-ai")
    time.sleep(2)

    yield

    process.terminate()
