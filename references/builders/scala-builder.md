# Scala Builder

Use this reference for big data processing with Apache Spark, functional programming on the JVM, Play Framework web applications, and projects that mix functional and object-oriented design.

## Use It For

- Apache Spark data processing and ETL jobs
- Functional data pipelines with ZIO, Cats Effect, or FS2
- Play Framework or http4s web services
- Type-safe command-line tools with Decline or Scallop
- Kafka consumers and producers with fs2-kafka or Alpakka
- Akka actor-based distributed systems
- Migrating complex Java logic to a more expressive JVM language

## Default Approach

- Target **Scala 3** for new projects — Scala 2 only for existing codebases.
- Use **sbt** for project management; use Mill as an alternative for simpler builds.
- Use **ZIO 2** or **Cats Effect 3** for effect-based concurrency in new projects.
- Use **case classes** for data; use **sealed traits** with `enum` for algebraic data types.
- Load secrets from environment variables — never hard-code credentials in source.

## Project Structure

```
my-app/
  build.sbt
  project/
    build.properties   ← sbt version
    plugins.sbt
  src/
    main/scala/com/example/
      Main.scala
      services/
      models/
    test/scala/com/example/
```

## Quality Bar

- Enable `-Xfatal-warnings` in `scalacOptions` — all warnings become errors.
- Prefer `Option`, `Either`, and effect types over throwing exceptions in library code.
- Use pattern matching exhaustively — `sealed` + `case` + `match` prevents unhandled cases at compile time.
- Avoid `null` — use `Option` or effect types for absent values.
- For Spark: use `Dataset[T]` over untyped `DataFrame` for compile-time column safety.

## What To Deliver

- Provide `build.sbt` with exact library versions.
- Provide the exact build and run command (`sbt run`, `sbt assembly` for fat jars).
- For Spark jobs: explain how to submit (`spark-submit`) and cluster vs local mode.
- State the Scala version and JVM target in `build.sbt`.

## Deep References

Load these when the task is non-trivial:

- [../patterns/scala-patterns.md](../patterns/scala-patterns.md) — `build.sbt` skeleton, case class and sealed trait idioms, `Option`/`Either` error handling, ZIO effect skeleton, Spark `Dataset` pipeline basics, anti-patterns.
