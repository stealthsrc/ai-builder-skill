# TypeScript Node.js Patterns

Load this reference when the task requires more than a simple Node script. It provides reusable idioms and anti-patterns for CLI tools, lightweight APIs, and file-processing pipelines.

Pair with [../builders/typescript-node-builder.md](../builders/typescript-node-builder.md) for routing context and with [../rules/security-baseline.md](../rules/security-baseline.md) when the script handles secrets, external APIs, or user-supplied file paths.

---

## 1. Project Skeleton

Minimal `package.json` and `tsconfig.json` for a TypeScript script that runs with `tsx`.

```json
// package.json
{
  "name": "my-tool",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "start": "tsx src/index.ts",
    "build": "tsc --noEmit"
  },
  "dependencies": {
    "dotenv": "^16.4.5"
  },
  "devDependencies": {
    "@types/node": "^20.14.0",
    "tsx": "^4.15.0",
    "typescript": "^5.5.0"
  }
}
```

```json
// tsconfig.json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "skipLibCheck": true,
    "outDir": "dist"
  },
  "include": ["src"]
}
```

Run: `npm install && npx tsx src/index.ts`

---

## 2. Commander CLI Pattern

Use `commander` for scripts with multiple options or subcommands.

```typescript
import { program } from 'commander';
import 'dotenv/config';

program
  .name('my-tool')
  .description('Process CSV files and call an API.')
  .requiredOption('-i, --input <path>', 'Input CSV file')
  .option('-o, --output <path>', 'Output CSV file', 'output.csv')
  .option('--dry-run', 'Preview without writing output', false)
  .option('-v, --verbose', 'Verbose logging', false)
  .parse();

const opts = program.opts<{
  input: string;
  output: string;
  dryRun: boolean;
  verbose: boolean;
}>();
```

---

## 3. Async Error Handling

Wrap the main entry point in a top-level `try/catch` that prints a friendly message and exits with a non-zero code.

```typescript
async function main(): Promise<void> {
  // ... work ...
}

main().catch((err: unknown) => {
  const message = err instanceof Error ? err.message : String(err);
  console.error('[ERROR]', message);
  process.exit(1);
});
```

Never use `.catch(console.error)` alone — it exits 0 and masks failures in CI.

---

## 4. CSV Read and Write with fast-csv

```typescript
import { parse, writeToPath } from 'fast-csv';
import { createReadStream } from 'node:fs';

interface Row { id: string; amount: string; }

async function readCsv(filePath: string): Promise<Row[]> {
  return new Promise((resolve, reject) => {
    const rows: Row[] = [];
    createReadStream(filePath)
      .pipe(parse<Row, Row>({ headers: true, trim: true }))
      .on('data', row => rows.push(row))
      .on('error', reject)
      .on('end', () => resolve(rows));
  });
}

async function writeCsv(filePath: string, rows: Row[]): Promise<void> {
  await new Promise<void>((resolve, reject) => {
    writeToPath(filePath, rows, { headers: true })
      .on('finish', resolve)
      .on('error', reject);
  });
}
```

---

## 5. HTTP Client with Retry

Use `axios` with `axios-retry` for resilient external API calls.

```typescript
import axios from 'axios';
import axiosRetry from 'axios-retry';

const client = axios.create({ timeout: 10_000 });
axiosRetry(client, {
  retries: 3,
  retryDelay: axiosRetry.exponentialDelay,
  retryCondition: err =>
    axiosRetry.isNetworkError(err) || (err.response?.status ?? 0) >= 500,
});

async function callApi(url: string, apiKey: string): Promise<unknown> {
  const { data } = await client.get(url, {
    headers: { Authorization: `Bearer ${apiKey}` },
  });
  return data;
}
```

---

## 6. Secrets from Environment

Load with `dotenv` at the top of the entry point. Validate presence before use.

```typescript
import 'dotenv/config';

function requireEnv(name: string): string {
  const value = process.env[name];
  if (!value) throw new Error(`Missing required environment variable: ${name}`);
  return value;
}

const API_KEY = requireEnv('API_KEY');
const BASE_URL = requireEnv('BASE_URL');
```

Provide an `.env.example` file that lists every variable with a description but no real values.

---

## 7. Safe Child Process Execution

Prefer `execFile` over `exec` to prevent shell injection. Always validate command and arguments.

```typescript
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';

const execFileAsync = promisify(execFile);

async function runGit(args: string[]): Promise<string> {
  const { stdout } = await execFileAsync('git', args, { cwd: process.cwd() });
  return stdout.trim();
}

// ✓ Safe: argument list, no shell interpolation
const branch = await runGit(['rev-parse', '--abbrev-ref', 'HEAD']);

// ✗ Unsafe: never build a shell string with user input
// exec(`git checkout ${userInput}`);
```

---

## 8. Stream Processing for Large Files

Never read a large file entirely into memory. Use Node streams or `readline` for line-by-line processing.

```typescript
import { createReadStream } from 'node:fs';
import { createInterface } from 'node:readline';

async function processLargeFile(filePath: string): Promise<number> {
  const rl = createInterface({
    input: createReadStream(filePath),
    crlfDelay: Infinity,
  });
  let count = 0;
  for await (const line of rl) {
    if (line.trim()) count++;
  }
  return count;
}
```

---

## 9. Path Safety

Always resolve paths before using them in filesystem operations. Prevent directory traversal from user-supplied inputs.

```typescript
import { resolve, relative } from 'node:path';

function safePath(baseDir: string, userInput: string): string {
  const resolved = resolve(baseDir, userInput);
  if (!resolved.startsWith(resolve(baseDir))) {
    throw new Error(`Path traversal rejected: ${userInput}`);
  }
  return resolved;
}
```

---

## 10. Anti-Patterns

| Anti-pattern | Problem | Fix |
|---|---|---|
| `require('child_process').exec(cmd)` with user input | Shell injection | `execFile` with argument array |
| `process.env.KEY` without validation | Silent `undefined` causes cryptic errors | `requireEnv()` guard at startup |
| `fs.readFileSync` on large files | OOM risk | `createReadStream` + `readline` |
| `any` type on API response | Hides shape errors at compile time | Define an interface, use `z.parse()` with zod if shape is untrusted |
| Unhandled promise in `.on('error')` | Process crash without meaningful message | Always wire `.on('error', reject)` in stream pipelines |
| Hard-coded absolute paths | Breaks on other machines | `path.resolve(__dirname, '..', 'data')` or config from env |
