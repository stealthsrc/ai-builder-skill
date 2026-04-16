# Go Patterns

Load this reference when the task requires more than a trivial Go program. It provides reusable idioms for CLI tools, error wrapping, CSV processing, HTTP, goroutines, and safe subprocesses.

Pair with [../builders/go-builder.md](../builders/go-builder.md) for routing context.

---

## 1. Module Skeleton

```
# Initialize
go mod init github.com/myorg/my-tool

# Add dependencies
go get github.com/spf13/cobra
go get github.com/gocarina/gocsv
```

```go
// main.go
package main

import (
    "fmt"
    "os"

    "github.com/myorg/my-tool/cmd"
)

func main() {
    if err := cmd.Execute(); err != nil {
        fmt.Fprintln(os.Stderr, err)
        os.Exit(1)
    }
}
```

---

## 2. Cobra CLI Pattern

```go
// cmd/root.go
package cmd

import (
    "github.com/spf13/cobra"
    "os"
)

var (
    inputPath  string
    outputPath string
    dryRun     bool
)

var rootCmd = &cobra.Command{
    Use:   "my-tool",
    Short: "Process CSV files and generate a report",
    RunE:  run,
}

func init() {
    rootCmd.Flags().StringVarP(&inputPath,  "input",  "i", "",           "Input CSV file (required)")
    rootCmd.Flags().StringVarP(&outputPath, "output", "o", "report.json","Output file")
    rootCmd.Flags().BoolVarP(  &dryRun,    "dry-run","n", false,         "Preview without writing")
    _ = rootCmd.MarkFlagRequired("input")
}

func Execute() error { return rootCmd.Execute() }

func run(cmd *cobra.Command, args []string) error {
    return process(inputPath, outputPath, dryRun)
}
```

---

## 3. Error Wrapping

```go
import "fmt"

// Always wrap errors with context using %w so callers can unwrap
func readFile(path string) ([]byte, error) {
    data, err := os.ReadFile(path)
    if err != nil {
        return nil, fmt.Errorf("readFile %s: %w", path, err)
    }
    return data, nil
}

// Caller can inspect with errors.Is or errors.As
if errors.Is(err, os.ErrNotExist) {
    log.Printf("File not found: %s", path)
}
```

---

## 4. CSV Read and Write

```go
import (
    "encoding/csv"
    "os"
)

type Invoice struct {
    ID     string
    Region string
    Amount float64
}

func readCSV(path string) ([]Invoice, error) {
    f, err := os.Open(path)
    if err != nil { return nil, fmt.Errorf("open csv: %w", err) }
    defer f.Close()

    r := csv.NewReader(f)
    r.TrimLeadingSpace = true
    records, err := r.ReadAll()
    if err != nil { return nil, fmt.Errorf("parse csv: %w", err) }

    var invoices []Invoice
    for _, rec := range records[1:] { // skip header
        amt, _ := strconv.ParseFloat(rec[2], 64)
        invoices = append(invoices, Invoice{rec[0], rec[1], amt})
    }
    return invoices, nil
}
```

---

## 5. context.Context Propagation

Every function that does I/O must accept a `context.Context` as its first argument.

```go
func fetchData(ctx context.Context, url, token string) ([]byte, error) {
    req, err := http.NewRequestWithContext(ctx, http.MethodGet, url, nil)
    if err != nil { return nil, fmt.Errorf("build request: %w", err) }
    req.Header.Set("Authorization", "Bearer "+token)

    client := &http.Client{Timeout: 15 * time.Second}
    resp, err := client.Do(req)
    if err != nil { return nil, fmt.Errorf("fetch %s: %w", url, err) }
    defer resp.Body.Close()

    if resp.StatusCode < 200 || resp.StatusCode >= 300 {
        return nil, fmt.Errorf("HTTP %d from %s", resp.StatusCode, url)
    }
    return io.ReadAll(resp.Body)
}
```

---

## 6. Goroutines and WaitGroup

```go
import "sync"

func processAll(ctx context.Context, items []Invoice) error {
    var wg sync.WaitGroup
    errs := make(chan error, len(items))

    for _, item := range items {
        wg.Add(1)
        go func(inv Invoice) {
            defer wg.Done()
            if err := process(ctx, inv); err != nil {
                errs <- fmt.Errorf("process %s: %w", inv.ID, err)
            }
        }(item) // capture item by value, not reference
    }

    wg.Wait()
    close(errs)

    for err := range errs {
        if err != nil { return err } // return first error
    }
    return nil
}
```

---

## 7. Safe Subprocess

```go
import "os/exec"

func runGit(ctx context.Context, args ...string) (string, error) {
    cmd := exec.CommandContext(ctx, "git", args...)
    out, err := cmd.Output()
    if err != nil {
        var exitErr *exec.ExitError
        if errors.As(err, &exitErr) {
            return "", fmt.Errorf("git %v: %s", args, exitErr.Stderr)
        }
        return "", fmt.Errorf("git %v: %w", args, err)
    }
    return strings.TrimSpace(string(out)), nil
}

// ✓ Argument list — no shell injection
branch, err := runGit(ctx, "rev-parse", "--abbrev-ref", "HEAD")
```

---

## 8. Anti-Patterns

| Anti-pattern | Problem | Fix |
|---|---|---|
| Ignoring an error with `_` | Silent failure | Handle or explicitly wrap and return |
| `fmt.Errorf("msg: %v", err)` | Loses the error type for unwrapping | Use `%w` not `%v` |
| Goroutine without `wg.Add`/`wg.Done` | Race or goroutine leak | `sync.WaitGroup` or `errgroup` |
| `exec.Command("sh", "-c", userInput)` | Shell injection | `exec.Command("cmd", arg1, arg2)` |
| `log.Fatal` inside library code | Calls `os.Exit(1)` — skips defers | Return errors; `log.Fatal` only in `main` |
| Global `http.Client` with no timeout | Hangs on slow servers | `http.Client{Timeout: 15 * time.Second}` |
| Loop variable capture in goroutine (pre-Go 1.22) | All goroutines share the last value | Pass item as a parameter or use Go 1.22+ |
