---
name: concise-dev
description: >
  Smallest complete change mode for any coding task (writing, fixing,
  refactoring, reviewing, choosing dependencies). Levels: lite, full (default).
---

# Concise Dev

Active for the whole session until the user says "stop concise-dev". Switch level with `/concise-dev lite|full`.

## Rules

1. Read callers, tests, and config before editing.
2. Reuse an existing codebase helper or standard-library feature; never add a dependency for a few lines.
3. Non-trivial logic leaves a unit test or assert-based check.
4. Never cut: boundary validation, security, accessibility, or real hardware calibration.
