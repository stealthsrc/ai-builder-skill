# Rust Patterns

Load this reference when the task requires more than a trivial Rust program. It provides reusable idioms for CLI tools, error handling, file processing, HTTP, and async with Tokio.

Pair with [../builders/rust-builder.md](../builders/rust-builder.md) for routing context.

---

## 1. Cargo Skeleton

```toml
# Cargo.toml
[package]
name    = "my-tool"
version = "0.1.0"
edition = "2021"

[dependencies]
clap     = { version = "4", features = ["derive"] }
anyhow   = "1"
serde    = { version = "1", features = ["derive"] }
serde_json = "1"
csv      = "1"

[profile.release]
lto    = true
strip  = true
```

Build: `cargo build --release && ./target/release/my-tool`

---

## 2. clap CLI with Derive Macro

```rust
use clap::Parser;
use std::path::PathBuf;

#[derive(Parser, Debug)]
#[command(name = "my-tool", about = "Process CSV and generate a report")]
struct Cli {
    /// Input CSV file
    #[arg(short, long)]
    input: PathBuf,

    /// Output JSON file
    #[arg(short, long, default_value = "report.json")]
    output: PathBuf,

    /// Preview without writing output
    #[arg(short, long)]
    dry_run: bool,
}

fn main() -> anyhow::Result<()> {
    let cli = Cli::parse();
    if !cli.input.exists() {
        anyhow::bail!("Input file not found: {}", cli.input.display());
    }
    run(&cli)
}
```

---

## 3. anyhow Error Handling

```rust
use anyhow::{Context, Result};
use std::fs;

fn read_config(path: &str) -> Result<String> {
    fs::read_to_string(path)
        .with_context(|| format!("Failed to read config: {path}"))
}

// Propagate with ? — the ? operator converts any error to anyhow::Error
fn run(cli: &Cli) -> Result<()> {
    let config = read_config("config.toml")?;
    let rows   = read_csv(&cli.input)?;
    // ...
    Ok(())
}
```

For library crates, use `thiserror` to define typed error enums instead of `anyhow`.

---

## 4. CSV Read and Write

```rust
use csv::{Reader, Writer};
use serde::{Deserialize, Serialize};

#[derive(Debug, Deserialize, Serialize)]
struct Invoice {
    id:     String,
    region: String,
    amount: f64,
}

fn read_csv(path: &std::path::Path) -> anyhow::Result<Vec<Invoice>> {
    let mut rdr = Reader::from_path(path)?;
    let invoices: Vec<Invoice> = rdr.deserialize().collect::<Result<_, _>>()?;
    Ok(invoices)
}

fn write_csv(path: &std::path::Path, invoices: &[Invoice]) -> anyhow::Result<()> {
    let mut wtr = Writer::from_path(path)?;
    for inv in invoices { wtr.serialize(inv)?; }
    wtr.flush()?;
    Ok(())
}
```

---

## 5. Buffered File Processing

Never read large files with `fs::read_to_string`. Use `BufReader` for line-by-line streaming.

```rust
use std::io::{BufRead, BufReader};
use std::fs::File;

fn count_lines(path: &std::path::Path) -> anyhow::Result<usize> {
    let file   = File::open(path)?;
    let reader = BufReader::new(file);
    let count  = reader.lines().count();
    Ok(count)
}
```

---

## 6. Tokio Async HTTP Client

```rust
// Cargo.toml: tokio = { version = "1", features = ["full"] }, reqwest = { version = "0.12", features = ["json"] }
use reqwest::Client;
use serde::Deserialize;

#[derive(Deserialize)]
struct ApiResponse { score: f64 }

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let client = Client::builder()
        .timeout(std::time::Duration::from_secs(15))
        .build()?;

    let resp: ApiResponse = client
        .get("https://api.example.com/score")
        .bearer_auth(std::env::var("API_KEY")?)
        .send()
        .await?
        .error_for_status()?
        .json()
        .await?;

    println!("Score: {}", resp.score);
    Ok(())
}
```

---

## 7. Safe Subprocess Execution

```rust
use std::process::Command;

fn run_git(args: &[&str]) -> anyhow::Result<String> {
    let output = Command::new("git")
        .args(args)
        .output()?;

    if !output.status.success() {
        let stderr = String::from_utf8_lossy(&output.stderr);
        anyhow::bail!("git failed: {}", stderr.trim());
    }
    Ok(String::from_utf8(output.stdout)?.trim().to_string())
}

// ✓ Argument list — no shell injection
let branch = run_git(&["rev-parse", "--abbrev-ref", "HEAD"])?;
```

---

## 8. Anti-Patterns

| Anti-pattern | Problem | Fix |
|---|---|---|
| `.unwrap()` in production code | Panic with no context on `None` or `Err` | `?` operator with `anyhow` or `.context("...")` |
| `unwrap()` on env var | Panic if variable missing | `std::env::var("KEY").context("API_KEY not set")?` |
| `fs::read_to_string` on large file | OOM for multi-GB files | `BufReader` + line iteration |
| `unsafe` without a comment | Safety invariant undocumented | Add `// SAFETY:` comment explaining the invariant |
| `.clone()` everywhere | Hides ownership problems | Rethink ownership or use references |
| Blocking `std::thread::sleep` in async | Blocks the executor | `tokio::time::sleep(duration).await` |
| String-based subprocess with user input | Shell injection | `Command::new("cmd").args([...])` — never `sh -c "cmd {input}"` |
