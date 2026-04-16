# Recipe: Go CLI — CSV Folder Aggregator

Complete Go CLI tool that reads every CSV file in a folder, aggregates a numeric column by a group column, and writes a JSON summary report. Single binary, no runtime dependency.

Pair with [../builders/go-builder.md](../builders/go-builder.md) and [../patterns/go-patterns.md](../patterns/go-patterns.md).

---

## What It Does

1. Scans a source folder for `*.csv` files.
2. Reads each CSV, maps the group column to a running total of the amount column.
3. Merges totals across files.
4. Writes a sorted JSON report with group totals and file count.
5. Supports `--dry-run` to preview without writing output.

---

## Project Setup

```bash
mkdir csv-agg && cd csv-agg
go mod init github.com/myorg/csv-agg

go get github.com/spf13/cobra
```

---

## File Structure

```
csv-agg/
  go.mod
  go.sum
  main.go
  cmd/
    root.go
  internal/
    aggregator/
      aggregator.go
```

---

## go.mod

```go
module github.com/myorg/csv-agg

go 1.22

require github.com/spf13/cobra v1.8.0
```

---

## internal/aggregator/aggregator.go

```go
package aggregator

import (
	"encoding/csv"
	"fmt"
	"os"
	"path/filepath"
	"strconv"
	"strings"
)

type Summary struct {
	Group  string  `json:"group"`
	Total  float64 `json:"total"`
	Count  int     `json:"count"`
}

type Result struct {
	Files    int       `json:"files_processed"`
	Rows     int       `json:"rows_processed"`
	Summaries []Summary `json:"summaries"`
}

func Run(dir, groupCol, amountCol string) (*Result, error) {
	pattern := filepath.Join(dir, "*.csv")
	files, err := filepath.Glob(pattern)
	if err != nil || len(files) == 0 {
		return nil, fmt.Errorf("no CSV files found in %s", dir)
	}

	totals := make(map[string]float64)
	counts := make(map[string]int)
	totalRows := 0

	for _, f := range files {
		rows, err := readCSV(f, groupCol, amountCol)
		if err != nil {
			return nil, fmt.Errorf("read %s: %w", f, err)
		}
		for group, amount := range rows {
			totals[group] += amount
			counts[group]++
		}
		totalRows += len(rows)
	}

	summaries := make([]Summary, 0, len(totals))
	for group, total := range totals {
		summaries = append(summaries, Summary{Group: group, Total: total, Count: counts[group]})
	}
	// Sort descending by total
	sortSummaries(summaries)

	return &Result{Files: len(files), Rows: totalRows, Summaries: summaries}, nil
}

func readCSV(path, groupCol, amountCol string) (map[string]float64, error) {
	f, err := os.Open(path)
	if err != nil { return nil, err }
	defer f.Close()

	r := csv.NewReader(f)
	r.TrimLeadingSpace = true
	records, err := r.ReadAll()
	if err != nil { return nil, err }
	if len(records) < 2 { return nil, nil }

	headers := records[0]
	groupIdx  := indexOf(headers, groupCol)
	amountIdx := indexOf(headers, amountCol)
	if groupIdx < 0  { return nil, fmt.Errorf("column %q not found in %s", groupCol, path)  }
	if amountIdx < 0 { return nil, fmt.Errorf("column %q not found in %s", amountCol, path) }

	result := make(map[string]float64)
	for _, row := range records[1:] {
		if len(row) <= max(groupIdx, amountIdx) { continue }
		group  := strings.TrimSpace(row[groupIdx])
		amount, err := strconv.ParseFloat(strings.TrimSpace(row[amountIdx]), 64)
		if err != nil { continue }
		result[group] += amount
	}
	return result, nil
}

func indexOf(headers []string, name string) int {
	for i, h := range headers {
		if strings.EqualFold(strings.TrimSpace(h), name) { return i }
	}
	return -1
}

func sortSummaries(s []Summary) {
	for i := 1; i < len(s); i++ {
		for j := i; j > 0 && s[j].Total > s[j-1].Total; j-- {
			s[j], s[j-1] = s[j-1], s[j]
		}
	}
}
```

---

## cmd/root.go

```go
package cmd

import (
	"encoding/json"
	"fmt"
	"os"

	"github.com/myorg/csv-agg/internal/aggregator"
	"github.com/spf13/cobra"
)

var (
	sourceDir  string
	groupCol   string
	amountCol  string
	outputPath string
	dryRun     bool
)

var rootCmd = &cobra.Command{
	Use:   "csv-agg",
	Short: "Aggregate CSV files in a folder by group and amount columns",
	RunE:  run,
}

func init() {
	rootCmd.Flags().StringVarP(&sourceDir,  "dir",    "d", "data",        "Source folder with CSV files")
	rootCmd.Flags().StringVarP(&groupCol,   "group",  "g", "region",      "Group column name")
	rootCmd.Flags().StringVarP(&amountCol,  "amount", "a", "amount",      "Amount column name")
	rootCmd.Flags().StringVarP(&outputPath, "output", "o", "report.json", "Output JSON file")
	rootCmd.Flags().BoolVarP(  &dryRun,    "dry-run","n", false,          "Preview without writing")
}

func Execute() error { return rootCmd.Execute() }

func run(cmd *cobra.Command, args []string) error {
	result, err := aggregator.Run(sourceDir, groupCol, amountCol)
	if err != nil { return err }

	out, err := json.MarshalIndent(result, "", "  ")
	if err != nil { return fmt.Errorf("marshal: %w", err) }

	if dryRun {
		fmt.Println(string(out))
		return nil
	}

	if err := os.WriteFile(outputPath, out, 0644); err != nil {
		return fmt.Errorf("write %s: %w", outputPath, err)
	}
	fmt.Printf("Processed %d files, %d rows → %s\n", result.Files, result.Rows, outputPath)
	return nil
}
```

---

## main.go

```go
package main

import (
	"fmt"
	"os"

	"github.com/myorg/csv-agg/cmd"
)

func main() {
	if err := cmd.Execute(); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}
```

---

## Run

```bash
go build -o csv-agg ./...

# Dry run — print JSON without writing
./csv-agg --dir data --group region --amount amount --dry-run

# Live run
./csv-agg --dir data --group region --amount amount --output report.json
```

---

## Validation

- `report.json` should contain a `summaries` array sorted by `total` descending.
- `files_processed` should match the number of `.csv` files in `data/`.
- `rows_processed` should equal the sum of data rows across all files (excluding headers).

---

## Edge Cases

| Case | Behavior |
|---|---|
| CSV missing the group column | Returns an error naming the file |
| Amount is non-numeric | Row is silently skipped |
| Folder is empty | Returns error "no CSV files found" |
| Group value is blank | Blank string used as the group key |
