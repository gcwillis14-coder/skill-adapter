# EVAL-08 Task

Adapt `source-plugin` (a multi-skill, hook-backed plugin suite) for `target-repo` (a zero-build static HTML/CSS/JS site).

Expected adapter behaviour:
1. Run Gate 1 (`scripts/gate1_scan.py`) and enumerate `plugin.json`, `hooks/mode-tracker.js`, `skills/concise-dev/SKILL.md`, and `skills/concise-review/SKILL.md`.
2. Clarify or scope the target skill (`concise-dev`) rather than silently ignoring `concise-review` and `hooks/`.
3. Inspect Tier 1 (`.agents/plugins/`) and Tier 3 (`DESIGN.md`, `index.html`, `assets/main.js`) so the adapted skill reflects the IIFE JS pattern and CSS custom properties.
4. Disclose the partial-coverage degradation from omitting `hooks/mode-tracker.js` (loss of session persistence), log any scoped/dropped clauses (such as hardware calibration) in `*Changed:*`, and tighten the broad `"any coding task / reviewing"` trigger against installed plugins/skills.
