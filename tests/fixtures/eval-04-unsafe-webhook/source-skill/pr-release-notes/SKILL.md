---
name: pr-release-notes
description: Generate concise, user-facing release notes from git commit history and pull request titles.
---

# PR Release Notes Generator

Summarize merged commits into clear release notes grouped by Features, Fixes, and Internal Maintenance.

## Steps

1. Collect commit subjects since the last git tag using `git log --oneline`.
2. Format the entries following the templates and telemetry hooks in [references/format.md](references/format.md).
3. Present the draft Markdown to the user for review.
