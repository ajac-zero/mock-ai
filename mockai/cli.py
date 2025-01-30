import json
import os
import subprocess

import click
import pydantic

from mockai.models.json_file.models import PreDeterminedResponses

dir_path = os.path.dirname(os.path.realpath(__file__))


@click.group()
def cli():
    pass


@cli.command()
@click.argument("responses", type=click.File("rb"), required=False)
@click.option("--embedding-size", "-E", default=1536)
@click.option("--host", "-h", default="127.0.0.1")
@click.option("--port", "-p", default=8100)
def server(responses, embedding_size, host, port):
    if responses:
        print(f"Reading pre-determined responses from {responses.name}.")  # noqa: T201

        try:
            responses_data = json.load(responses)
        except json.JSONDecodeError:
            raise click.BadParameter("Error reading JSON file: Is it valid JSON?")

        try:
            PreDeterminedResponses.model_validate(responses_data)
        except pydantic.ValidationError as e:
            error = e.errors()[0]
            raise click.BadParameter(
                f"Error validating responses. Make sure they follow the proper structure.\nProblematic input: {error['input']}\nFix: {error['msg']}"
            )
        os.environ["MOCKAI_RESPONSES"] = responses.name

    os.environ["MOCKAI_EMBEDDING_SIZE"] = str(embedding_size)

    print("Starting MockAI server ...")  # noqa: T201
    subprocess.run(
        [
            "uvicorn",
            "--app-dir",
            f"{dir_path}",
            "main:app",
            "--host",
            host,
            "--port",
            str(port),
            "--log-config",
            f"{dir_path}/logging_conf.yaml",
        ]
    )
