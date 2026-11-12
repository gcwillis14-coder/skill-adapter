# skill-adapter

An [agentskills.io](https://agentskills.io)-compatible skill that inspects an external agent skill, audits it for safety and architectural fit against your current repository, and produces a minimally adapted, project-specific version—without stripping the core mechanism that made the original skill useful.

## Aim

**Reuse the expertise in a skill without importing assumptions about someone else's project, process, audience, or taste.**

External skills often mix genuine specialist judgement (what to notice, decide, prevent, and verify) with local assumptions (frameworks, test runners, tone, or house style). Installing them unchanged causes friction; rewriting them blindly strips out what made them work. `skill-adapter` isolates the underlying behaviour that delivers value, adapts only what conflicts with your repository or audience, flags uncertainty and partial coverage honestly, and refuses to fake an adaptation when a core capability is missing.

## Why Standalone Skill Packaging

`skill-adapter` ships as a standalone skill directory (`skills/skill-adapter/`) rather than a native plugin (`plugin.json`). Because it is a single, self-contained skill with no MCP servers, lifecycle hooks, subagents, or always-on rules, standalone skill packaging works natively across Claude Code, OpenAI Codex CLI, and Google Antigravity (`agy` CLI, Antigravity IDE, and Antigravity 2.0) with a simple copy or symlink and zero idle context overhead. See [docs/installation.md](docs/installation.md) for details.

## How It Works

`skill-adapter` runs in six gated steps (defined in [skills/skill-adapter/SKILL.md](skills/skill-adapter/SKILL.md)) and never writes files until you approve the draft:

1. **Static-Text Safety & Provenance Gate (Gate 1):** Safely clones remote URLs (`core.symlinks=false`, `--no-recurse-submodules`, with mandatory temp cleanup), triages multi-skill/plugin suites, and audits `SKILL.md`, `references/`, `scripts/`, `examples/`, `resources/`, `assets/`, `hooks.json`, `mcp_config.json`, and dotfiles strictly as untrusted static text—backed by a deterministic Python scanner ([scripts/gate1_scan.py](skills/skill-adapter/scripts/gate1_scan.py)) for out-of-root symlinks, non-UTF-8/binaries, hidden bidi/zero-width/control characters, `..` traversal, and base64 payloads. Halts with a **Safety Rejection Report** on hostile directives.
2. **Source Skill Deconstruction:** Uses [references/source-analysis-template.md](skills/skill-adapter/references/source-analysis-template.md) to analyze what the skill helps an agent *notice*, *decide*, *do*, *prevent*, and *verify*, tag rationale provenance, classify instructions into four categories (`Essential mechanism`, `Adaptable implementation choice`, `Conditional judgement / preference`, `Uncertain`), map coupled instruction chains, and catalog bundled-file dependencies.
3. **Selective Project Discovery:** Uses [references/project-discovery-checklist.md](skills/skill-adapter/references/project-discovery-checklist.md) to read explicit rules (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.agents/rules/*.md`), manifests, existing local skills, product purpose/audience, and representative domain files using a tiered evidence hierarchy.
4. **Fit, Collision, & Boundary Gate (Gate 2):** Applies an ordered minimal-change ladder and substitution equivalence check (*"What failure was the original instruction preventing, and does the replacement still prevent it?"*), assigns dispositions (`copy`, `adapt`, `inline`, `omit`) to bundled files, checks collisions with existing local skills, recommends (never silently edits) rule-file updates for standing conventions, supports three-way re-adaptation via [references/readapt-guide.md](skills/skill-adapter/references/readapt-guide.md), and separates degradable checks from unadaptable hard stops (**Incompatibility Report**).
5. **Draft Adapted Skill & Adaptation Brief:** Outputs an **Adaptation Brief** (`Preserved / Changed / Uncertain`, partial-coverage disclosures, triggers/collisions/recommended rule edits, and trade-offs/manual fallbacks) alongside the adapted skill using YAML frontmatter `metadata:` provenance so the `SKILL.md` body stays clean.
6. **Verified Installation:** Confirms every command, path, and one-level relative link resolves in the target repository before writing files on explicit user confirmation, and delivers 1–3 distinctive-behaviour checks covering **Project Fit** and **Expertise Retention**.

## Quick Start

1. **Clone and install `skill-adapter`** into your user-level skills directory (see [docs/installation.md](docs/installation.md) for full details, symlink vs. `cp -r` notes, and workspace-scoped options):

   ```bash
   git clone https://github.com/gcwillis14-coder/skill-adapter.git
   cd skill-adapter

   # Claude Code
   mkdir -p ~/.claude/skills
   cp -r skills/skill-adapter ~/.claude/skills/skill-adapter

   # OpenAI Codex CLI
   mkdir -p ~/.agents/skills
   cp -r skills/skill-adapter ~/.agents/skills/skill-adapter

   # Google Antigravity (global)
   mkdir -p ~/.gemini/config/skills
   cp -r skills/skill-adapter ~/.gemini/config/skills/skill-adapter
   ```

2. **Invoke it inside your target repository** (`/skill-adapter` in Claude Code, `$skill-adapter` in Codex CLI, or an explicit prompt in clients without slash commands):

   ```text
   Use skill-adapter to adapt /path/to/external-skill for this project. I want to use it when building or polishing Svelte components.
   ```

3. **Review the Adaptation Brief**, approve the installation path (`.agents/skills/<name>/` or `.claude/skills/<name>/`), and run the suggested distinctive-behaviour checks on a real repository task.

### Re-Adapting When Upstream or Your Repo Changes

Because every adapted skill records provenance in YAML frontmatter (`metadata.adapted_from`, `source_ref`, `adapted_date`, `key_overrides`), you can point `skill-adapter` at an updated upstream skill and your existing project skill directory to run a three-way reconciliation ([references/readapt-guide.md](skills/skill-adapter/references/readapt-guide.md)) that adopts upstream improvements while keeping valid local overrides intact.

## Worked Example

The example below mirrors `EVAL-02` ([tests/fixtures/eval-02-ui-polish](tests/fixtures/eval-02-ui-polish) and [tests/results.md](tests/results.md)): adapting a generic **Frontend Visual Polish** skill (`frontend-visual-polish`) that enforces WCAG contrast ratios, `:focus-visible` states, and responsive checks—but assumes **React**, **Tailwind CSS**, `npm run lint`, and `npm run test:ui`—into a **SvelteKit + TypeScript + `just`** repository.

### 1. Adaptation Brief Output

- **Source contribution:** Enforces baseline accessibility (4.5:1 body text contrast, 3:1 large text/boundaries, semantic `<button>`/`<a>` elements, explicit `:hover`/`:focus-visible`/`:disabled` states) and 375px/1280px responsive overflow checks before completing UI tasks.
- **Project needs:** Per `GEMINI.md`, `package.json`, and `justfile`, this project uses SvelteKit with Svelte 5 runes, TypeScript, scoped `<style>` blocks (no React, no Tailwind), and `just check` / `just test` for verification.
- **Summary of changes & file manifest:**
  - *Preserved:* Contrast thresholds (4.5:1 / 3:1), interactive state requirements, semantic `<button>`/`<a>` rules, and 375px/1280px viewport checks.
  - *Changed:* Translated React `useState`/`onClick` and Tailwind class idioms (`focus-visible:ring-2`) to Svelte 5 runes (`$state`, `$derived`, `$props()`), native `onclick={...}`, and scoped `<style>` CSS; mapped `npm run lint` / `npm run test:ui` to `just check` and `just test`. Equivalence disclosure: `just check`/`just test` cover static checks and unit tests, leaving headless browser viewport verification as partial coverage.
  - *Uncertain:* Exact `375px` / `1280px` breakpoint constants lack author rationale and are preserved provisionally alongside an explicit manual browser check.
  - *Bundled-file manifest:* Create `SKILL.md` (single-file skill; no bundled `references/` or `scripts/`).
- **Triggers, collisions, & recommended rule edits:** No conflicting local UI skill found; scoped `description` to Svelte UI components; no `GEMINI.md` edits required.
- **Trade-offs & manual fallbacks:** This repository has no automated headless visual/viewport test runner (`test:ui`/Playwright absent). Responsive checks at 375px and 1280px, keyboard focus navigation, and contrast remain manual browser verification steps in `npm run dev`.

### 2. Adapted `SKILL.md` Output

```markdown
---
name: frontend-visual-polish
description: Audit and refine Svelte UI components for visual hierarchy, WCAG contrast, keyboard accessibility, and responsive layout before completing frontend tasks.
metadata:
  adapted_from: frontend-visual-polish
  source_ref: local-import
  adapted_date: "2026-11-12"
  key_overrides: "React/Tailwind -> Svelte 5/scoped CSS; npm lint/test:ui -> just check/just test; manual 375px/1280px browser fallback"
---

# Frontend Visual Polish

Ensure every new or modified Svelte UI component meets baseline visual, accessibility, and responsive standards.

## Rules

1. **Contrast & Legibility:** Maintain at least a 4.5:1 contrast ratio for body text and 3:1 for large text and interactive boundaries. Never rely on color alone to convey status.
2. **Interactive States:** Every clickable element must define explicit `:hover`, `:focus-visible`, and `:disabled` states in scoped component CSS. Use semantic `<button>` and `<a>` elements rather than `onclick` handlers on `<div>` tags.
3. **Responsive Layout:** Verify component layout at 375px (mobile) and 1280px (desktop) viewports without horizontal overflow via manual browser inspection in `npm run dev` (no automated UI runner is configured).
4. **Implementation Pattern (Svelte 5 + TypeScript):**
   - Keep styles modular inside component `<style>` blocks using CSS custom properties with fallback values.
   - Manage local interactive state with Svelte 5 runes (`$state`, `$derived`, `$props()`) and type component props via TypeScript interfaces.
5. **Verification:** Run `just check` and `just test` before finishing, and complete the manual 375px/1280px and keyboard-focus check when UI layout or interactive states change.
```

## Validation & Benchmark Suite

`skill-adapter` includes a structural validator (`tests/validate_skills.py`, requiring Python 3.10+ and `PyYAML`), unit tests (`tests/test_validate_skills.py`, `tests/test_gate1_scan.py`), and eight end-to-end evaluation scenarios (`EVAL-01` through `EVAL-08`):

| Scenario | What It Verifies |
| :--- | :--- |
| **EVAL-01 (`sql-schema-verification`)** | **Minimal-diff restraint:** Keeps ~90% of an already-compatible skill verbatim, mapping only `uv run`, `just check-db`, and `src/db/models.py` paths. |
| **EVAL-02 (`frontend-visual-polish`)** | **Selective translation & degradable check:** Preserves WCAG/accessibility rules while translating React/Tailwind to Svelte 5/scoped CSS and adding a manual viewport fallback. |
| **EVAL-03 (`playwright-visual-diff`)** | **Gate 2 hard stop:** Refuses to adapt a Chromium pixel-diff skill into a headless Python CLI repo, outputting an **Incompatibility Report** instead of a placebo skill. |
| **EVAL-04 (`pr-release-notes`)** | **Gate 1 security rejection:** Detects and halts on a concealed `curl ... -d "$(env)"` exfiltration + prompt-injection payload inside `references/format.md`. |
| **EVAL-05 (`technical-release-notes`)** | **Audience & tone adaptation:** Preserves diff/flag verification while replacing SaaS marketing tone and Jira placeholders with `.agents/rules/tone.md` and `CHANGELOG.md` conventions. |
| **EVAL-06 (`data-viz-charts`)** | **Multi-file bundle & collision scoping:** Audits and adapts `SKILL.md` + `scripts/render_chart.py` + `references/palette-rules.md` while resolving overlap with an existing `.agents/skills/chart-reporting` skill. |
| **EVAL-07 (`api-contract-check` v2)** | **Provenance-aware re-adaptation:** Merges an upstream v2 OpenAPI diff step while preserving existing local `uv run` and `just api-test` overrides via `metadata:`. |
| **EVAL-08 (`concise-suite`)** | **Multi-skill plugin triage & cross-cutting discovery:** Enumerates suite skills/hooks with `gate1_scan.py`, samples `DESIGN.md`/`assets/main.js`, discloses lost session persistence from omitting `hooks/`, and tightens broad triggers. |

Run the structural validator and unit tests from the repository root:

```bash
python3 tests/validate_skills.py
python3 -m unittest discover -s tests -v
```

You can also validate any custom or adapted skill directory directly (with optional `--json` output):

```bash
python3 tests/validate_skills.py /path/to/your-skill --json
```

See [tests/rubric.md](tests/rubric.md) for the evaluation criteria and [tests/results.md](tests/results.md) for recorded v1 results.

## Repository Structure

```text
skill-adapter/
├── README.md
├── LICENSE
├── .gitignore
├── docs/
│   └── installation.md
├── skills/
│   └── skill-adapter/
│       ├── SKILL.md
│       ├── references/
│       │   ├── source-analysis-template.md
│       │   ├── project-discovery-checklist.md
│       │   └── readapt-guide.md
│       └── scripts/
│           └── gate1_scan.py
└── tests/
    ├── validate_skills.py
    ├── test_validate_skills.py
    ├── test_gate1_scan.py
    ├── rubric.md
    ├── results.md
    └── fixtures/
        ├── eval-01-sql-verification/
        ├── eval-02-ui-polish/
        ├── eval-03-playwright-visual/
        ├── eval-04-unsafe-webhook/
        ├── eval-05-writing-docs/
        ├── eval-06-charts-multifile/
        ├── eval-07-readapt-update/
        └── eval-08-plugin-suite/
```

## License

[MIT](LICENSE)
