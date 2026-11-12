# Source Skill Analysis Template

Complete every section in Step 2 before inspecting the target repository. Ground every entry in exact source lines.

## 1. Identity & Provenance

- **Skill Name:** `<name from YAML frontmatter>`
- **Origin:** `<URL, repository path, or local directory>`
- **Version / Ref:** `<full Git commit SHA or local snapshot SHA-256; tag/date only as extra labels>`
- **Source Path / Digest:** `<selected subdirectory and scanner snapshot_sha256>`
- **Review Scope / Manifest:** `<audited files, per-file hashes/permissions, excluded root Git metadata, governing suite files>`
- **Bundled Assets:** `<list files under references/, scripts/, examples/, resources/, assets/, or "None">`

## 2. Purpose, Trigger Audit & Behavioral Expertise Lens

- **Target Outcome:** `<1 sentence: what failure mode or task quality does this skill improve?>`
- **Invocation Mode & Description Quality:** `<model-invoked | user-invoked; assess length (<=1024 chars), trigger precision, <500 lines, <=1-level links>`
- **Trigger Boundaries:** `<Activate when ... | Exclude when ...>`
- **Notice (specialist attention):** `<what signals, smells, or edge cases the skill trains the agent to spot>`
- **Decide (judgement between options):** `<trade-offs or branching choices the skill governs>`
- **Do / Sequence (workflow dependencies):** `<ordered steps or gates that structure execution>`
- **Prevent (safeguards):** `<specific failure modes or regressions each constraint blocks>`
- **Verify (good-enough bar):** `<how completion quality and correctness are established>`
- **Rationale Provenance:** `<tag key rules as explicit author rationale | inferred | unexplained/unsupported absolute>`

## 3. Four-Category Instruction Classification

| Instruction / Rule | Classification | Condition / Dependency / Rationale |
| :--- | :--- | :--- |
| `<e.g., Inspect schema before writing queries>` | **Essential mechanism** (Keep) | `<Prevents hallucinated columns; independent of SQL dialect>` |
| `<e.g., Run tests with npm test>` | **Adaptable implementation choice** (Translate) | `<Assumes Node/npm; map to verified project test runner>` |
| `<e.g., Always wrap tables in collapsible sections>` | **Conditional judgement / preference** (Scope/Drop) | `<Adds value when ...; reflects foreign taste/process when ...>` |
| `<e.g., Unexplained "always limit to 3 bullets">` | **Uncertain** (Flag & Probe) | `<Rationale unstated; preserve provisionally or test without>` |

## 4. Hard Requirements, Coupled Chains & Bundled Files

- **Required Tools / Runtimes:** `<CLIs, MCP servers, browsers, compilers, or APIs assumed by the skill>`
- **Coupled Instruction Chains:** `<list each chain by type: input dependency (B consumes A's output) | post-transformation check (C validates B) | conditional safety (guard tied to earlier branch)>`
- **Adaptation Boundaries:** `<core gates or invariants required to keep the skill effective>`

| Bundled File Path | Role in Skill | External Dependencies | Planned Disposition |
| :--- | :--- | :--- | :--- |
| `<e.g., scripts/render.py>` | `<Generates chart PNGs>` | `<Python 3, matplotlib>` | `<copy | adapt | inline | omit>` |
| `<e.g., references/style.md>` | `<Chart color & label rules>` | `<None>` | `<copy | adapt | inline | omit>` |
