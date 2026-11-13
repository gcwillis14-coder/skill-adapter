# skill-adapter

> Customise and adapt external agent skills to your project's stack, tools, and rules—without stripping the reason you're adding it in the first place.

An [agentskills.io](https://agentskills.io)-compatible skill that inspects an external agent skill, audits it for safety and architectural fit against your repository, and produces a clean, project-specific adaptation.

See [SCOPE.md](SCOPE.md) for what `skill-adapter` adapts and our explicit non-goals.

---

## Why Standalone Skill Packaging

`skill-adapter` ships as a standalone skill directory (`skills/skill-adapter/`) rather than a native plugin bundle:

- **Follows `agentskills.io`:** Simple directory layout (`SKILL.md` + `references/` + `scripts/`) requiring no background services, daemons, or compile steps.
- **Tested & Verified:** Tested and confirmed in **OpenAI Codex CLI** and **Google Antigravity**.
- **Untested Community Targets:** Built on open standards, so it should work in **Claude Code**, **Cursor**, **Windsurf**, **GitHub Copilot**, and **OpenCode**—untested; please open an issue if you encounter friction. Installation in a supported-looking directory does not guarantee that a client will discover or invoke a skill.
- **Zero Idle Overhead:** Declares `disable-model-invocation: true` so it never consumes context tokens until you explicitly invoke it.

---

## Quick Start

### 1. Install `skill-adapter`

#### Tested Clients

```bash
# OpenAI Codex CLI / shared .agents/skills
mkdir -p ~/.agents/skills && cp -r skills/skill-adapter ~/.agents/skills/skill-adapter

# Google Antigravity (global)
mkdir -p ~/.gemini/config/skills && cp -r skills/skill-adapter ~/.gemini/config/skills/skill-adapter
```

#### Untested Clients (Should Work — Open an Issue)

```bash
# Claude Code
mkdir -p ~/.claude/skills && cp -r skills/skill-adapter ~/.claude/skills/skill-adapter

# Cursor
mkdir -p ~/.cursor/skills && cp -r skills/skill-adapter ~/.cursor/skills/skill-adapter

# Windsurf
mkdir -p ~/.codeium/windsurf/skills && cp -r skills/skill-adapter ~/.codeium/windsurf/skills/skill-adapter

# GitHub Copilot (VS Code)
mkdir -p ~/.copilot/skills && cp -r skills/skill-adapter ~/.copilot/skills/skill-adapter
```

Or install via `npx skills`:

```bash
npx skills add https://github.com/gcwillis14-coder/skill-adapter
```

See [docs/installation.md](docs/installation.md) for detailed paths, symlink guidance, and project-local setup.

---

### 2. Invoke Inside Your Target Repository

Run `skill-adapter` via command or prompt:

```text
Use skill-adapter to adapt /path/to/external-skill for this project. I want to use it when building or polishing Svelte components.
```

### 3. Review the Adaptation Brief

`skill-adapter` runs in six steps (defined in [skills/skill-adapter/SKILL.md](skills/skill-adapter/SKILL.md)). It presents the complete draft and asks for your approval before installation, even if you requested installation:

1. **Gate 1 (Static Hygiene Audit):** Inspects source files as untrusted text for safety and filesystem issues. A lightweight format check follows; neither format validation nor a scanner PASS is a semantic safety verdict.
2. **Source Skill Deconstruction:** Identifies what the skill helps an agent notice, decide, do, prevent, and verify.
3. **Project Discovery:** Reads repository rules (`AGENTS.md`, `GEMINI.md`, `CLAUDE.md`), configs, and toolchains using a strict evidence hierarchy.
4. **Gate 2 (Fit & Boundary Audit):** Checks fit and collisions, proposes alternatives for capability clashes, and asks before changing meaningful coverage.
5. **Draft Adapted Skill & Adaptation Brief:** Presents the complete draft, destination, changes and limitations for your review and installation approval.
6. **Verified Installation:** After approval, installs project-locally by default, checks the result proportionately, and explains invocation and whether discovery was verified. Bundled scripts default to non-executable `0644`.

---

## Worked Example

Adapting a generic **Frontend Visual Polish** skill (`frontend-visual-polish`)—which enforces WCAG contrast ratios, `:focus-visible` states, and responsive checks, but assumes **React**, **Tailwind CSS**, and `npm run test:ui`—into a **SvelteKit + TypeScript + `just`** repository:

### 1. Adaptation Brief Output

- **Source contribution:** Enforces baseline accessibility (4.5:1 body text contrast, 3:1 large text/boundaries, semantic `<button>`/`<a>` elements, explicit `:hover`/`:focus-visible`/`:disabled` states) and 375px/1280px responsive overflow checks.
- **Project needs:** Per `GEMINI.md`, `package.json`, and `justfile`, this project uses SvelteKit with Svelte 5 runes, TypeScript, scoped `<style>` blocks (no React, no Tailwind), and `just check` / `just test` for verification.
- **Summary of changes:**
  - *Preserved:* Contrast thresholds (4.5:1 / 3:1), interactive state requirements, semantic elements, and 375px/1280px viewport checks.
  - *Changed:* Translated React `useState`/`onClick` and Tailwind classes to Svelte 5 runes (`$state`, `$derived`, `$props()`), native `onclick={...}`, and scoped `<style>` CSS; mapped `npm run lint` / `npm run test:ui` to `just check` and `just test`.
  - *Uncertain:* Exact `375px` / `1280px` breakpoint constants lack author rationale and are preserved provisionally alongside a manual browser check.
- **Trade-offs & manual fallbacks:** This repository has no automated headless visual test runner (`test:ui`/Playwright absent). Responsive checks at 375px/1280px remain manual browser verification steps in `npm run dev`.

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

---

## Example Scenarios

The repository includes eight concrete input/output scenarios in [tests/fixtures/](tests/fixtures/) illustrating how `skill-adapter` handles diverse repository constraints:

| Scenario | Input & Project Context | Expected Adaptation Behavior |
| :--- | :--- | :--- |
| **[eval-01-sql-verification](tests/fixtures/eval-01-sql-verification)** | SQL verification skill in a matching Python/PostgreSQL repo | **Minimal pass:** Keeps ~90% of phrasing verbatim; maps only `uv run` and project model paths. |
| **[eval-02-ui-polish](tests/fixtures/eval-02-ui-polish)** | React/Tailwind visual polish skill in a SvelteKit repo | **Partial conflict & fallback:** Preserves accessibility checks while translating idioms and disclosing manual fallbacks. |
| **[eval-03-playwright-visual](tests/fixtures/eval-03-playwright-visual)** | Chromium visual diff skill in a headless Python CLI repo | **Unadaptable hard stop (Gate 2):** Refuses adaptation with an Incompatibility Report instead of generating a placebo. |
| **[eval-04-unsafe-webhook](tests/fixtures/eval-04-unsafe-webhook)** | Skill concealing environment exfiltration in references | **Security rejection (Gate 1):** Halts on suspicious payload without executing untrusted code. |
| **[eval-05-writing-docs](tests/fixtures/eval-05-writing-docs)** | SaaS marketing release-notes skill in a terse OSS repo | **Audience & tone adaptation:** Preserves diff verification while matching local `tone.md` conventions. |
| **[eval-06-charts-multifile](tests/fixtures/eval-06-charts-multifile)** | Multi-file skill overlapping an existing local reporting skill | **Bundle triage & collision resolution:** Adapts scripts and references; scopes boundaries cleanly with existing skills. |
| **[eval-07-readapt-update](tests/fixtures/eval-07-readapt-update)** | Upstream v2 release of a previously adapted skill | **Re-adaptation:** Merges upstream changes while preserving local project overrides via YAML `metadata:`. |
| **[eval-08-plugin-suite](tests/fixtures/eval-08-plugin-suite)** | Full plugin bundle with multiple skills and hooks | **Suite triage:** Scopes individual target skill, discloses omitted hook capabilities, and tightens triggers. |

---

## Validating Skill Layout

To verify any skill against `agentskills.io` structural requirements (frontmatter, length, and relative links):

```bash
python3 tests/validate_skills.py /path/to/your-skill
```

---

## Repository Structure

```text
skill-adapter/
├── README.md
├── SCOPE.md
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
    └── fixtures/
```

---

## License

[MIT](LICENSE)
