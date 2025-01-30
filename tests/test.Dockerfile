FROM ghcr.io/astral-sh/uv:python3.10-alpine

# Install gcc
RUN apk add --no-cache gcc musl-dev python3-dev linux-headers

# Set up working directory
WORKDIR /app

# Copy project to the working directory
COPY pyproject.toml uv.lock tests/responses.json ./

COPY mockai/ ./mockai/

# Install the dependencies
RUN touch README.md && uv sync --all-extras --dev

# Expose the port
EXPOSE 8100

# Set the entrypoint
ENTRYPOINT [ "uv", "run", "ai-mock", "server", "-h", "0.0.0.0", "-p", "8100", "responses.json" ]
