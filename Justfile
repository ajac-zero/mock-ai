_default:
    @just --list --unsorted

# Start development server with hot-reload
dev-server:
    @uv run uvicorn main:app --app-dir ./mockai --port 8100 --reload

# Run all tests
test-all:
    @uv run pytest -q
    @uv build

# Run tests for OpenAI
test-openai:
    @uv run pytest -v ./tests/test_openai.py

# Run tests for Anthropic
test-anthropic:
    @uv run pytest -v ./tests/test_anthropic.py

# Run linting and formatting
tidy:
    @uv run ruff check --fix
    @uv run ruff format

# Build the package with uv and hatchling
build:
    @uv build

# Publish the package to PyPI
publish:
    @uv publish

# Build the docker image
docker-build VERSION="latest":
    @docker build --no-cache -t ajaczero/mock-ai:{{ VERSION }} .

# Run the docker container interactively
docker run:
    @docker run --rm -it -p 8100:8100 --name mockai-public -v $(pwd)/tests:/tests \
      ajaczero/mock-ai:latest

# Publish the container to Dockerhub
docker-publish VERSION="latest":
    @docker push ajaczero/mock-ai:{{ VERSION }}
