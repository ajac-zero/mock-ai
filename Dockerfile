FROM ghcr.io/astral-sh/uv:python3.10-alpine


# Install gcc
RUN apk add --no-cache gcc musl-dev python3-dev linux-headers

# Set up working directory
WORKDIR /app

# Copy everything to the working directory
COPY . /app

# Install the dependencies
RUN uv sync


# Expose the port
EXPOSE 8100

ENTRYPOINT ["uv","run","ai-mock", "server", "-h", "0.0.0.0", "-p", "8100"]
