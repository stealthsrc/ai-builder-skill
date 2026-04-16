# Recipe: R CSV to Quarto HTML Report

Complete R script and Quarto document that reads a CSV, computes summary statistics, draws a ggplot2 bar chart, and renders a self-contained HTML report.

Pair with [../builders/r-builder.md](../builders/r-builder.md) and [../patterns/r-patterns.md](../patterns/r-patterns.md).

---

## What It Does

1. Reads a CSV file with `readr` into a tibble.
2. Computes group-level summary statistics (count, total, average) with `dplyr`.
3. Draws a horizontal bar chart with `ggplot2` sorted by total.
4. Renders a self-contained HTML report via Quarto (or R Markdown as fallback).
5. Writes a companion summary CSV.

---

## Setup

```r
# Install packages (run once)
install.packages(c("quarto", "here", "readr", "dplyr", "ggplot2", "scales", "writexl"))
# Or restore from renv.lock:
# renv::restore()
```

Quarto CLI: download from https://quarto.org/docs/get-started/

---

## Project Layout

```
my-report/
  report.qmd         ← Quarto document (source below)
  analysis.R         ← standalone R script (source below)
  data/
    invoices.csv
  output/            ← created automatically
```

---

## analysis.R — Standalone Script

```r
# analysis.R — run with: Rscript analysis.R
# frozen_string_literal equivalent: options(stringsAsFactors = FALSE)

suppressPackageStartupMessages({
  library(here)
  library(readr)
  library(dplyr)
  library(ggplot2)
  library(scales)
  library(writexl)
})

# ---- Configuration ----
INPUT_FILE  <- here("data", "invoices.csv")
OUTPUT_DIR  <- here("output")
AMOUNT_COL  <- "amount"   # numeric column to summarize
GROUP_COL   <- "region"   # grouping column

# ---- Guards ----
if (!file.exists(INPUT_FILE)) stop("Input not found: ", INPUT_FILE)
dir.create(OUTPUT_DIR, showWarnings = FALSE, recursive = TRUE)

# ---- Load ----
invoices <- read_csv(INPUT_FILE, show_col_types = FALSE)
message("Loaded ", nrow(invoices), " rows, ", ncol(invoices), " columns")
stopifnot(AMOUNT_COL %in% names(invoices), GROUP_COL %in% names(invoices))

# ---- Summarize ----
summary_df <- invoices |>
  filter(!is.na(.data[[AMOUNT_COL]]), .data[[AMOUNT_COL]] > 0) |>
  group_by(.data[[GROUP_COL]]) |>
  summarize(
    count         = n(),
    total_revenue = sum(.data[[AMOUNT_COL]]),
    avg_amount    = mean(.data[[AMOUNT_COL]]),
    .groups       = "drop"
  ) |>
  arrange(desc(total_revenue))

message("Summary groups: ", nrow(summary_df))

# ---- Chart ----
p <- ggplot(summary_df, aes(
    x = total_revenue,
    y = reorder(.data[[GROUP_COL]], total_revenue)
  )) +
  geom_col(fill = "#2563eb", width = 0.65) +
  geom_text(aes(label = comma(total_revenue, accuracy = 1)),
            hjust = -0.1, size = 3.5, color = "#1e293b") +
  scale_x_continuous(labels = comma, expand = expansion(mult = c(0, 0.15))) +
  labs(
    title = paste("Revenue by", tools::toTitleCase(GROUP_COL)),
    x     = paste("Total", tools::toTitleCase(AMOUNT_COL)),
    y     = NULL
  ) +
  theme_minimal(base_size = 13) +
  theme(
    plot.title       = element_text(face = "bold"),
    panel.grid.major.y = element_blank(),
    panel.grid.minor   = element_blank()
  )

ggsave(file.path(OUTPUT_DIR, "chart.png"), p, width = 9, height = 5, dpi = 150)
message("Chart saved: output/chart.png")

# ---- Export ----
write_csv(summary_df, file.path(OUTPUT_DIR, "summary.csv"))
write_xlsx(list(Summary = summary_df, Raw = invoices), file.path(OUTPUT_DIR, "report.xlsx"))
message("Outputs written to output/")

# ---- Print ----
print(summary_df)
```

---

## report.qmd — Quarto Document

```yaml
---
title: "Invoice Revenue Report"
date: today
format:
  html:
    self-contained: true
    theme: flatly
    toc: true
execute:
  echo: false
  warning: false
---
```

````r
```{r setup}
library(readr); library(dplyr); library(ggplot2); library(scales); library(knitr)
invoices   <- read_csv(here::here("data", "invoices.csv"), show_col_types = FALSE)
summary_df <- invoices |>
  filter(amount > 0) |>
  group_by(region) |>
  summarize(count = n(), total_revenue = sum(amount), avg = mean(amount), .groups = "drop") |>
  arrange(desc(total_revenue))
```

## Summary

Total invoices analysed: **`r nrow(invoices)`**  
Regions covered: **`r nrow(summary_df)`**  
Total revenue: **`r comma(sum(summary_df$total_revenue))`**

## Revenue by Region

```{r chart, fig.width=9, fig.height=5}
ggplot(summary_df, aes(x = total_revenue, y = reorder(region, total_revenue))) +
  geom_col(fill = "#2563eb") +
  geom_text(aes(label = comma(total_revenue, accuracy=1)), hjust=-0.1, size=3.5) +
  scale_x_continuous(labels = comma, expand = expansion(mult = c(0,0.15))) +
  labs(title = "Revenue by Region", x = "Total Revenue", y = NULL) +
  theme_minimal(base_size=13)
```

## Data Table

```{r table}
kable(summary_df, col.names = c("Region","Orders","Total Revenue","Avg Amount"),
      format.args = list(big.mark = ","), digits = 2)
```
````

---

## Run

```bash
# Standalone script
Rscript analysis.R

# Quarto report
quarto render report.qmd
# → output: report.html (self-contained, shareable)
```

---

## Validation

- `output/chart.png` — bars sorted by descending revenue, labeled with values.
- `output/summary.csv` — one row per group, correct totals.
- `report.html` — opens in any browser, shows chart and table without an R server.

---

## Edge Cases

| Case | Behavior |
|---|---|
| CSV has no rows with amount > 0 | Summary has 0 rows; chart renders empty |
| GROUP_COL has many levels (> 20) | Chart becomes crowded — consider limiting with `top_n(10)` |
| AMOUNT_COL contains non-numeric text | `read_csv` will parse as character; `filter` step will error |
| Quarto not installed | Use `rmarkdown::render("report.Rmd")` with equivalent `.Rmd` file |
