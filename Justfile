default:
    @just --list

# Start development server with hot-reload
dev-server:
    @poetry run uvicorn main:app --app-dir ./mockai --port 8100 --reload

test-server:
    @docker build -t mockai-test . -f test.Dockerfile
    @docker run -d -p 8100:8100 --name mockai-test -v $(pwd)/tests:/app/tests --entrypoint poetry \
      mockai-test run ai-mock server ./tests/responses.json --port 8100 -h 0.0.0.0



# Cleans up the default port for the server
clean-port: stop-test-server
    @kill -9 $(lsof -t -i:8100)


stop-test-server:
    @docker rm -f mockai-test

test-all: stop-test-server test-server
    @poetry run pytest -q

test-openai: stop-test-server test-server
    @poetry run pytest -v ./tests/test_openai.py

test-anthropic: stop-test-server test-server
    @poetry run pytest -v ./tests/test_anthropic.py

tidy:
    @poetry run ruff check --fix
    @poetry run ruff format
    @just --fmt --unstable

publish:
    poetry build
    poetry publish

install:
    poetry install --extras "all"

push VERSION:
    docker build --no-cache -t ajaczero/mock-ai:{{ VERSION }} .
    docker tag ajaczero/mock-ai:{{ VERSION }} ajaczero/mock-ai:latest
    docker push ajaczero/mock-ai:{{ VERSION }}
    docker push ajaczero/mock-ai:latest
