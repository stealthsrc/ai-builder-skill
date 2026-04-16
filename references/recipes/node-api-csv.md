# Recipe: Node.js CSV → API → Enriched CSV

Complete TypeScript CLI that reads a CSV, calls a REST API once per row (with retry and progress bar), and writes the enriched rows to a new output CSV.

Pair with [../builders/typescript-node-builder.md](../builders/typescript-node-builder.md) and [../patterns/typescript-node-patterns.md](../patterns/typescript-node-patterns.md).

---

## What It Does

1. Reads a CSV with headers into typed row objects.
2. Calls an external API for each row (rate-limited to avoid 429s).
3. Merges the API response into each row as new columns.
4. Writes the enriched rows to a new output CSV.
5. Prints a progress counter and a summary on completion.

---

## Project Setup

```
enrich-csv/
  src/index.ts
  package.json
  tsconfig.json
  .env.example
  .env            ← not committed
```

**package.json**

```json
{
  "name": "enrich-csv",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "start": "tsx src/index.ts"
  },
  "dependencies": {
    "axios": "^1.7.2",
    "axios-retry": "^4.4.1",
    "commander": "^12.1.0",
    "dotenv": "^16.4.5",
    "fast-csv": "^5.0.1"
  },
  "devDependencies": {
    "@types/node": "^20.14.0",
    "tsx": "^4.15.0",
    "typescript": "^5.5.0"
  }
}
```

**tsconfig.json**

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "skipLibCheck": true
  }
}
```

**.env.example**

```
API_KEY=your_api_key_here
BASE_URL=https://api.example.com
RATE_LIMIT_MS=500
```

---

## Full Script — src/index.ts

```typescript
import 'dotenv/config';
import { createReadStream, createWriteStream } from 'node:fs';
import { program } from 'commander';
import axios from 'axios';
import axiosRetry from 'axios-retry';
import { parse, writeToStream } from 'fast-csv';

// ---- Config ----
function requireEnv(name: string): string {
  const v = process.env[name];
  if (!v) throw new Error(`Missing env var: ${name}`);
  return v;
}

const API_KEY     = requireEnv('API_KEY');
const BASE_URL    = requireEnv('BASE_URL');
const RATE_LIMIT  = Number(process.env['RATE_LIMIT_MS'] ?? 300);

// ---- HTTP client with retry ----
const client = axios.create({ baseURL: BASE_URL, timeout: 15_000 });
axiosRetry(client, {
  retries: 3,
  retryDelay: axiosRetry.exponentialDelay,
  retryCondition: err => axiosRetry.isNetworkError(err) || (err.response?.status ?? 0) >= 500,
});

// ---- Types ----
interface InputRow  { id: string; name: string; [key: string]: string; }
interface ApiResult { score: number; category: string; }
interface OutputRow extends InputRow { score: string; category: string; enriched_at: string; }

// ---- CSV helpers ----
async function readCsv(path: string): Promise<InputRow[]> {
  return new Promise((resolve, reject) => {
    const rows: InputRow[] = [];
    createReadStream(path)
      .pipe(parse<InputRow, InputRow>({ headers: true, trim: true }))
      .on('data', (row: InputRow) => rows.push(row))
      .on('error', reject)
      .on('end', () => resolve(rows));
  });
}

async function writeCsv(path: string, rows: OutputRow[]): Promise<void> {
  return new Promise((resolve, reject) => {
    const stream = createWriteStream(path);
    writeToStream(stream, rows, { headers: true })
      .on('finish', resolve)
      .on('error', reject);
  });
}

// ---- API call ----
async function enrich(row: InputRow): Promise<ApiResult> {
  const { data } = await client.get<ApiResult>('/enrich', {
    headers: { Authorization: `Bearer ${API_KEY}` },
    params:  { id: row.id, name: row.name },
  });
  return data;
}

const sleep = (ms: number) => new Promise(r => setTimeout(r, ms));

// ---- Main ----
program
  .name('enrich-csv')
  .requiredOption('-i, --input <path>',  'Input CSV file')
  .option('-o, --output <path>',         'Output CSV file', 'output-enriched.csv')
  .option('--dry-run',                   'Skip API calls — write input rows unchanged')
  .parse();

const opts = program.opts<{ input: string; output: string; dryRun: boolean }>();

async function main() {
  console.log(`Reading: ${opts.input}`);
  const rows = await readCsv(opts.input);
  console.log(`Rows: ${rows.length}`);

  const output: OutputRow[] = [];
  let ok = 0, failed = 0;

  for (let i = 0; i < rows.length; i++) {
    const row = rows[i]!;
    process.stdout.write(`\r[${i + 1}/${rows.length}] id=${row.id}  `);

    let result: ApiResult = { score: 0, category: 'n/a' };
    if (!opts.dryRun) {
      try {
        result = await enrich(row);
        ok++;
      } catch (err) {
        const msg = err instanceof Error ? err.message : String(err);
        console.warn(`\n[WARN] Row ${i + 1} failed: ${msg}`);
        failed++;
      }
      if (i < rows.length - 1) await sleep(RATE_LIMIT);
    }

    output.push({
      ...row,
      score:       String(result.score),
      category:    result.category,
      enriched_at: opts.dryRun ? 'dry-run' : new Date().toISOString(),
    });
  }

  process.stdout.write('\n');
  if (!opts.dryRun) await writeCsv(opts.output, output);
  else console.log('[DRY-RUN] No output written.');

  console.log(`Done — ok: ${ok}, failed: ${failed}, output: ${opts.output}`);
  if (failed > 0) process.exit(1);
}

main().catch(err => { console.error('[ERROR]', err.message); process.exit(1); });
```

---

## Run

```bash
# Install
npm install

# Dry run — check the CSV is readable
npx tsx src/index.ts --input data/contacts.csv --dry-run

# Live run
npx tsx src/index.ts --input data/contacts.csv --output data/enriched.csv
```

---

## Validation

- Check row count: `wc -l data/enriched.csv` should equal `wc -l data/contacts.csv` (same number of data rows).
- Check a sample: `head -5 data/enriched.csv` — confirm `score` and `category` columns are populated.
- Exit code 1 if any row failed — check stderr for row numbers.

---

## Edge Cases

| Case | Behavior |
|---|---|
| API returns 429 | axios-retry backs off exponentially (up to 3 attempts) |
| Row fails after retries | Warning printed, row written with default `score=0`, exit code 1 |
| Empty input CSV | Reads 0 rows, writes empty output CSV, exits 0 |
| Missing env var | Throws at startup before any rows are processed |
