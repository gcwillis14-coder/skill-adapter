# AGENTS.md

## Stack & Commands

- Python 3.12+ managed with `uv` (never invoke bare `python` or `pip`).
- PostgreSQL + SQLAlchemy 2.0 (`src/db/models.py`) + Alembic (`alembic/versions/`).
- Task runner: `just test` runs `uv run pytest`, `just check-db` runs `uv run python -m src.db.check_plan`.
- Never fabricate column names; verify against `src/db/models.py` and migrations first.
