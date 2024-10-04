dev-server:
  poetry run uvicorn main:app --app-dir ./mockai --port 8100

test-server:
  poetry run mockai ./tests/responses.json

test-all:
  poetry run pytest -q

test-openai:
  poetry run pytest -v ./tests/test_openai.py

test-anthropic:
  poetry run pytest -v ./tests/test_anthropic.py
