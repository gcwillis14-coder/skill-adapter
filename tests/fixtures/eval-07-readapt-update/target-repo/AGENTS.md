# AGENTS.md

## FastAPI Backend Rules

- Python 3.12+ with `uv` and `just`.
- Route handlers live in `src/api/routes.py`; OpenAPI snapshot is checked via `just openapi-diff` (defined in `justfile`).
- API tests run via `just api-test` (`uv run pytest tests/api/`).
- Never use bare `python` or `pytest`.
