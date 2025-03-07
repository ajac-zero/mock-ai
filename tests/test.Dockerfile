FROM python:3.12-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set up working directory
WORKDIR /app

# Copy project to the working directory
COPY pyproject.toml uv.lock tests/responses.json ./

COPY mockai/ ./mockai/

# Install the dependencies
RUN touch README.md && uv sync --all-extras

# Expose the port
EXPOSE 8100

# Set the entrypoint
ENTRYPOINT [ "uv", "run", "ai-mock", "server", "-h", "0.0.0.0", "-p", "8100", "responses.json" ]
