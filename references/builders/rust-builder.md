# Rust Builder

Use this reference for systems tools, high-performance CLI utilities, WebAssembly targets, and any workflow where safety, speed, and zero-cost abstractions matter.

## Use It For

- Command-line tools and automation scripts that need native performance
- File processing utilities (parsing, transforming, compressing large files)
- WebAssembly (WASM) modules for browser or serverless edge environments
- Systems components, embedded firmware (with `no_std`)
- Network tools, protocol implementations, and proxies
- Replacing unsafe shell scripts with a memory-safe compiled alternative
- High-throughput data pipelines where Python or Node are bottlenecks

## Default Approach

- Use **Rust stable** (current release). Pin a minimum version in `rust-toolchain.toml` when needed.
- Use **`cargo`** for all project management — no alternative build tool needed.
- Use **`clap`** for CLI argument parsing.
- Use **`serde`** with `serde_json` or `csv` for data serialization.
- Prefer `anyhow` or `thiserror` for error handling — avoid `unwrap()` and `expect()` in non-test production paths.
- Use `tokio` for async I/O when networking or concurrency is needed.

## Project Structure

```
my-tool/
  Cargo.toml
  Cargo.lock        ← commit this for binaries
  src/
    main.rs         ← entry point
    lib.rs          ← library code (if applicable)
    commands/
    models/
  tests/
    integration_test.rs
```

## Quality Bar

- Run `cargo clippy -- -D warnings` as part of CI — Clippy catches many correctness issues.
- Run `cargo fmt --check` for consistent formatting.
- No `unwrap()` in library code — return `Result<T, E>` and let the caller decide.
- Use `#[derive(Debug)]` on all structs and enums.
- Prefer `PathBuf` over `String` for filesystem paths.
- Use `BufReader`/`BufWriter` for line-by-line file processing — never read entire large files into memory with `read_to_string`.

## Safety And Practicality

- Rust's borrow checker prevents most memory safety bugs at compile time — explain borrow errors rather than working around them with `clone()`.
- Avoid `unsafe` blocks unless genuinely necessary (FFI, intrinsics). Every `unsafe` block needs a comment explaining the invariant being upheld.
- For subprocess execution, use `std::process::Command` with an argument list — never construct shell strings.

## What To Deliver

- Provide `Cargo.toml` with exact dependency versions.
- Provide the exact `cargo build --release` command and where the binary lands (`target/release/my-tool`).
- Explain any system-level dependencies (OpenSSL, libz, etc.) and how to install them.
- Mention cross-compilation targets if the user is building for a different platform.

## Deep References

Load these when the task is non-trivial:

- [../patterns/rust-patterns.md](../patterns/rust-patterns.md) — Cargo skeleton, `clap` CLI derive macro, `anyhow`/`thiserror` error handling, `serde` JSON/CSV, `tokio` async, `BufReader` file processing, safe `Command` execution, anti-patterns.
