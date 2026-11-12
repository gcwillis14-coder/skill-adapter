# EVAL-01: Already Compatible (Minimal Diff)

## Source Skill
`source-skill/sql-schema-verification/`

## Target Repository
`target-repo/` (Python + PostgreSQL/SQLAlchemy + `uv` + `just`)

## Adapter Assertions
- **Decision:** Proceed to adaptation (passes Gate 1 and Gate 2).
- **Mechanism Preservation:** Retains all 4 workflow steps (schema inspection, type/nullability check, read-only `EXPLAIN`, flagging unverified assumptions).
- **Restraint / Minimal Diff:** Keeps ~85–95% of source phrasing verbatim without inventing extra sections or boilerplate.
- **Grounded Translation:** Points Step 1 to `src/db/models.py` and `alembic/versions/`, and maps DB check examples to `uv run` / `just check-db` without inventing unverified commands.
- **Provenance:** Stores `adapted_from`, `source_ref`, `adapted_date`, and `key_overrides` in YAML frontmatter `metadata:` (clean Tier 2 body, no HTML comment provenance).

## Downstream Representative Task
> Write a PostgreSQL query (and explain how you verified it) that computes total settled amount in dollars per account email for Q1, ensuring unsettled rows are excluded safely.

### Expected Downstream Lift
- **No Skill:** May guess column names (`amount`, `email`, `status`) or omit `settled_at IS NOT NULL` / `EXPLAIN` / unverified live DB note.
- **Unadapted Original Skill:** Inspects schema and notes `EXPLAIN`, but gives generic CLI guidance rather than `src/db/models.py`, `uv run`, or `just check-db`.
- **Adapted Skill:** Cites `accounts.owner_email`, `ledger_entries.amount_cents`, and nullable `ledger_entries.settled_at` directly from `src/db/models.py`, handles `settled_at IS NOT NULL`, uses `uv run` / `just check-db`, and flags that live PostgreSQL `EXPLAIN` was not executed if no DB instance is running.
