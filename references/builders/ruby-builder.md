# Ruby Builder

Use this reference for automation scripts, command-line tools, web applications with Ruby on Rails or Sinatra, file processing pipelines, and tasks where Ruby's expressiveness and rich standard library are a good fit.

## Use It For

- Automation and file management scripts
- Command-line tools and rake tasks
- Ruby on Rails web applications and APIs
- Sinatra or Roda for lightweight web services
- Static site generation with Jekyll
- REST API clients and data fetching pipelines
- System administration scripts on Linux and macOS
- Maintaining or extending existing Ruby codebases

## Default Approach

- Target **Ruby 3.2+** for new projects.
- Use **Bundler** for dependency management — always provide a `Gemfile` and lock file.
- Use `optparse` for CLI argument parsing in scripts; use Thor or `dry-cli` for larger tools.
- Load secrets from environment variables — never hard-code credentials.
- Use `begin`/`rescue` with specific exception classes — never a bare `rescue` that swallows all exceptions.

## Project Structure (Script)

```
my-tool/
  my_tool.rb      ← entry point
  lib/
    my_tool/
      csv_reader.rb
      api_client.rb
  Gemfile
  Gemfile.lock
  .env.example
```

## Quality Bar

- Use `frozen_string_literal: true` at the top of every file — prevents accidental string mutation and speeds up execution.
- Use keyword arguments for methods with more than two parameters.
- Prefer `Pathname` over raw string paths for filesystem work.
- Always use parameterized SQL queries with `?` placeholders when using SQLite or pg gems — never string interpolation.
- Rescue only the exceptions you expect — avoid `rescue StandardError` in production paths.

## What To Deliver

- Provide the `Gemfile` with exact gem versions or ranges.
- Provide the exact run command (`ruby my_tool.rb --help`, `bundle exec rake task`).
- Explain environment variable setup and `.env` conventions.
- Mention the Ruby version requirement and how to set it (`.ruby-version`, `rbenv`, `asdf`).

## Deep References

Load these when the task is non-trivial:

- [../patterns/ruby-patterns.md](../patterns/ruby-patterns.md) — script skeleton with `frozen_string_literal`, `optparse` CLI, CSV stdlib idioms, `Net::HTTP` and Faraday HTTP client, `FileUtils` file operations, logging, SQLite3 safe queries, anti-patterns.
- [../recipes/ruby-file-organizer.md](../recipes/ruby-file-organizer.md) — Ruby script that organizes files in a folder by last-modified date into `YYYY/MM/` subdirectories with dry-run mode and a move log.
