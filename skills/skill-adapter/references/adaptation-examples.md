# Adaptation examples

These shortened, redacted summaries are reconstructed from three real adaptation runs in a static portfolio project. They illustrate decisions, not automated tests or guarantees of future behavior. Names and paths are generalized. The runs did not verify live skill discovery or invocation.

## Local writing skill

**User:** Adapt a local writing skill for this project.

**Adapter:** The skill reviews prose for formulaic writing. The project already has an adjacent copy and design skill; its project rules take precedence. The imported skill provides a more detailed sentence-level editing process, so their triggers may overlap.

**Changes:** Original behavior → unchanged → the project did not require a behavioral substitution. Added provenance and removed blank lines to stay below the length limit. The standalone file was inspected; any unprovided companion files could not be verified.

**Outcome:** The user approved installation. Structural validation passed; actual use was not tested. A clearer explanation of the overlap would have improved the review.

## Git repository: website jury

**User:** Adapt a website scoring skill from a Git repository.

**Adapter:** The project is served as static files, while the skill expects a production build. Serving those files directly could replace the build step. The project has no local Playwright or axe-core installation, and the source can fetch a library and delete PNGs in its output directory.

**Decision:** Preserve browser-based measurements with separately approved tool setup and isolated output; discuss a limited manual review with its missing coverage; or stop. A scanner flag corresponded to an integrity hash, not a semantic safety verdict; the full bundle audit remained incomplete.

**Outcome:** The user chose to stop. No jury skill was installed or run.

## Git subdirectory: re-explanation skill

**User:** Adapt an explicitly invoked skill that re-explains the previous answer.

**Adapter:** Source → adapted: use the project glossary → use it when available. The project had no glossary in the initial search. The explicit invocation mode and agent configuration were preserved.

**Outcome:** The user approved installation and structural validation passed. Live discovery and invocation were not tested. The adapter missed an opportunity to offer a separate, user-approved glossary creation task; making glossary use optional was not equivalent to creating one.
