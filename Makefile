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

compile:
	uv run nuitka --standalone --clang --disable-ccache --python-flag=no_site --lto=yes --output-filename=pd .venv/bin/pd
