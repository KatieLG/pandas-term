lint:
	uv run ruff check
	uv run ty check

format:
	uv run ruff check --fix
	uv run ruff format

test:
	uv run pytest

coverage:
	uv run coverage run -m pytest
	coverage report

check: format lint test
