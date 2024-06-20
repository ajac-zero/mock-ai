.PHONY: test
test:
	@PYTHONPATH=. pytest

.PHONY: format
format:
	@ruff check --fix
	@ruff format
