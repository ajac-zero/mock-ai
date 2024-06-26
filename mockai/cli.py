import os
import subprocess

import typer

cli = typer.Typer()

dir_path = os.path.dirname(os.path.realpath(__file__))


@cli.command()
def start(host: str = "127.0.0.1", port: int = 8100):
    typer.echo(f"Starting MockAI server on http://{host}:{port}...\n")
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
