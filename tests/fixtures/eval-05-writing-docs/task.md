# EVAL-05: Technical Writing / Release Notes Adaptation (Audience & Tone)

## Source Skill
`source-skill/technical-release-notes/` (includes `references/style-guide.md`)

## Target Repository
`target-repo/` (Open-source engineering CLI `wirecheck` with `GEMINI.md`, `.agents/rules/tone.md`, `CHANGELOG.md`, `docs/architecture.md`)

## Adapter Assertions
- **Decision:** Proceed to adaptation (passes Gate 1 and Gate 2).
- **Mechanism Preservation:** Retains diff/symbol/command verification before drafting and link/path verification before finishing.
- **Audience & Tone Adaptation:** Drops SaaS marketing hype, customer-success blurbs, Jira `PROJ-123` requirements, and SaaS dashboard upgrade callouts; adapts both `SKILL.md` and `references/style-guide.md` (or omits/inlines replaced guide) to match `.agents/rules/tone.md` and `CHANGELOG.md` headings (`### Added`, `### Changed`, `### Fixed`, `### Breaking`).
- **Standing-Rule Boundary:** Reads `GEMINI.md` and `.agents/rules/tone.md` without modifying them silently.
- **Provenance & Budget:** Stores `metadata:` provenance in frontmatter; keeps relative links `<= 1` level deep and `SKILL.md < 500` lines.

## Downstream Representative Task
> Draft a `CHANGELOG.md` entry under `## [Unreleased]` for adding `--format json` to `wirecheck diff` (matching `docs/architecture.md`) and fixing exit code handling on missing files.

### Expected Downstream Lift
- **No Skill:** May write generic prose or miss verifying `docs/architecture.md` flags/links.
- **Unadapted Original Skill:** Adds a marketing "Highlights" paragraph, omits exact CLI flags/module names per original `style-guide.md`, or invents `PROJ-123` Jira links and a SaaS dashboard callout.
- **Adapted Skill:** Verifies `--format json` against `docs/architecture.md`, writes terse factual entries under `### Added` / `### Fixed` matching `CHANGELOG.md` and `.agents/rules/tone.md`, and checks links/paths without marketing fluff or Jira placeholders.
