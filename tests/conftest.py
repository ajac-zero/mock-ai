import pytest
from testcontainers.core.container import DockerContainer
from testcontainers.core.image import DockerImage
from testcontainers.core.waiting_utils import wait_for_logs


@pytest.fixture(scope="session", autouse=True)
def mockai_server():
    with DockerImage(
        path=".", dockerfile_path="tests/test.Dockerfile", tag="ajac-zero/mock-ai:test"
    ) as image:
        with DockerContainer(str(image)).with_bind_ports(8100, 8100) as container:
            wait_for_logs(container, "Uvicorn running on http://0.0.0.0:8100")
            yield container
