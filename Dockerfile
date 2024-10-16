FROM ghcr.io/astral-sh/uv:python3.12-alpine

WORKDIR /app

RUN uv pip install ai-mock --system --no-cache

ENTRYPOINT ["mockai", "-h", "0.0.0.0"]
