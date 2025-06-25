# Gemini Project Notebook

This document helps the Gemini agent understand the project's context, conventions, and commands.

## Project Overview

A Python wrapper for the "Everything" search (es.exe) command-line tool by Voidtools. It provides a library and alternative frontends (MCP, Gradio) for the search functionality.

## Key Technologies

- **Programming Language(s):** Python (3.10+)
- **Framework(s):** N/A (It's a library, with optional Gradio UI)
- **Key Libraries:** `mcp`, `gradio`
- **Package Manager:** Poetry

## Development Workflow

### Running the Application

- **CLI:** `poetry run everything-search --help`
- **MCP Server:** `poetry run everything-search-mcp`
- **Gradio UI:** `poetry run everything-search-gradio`
- **Notes:** The core logic is a Python wrapper around the `es.exe` command-line tool.

### Running Tests

- **Command:** `make test` or `poetry run pytest -v --cov`
- **Notes:** Tests are located in the `tests/` directory and use `pytest` and `pytest-cov`.

### Linting and Formatting

- **Linter Command:** `make lint` (runs black, isort, flake8, mypy)
- **Formatter Command:** `make format` (runs black, isort)

### Building the Project

- **Command:** `make build` or `poetry build`
- **Output Directory:** `dist/`

## Important Files

- **Configuration:** `pyproject.toml` (for dependencies, project metadata, and tool configuration)
- **Entrypoint:** `everything_search.py` (main library), `mcp_server.py` (MCP interface), `gradio_app.py` (Gradio interface)
- **Build/Task Runner:** `Makefile`

## Architectural Notes

The project is a wrapper around an external command-line executable (`es.exe`). It's designed to be used as a Python library but also provides alternative server-based interfaces for interacting with the search functionality. It uses standard Python tooling (`poetry`, `pytest`, `black`, `mypy`) for dependency management, testing, and code quality.