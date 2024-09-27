from typing import Annotated

PORT = 8100
BASE_ENDPOINT = f"http://localhost:{PORT}"
API_KEY = "mock!"
NOT_AVAILABLE = Annotated[None, "Required library is not installed"]
