import json
import os
import subprocess

import click
import pydantic

from mockai.models import PreDeterminedResponse

dir_path = os.path.dirname(os.path.realpath(__file__))


@click.command()
@click.argument("responses", type=click.File("rb"), required=False)
@click.option("--host", "-h", default="127.0.0.1")
@click.option("--port", "-p", default=8100)
def cli(host, port, responses):
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
            raise click.BadParameter(
                f"Error validating responses. Make sure the follow the proper structure: {e}"
            )

        os.environ["MOCKAI_RESPONSES"] = json.dumps(responses_data)

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
