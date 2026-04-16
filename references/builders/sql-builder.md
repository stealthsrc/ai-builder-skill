# SQL Builder

Use this reference for standalone SQL work: schema migrations, complex reporting queries, database cleanup scripts, index tuning, and any task where SQL itself is the primary deliverable — not a Python or Node wrapper around it.

## Use It For

- Schema migrations (CREATE TABLE, ALTER TABLE, DROP COLUMN)
- Reporting queries: CTEs, window functions, aggregations, ranked results
- Data cleanup and normalization scripts
- Index analysis and creation
- Stored procedures and views
- Ad-hoc data exploration and auditing queries
- Database maintenance scripts (VACUUM, ANALYZE, REINDEX)
- Parameterized queries for safe application use

## Database Targets

| Database | Notes |
|---|---|
| **SQLite** | Default for local/embedded use. File-based, zero setup. |
| **PostgreSQL** | Default for production web apps and analytics. |
| **MySQL / MariaDB** | Common in legacy stacks and WordPress environments. |
| **SQL Server (T-SQL)** | Windows enterprise, Azure SQL Database. |
| **DuckDB** | In-process analytics; queries CSV and Parquet files directly. |

State the target database — syntax differs for window functions, date handling, string functions, and LIMIT/TOP.

## Default Approach

- Write ANSI SQL by default unless a database-specific feature is required.
- Use CTEs (`WITH`) for multi-step logic — avoid nested subqueries beyond one level.
- Always use parameterized placeholders (`?`, `$1`, `@param`) in queries meant for application use — never string interpolation.
- Prefer explicit column lists over `SELECT *` in production queries.
- For destructive operations (DELETE, DROP, TRUNCATE), lead with a SELECT that shows affected rows before commenting out or executing the mutation.

## Migration Safety Rules

- Wrap migrations in a transaction when the database supports transactional DDL (PostgreSQL, SQLite).
- Always write a rollback (`DOWN`) migration alongside the forward (`UP`) migration.
- For large tables: use `ADD COLUMN … DEFAULT NULL` first (never a non-null default with backfill in a single step — it locks the table).
- Test on a copy or a staging database before running on production.

## What To Deliver

- State the target database and version.
- Provide the exact SQL script ready to run.
- For migrations: provide both `UP` and `DOWN` scripts.
- Explain what the query or migration does and what rows or schema it affects.
- Provide the CLI command to run the script (`sqlite3 db.sqlite < script.sql`, `psql -d mydb -f script.sql`, etc.).

## Deep References

Load these when the task is non-trivial:

- [../patterns/sql-patterns.md](../patterns/sql-patterns.md) — SELECT with CTEs, window functions, safe UPDATE and DELETE patterns, safe migration skeleton, index creation, EXPLAIN ANALYZE, parameterized query usage, anti-patterns.
- [../recipes/sql-migration.md](../recipes/sql-migration.md) — versioned migration pair (UP + DOWN) with transaction wrapping, rollback test, and apply script.
