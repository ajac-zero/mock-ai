import os
import subprocess
from typing import Annotated, Optional

from rich import print
from typer import Argument, FileText, Typer

cli = Typer()

dir_path = os.path.dirname(os.path.realpath(__file__))


@cli.command()
def start(
    responses: Annotated[Optional[FileText], Argument()] = None,
    host: str = "127.0.0.1",
    port: int = 8100,
):
    if responses:
        print(f"[cyan]Reading pre-determined responses from[/cyan] [bold yellow]{responses.name}[/bold yellow].")
        os.environ["MOCKAI_RESPONSES"] = responses.read()

    url = f"http://{host}:{port}"
    print(f"[green]Starting MockAI server on[/green] [link={url}][bold blue]{url}[/bold blue][/link] ...")
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
