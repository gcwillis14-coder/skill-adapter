# EVAL-06: Multi-File Bundle & Local Skill Collision

## Source Skill
`source-skill/data-viz-charts/` (`SKILL.md` + `scripts/render_chart.py` + `references/palette-rules.md`)

## Target Repository
`target-repo/` (Python `uv` analytics repo with existing `.agents/skills/chart-reporting/SKILL.md` enforcing Okabe-Ito palette and `reports/output/*.svg`)

## Adapter Assertions
- **Decision:** Proceed to adaptation (passes Gate 1 and Gate 2), addressing bundled files and local skill collision.
- **Multi-File Handling:** Audits and maps every bundled file:
  - `scripts/render_chart.py` (copy or adapt default `--palette okabe-ito` / verify `uv run python scripts/render_chart.py`)
  - `references/palette-rules.md` (adapt `corporate`/`build/charts/*.png` to `okabe-ito`/`reports/output/*.svg`, keeping 1-level relative link).
- **Collision Detection & Trigger Precision:** Detects `.agents/skills/chart-reporting/SKILL.md`, highlights overlap on palette/output rules, and proposes explicit boundary sharpening (e.g., narrowing `data-viz-charts` description/scope to chart rendering & data-verification workflow while deferring or merging with `chart-reporting`) rather than silently overwriting or colliding.
- **Grounded Commands:** Translates `python scripts/render_chart.py ...` to `uv run python scripts/render_chart.py ... --palette okabe-ito --out reports/output/...svg`.

## Downstream Representative Task
> Render a bar chart SVG for `SAMPLE_METRICS` from `src/reports/monthly.py` into `reports/output/latency.svg` using the repo's required palette and runner.

### Expected Downstream Lift
- **No Skill:** Writes custom code or guesses colors/paths without checking units or running the bundled script.
- **Unadapted Original Skill:** Invokes bare `python`, passes `--palette corporate`, and writes to `build/charts/out.png` — violating `AGENTS.md` and `chart-reporting`.
- **Adapted Skill:** Uses `uv run python scripts/render_chart.py` with `--palette okabe-ito` and `--out reports/output/latency.svg`, preserves `ms` units, and respects `chart-reporting` boundaries.
