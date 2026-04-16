# Go Builder

Use this reference for CLI tools, REST APIs, microservices, file processing utilities, and automation scripts that benefit from Go's fast compilation, single-binary output, and strong concurrency model.

## Use It For

- Command-line tools with fast startup and single-binary distribution
- REST APIs and gRPC services
- File and data processing pipelines
- Web scrapers and automation scripts
- Docker-based microservices
- Cloud-native tooling (Kubernetes operators, CI helpers)
- Cross-platform binaries that work on Linux, macOS, and Windows without a runtime

## Default Approach

- Target **Go 1.22+** for new projects.
- Use **`cobra`** for non-trivial CLIs with subcommands; use `flag` or `os.Args` for simple single-command tools.
- Use the **standard library** (`net/http`, `encoding/json`, `encoding/csv`) before reaching for third-party packages.
- Load secrets from environment variables — never hard-code credentials.
- Return errors explicitly — never `panic` in library code.
- Use `context.Context` as the first argument to any function that does I/O, network calls, or long-running work.

## Project Structure

```
my-tool/
  go.mod
  go.sum
  main.go          ← thin entry point
  cmd/
    root.go        ← cobra root command
    run.go
  internal/
    processor/
    client/
  Makefile         ← build, lint, test targets
```

## Quality Bar

- Run `go vet ./...` and `staticcheck ./...` (or `golangci-lint`) in CI.
- All exported functions, types, and package-level variables must have doc comments.
- Use `io.Reader`/`io.Writer` interfaces for functions that process streams — makes them testable.
- Never ignore an error: `if err != nil { return fmt.Errorf("context: %w", err) }`.
- Use `%w` in `fmt.Errorf` to wrap errors so callers can `errors.Is` and `errors.As`.

## Safety And Practicality

- Use `exec.Command` with an argument list (not a shell string) for subprocesses.
- Validate and sanitize path inputs to prevent directory traversal.
- For concurrent work: prefer `sync.WaitGroup` + channels over goroutine leaks. Always cancel contexts.
- Do not log secrets — scrub sensitive fields before passing to `log.Printf` or structured loggers.

## What To Deliver

- Provide `go.mod` with the module path and Go version.
- Provide the exact build command (`go build -o my-tool ./cmd/my-tool`) and the output binary path.
- Explain environment variable setup.
- Provide a `Makefile` target for `build`, `test`, and `lint` for non-trivial projects.

## Deep References

Load these when the task is non-trivial:

- [../patterns/go-patterns.md](../patterns/go-patterns.md) — module skeleton, `cobra` CLI pattern, error wrapping, `context.Context` propagation, CSV read/write, `net/http` client with retry, goroutines and channels, `exec.Command` safe subprocess, anti-patterns.
- [../recipes/go-cli-tool.md](../recipes/go-cli-tool.md) — Go CLI that reads a folder of CSV files, aggregates data, and writes a summary JSON report.
