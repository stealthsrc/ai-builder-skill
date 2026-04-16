# SQL Patterns

Load this reference when the task requires more than a trivial SQL query. It provides reusable idioms for safe queries, migrations, window functions, CTEs, and performance hints.

Pair with [../builders/sql-builder.md](../builders/sql-builder.md) for routing context and with [../rules/security-baseline.md](../rules/security-baseline.md) for any migration that touches production data.

---

## 1. Safe SELECT with CTE

Use CTEs (`WITH`) for multi-step logic. Prefer explicit column lists over `SELECT *`.

```sql
-- ✓ Explicit columns + CTE for clarity
WITH recent_orders AS (
    SELECT
        order_id,
        customer_id,
        region,
        amount,
        order_date
    FROM orders
    WHERE order_date >= CURRENT_DATE - INTERVAL '30 days'
      AND status = 'completed'
),
regional_totals AS (
    SELECT
        region,
        COUNT(*)        AS order_count,
        SUM(amount)     AS total_revenue,
        AVG(amount)     AS avg_amount
    FROM recent_orders
    GROUP BY region
)
SELECT *
FROM regional_totals
ORDER BY total_revenue DESC;
```

---

## 2. Window Functions

Use window functions for running totals, ranks, and row comparisons without self-joins.

```sql
-- Running total per region
SELECT
    order_id,
    region,
    amount,
    SUM(amount) OVER (PARTITION BY region ORDER BY order_date) AS running_total,
    RANK()      OVER (PARTITION BY region ORDER BY amount DESC) AS rank_in_region,
    LAG(amount) OVER (PARTITION BY region ORDER BY order_date) AS prev_amount
FROM orders
WHERE status = 'completed';
```

---

## 3. Safe UPDATE and DELETE

Always preview affected rows with a SELECT before running a destructive mutation.

```sql
-- Step 1: preview what will change
SELECT id, status, amount
FROM orders
WHERE status = 'pending' AND order_date < CURRENT_DATE - INTERVAL '90 days';

-- Step 2: after confirming the preview, run the UPDATE
UPDATE orders
SET
    status     = 'expired',
    updated_at = CURRENT_TIMESTAMP
WHERE status = 'pending'
  AND order_date < CURRENT_DATE - INTERVAL '90 days';

-- Step 3 (alternative): wrap in a transaction for safety
BEGIN;
UPDATE orders
SET status = 'expired'
WHERE status = 'pending' AND order_date < CURRENT_DATE - INTERVAL '90 days';
-- Inspect: SELECT COUNT(*) FROM orders WHERE status = 'expired';
COMMIT;  -- or ROLLBACK if the count looks wrong
```

---

## 4. Safe Migration Skeleton (UP + DOWN)

Always write both the UP migration (forward) and the DOWN migration (rollback).

```sql
-- migration_0001_add_invoice_status.up.sql
BEGIN;

ALTER TABLE invoices
    ADD COLUMN status       VARCHAR(20) NOT NULL DEFAULT 'pending',
    ADD COLUMN processed_at TIMESTAMPTZ;

CREATE INDEX idx_invoices_status ON invoices (status);

-- Record migration (if not using a migration tool)
INSERT INTO schema_migrations (version, applied_at)
VALUES ('0001', CURRENT_TIMESTAMP);

COMMIT;
```

```sql
-- migration_0001_add_invoice_status.down.sql
BEGIN;

DROP INDEX IF EXISTS idx_invoices_status;

ALTER TABLE invoices
    DROP COLUMN IF EXISTS processed_at,
    DROP COLUMN IF EXISTS status;

DELETE FROM schema_migrations WHERE version = '0001';

COMMIT;
```

---

## 5. Adding a NOT NULL Column to a Large Table

Never add a `NOT NULL` column with a backfill default in a single step — it locks the entire table on most databases.

```sql
-- PostgreSQL safe pattern (three steps)

-- Step 1: add as nullable with a server-side default
ALTER TABLE orders ADD COLUMN priority SMALLINT DEFAULT 1;

-- Step 2: backfill in small batches (prevents lock escalation)
-- Run this in a loop until 0 rows updated
UPDATE orders
SET priority = 1
WHERE priority IS NULL
LIMIT 10000;

-- Step 3: after all rows are populated, add the NOT NULL constraint
ALTER TABLE orders ALTER COLUMN priority SET NOT NULL;
ALTER TABLE orders ALTER COLUMN priority DROP DEFAULT;
```

---

## 6. Index Creation (Non-Blocking)

On PostgreSQL, use `CREATE INDEX CONCURRENTLY` to avoid locking reads during index build.

```sql
-- Standard (locks the table for writes during build — OK for small tables)
CREATE INDEX idx_orders_region ON orders (region);

-- Concurrent (no write lock — takes longer but safe on production tables)
CREATE INDEX CONCURRENTLY idx_orders_region_status
    ON orders (region, status)
    WHERE status != 'completed';
```

---

## 7. EXPLAIN ANALYZE

Check query performance before shipping. Look for `Seq Scan` on large tables — they indicate missing indexes.

```sql
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT region, SUM(amount)
FROM orders
WHERE status = 'completed' AND order_date >= '2025-01-01'
GROUP BY region;
```

Fix sequential scans by adding an index on the filtered columns. Re-run `EXPLAIN ANALYZE` to confirm improvement.

---

## 8. Parameterized Query Usage (Application Code)

SQL from application code must always use parameterized queries. These placeholders differ by database client:

| Database / Driver | Placeholder |
|---|---|
| SQLite (Python) | `?` |
| PostgreSQL (psycopg2) | `%s` or `%(name)s` |
| PostgreSQL (asyncpg) | `$1`, `$2` |
| MySQL (PyMySQL) | `%s` |
| SQL Server (pyodbc) | `?` |
| JDBC (Java) | `?` |

```python
# Python + SQLite — always pass values as a tuple
cursor.execute(
    "SELECT * FROM orders WHERE region = ? AND amount > ?",
    ("West", 1000.0)
)

# ✗ Never build SQL strings with user input
# cursor.execute(f"SELECT * FROM orders WHERE region = '{user_region}'")
```

---

## 9. Anti-Patterns

| Anti-pattern | Problem | Fix |
|---|---|---|
| `SELECT *` in production queries | Fragile — breaks when schema changes; wastes network | Explicit column list |
| Multi-step migration without transaction | Partial migration leaves DB in bad state | Wrap in `BEGIN`/`COMMIT` |
| `DROP TABLE` without `IF EXISTS` | Error on clean schemas | `DROP TABLE IF EXISTS` |
| `ALTER TABLE ADD COLUMN NOT NULL` with backfill | Full table lock | Three-step: add nullable → backfill → add constraint |
| String concatenation in application SQL | SQL injection | Parameterized queries |
| No rollback (`DOWN`) migration | Cannot recover from failed deploy | Always write both UP and DOWN |
| `TRUNCATE` without confirming target | Destroys data instantly, no WHERE clause | Preview with `SELECT COUNT(*)` first |
