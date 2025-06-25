.PHONY: help install test lint format clean build publish

help:
	@echo "Available commands:"
	@echo "  install     Install dependencies with Poetry"
	@echo "  test        Run tests with coverage"
	@echo "  lint        Run all linting tools"
	@echo "  format      Format code with black and isort"
	@echo "  clean       Clean build artifacts and cache"
	@echo "  build       Build the package"
	@echo "  publish     Publish to PyPI (requires PYPI_TOKEN)"

install:
	poetry install

test:
	poetry run pytest -v --cov

lint:
	poetry run black --check .
	poetry run isort --check-only .
	poetry run flake8 .
	poetry run mypy .

format:
	poetry run black .
	poetry run isort .

clean:
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	find . -type d -name "__pycache__" -exec rm -rf {} +

build: clean
	poetry build

publish: build
	poetry publish