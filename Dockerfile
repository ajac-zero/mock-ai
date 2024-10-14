FROM ghcr.io/astral-sh/uv:python3.12-alpine

WORKDIR /app

ENTRYPOINT ["uvx", "--from=ai-mock", "mockai"]

CMD ["-h", "0.0.0.0"]
