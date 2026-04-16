# Elixir Builder

Use this reference for web APIs with Phoenix, real-time features, fault-tolerant distributed systems, data pipelines with Broadway, and vibe-coded backend prototypes that need concurrency out of the box.

## Use It For

- Phoenix web applications and REST or JSON APIs
- Real-time features with Phoenix LiveView or Channels (WebSocket)
- Fault-tolerant background job processing with Broadway or Oban
- Distributed systems and clustered applications on the BEAM VM
- Data transformation pipelines with Enum and Stream
- LiveBook notebooks for interactive data exploration
- CLI scripts with Mix tasks

## Default Approach

- Target **Elixir 1.16+** and **OTP 26+** for new projects.
- Use **Phoenix** for any web or API work — do not write a raw Plug server.
- Use **Ecto** for database access — parameterized queries only, never string interpolation in Ecto SQL.
- Load secrets from runtime config (`config/runtime.exs`) using `System.fetch_env!("VAR")` — never in `config/config.exs`.
- Use pattern matching and function clauses rather than `if`/`else` for conditional logic.
- Prefer processes (`GenServer`, `Task`, `Agent`) over shared mutable state.

## Project Structure

```
my_app/
  mix.exs
  config/
    config.exs
    runtime.exs      ← secrets from env at runtime
  lib/
    my_app/
      application.ex
      worker.ex
    my_app_web/
      router.ex
      controllers/
      live/
  test/
  priv/
    repo/migrations/
```

## Quality Bar

- Run `mix credo` and `mix dialyzer` (Dialyxir) for static analysis.
- Use `@spec` type annotations on public functions.
- Use `with` for multi-step pipelines that can fail — avoid nested `case` statements.
- Never use `send/receive` for request/response patterns — use `GenServer.call` instead.
- Always supervise processes — orphaned processes leak memory until VM restart.

## What To Deliver

- Provide `mix.exs` with exact dependency versions.
- Provide the exact setup commands (`mix deps.get && mix ecto.setup && mix phx.server`).
- Explain `config/runtime.exs` secret loading and which env vars are required.
- For LiveView: describe the route, mount, and handle_event flow.

## Deep References

Load these when the task is non-trivial:

- [../patterns/elixir-patterns.md](../patterns/elixir-patterns.md) — Mix application skeleton, GenServer template, Ecto parameterized query idioms, Phoenix router + controller pattern, `with` error pipeline, `Stream` lazy enumeration, anti-patterns.
