# Elixir Patterns

Load this reference when the task requires more than a trivial Elixir program. It provides reusable idioms for Mix applications, GenServer, Ecto queries, Phoenix routing, and the `with` error pipeline.

Pair with [../builders/elixir-builder.md](../builders/elixir-builder.md) for routing context.

---

## 1. Mix Application Skeleton

```elixir
# mix.exs
defmodule MyApp.MixProject do
  use Mix.Project

  def project do
    [
      app:     :my_app,
      version: "0.1.0",
      elixir:  "~> 1.16",
      deps:    deps()
    ]
  end

  def application do
    [extra_applications: [:logger], mod: {MyApp.Application, []}]
  end

  defp deps do
    [
      {:ecto_sql,  "~> 3.11"},
      {:postgrex,  "~> 0.18"},
      {:jason,     "~> 1.4"},
      {:req,       "~> 0.5"},
      {:credo,     "~> 1.7", only: [:dev, :test], runtime: false}
    ]
  end
end
```

Run: `mix deps.get && mix run --no-halt`

---

## 2. GenServer Template

```elixir
defmodule MyApp.InvoiceWorker do
  use GenServer
  require Logger

  # ---- Client API ----
  def start_link(opts \\ []) do
    GenServer.start_link(__MODULE__, opts, name: __MODULE__)
  end

  def process(invoice_id) do
    GenServer.call(__MODULE__, {:process, invoice_id}, 10_000)
  end

  # ---- Server Callbacks ----
  @impl true
  def init(_opts) do
    Logger.info("InvoiceWorker started")
    {:ok, %{count: 0}}
  end

  @impl true
  def handle_call({:process, id}, _from, state) do
    result = do_process(id)
    {:reply, result, %{state | count: state.count + 1}}
  end

  defp do_process(id) do
    # ... business logic ...
    {:ok, id}
  end
end
```

---

## 3. with Error Pipeline

Use `with` for multi-step operations where any step can return `{:error, reason}`.

```elixir
def create_invoice(attrs) do
  with {:ok, validated}  <- validate(attrs),
       {:ok, invoice}    <- Repo.insert(Invoice.changeset(%Invoice{}, validated)),
       {:ok, _email}     <- Mailer.send_confirmation(invoice) do
    {:ok, invoice}
  else
    {:error, %Ecto.Changeset{} = changeset} ->
      {:error, {:validation, changeset}}
    {:error, :email_failed} ->
      # Invoice was inserted — still return success, log the email failure
      Logger.warning("Confirmation email failed for invoice #{invoice.id}")
      {:ok, invoice}
    {:error, reason} ->
      {:error, reason}
  end
end
```

---

## 4. Ecto Parameterized Queries

Never string-interpolate user input into `Repo.query!`. Use Ecto schema queries or `$1` fragments.

```elixir
import Ecto.Query

# ✓ Safe: Ecto query — parameterized automatically
def find_by_region(region) do
  from(i in Invoice,
    where: i.region == ^region and i.amount > 0,
    order_by: [desc: i.amount],
    select: {i.id, i.region, i.amount}
  )
  |> Repo.all()
end

# ✓ Safe: raw SQL with parameterized placeholders
def total_by_region(region) do
  Repo.query!(
    "SELECT SUM(amount) FROM invoices WHERE region = $1",
    [region]
  )
end

# ✗ Never: string interpolation in SQL
# Repo.query!("SELECT * FROM invoices WHERE region = '#{region}'")
```

---

## 5. Phoenix Router + Controller Pattern

```elixir
# router.ex
scope "/api", MyAppWeb do
  pipe_through :api
  resources "/invoices", InvoiceController, only: [:index, :show, :create]
end

# invoice_controller.ex
defmodule MyAppWeb.InvoiceController do
  use MyAppWeb, :controller

  def index(conn, params) do
    region   = Map.get(params, "region", "")
    invoices = Invoices.list(region: region)
    render(conn, :index, invoices: invoices)
  end

  def create(conn, %{"invoice" => attrs}) do
    case Invoices.create(attrs) do
      {:ok, invoice}    -> conn |> put_status(:created) |> render(:show, invoice: invoice)
      {:error, changeset} -> conn |> put_status(:unprocessable_entity) |> render(:error, changeset: changeset)
    end
  end
end
```

---

## 6. Stream for Lazy Enumeration

```elixir
# Process a large CSV without loading everything into memory
defmodule MyApp.CsvProcessor do
  def process(path) do
    path
    |> File.stream!()
    |> Stream.drop(1)  # skip header
    |> Stream.map(&String.trim/1)
    |> Stream.filter(&(&1 != ""))
    |> Stream.map(&parse_row/1)
    |> Enum.reduce(%{}, &aggregate/2)
  end

  defp parse_row(line) do
    [id, region, amount] = String.split(line, ",", parts: 3)
    %{id: id, region: region, amount: String.to_float(amount)}
  end

  defp aggregate(row, acc) do
    Map.update(acc, row.region, row.amount, &(&1 + row.amount))
  end
end
```

---

## 7. Anti-Patterns

| Anti-pattern | Problem | Fix |
|---|---|---|
| Secrets in `config/config.exs` | Compiled into the release — visible in build artifacts | `config/runtime.exs` with `System.fetch_env!` |
| Bare `Repo.query!` with string interpolation | SQL injection | Ecto schema queries or `$1` placeholders |
| `spawn` without supervision | Orphaned process; no restart on crash | `DynamicSupervisor` + `GenServer` |
| Nested `case` for multi-step failures | Deep nesting, hard to read | `with` expression |
| `send`/`receive` for request-response | No timeout, no backpressure | `GenServer.call` with timeout |
| `Enum.map` on huge collections | Loads all results into memory | `Stream.map` + lazy pipeline |
| No `@spec` on public functions | Dialyzer cannot catch type errors | Add `@spec` to all public API |
