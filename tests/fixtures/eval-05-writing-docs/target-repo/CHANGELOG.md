# Changelog

## [Unreleased]

### Added
- `wirecheck diff --strict` exits with code `2` when required response fields are removed.

### Fixed
- `wirecheck validate` now rejects invalid `$ref` targets instead of silently skipping them.
