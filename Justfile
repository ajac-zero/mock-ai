default:
  just --list

# Start development server with hot-reload
dev-server:
  poetry run uvicorn main:app --app-dir ./mockai --port 8100 --reload

# Start test server with pre-determined responses
test-server:
  poetry run mockai ./tests/responses.json

test-all:
  poetry run pytest -q

test-openai:
  poetry run pytest -v ./tests/test_openai.py

test-anthropic:
  poetry run pytest -v ./tests/test_anthropic.py

tidy:
  poetry run ruff check --fix
  poetry run ruff format

publish:
  poetry build
  poetry publish

push VERSION:
  docker build --no-cache -t ajaczero/mock-ai:{{VERSION}} .
  docker tag ajaczero/mock-ai:{{VERSION}} ajaczero/mock-ai:latest
  docker push ajaczero/mock-ai:{{VERSION}}
  docker push ajaczero/mock-ai:latest
