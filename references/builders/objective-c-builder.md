# Objective-C Builder

Use this reference for maintaining and extending existing Objective-C iOS or macOS codebases. For new development, use the Swift builder instead.

## Use It For

- Maintaining legacy iOS or macOS apps written in Objective-C
- Extending Objective-C frameworks or SDKs that have not been migrated
- Writing Objective-C wrappers around C libraries for use in Swift projects
- CocoaPods-based projects where existing pods are Objective-C

## Prefer Swift for New Code

Objective-C is the predecessor to Swift on Apple platforms. Apple actively encourages migration. For any new iOS or macOS feature, component, or app:

- Use the [Swift builder](swift-builder.md) instead.
- Swift and Objective-C interoperate in the same project — new Swift files can call existing Objective-C code.
- Incremental migration: add new features in Swift, migrate old Objective-C modules over time.

## Working With Legacy Objective-C

- Enable ARC (Automatic Reference Counting) — do not write manual `retain`/`release` unless maintaining very old code.
- Use `nullability` annotations (`_Nullable`, `_Nonnull`) on all declarations to improve Swift interoperability.
- Use modern Objective-C literals (`@"string"`, `@[]`, `@{}`).
- Prefer `NSError **` error out-parameters over exception throwing.
- Keep `.h` header files minimal — expose only what callers need.

## Interop With Swift

- Add a bridging header (`ProjectName-Bridging-Header.h`) to expose Objective-C APIs to Swift.
- Add `@objc` and `@objcMembers` annotations to Swift classes that need to be callable from Objective-C.
- Import Swift-generated headers with `#import "ModuleName-Swift.h"` in Objective-C files.

## What To Deliver

- State whether ARC is enabled.
- Explain where the code goes (`.m` implementation file, `.h` header, or category extension).
- For mixed projects: explain the bridging header setup.
