# Re-Adapting & Updating an Existing Adapted Skill

Run this procedure in Step 4 when the target skill directory already exists and carries `metadata.adapted_from` in its `SKILL.md` frontmatter.

## 1. Inspect the Installed Adapted Skill

1. Read the existing `SKILL.md` and every file in its `references/` and `scripts/` subdirectories.
2. Extract frontmatter `metadata:` fields:
   - `adapted_from`: upstream skill name or URL
   - `source_ref`: previously adapted version, tag, commit SHA, or date
   - `adapted_date`: date of the previous adaptation
   - `key_overrides`: recorded local stack, command, and fallback overrides
3. List every local difference from a generic skill (translated commands, scoped paths, manual fallbacks, custom triggers, adapted scripts/references).

## 2. Re-Run Gates on the Updated Upstream & Repo

1. Run **Step 1 (Gate 1)** static-text safety review on the new upstream directory first—treat every upstream update as untrusted until verified.
2. Run **Step 2** source analysis on the new upstream version to identify added, modified, and removed instructions or bundled files.
3. Refresh **Step 3** discovery against the current repository state to verify whether each prior local override still matches Tier 1–3 evidence.

## 3. Three-Way Reconciliation Rules

Reconcile **(A) Previous adapted skill + `key_overrides`**, **(B) New upstream source**, and **(C) Current repository evidence**:

| Upstream Change | Local Override State | Action |
| :--- | :--- | :--- |
| **Added rule / step** | Compatible with repo | Adopt the new step; translate any generic commands/paths to verified local equivalents. |
| **Added rule / step** | Conflicts with Tier 1 rule | Drop or make conditional; document the conflict in the brief. |
| **Modified shared rule** | Active `key_override` in same section | Keep the local stack override while integrating genuine upstream improvements to the core mechanism. |
| **Modified or unchanged** | Prior override now stale (repo changed) | Update or retire the override to match current Tier 1–3 evidence. |
| **Removed section** | Dependent local override exists | Retain only if a verified local rule still requires it; otherwise drop cleanly. |
| **Added / updated bundled file** | Exists in `references/` or `scripts/` | Audit safety (Step 1), merge local adaptations if modified locally, or copy if compatible. |

## 4. Update Provenance & Adaptation Brief

- Update frontmatter `metadata:` in the draft:
  - Keep `adapted_from` consistent.
  - Advance `source_ref` to the new upstream ref/date and `adapted_date` to today's date.
  - Refresh `key_overrides` to reflect the active set of local overrides.
- Include an **Upstream Delta & Override Preservation** subsection in the Step 5 Adaptation Brief listing:
  1. What changed upstream since the previous `source_ref`.
  2. Which local `key_overrides` were preserved, updated, or retired.
  3. Any newly introduced degradations or bundled-file updates requiring confirmation.
