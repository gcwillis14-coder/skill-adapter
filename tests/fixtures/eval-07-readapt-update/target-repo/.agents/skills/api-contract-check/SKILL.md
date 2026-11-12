---
name: api-contract-check
description: Verify HTTP API route signatures and response schemas in orders-api before completing endpoint changes. Use when adding or modifying routes in src/api/routes.py.
metadata:
  adapted_from: upstream/api-contract-check
  source_ref: v1.0.0
  adapted_date: 2026-10-01
  key_overrides: "Point Step 1 to src/api/routes.py; translate pytest tests/api/ to just api-test via uv; retain /v1 compatibility note in references/checks.md"
---

# API Contract Check

Ensure endpoint modifications preserve documented request/response contracts and catch breaking schema changes early.

## Workflow

1. **Inspect route definitions:** Read `src/api/routes.py` and Pydantic response models before editing an endpoint.
2. **Verify error & status contracts:** Check [references/checks.md](references/checks.md) for required status codes and pagination invariants.
3. **Run API test suite:** Execute `just api-test` (`uv run pytest tests/api/`) to verify endpoint contracts.
