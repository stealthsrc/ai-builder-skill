# Kotlin Patterns

Load this reference when the task requires more than a trivial Kotlin program. It provides reusable idioms for Gradle builds, coroutines, data classes, extension functions, and Ktor APIs.

Pair with [../builders/kotlin-builder.md](../builders/kotlin-builder.md) for routing context.

---

## 1. Gradle Kotlin DSL Skeleton

```kotlin
// build.gradle.kts
plugins {
    kotlin("jvm") version "1.9.24"
    application
}

group   = "com.example"
version = "1.0.0"

repositories { mavenCentral() }

dependencies {
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.8.1")
    implementation("com.github.ajalt.clikt:clikt:4.4.0")
    implementation("com.github.doyaaaaaken:kotlin-csv-jvm:1.9.3")
    testImplementation(kotlin("test"))
}

application { mainClass.set("com.example.MainKt") }

tasks.test { useJUnitPlatform() }
```

---

## 2. Data Class and Sealed Class

```kotlin
// Immutable data object with auto-generated equals/hashCode/copy/toString
data class Invoice(
    val id:     String,
    val region: String,
    val amount: Double,
    val date:   String,
)

// Sealed class for exhaustive state modeling
sealed class Result<out T> {
    data class  Success<T>(val value: T) : Result<T>()
    data class  Failure(val error: Throwable) : Result<Nothing>()
    data object Loading : Result<Nothing>()
}

// when is exhaustive — compiler error if a case is missing
fun handleResult(result: Result<List<Invoice>>) = when (result) {
    is Result.Success -> println("Loaded ${result.value.size} invoices")
    is Result.Failure -> println("Error: ${result.error.message}")
    Result.Loading    -> println("Loading...")
}
```

---

## 3. Coroutine Patterns

```kotlin
import kotlinx.coroutines.*
import kotlinx.coroutines.flow.*

// Launch a coroutine and handle errors
fun main() = runBlocking {
    val job = launch(Dispatchers.IO) {
        try {
            processInvoices()
        } catch (e: CancellationException) {
            throw e  // always rethrow CancellationException
        } catch (e: Exception) {
            println("Error: ${e.message}")
        }
    }
    job.join()
}

// Flow for reactive data streams
fun invoiceFlow(): Flow<Invoice> = flow {
    val invoices = fetchFromApi()
    invoices.forEach { emit(it) }
}.flowOn(Dispatchers.IO)

// Collect in a coroutine
invoiceFlow()
    .filter { it.amount > 0 }
    .map    { it.copy(region = it.region.uppercase()) }
    .collect { println(it) }
```

---

## 4. Extension Functions

```kotlin
// Add behavior to existing types without subclassing
fun String.toInvoiceId(): String = "INV-${this.padStart(6, '0')}"
fun Double.toEuroString(): String = "€%.2f".format(this)
fun List<Invoice>.totalRevenue(): Double = sumOf { it.amount }

// Usage
println("42".toInvoiceId())          // INV-000042
println(1234.5.toEuroString())        // €1234.50
println(invoices.totalRevenue())
```

---

## 5. Resource Cleanup with use

```kotlin
import java.io.File

fun readCsv(path: String): List<Invoice> =
    File(path).bufferedReader().use { reader ->
        reader.lineSequence()
            .drop(1)  // skip header
            .mapNotNull { line ->
                val cols = line.split(',')
                if (cols.size < 4) null
                else Invoice(cols[0].trim(), cols[1].trim(), cols[2].toDouble(), cols[3].trim())
            }
            .toList()
    }
```

---

## 6. Ktor Minimal API

```kotlin
import io.ktor.server.application.*
import io.ktor.server.engine.*
import io.ktor.server.netty.*
import io.ktor.server.routing.*
import io.ktor.server.response.*
import io.ktor.server.plugins.contentnegotiation.*
import io.ktor.serialization.kotlinx.json.*

fun main() {
    embeddedServer(Netty, port = 8080) {
        install(ContentNegotiation) { json() }
        routing {
            get("/invoices") {
                val region = call.parameters["region"] ?: ""
                call.respond(InvoiceService.findByRegion(region))
            }
            get("/health") { call.respondText("ok") }
        }
    }.start(wait = true)
}
```

---

## 7. Anti-Patterns

| Anti-pattern | Problem | Fix |
|---|---|---|
| `var` for state that never changes | Mutability without reason | `val` by default |
| `!!` (non-null assertion) in production | `NullPointerException` on null | `?.let { }`, `?: default`, or `require(x != null)` |
| Blocking I/O on `Dispatchers.Main` | Freezes UI / blocks coroutine scheduler | `withContext(Dispatchers.IO) { ... }` |
| Catching `CancellationException` without rethrowing | Prevents coroutine cancellation | Always `throw e` after catching `CancellationException` |
| Scope functions chained 3+ levels deep | Unreadable nesting | Extract to named functions |
| `Thread.sleep` in a coroutine | Blocks the thread | `delay(ms)` — non-blocking coroutine sleep |
| Data class with mutable list fields | `copy()` shares the list reference | Use `List<T>` (read-only view) or copy explicitly |
