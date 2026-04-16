# Kotlin Builder

Use this reference for Android applications, JVM-based backend services, Gradle build scripts, and modern alternatives to Java in enterprise environments.

## Use It For

- Android applications (the primary language for new Android development)
- Backend services with Ktor or Spring Boot
- JVM command-line tools and scripts
- Gradle build logic in `build.gradle.kts`
- Multiplatform projects sharing code between Android and iOS (Kotlin Multiplatform)
- Replacing verbose Java code in existing JVM projects
- Data processing scripts on the JVM where Kotlin's syntax is cleaner than Java

## Default Approach

- Target **Kotlin 1.9+** and **JVM target 17+** for new projects.
- Use **Gradle with Kotlin DSL** (`build.gradle.kts`) for all new projects.
- Use **coroutines** (`kotlinx.coroutines`) for all async I/O — avoid blocking threads.
- Use **data classes** for DTOs and value objects — auto-generates `equals`, `hashCode`, `copy`, `toString`.
- Load secrets from environment variables — never hard-code credentials.
- Use the Kotlin standard library (`kotlin.io`, `kotlin.collections`) before adding third-party packages.

## Project Structure (Ktor API)

```
my-api/
  build.gradle.kts
  settings.gradle.kts
  src/
    main/kotlin/com/example/
      Application.kt
      routes/
      models/
      services/
    main/resources/
      application.conf
  test/kotlin/com/example/
```

## Quality Bar

- Enable `@file:Suppress` only with a comment explaining why — do not suppress null-safety warnings.
- Prefer `val` over `var` — immutability first.
- Use scope functions (`let`, `apply`, `run`, `also`) where they reduce nesting, but avoid chaining more than two.
- Use `sealed class` or `sealed interface` for exhaustive state modeling — pair with `when` expressions.
- In Android: use `ViewModel` + `StateFlow` for UI state; never update UI directly from background threads.

## What To Deliver

- Provide `build.gradle.kts` and `settings.gradle.kts` with exact dependency versions.
- Provide the exact build and run command (`./gradlew run`, `./gradlew assembleDebug`).
- For Android: state the `compileSdk`, `minSdk`, and target SDK versions.
- Explain environment variable or `local.properties` secret setup.

## Deep References

Load these when the task is non-trivial:

- [../patterns/kotlin-patterns.md](../patterns/kotlin-patterns.md) — Gradle Kotlin DSL skeleton, data class and sealed class idioms, coroutine launch/flow patterns, extension functions, `use` for resource cleanup, Ktor routing skeleton, anti-patterns.
