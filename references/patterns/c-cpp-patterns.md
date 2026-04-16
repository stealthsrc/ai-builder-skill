# C and C++ Patterns

Load this reference when the task requires more than a trivial C or C++ program. It provides reusable idioms for safe memory management, build configuration, and common anti-patterns.

Pair with [../builders/c-cpp-builder.md](../builders/c-cpp-builder.md) for routing context and with [../rules/security-baseline.md](../rules/security-baseline.md) for any code that processes external input, handles file paths, or executes commands.

---

## 1. CMake Skeleton

```cmake
# CMakeLists.txt
cmake_minimum_required(VERSION 3.20)
project(my_tool VERSION 1.0 LANGUAGES C CXX)

set(CMAKE_C_STANDARD 17)
set(CMAKE_CXX_STANDARD 17)

# Treat warnings as errors in development builds
if(CMAKE_BUILD_TYPE STREQUAL "Debug")
  add_compile_options(-Wall -Wextra -Wpedantic -Werror)
  add_compile_options(-fsanitize=address,undefined)
  add_link_options(-fsanitize=address,undefined)
endif()

add_executable(my_tool src/main.c src/util.c)
target_include_directories(my_tool PRIVATE include)
```

Build:
```bash
cmake -B build -DCMAKE_BUILD_TYPE=Debug
cmake --build build
./build/my_tool
```

---

## 2. Safe String Handling in C

Never use `strcpy`, `sprintf`, or `gets` — always use their bounded equivalents.

```c
#include <string.h>
#include <stdio.h>
#include <stddef.h>

void safe_copy(char *dest, size_t dest_size, const char *src) {
    if (!dest || !src || dest_size == 0) return;
    strncpy(dest, src, dest_size - 1);
    dest[dest_size - 1] = '\0';  // always null-terminate
}

void safe_format(char *buf, size_t buf_size, const char *fmt, ...) {
    va_list args;
    va_start(args, fmt);
    int n = vsnprintf(buf, buf_size, fmt, args);
    va_end(args);
    if (n < 0 || (size_t)n >= buf_size) {
        /* output was truncated — handle or log */
    }
}
```

---

## 3. Error Code Pattern in C

Return an int error code from every function that can fail. Never return -1 for multiple different errors.

```c
typedef enum {
    ERR_OK       = 0,
    ERR_IO       = 1,
    ERR_NOMEM    = 2,
    ERR_INVALID  = 3,
} Error;

const char *err_str(Error e) {
    switch (e) {
        case ERR_OK:      return "ok";
        case ERR_IO:      return "I/O error";
        case ERR_NOMEM:   return "out of memory";
        case ERR_INVALID: return "invalid argument";
        default:          return "unknown error";
    }
}

Error read_file(const char *path, char **out, size_t *out_len) {
    FILE *f = fopen(path, "rb");
    if (!f) return ERR_IO;
    // ... read, populate *out and *out_len ...
    fclose(f);
    return ERR_OK;
}
```

---

## 4. RAII in C++ with unique_ptr

Use `std::unique_ptr` to ensure resources are released even on exceptions.

```cpp
#include <memory>
#include <fstream>
#include <stdexcept>

std::string read_file(const std::string &path) {
    std::ifstream file(path, std::ios::binary);
    if (!file) throw std::runtime_error("Cannot open: " + path);

    return { std::istreambuf_iterator<char>(file),
             std::istreambuf_iterator<char>() };
}

// Custom deleter for C resources wrapped in unique_ptr
struct FILEDeleter { void operator()(FILE *f) const { if (f) fclose(f); } };
using UniqueFile = std::unique_ptr<FILE, FILEDeleter>;

UniqueFile open_safe(const char *path, const char *mode) {
    return UniqueFile(fopen(path, mode));
}
```

---

## 5. Struct Pattern (C)

Group related data into structs. Initialize explicitly — never use uninitialized struct fields.

```c
typedef struct {
    char   name[64];
    double amount;
    int    invoice_id;
} Invoice;

/* zero-initialize — all fields start at known state */
Invoice inv = {0};
snprintf(inv.name, sizeof(inv.name), "Acme Corp");
inv.amount     = 1234.56;
inv.invoice_id = 42;
```

---

## 6. Simple Makefile (Single-File Tools)

```makefile
CC      = gcc
CFLAGS  = -std=c17 -Wall -Wextra -Wpedantic -O2
TARGET  = my_tool
SRC     = main.c

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) -o $@ $^

clean:
	rm -f $(TARGET)

.PHONY: clean
```

---

## 7. AddressSanitizer and Valgrind

Run during development to catch memory errors before they reach production.

```bash
# AddressSanitizer (GCC / Clang — fast, compile-time instrumentation)
gcc -fsanitize=address,undefined -g -o my_tool main.c && ./my_tool

# Valgrind (slower but works on any binary)
valgrind --leak-check=full --error-exitcode=1 ./my_tool
```

Always fix ASan/Valgrind reports before shipping. "It runs fine" is not the same as "it is correct."

---

## 8. Anti-Patterns

| Anti-pattern | Problem | Fix |
|---|---|---|
| `strcpy(dst, src)` | Buffer overflow if `src` longer than `dst` | `strncpy` + manual null-terminate, or `snprintf` |
| `gets(buf)` | No bounds at all — always a vulnerability | `fgets(buf, sizeof(buf), stdin)` |
| `malloc` without checking NULL | Crash or corruption on OOM | `if (!ptr) { perror("malloc"); exit(EXIT_FAILURE); }` |
| Missing `fclose`/`free` | Resource leak | Use `goto cleanup` pattern in C or `unique_ptr` in C++ |
| `sprintf(buf, "%s", user_input)` | Buffer overflow or format string injection | `snprintf(buf, sizeof(buf), "%s", user_input)` |
| Returning pointer to local variable | Dangling pointer — undefined behavior | Return by value, heap-allocate, or use output parameter |
| `system("cmd " + user_input)` | Shell injection | `execv`/`execvp` with argument array |
| Casting `int` to pointer | UB on 64-bit | Use `intptr_t` / `uintptr_t` for pointer-sized integers |
