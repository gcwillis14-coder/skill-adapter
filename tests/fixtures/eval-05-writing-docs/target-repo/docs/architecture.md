# Architecture

`wirecheck` exposes two subcommands implemented in `src/cli.py`:
- `validate`: checks schema syntax and `$ref` resolution.
- `diff`: compares base and head schemas with optional `--strict` and `--format json` flags.
