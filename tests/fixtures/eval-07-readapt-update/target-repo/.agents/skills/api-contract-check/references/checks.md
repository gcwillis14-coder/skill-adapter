# API Contract Checks

- Success responses must preserve existing top-level JSON keys.
- Breaking changes require a versioned route prefix (`/v2/...`), keeping `/v1` routes backward-compatible.
