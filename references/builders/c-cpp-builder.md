# C and C++ Builder

Use this reference for systems programming, embedded targets, performance-critical tools, command-line utilities, and any task that requires direct hardware access or maximum runtime performance.

## Use It For

- Command-line tools and system utilities that need near-zero overhead
- Embedded systems and microcontroller firmware (Arduino, STM32, ESP32)
- Game engines, graphics, and real-time systems
- Operating system components, drivers, and kernel-adjacent code
- High-performance data processing where Python or Node are too slow
- Interfacing with C libraries from other languages (FFI targets)
- Existing C or C++ codebases that need extension or maintenance

## When To Choose C vs C++

- **C**: simple procedural tools, embedded targets with limited runtime, maximum ABI compatibility, strict memory constraints
- **C++**: object-oriented or generic design, STL containers, modern RAII memory management, large codebases

## Default Approach

- Target **C17** or **C++17** unless the user specifies a constraint (embedded target, MSVC version, etc.).
- Use **CMake** for cross-platform builds; use a plain Makefile only for small single-file tools.
- Enable warnings: `-Wall -Wextra -Wpedantic` for GCC/Clang. Treat warnings as errors in new code.
- Use `valgrind` or AddressSanitizer (`-fsanitize=address`) to catch memory errors in development.
- Prefer stack allocation and RAII over raw `malloc`/`free` in C++.

## Memory Safety Rules

- In C: every `malloc` must have a paired `free`; every file opened must be closed.
- In C: never access memory past the end of a buffer — validate sizes before `memcpy`, `strcpy`, or `sprintf`.
- In C++: prefer `std::string`, `std::vector`, `std::unique_ptr`, and `std::array` over raw pointers and arrays.
- Never return a pointer to a local variable.
- Zero-initialize buffers before use when the content is sensitive.

## What To Deliver

- State the C standard or C++ standard being targeted.
- Provide a `CMakeLists.txt` or Makefile with the exact build commands.
- Show how to compile and run on the user's platform (Linux, macOS, Windows/MSVC or MinGW).
- State any external library dependencies (include install command).
- For embedded targets, state the toolchain, board, and flash command.

## Deep References

Load these when the task is non-trivial:

- [../patterns/c-cpp-patterns.md](../patterns/c-cpp-patterns.md) — CMake skeleton, safe string handling, struct idioms, error codes, RAII in C++, Makefile basics, AddressSanitizer, anti-patterns.
