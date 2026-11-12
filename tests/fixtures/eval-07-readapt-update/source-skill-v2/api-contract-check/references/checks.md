# API Contract Checks

- Success responses must preserve existing top-level JSON keys.
- Breaking changes require a versioned route prefix (`/v2/...`).
- **OpenAPI check (v2):** Verify every response model produces a valid OpenAPI schema without untyped `Any` payloads.
