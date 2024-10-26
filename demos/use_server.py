# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "openai",
#     "rich",
# ]
# ///
from openai import OpenAI
from rich.console import Console


def main() -> None:
    console = Console()

    client = OpenAI(base_url="http://localhost:8100/openai", api_key="None")

    prompt = input("> ")

    response = client.chat.completions.create(
        model="gpt-5", messages=[{"role": "user", "content": prompt}]
    )

    console.print("Prompt: ", style="blue", end=" ")
    console.print(prompt)

    message = response.choices[0].message
    console.print("Response object:", style="bold red", end=" ")
    console.print(message)

    content = message.content
    console.print("Respobe content: ", style="red", end=" ")
    console.print(content)


if __name__ == "__main__":
    main()
