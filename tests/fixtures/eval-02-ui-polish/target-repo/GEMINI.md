# GEMINI.md

## Frontend Architecture

- Framework: SvelteKit + Svelte 5 runes (`$state`, `$props`, `$derived`) + TypeScript + MapLibre GL JS.
- Styling: Scoped `<style>` blocks in `.svelte` components using CSS custom properties from `src/app.css` (no Tailwind CSS, no React).
- Event handlers: Use Svelte 5 DOM attributes (`onclick={...}`, not `on:click` or React `onClick`).
- Task runner: Use `just check` and `just test` (no `test:ui` or Playwright runner is configured).
