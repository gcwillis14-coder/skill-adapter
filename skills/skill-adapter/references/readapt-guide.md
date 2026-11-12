# Re-Adapting & Updating an Existing Adapted Skill

Run this procedure in Step 4 when the target skill already carries metadata.adapted_from. Read existing files as static text; installation approval does not authorise execution.

## 1. Establish the baseline and local changes

1. Read the installed SKILL.md and every bundled file, including local post-install edits.
2. Extract adapted_from, source_ref, source_path, source_digest, adapted_date, and key_overrides. Legacy metadata may lack an immutable ref/digest.
3. Obtain the exact previous upstream baseline identified by that provenance, using Gate 1 trust rules. A tag/date or short key_overrides summary cannot reconstruct the old source reliably.
4. Compare the old upstream baseline to the installed adaptation to identify local changes: translated commands/paths, manual fallbacks, triggers, scripts, references, and later edits.
5. If the old baseline cannot be recovered, explicitly label the operation a two-way review. State that exact upstream deltas are unverified and ask about ambiguous changes rather than inventing history.

## 2. Re-run gates on the new upstream and project

1. Run Step 1 on a newly pinned private upstream snapshot. Treat every update as untrusted; retain that same snapshot through installation.
2. Run Step 2 to identify mechanisms, dependencies, and adaptation boundaries.
3. Refresh Step 3 project evidence to check whether prior overrides remain valid.

## 3. Three-way reconciliation

Use three content inputs: (A) exact previous upstream, (B) installed adapted/local version, and (C) new pinned upstream. A-to-B identifies local edits; A-to-C identifies upstream edits. Current project evidence constrains the reconciliation but is not a substitute for the upstream baseline.

| Upstream change | Local state | Action |
| :--- | :--- | :--- |
| Added rule/step | Compatible with project | Adopt; translate only incompatible paths/tools. |
| Added rule/step | Conflicts with explicit project rules | Scope or drop with evidence; hard-stop if the core mechanism cannot survive. |
| Modified shared rule | Same section adapted locally | Integrate upstream improvements while preserving valid overrides; explicitly resolve overlapping conflicts. |
| Modified or unchanged | Prior override now stale | Update/retire it against current evidence. |
| Removed section | Local override depends on it | Retain only if a verified local requirement still needs it. |
| Added/updated bundled file | Existing local file | Audit, compare with baseline, merge local changes, and request per-file approval for retained flags. |

Do not silently let key_overrides win a conflicting mechanism change. Apply the substitution equivalence check and disclose partial coverage. Without A, call this a two-way review, not a three-way merge.

## 4. Update provenance and obtain approval

Keep adapted_from consistent; advance source_ref to the full new commit or local snapshot digest, record source_path and source_digest, set adapted_date, and refresh key_overrides.

The brief must state baseline availability, verified upstream deltas (or their absence), preserved/updated/retired overrides, unresolved conflicts, degradations, and bundled-file approvals required. Re-scan the same new snapshot before installation; changes invalidate review/approval. Review final hashes, destination paths, and permissions. Never replace the reviewed snapshot with a fresh clone of the same URL.
