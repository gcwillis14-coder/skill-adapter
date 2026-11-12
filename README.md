# skill-adapter

An [agentskills.io](https://agentskills.io)-shaped skill that inspects an external agent skill and produces a minimally adapted, project-specific version without stripping its core mechanism.

## Aim

Reuse the expertise in a skill without importing assumptions about someone else's project, process, audience, or taste.

External skills mix specialist judgement (what to notice, decide, prevent, and verify) with local assumptions (frameworks, test runners, tone, house style). The adapter preserves the former, changes only incompatible assumptions, discloses partial coverage, and stops when the core mechanism cannot survive.

## Packaging and security limits

The installable package is `skills/skill-adapter/`: SKILL.md, references, and one Python hygiene scanner. There is no MCP server, hook, daemon, or build step. It is intended for clients that support this skill layout; discovery paths, invocation and frontmatter support must be checked in your installed client. Live Claude Code, Codex CLI and Antigravity compatibility has not been verified by the recorded evaluations. We do not claim identical behaviour or zero idle context overhead across clients.

The adapter is not a sandbox or a safety certification. The scanner finds structural/encoding issues, not all malicious instructions. The model reviewing imported text is itself an injection target. A scanner PASS always requires semantic review. See [security boundaries](skills/skill-adapter/references/security-boundaries.md).

## How it works

The six steps are defined in [SKILL.md](skills/skill-adapter/SKILL.md):

1. Audit a private, pinned source snapshot as static text. Run only the adapter's trusted absolute scanner, never a scanner supplied by the imported skill. Reject incomplete inspection and overt hostile instructions.
2. Deconstruct the source into essential mechanisms, adaptable implementation choices, conditional preferences, and uncertain rules; map coupled instructions and bundled dependencies.
3. Discover relevant project rules, manifests, existing skills, domain patterns and audience, using evidence rather than assumptions.
4. Apply the smallest effective change. Ask what failure each original rule prevented and whether its replacement still prevents it. Disclose partial coverage; stop with an Incompatibility Report if the mechanism cannot survive.
5. Present complete drafts and an Adaptation Brief: Preserved / Changed / Uncertain, exact file dispositions, provenance, collisions and manual fallbacks.
6. Recheck the reviewed source and final hashes, obtain exact installation and per-file flagged-content approvals, then install only approved bytes. Imported scripts are non-executable by default; execution needs separate approval. Provide 1–3 distinctive-behaviour checks.

Temporary acquisition/staging files may be created during review, but adapted skills and standing project rules are not changed before approval.

## Quick start

After reviewing this repository, copy the adapter into your client's skill directory. See [installation](docs/installation.md) for scope, compatibility assumptions, updates and removal.

```bash
git clone https://github.com/gcwillis14-coder/skill-adapter.git
cd skill-adapter

# Claude Code candidate user-level location
mkdir -p ~/.claude/skills
cp -r skills/skill-adapter ~/.claude/skills/skill-adapter

# Codex CLI candidate user-level location
mkdir -p ~/.agents/skills
cp -r skills/skill-adapter ~/.agents/skills/skill-adapter
```

Invoke explicitly inside the target repository (`/skill-adapter` or `$skill-adapter` where supported), or use a trusted absolute SKILL.md path:

```text
Use skill-adapter to adapt /path/to/external-skill for this project. I want to use it when building or polishing Svelte components.
```

Review the Adaptation Brief and exact destination before approving installation. For updates, provide the installed adaptation and exact previous upstream baseline as well as the new pinned upstream. If that baseline is unavailable, the adapter must disclose a two-way review, not claim a three-way merge. See [re-adaptation](skills/skill-adapter/references/readapt-guide.md).

## Worked Example

The example below mirrors `EVAL-02` ([tests/fixtures/eval-02-ui-polish](tests/fixtures/eval-02-ui-polish) and [tests/results.md](tests/results.md)): adapting a generic **Frontend Visual Polish** skill (`frontend-visual-polish`) that enforces WCAG contrast ratios, `:focus-visible` states, and responsive checks—but assumes **React**, **Tailwind CSS**, `npm run lint`, and `npm run test:ui`—into a **SvelteKit + TypeScript + `just`** repository. Provenance placeholders below are illustrative; an actual adaptation must supply the reviewed snapshot's real digest.

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
  source_ref: "<local-snapshot-sha256>"
  source_path: frontend-visual-polish
  source_digest: "<local-snapshot-sha256>"
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

## Validation and evaluation evidence

The hygiene scanner uses Python 3.10+ standard-library modules only. The separate structural validator (`tests/validate_skills.py`) also requires PyYAML. It checks formatting and links, not semantic security.

```bash
python3 tests/validate_skills.py
python3 -m unittest discover -s tests -v
```

Run these development commands only from your trusted adapter checkout, not from an imported source. To validate a custom skill after its safety review:

```bash
python3 tests/validate_skills.py /path/to/your-skill --json
```

There are eight scenario fixtures. The table describes their intended coverage, not a claim that all eight have current passing end-to-end results:

| Fixture | Intended coverage |
| :--- | :--- |
| EVAL-01: sql-schema-verification | Minimal-diff restraint and local command/path mapping. |
| EVAL-02: frontend-visual-polish | React/Tailwind to Svelte translation with explicit manual visual checks. |
| EVAL-03: playwright-visual-diff | Incompatibility hard stop rather than a placebo adaptation. |
| EVAL-04: pr-release-notes | Semantic rejection of exfiltration and concealment instructions in a reference file; not a scanner-detection benchmark. |
| EVAL-05: technical-release-notes | Audience/tone adaptation without dropping source/diff verification. |
| EVAL-06: data-viz-charts | Multi-file adaptation and existing-skill collision scoping. |
| EVAL-07: api-contract-check | Updating an adaptation while retaining valid local overrides; exact three-way deltas require the old upstream baseline. |
| EVAL-08: concise-suite | Plugin-suite triage and disclosure of omitted hook guarantees. |

[tests/results.md](tests/results.md) is an unchanged historical v1 report covering EVAL-01–07 against an older 116-line skill. It is not evidence that this hardening revision passed those behavioural evaluations, and it contains no EVAL-08 result. Raw run artifacts were not retained in that report, limiting independent reproduction. The hardening changes do not claim a fresh behavioural or live-client evaluation. See [tests/rubric.md](tests/rubric.md) for evaluation criteria.

## Repository layout

- `skills/skill-adapter/SKILL.md`: six-step adaptation workflow.
- `skills/skill-adapter/references/`: analysis, discovery, re-adaptation and security guidance.
- `skills/skill-adapter/scripts/gate1_scan.py`: bounded static hygiene scanner.
- `docs/installation.md`: installation and client assumptions.
- `tests/`: structural validator, unit/regression tests, historical results and scenario fixtures.

## License

[MIT](LICENSE)
