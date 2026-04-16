# Lua Builder

Use this reference for Roblox game scripting, game engine extensions (Love2D, PICO-8, Defold), Neovim plugin configuration, and embedded scripting in C/C++ host applications.

## Use It For

- Roblox Studio game scripts (ModuleScript, LocalScript, Script)
- Love2D games and interactive prototypes
- Neovim plugin configuration in Lua
- Embedded scripting in C/C++ apps that expose a Lua API (Redis, Nginx, WoW addons)
- PICO-8 cartridge scripts
- Defold game engine scripts
- Lightweight automation scripts where a minimal runtime footprint matters

## Target Environments

| Environment | Lua version | Notes |
|---|---|---|
| Roblox Studio | Luau (Roblox Lua) | Strict type annotations with `: type`; `task` library instead of `wait()` |
| Neovim | LuaJIT (5.1 compat) | `vim.api`, `vim.keymap`, `vim.fn` APIs |
| Love2D | Lua 5.4 | `love.update`, `love.draw` callbacks |
| Standard Lua | 5.4 | `luac`, `lua` binaries, `luarocks` for packages |
| Redis / OpenResty | LuaJIT | `redis.call()`, `ngx.*` APIs respectively |

## Default Approach

- Write for the target environment's Lua version — they are not interchangeable.
- Use the module pattern (`local M = {}; return M`) for reusable code.
- Prefer local variables over globals — global namespace pollution is the most common Lua bug.
- Use metatables and `__index` for object-oriented patterns only when needed — prefer simple tables.
- In Roblox: use `task.wait()`, not `wait()`; use `Workspace:FindFirstChild()` rather than `.` indexing to avoid nil errors.

## Quality Bar

- Always declare variables `local` unless they must be global.
- Validate function arguments at the entry point — Lua has no type enforcement.
- For Roblox: enable strict mode with `--!strict` at the top of Luau scripts for type checking.
- Handle `nil` returns explicitly — Lua functions return `nil` by default and this is a frequent source of errors.
- Comment any metatable or closure pattern that is not obvious — Lua's OOP is implicit.

## What To Deliver

- State the target environment and Lua version clearly.
- For standalone Lua: provide the exact run command (`lua script.lua`).
- For Roblox: explain which service to place the script in and whether it runs on Server or Client.
- For Neovim: explain which config file to place the module in (`~/.config/nvim/lua/`).

## Deep References

Load these when the task is non-trivial:

- [../patterns/lua-patterns.md](../patterns/lua-patterns.md) — module pattern, table-as-object with metamethods, coroutine skeleton, Roblox script structure and `task` library, Neovim plugin skeleton, error handling with `pcall`/`xpcall`, anti-patterns.
