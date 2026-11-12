# EVAL-07: Re-Adapt / Update Existing Adapted Skill

## Source Skill (Upstream v2)
`source-skill-v2/api-contract-check/` (adds Step 4 OpenAPI schema diff check and updates `references/checks.md`)

## Target Repository
`target-repo/` (already contains `.agents/skills/api-contract-check/` adapted from `v1.0.0` with YAML frontmatter `metadata:` provenance and local `src/api/routes.py` / `just api-test` / `/v1` overrides)

## Adapter Assertions
- **Decision:** Enter Re-adapt / Update branch (`references/readapt-guide.md`) at Step 4.
- **Provenance Read & Update:** Reads existing `metadata:` (`adapted_from`, `source_ref: v1.0.0`, `adapted_date: 2026-10-01`, `key_overrides`) and advances `source_ref` / `adapted_date` / `key_overrides` in the new draft.
- **Upstream Adoption:** Incorporates upstream v2 Step 4 (OpenAPI schema diff) and translates `python scripts/export_openapi.py --diff` (non-existent script) to the verified local command `just openapi-diff` from `justfile` / `AGENTS.md`.
- **Override Preservation:** Preserves local overrides (`src/api/routes.py`, `just api-test`, `/v1` backward-compatibility note in `references/checks.md`) while merging upstream v2's `Any`-payload OpenAPI rule into `references/checks.md`.
- **Brief Section:** Includes an **Upstream Delta & Override Preservation** summary in the Adaptation Brief.

## Downstream Representative Task
> Add a `currency: str` field to `OrderSummary` in `src/api/routes.py` without breaking existing `/v1` consumers, and run the required contract and OpenAPI checks.

### Expected Downstream Lift
- **No Skill:** Modifies `OrderSummary` without running `just openapi-diff` or checking `/v1` backward compatibility.
- **Unadapted Original Skill (v2):** Instructs running `pytest tests/api/` and `python scripts/export_openapi.py --diff`, which fails because `scripts/export_openapi.py` does not exist in `target-repo/`.
- **Adapted Skill (re-adapted v2):** Inspects `src/api/routes.py`, adds backward-compatible default or `/v2` consideration per `references/checks.md`, and runs/cites `just api-test` and `just openapi-diff`.
