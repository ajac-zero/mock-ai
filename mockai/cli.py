import json
import os
import subprocess

import click
import pydantic

from mockai.models import PreDeterminedResponse

dir_path = os.path.dirname(os.path.realpath(__file__))


@click.command()
@click.argument("responses", type=click.File("rb"), required=False)
@click.option("--embedding-size", "-E", default=1536)
@click.option("--host", "-h", default="127.0.0.1")
@click.option("--port", "-p", default=8100)
def cli(responses, embedding_size, host, port):
    if responses:
        print(f"Reading pre-determined responses from {responses.name}.")

        try:
            responses_data = json.load(responses)
        except json.JSONDecodeError:
            raise click.BadParameter("Error reading JSON file: Is it valid JSON?")

        try:
            for response in responses_data:
                PreDeterminedResponse.model_validate(response)
        except pydantic.ValidationError as e:
            error = e.errors()[0]
            raise click.BadParameter(
                f"Error validating responses. Make sure they follow the proper structure.\nProblematic input: {error['input']}\nFix: {error['msg']}"
            )
        os.environ["MOCKAI_RESPONSES"] = responses.name

    os.environ["MOCKAI_EMBEDDING_SIZE"] = str(embedding_size)

    print(f"Starting MockAI server ...")
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
        ]
    )
