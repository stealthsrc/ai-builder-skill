# Swift Builder

Use this reference for iOS and macOS applications, SwiftUI interfaces, command-line tools on macOS, and automation via Shortcuts or Swift scripts.

## Use It For

- iOS and iPadOS apps with SwiftUI or UIKit
- macOS apps with SwiftUI or AppKit
- Command-line tools compiled with Swift Package Manager
- macOS Shortcuts actions and App Intents
- watchOS and tvOS apps
- Server-side Swift with Vapor or Hummingbird
- Replacing AppleScript or shell scripts for macOS automation with typed Swift code

## Default Approach

- Target **Swift 5.9+** (Xcode 15+) for new projects; use **SwiftUI** for all new UI unless UIKit is required for a specific control.
- Use **Swift Package Manager** for CLI tools and libraries — avoid CocoaPods for new projects.
- Use `async`/`await` throughout — avoid callback chains and NotificationCenter where structured concurrency applies.
- Use `Codable` for all JSON serialization and deserialization.
- Load secrets from the Keychain, not from `UserDefaults` or hardcoded strings.

## Project Structure (CLI Tool)

```
MyTool/
  Package.swift
  Sources/
    MyTool/
      main.swift
      Commands/
      Models/
  Tests/
    MyToolTests/
```

## Quality Bar

- Enable strict concurrency checking (`-strict-concurrency=complete`) for Swift 6 readiness.
- Use `guard let` for early exit on optional unwrapping — avoid force-unwrap (`!`) outside of tests.
- Prefer `enum` with associated values over boolean flags for state.
- Handle all `throws` — never use `try!` in production paths.
- Use `Task` and structured concurrency (`async let`, `TaskGroup`) rather than `DispatchQueue` for new code.

## Safety And Practicality

- Never store sensitive data (tokens, passwords) in `UserDefaults` — use the Keychain via `Security.framework` or a wrapper like `KeychainAccess`.
- Validate URL components before constructing `URLRequest` — malformed URLs crash at runtime.
- For file access on macOS: respect the sandbox by using `NSOpenPanel` or security-scoped bookmarks rather than arbitrary path access.

## What To Deliver

- State the minimum OS version and Xcode version required.
- For CLI tools: provide the exact `swift build` and run commands.
- For iOS/macOS apps: describe the Xcode setup steps and any capability flags needed (entitlements, privacy strings).
- List any package dependencies from `Package.swift` with their URLs and versions.

## Deep References

Load these when the task is non-trivial:

- [../patterns/swift-patterns.md](../patterns/swift-patterns.md) — Package.swift skeleton, SwiftUI view structure, `async`/`await` URLSession idioms, `Codable` JSON patterns, `FileManager` safe file operations, `ArgumentParser` CLI, anti-patterns.
