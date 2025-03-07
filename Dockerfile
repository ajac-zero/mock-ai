FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
  --mount=type=bind,source=README.md,target=README.md \
  --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
  uv sync --no-dev

COPY mockai/ ./mockai/

FROM python:3.12-slim-bookworm AS runtime

COPY --from=builder /app /app

ENV PATH="/app/.venv/bin:$PATH"

ENTRYPOINT [ "ai-mock", "server", "-h", "0.0.0.0" ]

CMD [ "-p", "8100" ]
