---
name: technical-release-notes
description: Draft user-facing release notes and documentation updates from verified git commits and code diffs. Use when preparing a release changelog, feature announcement, or docs refresh.
---

# Technical Release Notes & Docs

Ground every release note and documentation update in verified code changes rather than commit titles alone.

## Workflow

1. **Inspect actual changes:** Compare the target diff or commit range against modified source files, CLI flags, and public APIs so every claim reflects implemented behavior.
2. **Follow audience and voice rules:** Apply the formatting and tone guidance in [references/style-guide.md](references/style-guide.md).
3. **Link issue trackers:** Attach Jira ticket IDs (`PROJ-123`) and a customer-success summary paragraph at the top of each release entry.
4. **Verify links and commands:** Confirm every documented file path, CLI flag, and internal Markdown link resolves in the repository before finishing.
