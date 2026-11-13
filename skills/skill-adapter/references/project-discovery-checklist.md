# Selective Project-Discovery Checklist

Use this checklist in Step 3 to gather only the repository context required for the source skill's domain and dependencies. Stop inspecting each tier once its relevant facts are resolved.

## Tier 1: Explicit Rules & Local Skills (Highest Authority)

Inspect documented project rules and existing skills before reading application code:

- **Agent instructions & rules:** `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.agents/rules/*.md`, `.cursorrules`, `.cursor/rules/`, `.windsurfrules`, `.windsurf/rules/`, `.github/copilot-instructions.md`
- **Existing local skills & plugins:** `.agents/skills/`, `.agents/plugins/`, `.claude/skills/`, `.cursor/skills/`, `.windsurf/skills/`, `.github/skills/`, `.opencode/skills/`, `.codex/skills/`, `~/.gemini/config/skills/` (note existing skills with `metadata.adapted_from` or overlapping triggers)
- **Contributor & style guides:** `CONTRIBUTING.md`, `STYLE.md`, `.editorconfig`
- **Record:** `<explicit constraints, banned/required tools, mandatory workflows, existing skill overlaps, or "None found">`

## Tier 2: Product Context, Build, Runtime & Task Manifests

Inspect product docs and manifests relevant to the source skill's domain and required tools:

- **Product purpose & audience (for writing, docs, UX, or domain skills):** `README.md`, `docs/`, package metadata descriptions
- **Dependencies & runtimes:** `pyproject.toml`, `package.json`, `Cargo.toml`, `go.mod`, `Dockerfile`
- **Task runners & CI:** `justfile`, `Makefile`, `package.json` scripts, `.github/workflows/`
- **Linter / formatter / type configs:** `ruff.toml`, `tsconfig.json`, `eslint.config.*`, `biome.json`
- **Record:** `<product purpose/audience and exact verified commands for test, lint, build, and runtime execution>`

## Tier 3: Domain-Specific Active Patterns (Selective)

Inspect 1–2 representative files only in the subsystem the skill touches:

- **Engineering / Backend:** Entry points, database/schema layer, or test suite structure (`src/`, `tests/`)
- **UI / Frontend:** Component structure, styling approach, state/routing setup (`src/routes/`, `src/components/`)
- **Data / Charts / Analytics:** Query patterns, visualization libraries, output formats
- **Writing / Docs:** Existing READMEs, documentation tone, release notes, structural conventions (`docs/`)
- **Cross-Cutting / General Coding & Review:** Top-level design/architecture docs (`DESIGN.md`, `ARCHITECTURE.md`) and 1–2 primary entrypoints (`index.html`, `assets/main.js`, `src/main.*`) so coding-discipline skills reflect real codebase patterns
- **Confidence Note:** `<state whether observed patterns are current or legacy/inconsistent>`

## Tier 4: User Intent, Target Mode & Single Clarification

- **Stated Goal:** `<why the user is importing or updating this skill>`
- **Target Skill Path:** `<new installation path or existing adapted skill path for re-adaptation>`
- **Observed Friction:** `<what fails or grates if the source skill runs unchanged>`
- **Single Clarifying Question (only if blocked):** `<one focused question if Tiers 1–3 leave critical intent unresolved>`
