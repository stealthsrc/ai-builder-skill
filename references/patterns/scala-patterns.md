# Scala Patterns

Load this reference when the task requires more than a trivial Scala program. It provides reusable idioms for sbt builds, functional data modeling, Option/Either error handling, and Spark pipelines.

Pair with [../builders/scala-builder.md](../builders/scala-builder.md) for routing context.

---

## 1. sbt Skeleton (Scala 3)

```scala
// build.sbt
ThisBuild / scalaVersion := "3.4.2"
ThisBuild / version      := "0.1.0"

lazy val root = project.in(file("."))
  .settings(
    name := "my-tool",
    libraryDependencies ++= Seq(
      "com.monovore" %% "decline"   % "2.4.1",
      "co.fs2"       %% "fs2-core"  % "3.10.2",
      "co.fs2"       %% "fs2-io"    % "3.10.2",
      "org.typelevel" %% "cats-effect" % "3.5.4",
    ),
    scalacOptions ++= Seq("-Xfatal-warnings", "-deprecation", "-feature"),
  )
```

Run: `sbt run` or `sbt assembly` for a fat JAR.

---

## 2. Case Class and Enum (Scala 3)

```scala
// Immutable data object
case class Invoice(
  id:     String,
  region: String,
  amount: Double,
  date:   java.time.LocalDate,
)

// Sealed enum for exhaustive state
enum ProcessResult:
  case Success(invoice: Invoice)
  case Failure(id: String, reason: String)
  case Skipped(id: String)

def describe(r: ProcessResult): String = r match
  case ProcessResult.Success(inv) => s"OK: ${inv.id} (${inv.amount})"
  case ProcessResult.Failure(id, reason) => s"FAIL: $id — $reason"
  case ProcessResult.Skipped(id) => s"SKIP: $id"
```

---

## 3. Option and Either Error Handling

```scala
def parseAmount(s: String): Option[Double] =
  s.toDoubleOption.filter(_ > 0)

def loadInvoice(id: String): Either[String, Invoice] =
  if id.startsWith("INV-") then Right(Invoice(id, "West", 100.0, java.time.LocalDate.now()))
  else Left(s"Invalid invoice ID: $id")

// Chain with for-comprehension
val result: Either[String, Double] = for
  invoice <- loadInvoice("INV-001")
  amount  <- Either.cond(invoice.amount > 0, invoice.amount, "Amount must be positive")
yield amount * 1.1  // apply 10% markup
```

---

## 4. Collections and Higher-Order Functions

```scala
val invoices: List[Invoice] = loadAll()

// Filter, group, aggregate
val totalByRegion: Map[String, Double] =
  invoices
    .filter(_.amount > 0)
    .groupBy(_.region)
    .map((region, invs) => region -> invs.map(_.amount).sum)

// Top 5 by amount
val top5: List[Invoice] =
  invoices.sortBy(-_.amount).take(5)

// Partition into valid and invalid
val (valid, invalid) = invoices.partition(_.amount > 0)
```

---

## 5. Spark Dataset Pipeline

```scala
import org.apache.spark.sql.{SparkSession, Dataset}
import org.apache.spark.sql.functions._

object RevenueReport:
  def run(spark: SparkSession, inputPath: String, outputPath: String): Unit =
    import spark.implicits._

    val invoices: Dataset[Invoice] = spark.read
      .option("header", "true")
      .option("inferSchema", "true")
      .csv(inputPath)
      .as[Invoice]

    val summary = invoices
      .filter($"amount" > 0)
      .groupBy($"region")
      .agg(
        count("*").as("order_count"),
        sum("amount").as("total_revenue"),
        avg("amount").as("avg_amount"),
      )
      .orderBy($"total_revenue".desc)

    summary.write
      .mode("overwrite")
      .option("header", "true")
      .csv(outputPath)

    println(s"Written to $outputPath")
```

---

## 6. Resource Safety with Cats Effect

```scala
import cats.effect.*
import fs2.*
import fs2.io.file.*

object CsvProcessor extends IOApp.Simple:
  val run: IO[Unit] =
    Files[IO].readAll(Path("invoices.csv"))
      .through(text.utf8.decode)
      .through(text.lines)
      .drop(1)  // skip header
      .filter(_.nonEmpty)
      .map(parseLine)
      .evalMap(processRow)
      .compile
      .drain
      .handleErrorWith(e => IO.println(s"Error: ${e.getMessage}"))
```

---

## 7. Anti-Patterns

| Anti-pattern | Problem | Fix |
|---|---|---|
| `null` values | `NullPointerException` at runtime | `Option[T]` for absent values |
| `throw` in library code | Forces callers to handle exceptions | Return `Either[Error, T]` or `IO[T]` |
| `return` inside functions | Breaks functional composition | Structure as expressions; use `yield` |
| `var` for mutable state | Shared mutable state in concurrent code | `val` + immutable data + `Ref[IO, T]` |
| Missing `-Xfatal-warnings` | Warnings silently accumulate | Enable in `scalacOptions` |
| Collecting Spark results with `.collect()` on large data | OOM — loads all rows to driver | Use `.write` or limit with `.take(n)` |
| Raw `Future` without `ExecutionContext` | Implicit EC confusion | Use Cats Effect `IO` or ZIO for explicit scheduling |
