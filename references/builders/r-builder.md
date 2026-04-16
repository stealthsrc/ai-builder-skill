# R Builder

Use this reference for statistical analysis, data visualization, CSV and Excel processing, R Markdown or Quarto reports, and data science workflows where R's ecosystem is the natural fit.

## Use It For

- Statistical analysis and hypothesis testing
- Data visualization with ggplot2
- CSV, Excel, and database data ingestion and cleaning
- Regression, time series, and forecasting models
- R Markdown or Quarto documents that blend code, output, and prose
- Automated report generation that renders to HTML, PDF, or Word
- Exploratory data analysis (EDA) for business data

## Default Approach

- Use **R 4.x** (current stable release).
- Use **tidyverse** (`dplyr`, `tidyr`, `readr`, `ggplot2`, `purrr`) as the default data manipulation layer for tabular work.
- Use **Quarto** for reproducible reports — it supersedes R Markdown for new work.
- Use `here::here()` for file paths — avoids working-directory surprises in scripts and reports.
- Load secrets from environment variables with `Sys.getenv()` — never hard-code API keys or database passwords.
- Write data transformations as pipelines using the native pipe `|>` (R 4.1+) or `%>%` from `magrittr`.

## Project Structure

```
my-report/
  analysis.R         ← main script or source file
  report.qmd         ← Quarto document (if rendering a report)
  data/
    input.csv
  output/
    report.html
  renv.lock          ← reproducible package versions via renv
```

## Quality Bar

- Use `renv` to lock package versions — prevents silent breaks when packages update.
- Separate data loading, cleaning, analysis, and output into clear sections or functions.
- Avoid `attach()` — use `df$column` or `with(df, ...)` explicitly.
- Never `rm(list=ls())` at the top of a script — it destroys the user's environment. Use a fresh R session instead.
- Always inspect the first rows (`head()`, `glimpse()`) after reading external data to catch encoding or parsing issues early.

## What To Deliver

- State required packages and the install command (`install.packages(c(...))` or `renv::restore()`).
- Provide the exact command to run the script or render the report (`Rscript analysis.R`, `quarto render report.qmd`).
- Explain any data path assumptions (`here::here("data", "input.csv")`).
- Describe the output format (HTML report, PNG chart, CSV, Excel).

## Deep References

Load these when the task is non-trivial:

- [../patterns/r-patterns.md](../patterns/r-patterns.md) — script skeleton with `here` and `renv`, tidyverse CSV read idioms, dplyr pipeline, ggplot2 theme skeleton, `writexl` Excel export, `tryCatch` error handling, anti-patterns.
- [../recipes/r-csv-report.md](../recipes/r-csv-report.md) — R script that reads a CSV, computes summary statistics, draws a ggplot2 chart, and renders a Quarto report to HTML.
