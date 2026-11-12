---
name: sql-schema-verification
description: Verify relational database schemas and query execution plans before writing or modifying SQL queries. Use when authoring analytical queries, migrations, or data extraction scripts.
---

# SQL Schema Verification

Never write SQL against assumed table or column names. Ground every query in verified schema definitions and execution plans.

## Workflow

1. **Inspect actual schema definitions:** Read the repository's DDL files, ORM models, or migration history before writing any `SELECT`, `JOIN`, or `WHERE` clause.
2. **Verify column types and nullability:** Confirm join keys share compatible types and check whether nullable columns require `COALESCE` or explicit `IS NOT NULL` filters.
3. **Check query plan:** Run a read-only `EXPLAIN` (never `EXPLAIN ANALYZE` on mutating statements) against a local or staging database if available to verify index usage and avoid full table scans on large tables.
4. **Flag unverified assumptions:** If live database access is unavailable, explicitly list which table/column names were verified from code versus assumed.
