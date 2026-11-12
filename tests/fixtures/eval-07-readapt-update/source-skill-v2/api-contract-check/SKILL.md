---
name: api-contract-check
description: Verify HTTP API route signatures, response schemas, and backward compatibility before completing endpoint changes. Use when adding or modifying REST endpoints.
---

# API Contract Check

Ensure endpoint modifications preserve documented request/response contracts and catch breaking schema changes early.

## Workflow

1. **Inspect route definitions:** Read the router handlers and Pydantic response models before editing an endpoint.
2. **Verify error & status contracts:** Check [references/checks.md](references/checks.md) for required status codes and pagination invariants.
3. **Run API test suite:** Execute `pytest tests/api/` to verify endpoint contracts.
4. **Diff OpenAPI schema (v2):** Run `python scripts/export_openapi.py --diff` (or compare exported OpenAPI JSON against `openapi.json`) to detect breaking field removals or type changes.
