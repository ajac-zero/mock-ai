from fastapi import FastAPI

from .clients.openai_client import OpenAI

app = FastAPI()

client = OpenAI()


@app.post("/chat/completions/create")
def create(message):
    client.chat.completions.create()
