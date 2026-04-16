# TypeScript Node.js Builder

Use this reference for CLI scripts, lightweight APIs, file automation, Discord bots, and vibe-coding workflows that need more than a browser page but less than a full backend framework.

## Use It For

- CLI tools and one-shot automation scripts
- Small REST APIs or webhook receivers (Express, Hono, Fastify)
- CSV, JSON, Excel, and file processing pipelines
- Discord, Slack, or Teams bots
- Scheduled jobs and cron-like scripts
- Node-native tools like scrapers, sitemaps, and report generators
- Cross-platform automation that runs on Windows, Mac, or Linux without PowerShell

## Default Approach

- Default to **TypeScript** with `tsx` for direct execution (`npx tsx script.ts`) — no compile step needed for scripts.
- Use Node 18 LTS or later. Prefer ESM (`"type": "module"` in package.json) for new projects.
- Keep scripts self-contained with a visible configuration block at the top.
- Use `commander` for non-trivial CLIs with multiple flags.
- Load secrets from environment variables with `dotenv` — never hard-code credentials.

## Project Setup

Minimal script setup:

```
package.json     – name, version, type: module, scripts, dependencies
tsconfig.json    – strict: true, target: ES2022, moduleResolution: bundler
script.ts        – the entry point
.env.example     – document expected env vars (never commit .env)
```

For an API:

```
src/
  index.ts       – server entry point
  routes/        – route handlers
  lib/           – shared utilities
```

## Quality Bar

- Use `strict: true` in tsconfig — no `any` escapes unless unavoidable.
- Validate external input (CLI args, API bodies, env vars) before use.
- Prefer `async`/`await` over callback chains.
- Always handle promise rejections — unhandled rejections crash Node 18+.
- Close DB connections, file handles, and HTTP servers cleanly.

## Safety And Practicality

- Load secrets from `process.env` with `.env` via `dotenv` — never from the command line where they appear in process lists.
- Use `child_process.execFile` (not `exec`) when running external commands to avoid shell injection.
- Validate and sanitize all user-supplied or external input before using it in filesystem paths, SQL, or HTML.
- Cap memory use for large file pipelines by using streams rather than loading entire files into buffers.

## What To Deliver

- Provide `package.json` with exact dependency versions.
- Provide `tsconfig.json` if the project is non-trivial.
- Provide the exact command to install and run (`npm install && npx tsx script.ts`).
- Explain environment variable setup and what each var controls.
- Include a quick validation path such as a `--dry-run` flag or test input.

## Deep References

Load these when the task is non-trivial:

- [../patterns/typescript-node-patterns.md](../patterns/typescript-node-patterns.md) — package.json + tsconfig skeleton, `commander` CLI pattern, `async`/`await` error handling, CSV with `fast-csv`, HTTP client with retry, `dotenv` secrets, safe `execFile`, stream processing, anti-patterns.
- [../recipes/node-api-csv.md](../recipes/node-api-csv.md) — TypeScript CLI that reads a CSV, calls a REST API per row, and writes enriched results to a new CSV with progress reporting.
