FROM python:3.11-buster AS builder

WORKDIR /app

RUN pip install poetry

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

COPY pyproject.toml poetry.lock README.md ./
COPY mockai ./mockai

RUN poetry install --without dev && rm -rf $POETRY_CACHE_DIR

FROM python:3.11-slim-buster AS runtime

WORKDIR /app

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

RUN mkdir data
COPY scripts ./scripts
COPY mockai ./mockai

ENTRYPOINT [ "python", "-m", "scripts.docker_start" ]
