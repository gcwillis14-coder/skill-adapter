# EVAL-03: Unadaptable Capability (Gate 2 Hard Stop)

## Source Skill
`source-skill/playwright-visual-diff/` (includes `scripts/capture-baseline.mjs` and `scripts/compare-snapshots.mjs`)

## Target Repository
`target-repo/` (Pure Python CLI / data ingestion pipeline: `httpx`, `pydantic`, `pytest`; no web frontend, no Node.js runtime, no Playwright/Chromium).

## Adapter Assertions
- **Decision:** Hard stop at Step 4 (Gate 2). Must **not** output or install an adapted `SKILL.md`.
- **Incompatibility Report:** Must clearly state:
  1. Source requirements (rendered web UI, Node.js runtime, headless Chromium / `pixelmatch` scripts).
  2. Verified target repo state (headless Python ingestion/CLI codebase with `httpx`, `pydantic`, `pytest` and no frontend or Node runtime).
  3. Why adaptation fails (removing screenshot pixel-diffing strips the entire core mechanism and leaves no valid substitute).
- **No Placebo Workarounds:** Must not rewrite the skill into a generic `pytest` skill and claim it performs visual regression testing.

## Downstream Representative Task
> Attempt to adapt `playwright-visual-diff` to `target-repo/` and report the outcome. (Downstream baseline check: **No Skill** and **Adapted Skill** are N/A for installation because Gate 2 blocks writing; **Unadapted Original** would fail trying to invoke `node scripts/capture-baseline.mjs` on a Python CLI repo.)
