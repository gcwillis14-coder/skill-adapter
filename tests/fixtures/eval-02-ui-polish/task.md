# EVAL-02: Partial Conflict (Tooling Translation + Honest Flagging)

## Source Skill
`source-skill/frontend-visual-polish/`

## Target Repository
`target-repo/` (SvelteKit + Svelte 5 runes + scoped `<style>` + `just`)

## Adapter Assertions
- **Decision:** Proceed to adaptation (passes Gate 1 and Gate 2 with Degradable Flag).
- **Mechanism Preservation:** Keeps 4.5:1 / 3:1 contrast, `:hover`/`:focus-visible`/disabled states, semantic `<button>`/`<a>` HTML, and 375px/1280px responsive check.
- **Framework Translation:** Replaces React `useState` / `onClick` and Tailwind utilities (`focus-visible:ring-2`, `sr-only`) with Svelte 5 `$state`/`$props`, `onclick`, and scoped `<style>` CSS.
- **Command Translation:** Replaces `npm run lint` and `npm run test:ui` with `just check` and `just test`.
- **Honest Flagging:** Explicitly flags that no automated `test:ui` / browser viewport runner exists in `package.json` or `justfile`, documenting manual 375px/1280px verification as a fallback.

## Downstream Representative Task
> Audit and fix `src/lib/components/FilterPanel.svelte` for accessibility, contrast, interactive states, and responsive behavior, and state what checks were run or must be done manually.

### Expected Downstream Lift
- **No Skill:** May fix the `<div onclick>` or leave contrast/focus-visible/375px unchecked.
- **Unadapted Original Skill:** Suggests Tailwind classes (`focus-visible:ring-2`), React `useState`, or `npm run test:ui` which fails in this SvelteKit repo.
- **Adapted Skill:** Fixes `<div class="toggle">` to semantic `<button>`, improves `#9aa0a6` low-contrast text on `#ffffff`, adds `:hover`/`:focus-visible`/disabled scoped CSS, uses Svelte 5 idioms, runs/cites `just check` and `just test`, and explicitly flags manual 375px/1280px viewport verification.
