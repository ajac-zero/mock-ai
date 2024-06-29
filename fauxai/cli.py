import os
import subprocess
from typing import Annotated, Optional

from typer import Argument, FileText, Typer, echo

cli = Typer()

dir_path = os.path.dirname(os.path.realpath(__file__))


@cli.command()
def start(
    responses: Annotated[Optional[FileText], Argument()] = None,
    host: str = "127.0.0.1",
    port: int = 8100,
):
    if responses:
        echo(f"Reading {responses.name}...")
        os.environ["FAUXAI_RESPONSES"] = responses.read()

    echo(f"Starting FauxAI server on http://{host}:{port}...")
    subprocess.run(
        [
            "uvicorn",
            "--app-dir",
            f"{dir_path}",
            "server:app",
            "--host",
            host,
            "--port",
            str(port),
        ]
    )
