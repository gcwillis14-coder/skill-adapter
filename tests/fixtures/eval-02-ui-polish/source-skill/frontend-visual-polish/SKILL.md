---
name: frontend-visual-polish
description: Audit and refine UI components for visual hierarchy, WCAG contrast, keyboard accessibility, and responsive layout before completing frontend tasks.
---

# Frontend Visual Polish

Ensure every new or modified UI component meets baseline visual, accessibility, and responsive standards.

## Rules

1. **Contrast & Legibility:** Maintain at least a 4.5:1 contrast ratio for body text and 3:1 for large text and interactive boundaries. Do not rely on color alone to convey status.
2. **Interactive States:** Every clickable element must define explicit `:hover`, `:focus-visible`, and disabled states. Use semantic `<button>` and `<a>` elements rather than `onClick` handlers on `<div>` tags.
3. **Responsive Layout:** Verify component layout at 375px (mobile) and 1280px (desktop) viewports without horizontal overflow.
4. **Implementation Pattern (React + Tailwind):**
   - Prefer Tailwind utility classes (`focus-visible:ring-2`, `sr-only`) over custom CSS files.
   - Manage interactive state with `useState` and keep presentational props typed via TypeScript interfaces.
5. **Verification:** Run `npm run lint` and `npm run test:ui` before finishing.
