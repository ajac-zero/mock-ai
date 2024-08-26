import json
import os
import subprocess
from typing import Annotated, Optional

import pydantic
from rich import print
from typer import Argument, FileText, Typer

from mockai.schemas import PreDeterminedResponse

cli = Typer()

dir_path = os.path.dirname(os.path.realpath(__file__))


@cli.command()
def start(
    response_file: Annotated[Optional[FileText], Argument()] = None,
    host: str = "127.0.0.1",
    port: int = 8100,
):
    if response_file:
        print(
            f"[cyan]Reading pre-determined responses from[/cyan] [bold yellow]{response_file.name}[/bold yellow]."
        )

        try:
            with open(response_file.name, "r") as f:
                responses_data = json.load(f)
        except json.JSONDecodeError:
            print("[red]Error reading JSON file: Is it valid JSON?[/red]")
            return

        try:
            for response in responses_data:
                PreDeterminedResponse.model_validate(response)
        except pydantic.ValidationError as e:
            print(
                f"[red]Error validating responses. Make sure the follow the proper structure: {e}[/red]"
            )
            return

        os.environ["MOCKAI_RESPONSES"] = json.dumps(responses_data)

    url = f"http://{host}:{port}"
    print(
        f"[green]Starting MockAI server on[/green] [link={url}][bold blue]{url}[/bold blue][/link] ..."
    )
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
