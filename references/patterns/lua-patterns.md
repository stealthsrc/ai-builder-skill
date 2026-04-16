# Lua Patterns

Load this reference when the task requires more than a trivial Lua script. It provides reusable idioms for the module pattern, metatables, coroutines, error handling, Roblox scripting, and Neovim plugin structure.

Pair with [../builders/lua-builder.md](../builders/lua-builder.md) for routing context.

---

## 1. Module Pattern

```lua
-- invoice.lua
local M = {}  -- module table — always local, never global

local CONFIG = {
  TAX_RATE = 0.20,
  CURRENCY = "EUR",
}

-- Private function (not exposed in M)
local function format_amount(n)
  return string.format("%s %.2f", CONFIG.CURRENCY, n)
end

-- Public API
function M.new(id, region, amount)
  assert(type(id)     == "string", "id must be a string")
  assert(type(amount) == "number" and amount >= 0, "amount must be non-negative")
  return { id = id, region = region, amount = amount }
end

function M.total_with_tax(invoice)
  return invoice.amount * (1 + CONFIG.TAX_RATE)
end

function M.display(invoice)
  return string.format("[%s] %s: %s", invoice.id, invoice.region,
    format_amount(M.total_with_tax(invoice)))
end

return M
```

Usage: `local Invoice = require("invoice")`

---

## 2. Table as Object with Metatables

```lua
local Invoice = {}
Invoice.__index = Invoice

function Invoice.new(id, region, amount)
  local self = setmetatable({}, Invoice)
  self.id     = id
  self.region = region
  self.amount = amount
  return self
end

function Invoice:total_with_tax(rate)
  rate = rate or 0.20
  return self.amount * (1 + rate)
end

function Invoice:__tostring()
  return string.format("Invoice{%s, %s, %.2f}", self.id, self.region, self.amount)
end

-- Usage
local inv = Invoice.new("INV-001", "West", 500)
print(inv:total_with_tax())  -- 600.0
print(tostring(inv))
```

---

## 3. Error Handling with pcall and xpcall

```lua
-- pcall: protected call — returns ok, result or ok, error_message
local ok, result = pcall(function()
  return parse_csv("invoices.csv")
end)

if not ok then
  print("[ERROR] " .. tostring(result))
  return
end

-- xpcall: protected call with a traceback handler
local function error_handler(err)
  return debug.traceback(tostring(err), 2)
end

local ok2, err = xpcall(function()
  process(result)
end, error_handler)

if not ok2 then
  io.stderr:write(err .. "\n")
end
```

---

## 4. Coroutines

```lua
-- Producer-consumer pattern with coroutines
local function csv_producer(path)
  return coroutine.create(function()
    local file = assert(io.open(path, "r"), "Cannot open: " .. path)
    for line in file:lines() do
      coroutine.yield(line)
    end
    file:close()
  end)
end

local producer = csv_producer("invoices.csv")
while true do
  local ok, line = coroutine.resume(producer)
  if not ok or line == nil then break end
  print(line)
end
```

---

## 5. Roblox Script Structure

```lua
-- LocalScript (runs on client)
--!strict  -- enable Luau strict type checking

local Players      = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local player       = Players.LocalPlayer
local RemoteEvent  = ReplicatedStorage:WaitForChild("InvoiceEvent", 10)

if not RemoteEvent then
  warn("InvoiceEvent not found in ReplicatedStorage")
  return
end

-- Use task.wait() NOT wait() — wait() is deprecated
task.wait(1)

RemoteEvent.OnClientEvent:Connect(function(data)
  -- Validate data before use
  if type(data) ~= "table" or not data.id then
    warn("Invalid event data received")
    return
  end
  print("Invoice received:", data.id)
end)
```

---

## 6. Neovim Plugin Skeleton

```lua
-- lua/my-plugin/init.lua
local M = {}

M.config = {
  highlight = true,
  keymaps   = true,
}

function M.setup(opts)
  M.config = vim.tbl_deep_extend("force", M.config, opts or {})
  if M.config.keymaps then M.set_keymaps() end
end

function M.set_keymaps()
  vim.keymap.set("n", "<leader>mi", M.show_info, { desc = "My Plugin: show info" })
end

function M.show_info()
  vim.notify("My Plugin is active", vim.log.levels.INFO)
end

return M
```

---

## 7. Anti-Patterns

| Anti-pattern | Problem | Fix |
|---|---|---|
| Global variables (`x = 5`) | Pollutes the shared namespace | Always `local x = 5` |
| `require` inside functions | Reloads module every call (depends on version) | Require at the top of the module |
| `table[#table + 1]` in a tight loop | Repeated length calculation | `table.insert(t, value)` or pre-size |
| No nil checks on function args | Silent bugs or confusing errors | `assert(x ~= nil, "x is required")` |
| Roblox: `wait()` | Deprecated, inconsistent timing | `task.wait(seconds)` |
| Roblox: direct `.` index on Instance | Errors if child does not exist | `:FindFirstChild("name")` with nil check |
| Neovim: global keymaps without `{desc}` | Undiscoverable in which-key | Always add `{ desc = "..." }` |
| Catching all errors and ignoring them | Masks bugs | Log the error with `warn()` or `print()` |
