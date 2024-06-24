import os
import subprocess

import typer

cli = typer.Typer()

dir_path = os.path.dirname(os.path.realpath(__file__))


@cli.command()
def start(port: int = 8000):
    typer.echo(f"Starting mock-ai server on port {port}...\n")
    subprocess.run(
        ["uvicorn", "--app-dir", f"{dir_path}", "server:app", "--port", f"{port}"]
    )
