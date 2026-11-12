---
name: playwright-visual-diff
description: Capture headless Chromium screenshots before and after UI changes and fail the task if pixel-diff thresholds exceed 0.5%.
---

# Playwright Visual Regression Loop

Prevent unintended visual regressions by comparing rendered DOM screenshots before and after every change.

## Mandatory Execution Loop

1. **Baseline Capture:** Start the local dev server and run `node scripts/capture-baseline.mjs --viewport=1280x800` to save PNG snapshots of target routes.
2. **Apply Code Changes:** Implement the requested layout or styling edits.
3. **Diff & Gate:** Run `node scripts/compare-snapshots.mjs --threshold=0.005`.
   - If `pixelmatch` reports greater than 0.5% diff outside intentional regions, inspect the generated `diff.png` artifact and fix layout shifts before completing the task.
   - Do not mark the task complete without a passing pixel-diff report.
