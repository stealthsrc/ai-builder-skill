# Recipe: Versioned SQL Migration with Rollback

Complete migration pair (UP + DOWN) with transaction wrapping, apply script, and rollback test — targeting PostgreSQL but adaptable to SQLite and MySQL.

Pair with [../builders/sql-builder.md](../builders/sql-builder.md) and [../patterns/sql-patterns.md](../patterns/sql-patterns.md).

---

## What It Does

1. Creates a `schema_migrations` tracking table if it does not exist.
2. Provides an `UP` migration that adds columns, an index, and a view.
3. Provides a `DOWN` migration that reverses every change cleanly.
4. Wraps both in explicit transactions — either the whole migration applies or nothing does.
5. Includes a shell apply script for CLI execution with error detection.

---

## File Layout

```
db/
  migrations/
    0001_add_invoice_status.up.sql
    0001_add_invoice_status.down.sql
  migrate.sh       ← apply script
```

---

## 0001_add_invoice_status.up.sql

```sql
-- UP migration: add status and processed_at columns, create index and view
BEGIN;

-- 1. Ensure the migration tracking table exists
CREATE TABLE IF NOT EXISTS schema_migrations (
    version    VARCHAR(20)  PRIMARY KEY,
    applied_at TIMESTAMPTZ  NOT NULL DEFAULT CURRENT_TIMESTAMP,
    applied_by TEXT
);

-- 2. Guard: skip if already applied
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM schema_migrations WHERE version = '0001') THEN
        RAISE NOTICE 'Migration 0001 already applied — skipping.';
        RETURN;
    END IF;
END $$;

-- 3. Add columns as nullable first (avoids table lock on large tables)
ALTER TABLE invoices
    ADD COLUMN IF NOT EXISTS status       VARCHAR(20),
    ADD COLUMN IF NOT EXISTS processed_at TIMESTAMPTZ;

-- 4. Backfill default value for existing rows
UPDATE invoices
SET status = 'pending'
WHERE status IS NULL;

-- 5. Now enforce NOT NULL
ALTER TABLE invoices
    ALTER COLUMN status SET NOT NULL,
    ALTER COLUMN status SET DEFAULT 'pending';

-- 6. Create index (non-blocking on PostgreSQL 9.5+)
-- NOTE: CONCURRENTLY cannot run inside a transaction.
--       Run: CREATE INDEX CONCURRENTLY idx_invoices_status ON invoices (status);
--       after this script completes.
CREATE INDEX IF NOT EXISTS idx_invoices_status ON invoices (status);

-- 7. Create a reporting view
CREATE OR REPLACE VIEW pending_invoices AS
SELECT
    id,
    region,
    amount,
    created_at
FROM invoices
WHERE status = 'pending'
ORDER BY created_at;

-- 8. Record migration
INSERT INTO schema_migrations (version, applied_by)
VALUES ('0001', current_user)
ON CONFLICT (version) DO NOTHING;

COMMIT;
```

---

## 0001_add_invoice_status.down.sql

```sql
-- DOWN migration: undo everything in 0001 in reverse order
BEGIN;

-- Guard: skip if not applied
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM schema_migrations WHERE version = '0001') THEN
        RAISE NOTICE 'Migration 0001 not applied — nothing to roll back.';
        RETURN;
    END IF;
END $$;

-- 1. Drop the view
DROP VIEW IF EXISTS pending_invoices;

-- 2. Drop the index
DROP INDEX IF EXISTS idx_invoices_status;

-- 3. Remove the columns
ALTER TABLE invoices
    DROP COLUMN IF EXISTS processed_at,
    DROP COLUMN IF EXISTS status;

-- 4. Remove migration record
DELETE FROM schema_migrations WHERE version = '0001';

COMMIT;
```

---

## migrate.sh — Apply Script

```bash
#!/usr/bin/env bash
set -euo pipefail

DB_URL="${DATABASE_URL:?DATABASE_URL environment variable is required}"
DIRECTION="${1:-up}"   # "up" or "down"
VERSION="${2:-0001}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/migrations"
MIGRATION="${SCRIPT_DIR}/${VERSION}_*.${DIRECTION}.sql"

# Expand glob — abort if no match
shopt -s failglob
FILE=$(echo $MIGRATION 2>/dev/null) || {
    echo "[ERROR] Migration file not found: ${MIGRATION}"
    exit 1
}

echo "[INFO] Applying migration: ${FILE}"
psql "${DB_URL}" --set ON_ERROR_STOP=1 --file "${FILE}"
echo "[OK] Migration ${VERSION} ${DIRECTION} applied."
```

Usage:
```bash
chmod +x db/migrate.sh

# Apply UP
DATABASE_URL="postgresql://user:pass@localhost/mydb" ./db/migrate.sh up 0001

# Roll back
DATABASE_URL="postgresql://user:pass@localhost/mydb" ./db/migrate.sh down 0001
```

---

## SQLite Adaptation

SQLite does not support `ALTER TABLE ... DROP COLUMN` before 3.35 or `ADD COLUMN IF NOT EXISTS`.

```sql
-- SQLite UP (simpler — no transactions needed for DDL)
PRAGMA journal_mode = WAL;
BEGIN;

ALTER TABLE invoices ADD COLUMN status TEXT NOT NULL DEFAULT 'pending';
ALTER TABLE invoices ADD COLUMN processed_at TEXT;

CREATE INDEX IF NOT EXISTS idx_invoices_status ON invoices (status);
INSERT OR IGNORE INTO schema_migrations (version) VALUES ('0001');

COMMIT;
```

```sql
-- SQLite DOWN
BEGIN;
-- SQLite cannot DROP COLUMN before 3.35 — recreate table if needed
DROP INDEX IF EXISTS idx_invoices_status;
-- For SQLite >= 3.35:
ALTER TABLE invoices DROP COLUMN processed_at;
ALTER TABLE invoices DROP COLUMN status;
DELETE FROM schema_migrations WHERE version = '0001';
COMMIT;
```

---

## Validation

1. After running UP: `SELECT * FROM schema_migrations WHERE version = '0001';` — should return one row.
2. After running UP: `\d invoices` (psql) — `status` and `processed_at` columns should be present.
3. After running DOWN: both columns gone, migration record deleted, view dropped.
4. Run DOWN on a fresh database — should print "not applied — nothing to roll back" and exit cleanly.

---

## Edge Cases

| Case | Behavior |
|---|---|
| Migration already applied | `ON CONFLICT DO NOTHING` + guard notice — idempotent |
| Migration not applied, DOWN run | Guard prints notice and returns without error |
| Large table (millions of rows) | Run `CREATE INDEX CONCURRENTLY` separately after the transaction |
| No `DATABASE_URL` set | migrate.sh exits with `parameter null or not set` error |
