# Swift Patterns

Load this reference when the task requires more than a trivial Swift program. It provides reusable idioms for Package.swift CLI tools, SwiftUI views, async/await networking, Codable JSON, and safe file operations.

Pair with [../builders/swift-builder.md](../builders/swift-builder.md) for routing context.

---

## 1. Package.swift CLI Skeleton

```swift
// Package.swift
// swift-tools-version: 5.9
import PackageDescription

let package = Package(
    name: "my-tool",
    platforms: [.macOS(.v13)],
    dependencies: [
        .package(url: "https://github.com/apple/swift-argument-parser", from: "1.3.0"),
    ],
    targets: [
        .executableTarget(
            name: "my-tool",
            dependencies: [
                .product(name: "ArgumentParser", package: "swift-argument-parser"),
            ]
        ),
    ]
)
```

Build: `swift build -c release && .build/release/my-tool`

---

## 2. ArgumentParser CLI

```swift
import ArgumentParser
import Foundation

@main
struct MyTool: AsyncParsableCommand {
    static let configuration = CommandConfiguration(
        commandName: "my-tool",
        abstract: "Process CSV files and generate a report."
    )

    @Argument(help: "Input CSV file.") var inputPath: String
    @Option(name: .shortAndLong, help: "Output file.") var output: String = "report.json"
    @Flag(name: .shortAndLong, help: "Dry run — no output written.") var dryRun = false

    func run() async throws {
        let url = URL(fileURLWithPath: inputPath)
        guard FileManager.default.fileExists(atPath: inputPath) else {
            throw ValidationError("File not found: \(inputPath)")
        }
        // ... work ...
    }
}
```

---

## 3. async/await URLSession

```swift
import Foundation

struct APIClient {
    let baseURL: URL
    let apiKey: String
    private let session = URLSession.shared

    func fetch<T: Decodable>(_ path: String, as type: T.Type) async throws -> T {
        var request = URLRequest(url: baseURL.appending(path: path))
        request.setValue("Bearer \(apiKey)", forHTTPHeaderField: "Authorization")
        request.timeoutInterval = 15

        let (data, response) = try await session.data(for: request)
        guard let http = response as? HTTPURLResponse, (200..<300).contains(http.statusCode) else {
            throw URLError(.badServerResponse)
        }
        return try JSONDecoder().decode(type, from: data)
    }
}
```

---

## 4. Codable JSON Pattern

```swift
import Foundation

struct Invoice: Codable {
    let id: String
    let region: String
    let amount: Double
    let date: Date

    enum CodingKeys: String, CodingKey {
        case id, region, amount
        case date = "invoice_date"  // map snake_case JSON key
    }
}

let decoder = JSONDecoder()
decoder.dateDecodingStrategy = .iso8601

let encoder = JSONEncoder()
encoder.dateEncodingStrategy = .iso8601
encoder.outputFormatting = [.prettyPrinted, .sortedKeys]

let invoices = try decoder.decode([Invoice].self, from: data)
let json     = try encoder.encode(invoices)
```

---

## 5. FileManager Safe File Operations

```swift
import Foundation

let fm = FileManager.default

// Create directory if needed
let outputDir = URL(fileURLWithPath: "output")
try fm.createDirectory(at: outputDir, withIntermediateDirectories: true)

// Safe write (atomic)
let outputFile = outputDir.appending(path: "report.json")
try json.write(to: outputFile, options: .atomic)

// Check existence before reading
guard fm.fileExists(atPath: inputPath) else {
    throw CocoaError(.fileNoSuchFile)
}
let data = try Data(contentsOf: URL(fileURLWithPath: inputPath))
```

---

## 6. SwiftUI View Structure

```swift
import SwiftUI

struct InvoiceListView: View {
    @StateObject private var viewModel = InvoiceViewModel()

    var body: some View {
        NavigationStack {
            List(viewModel.invoices) { invoice in
                InvoiceRow(invoice: invoice)
            }
            .navigationTitle("Invoices")
            .toolbar {
                Button("Refresh") { Task { await viewModel.load() } }
            }
            .overlay { if viewModel.isLoading { ProgressView() } }
            .alert("Error", isPresented: .constant(viewModel.error != nil)) {
                Button("OK") { viewModel.error = nil }
            } message: {
                Text(viewModel.error ?? "")
            }
        }
        .task { await viewModel.load() }
    }
}

@MainActor
class InvoiceViewModel: ObservableObject {
    @Published var invoices: [Invoice] = []
    @Published var isLoading = false
    @Published var error: String?

    func load() async {
        isLoading = true
        defer { isLoading = false }
        do {
            invoices = try await APIClient(baseURL: baseURL, apiKey: apiKey).fetch("/invoices", as: [Invoice].self)
        } catch {
            self.error = error.localizedDescription
        }
    }
}
```

---

## 7. Anti-Patterns

| Anti-pattern | Problem | Fix |
|---|---|---|
| Force-unwrap `!` in production | Crash on nil without context | `guard let` or `if let` with a fallback |
| `try!` | Crash on any error | `try` inside `do/catch` |
| `DispatchQueue.global().async` for new code | Callback pyramid; no structured lifetime | `Task { }` with `async`/`await` |
| Storing secrets in `UserDefaults` | Plaintext on disk, readable by other apps | Keychain via `Security.framework` |
| `@ObservedObject` on a view-owned object | Lifetime mismatch — object recreated on each view init | `@StateObject` for objects owned by the view |
| `NotificationCenter` for inter-view data | Implicit coupling, hard to test | `@EnvironmentObject` or dependency injection |
