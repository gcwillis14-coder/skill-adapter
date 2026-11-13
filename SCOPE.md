# Scope

`skill-adapter` customises external agent skills for your project without stripping the judgement that made them useful.

This document sets clear expectations on what `skill-adapter` will adapt, what it treats as out of scope, and when it will refuse an adaptation.

---

## What It Adapts

- **Tooling & Task Runners:** Maps foreign build, lint, and test commands to the tools discovered in your repository (e.g., `npm test` → `just test`, `cargo check`, or `uv run pytest`).
- **Repository Paths & File Conventions:** Updates paths to match your project's directory structure (`src/`, `app/`, `internal/`, schema files, migrations).
- **Framework & Component Idioms:** Translates component syntax and conventions to match your stack (e.g., React `useState` & Tailwind classes → Svelte 5 runes & scoped CSS), preserving the underlying validation rules (contrast, responsive viewports, accessibility).
- **Audience, Tone, & Project Rules:** Aligns documentation, PR notes, and review style with your repository's existing rules (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, or `.agents/rules/tone.md`).
- **Bundled Files & Multi-Skill Suites:** Audits bundled `references/` and `scripts/`, assigns explicit dispositions (`copy`, `adapt`, `inline`, `omit`), and scopes individual skills out of plugin suites (`plugin.json`, `hooks/`).
- **Collision Resolution:** Detects overlap with your existing project skills and proposes clean boundaries or explicit consolidation instead of silent overwrites.
- **Three-Way Re-Adaptation:** Merges upstream updates into previously adapted skills while preserving your existing local tool overrides via YAML frontmatter `metadata:`.

---

## What It Will NOT Adapt (Non-Goals)

- **No Placebo Skills (Missing Primitives):** When an essential capability is missing, `skill-adapter` explains the clash and discusses viable alternatives. If no safe, useful option is agreed, it reports the incompatibility rather than inventing a hollow skill.
- **No Silent Rule Alterations:** `skill-adapter` will never silently rewrite your repository's standing instruction files (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`). If an external skill carries repository-wide conventions, it recommends those additions in the Adaptation Brief for you to review and apply.
- **No Blind Code Execution:** `skill-adapter` never executes external scripts, hooks, or binaries during analysis. Gate 1 static scanning treats all source files as untrusted text.
- **No Unreviewed Executables:** Bundled scripts in `scripts/` are written with non-executable permissions (`0644`) by default. Executable permissions (`chmod +x`) require your explicit per-file confirmation.
- **No Full Codebase Transpilation:** `skill-adapter` adapts agent guidance, workflows, and inspection checklists. It is not an automated application porter or language transcompiler for third-party libraries.
