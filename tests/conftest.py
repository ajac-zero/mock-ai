import pytest
import requests


@pytest.fixture(scope="session", autouse=True)
def check_mockai_server():
    response = requests.get("http://localhost:8100/api/responses/read")
    response.raise_for_status()
    response = response.json()

    if not len(response):
        raise RuntimeError("ai-mock server not having any responsees")
    yield
