# Java Builder

Use this reference for enterprise applications, Android apps, Spring Boot microservices, command-line tools, and batch processing jobs that run on the JVM.

## Use It For

- Spring Boot REST APIs and microservices
- Android applications (paired with Kotlin for new code, Java for legacy)
- Command-line tools and batch jobs with complex logic
- Enterprise integrations (JMS, SOAP, JDBC, JPA/Hibernate)
- Cross-platform desktop apps with JavaFX or Swing
- Data processing pipelines where the JVM ecosystem is already in use
- Maintaining or extending existing Java codebases

## Default Approach

- Target **Java 21 LTS** for new projects unless the environment constrains an older version.
- Use **Maven** or **Gradle** (Gradle with Kotlin DSL for new projects).
- Prefer **Spring Boot 3.x** for web or service work — avoid building HTTP servers from scratch.
- Use `var` for local type inference where it improves readability.
- Load secrets from environment variables or Spring's `@Value` + `application.properties` — never hard-code credentials.
- Use try-with-resources for all `Closeable` resources.

## Project Structure (Maven)

```
my-tool/
  pom.xml
  src/
    main/
      java/com/example/
        Main.java
        service/
        model/
      resources/
        application.properties
    test/
      java/com/example/
```

## Quality Bar

- Enable warnings with `-Xlint:all` in the Maven compiler plugin.
- Use `Optional<T>` instead of returning `null` from methods.
- Use `Stream` API for collection transformations — avoid imperative loops when the stream is cleaner.
- Never swallow exceptions with an empty `catch` block.
- Validate external input (REST request bodies, CLI args, CSV data) at the entry point.

## What To Deliver

- Provide `pom.xml` or `build.gradle.kts` with exact dependency versions.
- Provide the exact build and run commands (`mvn package && java -jar target/...jar`).
- Explain any environment variable or property file setup.
- State the minimum Java version required.

## Deep References

Load these when the task is non-trivial:

- [../patterns/java-patterns.md](../patterns/java-patterns.md) — Maven project skeleton, Stream API idioms, Optional usage, try-with-resources, logging with SLF4J and Logback, `@SpringBootApplication` minimal setup, JDBC safe queries, anti-patterns.
