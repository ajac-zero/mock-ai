FROM ghcr.io/astral-sh/uv:python3.12-alpine

WORKDIR /app

RUN uv pip install ai-mock --system --no-cache

EXPOSE 8100

ENTRYPOINT ["ai-mock", "server", "-h", "0.0.0.0"]
