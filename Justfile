default:
    @just --list

# Start development server with hot-reload
dev-server:
    @uv run uvicorn main:app --app-dir ./mockai --port 8100 --reload

test-server:
    @docker build -t mockai-test . -f test.Dockerfile
    @docker run -d -p 8100:8100 --name mockai-test -v $(pwd)/tests:/tests --entrypoint uv \
      mockai-test run ai-mock server /tests/responses.json --port 8100 -h 0.0.0.0

# Cleans up the default port for the server
clean-port: stop-test-server
    @kill -9 $(lsof -t -i:8100)

stop-test-server:
    @docker rm -f mockai-test

test-all: stop-test-server test-server
    @uv run pytest -q

test-openai: stop-test-server test-server
    @uv run pytest -v ./tests/test_openai.py

test-anthropic: stop-test-server test-server
    @uv run pytest -v ./tests/test_anthropic.py

tidy:
    @uv run ruff check --fix
    @uv run ruff format
    @just --fmt --unstable

package-build:
    @uv build

publish: package-build
    @uv publish


install:
    @uv sync --all-extras

get-started: install
    @uv run pre-commit install

docker-build VERSION="latest":
    @docker build --no-cache -t ajaczero/mock-ai:{{ VERSION }} .

public-server:
    @docker run -d -p 8100:8100 --name mockai-public -v $(pwd)/tests:/tests \
      ajaczero/mock-ai:latest

push VERSION: package-build
    just docker-build {{ VERSION }}
    @docker tag ajaczero/mock-ai:{{ VERSION }} ajaczero/mock-ai:latest
    @docker push ajaczero/mock-ai:{{ VERSION }}
    @docker push ajaczero/mock-ai:latest
