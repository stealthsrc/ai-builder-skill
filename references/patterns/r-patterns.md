# R Patterns

Load this reference when the task requires more than a trivial R script. It provides reusable idioms for data loading, tidyverse pipelines, ggplot2 visualization, Excel export, error handling, and reproducibility.

Pair with [../builders/r-builder.md](../builders/r-builder.md) for routing context and with [../rules/security-baseline.md](../rules/security-baseline.md) when the script loads secrets or calls external APIs.

---

## 1. Script Skeleton with here and renv

```r
# analysis.R — reproducible, path-safe script

# ---- Reproducibility ----
# renv::restore()  # uncomment to restore exact package versions from renv.lock

library(here)       # path helpers — never setwd() or hard-coded paths
library(readr)      # fast, typed CSV reading
library(dplyr)      # data manipulation
library(tidyr)      # reshaping
library(ggplot2)    # visualization
library(writexl)    # Excel export without Java dependency

# ---- Configuration ----
INPUT_FILE  <- here("data", "invoices.csv")
OUTPUT_CSV  <- here("output", "summary.csv")
OUTPUT_XLSX <- here("output", "summary.xlsx")
CUTOFF_DATE <- as.Date("2025-01-01")

# ---- Guard ----
if (!file.exists(INPUT_FILE)) stop("Input file not found: ", INPUT_FILE)
dir.create(here("output"), showWarnings = FALSE)

# ---- Load ----
invoices <- read_csv(INPUT_FILE, show_col_types = FALSE)
message("Loaded ", nrow(invoices), " rows.")

# ---- Work ----
# ... see sections below ...
```

---

## 2. dplyr Pipeline Idioms

```r
# Filter, group, summarize, sort in one pipeline
summary_by_region <- invoices |>
  filter(!is.na(amount), amount > 0, date >= CUTOFF_DATE) |>
  group_by(region) |>
  summarize(
    order_count   = n(),
    total_revenue = sum(amount),
    avg_amount    = mean(amount),
    .groups       = "drop"
  ) |>
  arrange(desc(total_revenue))

# Quick check
glimpse(summary_by_region)
print(summary_by_region, n = 20)
```

---

## 3. ggplot2 Theme Skeleton

```r
# Custom minimal theme with consistent colors
my_theme <- theme_minimal(base_size = 13) +
  theme(
    plot.title       = element_text(face = "bold", size = 15),
    axis.text        = element_text(color = "#334155"),
    panel.grid.minor = element_blank(),
    legend.position  = "bottom"
  )

p <- ggplot(summary_by_region, aes(x = reorder(region, -total_revenue), y = total_revenue)) +
  geom_col(fill = "#2563eb", width = 0.6) +
  geom_text(aes(label = scales::comma(total_revenue)),
            vjust = -0.4, size = 3.5, color = "#1e293b") +
  scale_y_continuous(labels = scales::comma) +
  labs(title = "Revenue by Region", x = NULL, y = "Total Revenue") +
  my_theme

ggsave(here("output", "revenue-by-region.png"), p, width = 9, height = 5, dpi = 150)
```

---

## 4. Excel Export with writexl

```r
# writexl writes native .xlsx with no Java dependency
write_xlsx(
  list(
    Summary  = summary_by_region,
    Raw_Data = invoices
  ),
  path = OUTPUT_XLSX
)
message("Excel written: ", OUTPUT_XLSX)
```

---

## 5. Error Handling with tryCatch

```r
result <- tryCatch(
  {
    read_csv(INPUT_FILE, col_types = cols(amount = col_double(), date = col_date()))
  },
  error = function(e) {
    message("[ERROR] Failed to read input: ", conditionMessage(e))
    NULL
  },
  warning = function(w) {
    message("[WARN] ", conditionMessage(w))
    suppressWarnings(read_csv(INPUT_FILE))
  }
)
if (is.null(result)) stop("Aborting due to read error.")
```

---

## 6. Secrets from Environment

```r
api_key <- Sys.getenv("API_KEY")
if (nchar(api_key) == 0) stop("API_KEY environment variable is required.")

# For local dev, put variables in .Renviron (never commit it)
# ~/.Renviron:
# API_KEY=dev-key-here
```

---

## 7. renv for Package Reproducibility

```r
# Initialize (once per project)
renv::init()

# Save current state
renv::snapshot()

# Restore on a new machine or CI
renv::restore()
```

Always commit `renv.lock`. Never commit the `renv/library/` cache.

---

## 8. Anti-Patterns

| Anti-pattern | Problem | Fix |
|---|---|---|
| `setwd("/Users/me/project")` | Hardcoded path — breaks on other machines | `here::here("data", "file.csv")` |
| `rm(list=ls())` at script top | Destroys the user's global environment | Use a clean R session instead |
| `read.csv` without `stringsAsFactors` | Unexpected factor conversion in R < 4 | `readr::read_csv` or `read.csv(stringsAsFactors=FALSE)` |
| `attach(df)` | Pollutes global namespace | Use `df$column` or `with(df, ...)` |
| `library()` inside functions | Loads packages at call site unpredictably | Load at the script top |
| Hard-coded API keys in source | Credential leak | `Sys.getenv()` + `.Renviron` |
| No `renv.lock` | Script breaks when packages update | `renv::snapshot()` + commit the lock file |
| `for` loop over data frame rows | Slow — R is vectorized | `dplyr::mutate`, `purrr::map`, or vectorized functions |
