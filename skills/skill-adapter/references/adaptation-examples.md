# Adaptation examples

These redacted accounts are reconstructed from three adaptation runs in a static portfolio project. They summarize the conversations rather than quote them verbatim. Names and paths are generalized. They are examples of the process, not automated tests or guarantees of future behavior. None of the runs verified live skill discovery or invocation.

The target project was a personal portfolio served as static HTML, CSS and minimal JavaScript, with no build step. Its instructions favored concise, grounded copy and prohibited adding a frontend framework or build tools. It already had project-local skills, including one covering copy and visual design.

## Local writing skill

**User:** Adapt a local writing skill for this project.

**What the adapter found:** The incoming `SKILL.md` described a detailed process for identifying formulaic prose while preserving the writer's meaning and voice. Its frontmatter was readable, and the file was 498 lines long. It was supplied as a standalone file, so the adapter could not establish whether the original package included additional files.

The project's existing copy and design skill also covered generic wording. The incoming skill added a more detailed sentence-level editing process, but both could apply to the same copy. The project's standing instructions would still take precedence. The adapter flagged the overlap, though it could have explained more clearly when to use each skill.

**Changes proposed:**

- Prose-review behavior → unchanged: no project-specific substitution was needed.
- Source metadata → added: record the inspected file and its digest.
- Six blank lines → removed: make room for metadata while staying below the adapter's 500-line limit.

**Review and outcome:** The adapter presented the draft and its destination. The user approved, and the file was installed project-locally. Structural validation passed at 496 lines. The run did not demonstrate how the two writing skills work together or whether the installed skill is discovered and invoked.

## Git repository: website jury

**User:** Adapt a website scoring skill from a Git repository.

**What the adapter found:** The source contained a scoring workflow, two reference files and four scripts. It expected screenshots and browser measurements before scoring, and used a separate critic or a disclosed self-score. It also proposed building a local project before serving it.

The target was already a static site, so serving its existing files directly was a plausible project-specific replacement for the build step. Node was present, but project-local Playwright and axe-core were not found. The browser-based measurements therefore could not be assumed available.

The adapter also identified two side effects to address before use: the screenshot script can delete PNG files in its chosen output directory, and it can fetch axe-core from a CDN. A scanner flagged a base64-like string that was identified as an integrity hash for that download. The flag alone did not establish safety; the complete bundle audit was unfinished when the run stopped.

**Choice presented:**

1. Preserve browser-based scoring, with separately approved tool setup and a fresh, isolated output directory.
2. Discuss a manual review, explicitly identifying the automated measurements and evidence it would lack.
3. Stop the adaptation.

**Outcome:** The user chose to stop. No draft was approved, and the jury skill was neither installed nor run. In particular, the manual option was not claimed to produce an equivalent score.

## Git subdirectory: re-explanation skill

**User:** Adapt an explicitly invoked skill that re-explains the previous answer.

**What the adapter found:** The incoming skill asked the agent to re-explain its last answer with context, simpler technical English and the project's glossary. It was explicitly invoked, with that setting present in both its skill file and agent configuration.

The initial project search found no glossary. The adapter proposed making glossary use conditional rather than inventing project terminology or claiming a glossary existed.

**Changes proposed:**

- Require `GLOSSARY.md` → use it when available: accommodate the current project while retaining its purpose when a glossary exists.
- Explicit invocation → preserved: the installed skill should remain user-invoked on clients that honor the setting.
- Source agent configuration → copied: keep its display name and invocation policy.

**Review and outcome:** The user approved the two-file draft. Installation and structural validation passed; live discovery and invocation were not tested. The adapter missed a useful question: whether to create a glossary as a separate, approved project change, rather than merely making it optional. Creating one would need its own scope and approval.
