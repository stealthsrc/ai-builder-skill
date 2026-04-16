# Java Patterns

Load this reference when the task requires more than a trivial Java program. It provides reusable idioms for project setup, the Stream API, error handling, logging, and database access.

Pair with [../builders/java-builder.md](../builders/java-builder.md) for routing context and with [../rules/security-baseline.md](../rules/security-baseline.md) when the code handles secrets, database access, or external input.

---

## 1. Maven Skeleton

```xml
<!-- pom.xml -->
<project>
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.example</groupId>
  <artifactId>my-tool</artifactId>
  <version>1.0.0</version>

  <properties>
    <maven.compiler.source>21</maven.compiler.source>
    <maven.compiler.target>21</maven.compiler.target>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
  </properties>

  <dependencies>
    <dependency>
      <groupId>ch.qos.logback</groupId>
      <artifactId>logback-classic</artifactId>
      <version>1.5.6</version>
    </dependency>
  </dependencies>

  <build>
    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-compiler-plugin</artifactId>
        <version>3.13.0</version>
        <configuration><compilerArgs><arg>-Xlint:all</arg></compilerArgs></configuration>
      </plugin>
    </plugins>
  </build>
</project>
```

Build: `mvn package -q && java -jar target/my-tool-1.0.0.jar`

---

## 2. Stream API Idioms

```java
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

record Invoice(String id, String region, double amount) {}

// Group and sum
Map<String, Double> totalByRegion = invoices.stream()
    .filter(i -> i.amount() > 0)
    .collect(Collectors.groupingBy(
        Invoice::region,
        Collectors.summingDouble(Invoice::amount)
    ));

// Top 5 by amount
List<Invoice> top5 = invoices.stream()
    .sorted(Comparator.comparingDouble(Invoice::amount).reversed())
    .limit(5)
    .toList();  // Java 16+ — unmodifiable list
```

---

## 3. Optional Instead of Null Returns

```java
import java.util.Optional;

Optional<Invoice> findById(List<Invoice> invoices, String id) {
    return invoices.stream()
        .filter(i -> i.id().equals(id))
        .findFirst();
}

// Caller
findById(invoices, "INV-001")
    .map(Invoice::amount)
    .ifPresentOrElse(
        amount -> System.out.printf("Amount: %.2f%n", amount),
        () -> System.out.println("Invoice not found")
    );
```

---

## 4. Try-With-Resources

All `Closeable` resources (files, connections, streams) must use try-with-resources.

```java
import java.io.*;
import java.nio.file.*;
import java.nio.charset.StandardCharsets;

List<String> readLines(Path path) throws IOException {
    try (var reader = Files.newBufferedReader(path, StandardCharsets.UTF_8)) {
        return reader.lines().toList();
    }
}

void writeCsv(Path path, List<String[]> rows) throws IOException {
    try (var writer = Files.newBufferedWriter(path, StandardCharsets.UTF_8)) {
        for (var row : rows) {
            writer.write(String.join(",", row));
            writer.newLine();
        }
    }
}
```

---

## 5. Logging with SLF4J and Logback

```java
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class ReportService {
    private static final Logger log = LoggerFactory.getLogger(ReportService.class);

    public void run(List<Invoice> invoices) {
        log.info("Processing {} invoices", invoices.size());
        try {
            // ... work ...
            log.info("Done.");
        } catch (IOException e) {
            log.error("Failed to write report: {}", e.getMessage(), e);
            throw new RuntimeException("Report generation failed", e);
        }
    }
}
```

---

## 6. JDBC Safe Parameterized Queries

```java
import java.sql.*;

List<Invoice> queryByRegion(Connection conn, String region) throws SQLException {
    // ✓ Always use PreparedStatement — never string concatenation
    String sql = "SELECT id, region, amount FROM invoices WHERE region = ? AND amount > ?";
    try (var stmt = conn.prepareStatement(sql)) {
        stmt.setString(1, region);
        stmt.setDouble(2, 0.0);
        try (var rs = stmt.executeQuery()) {
            var result = new java.util.ArrayList<Invoice>();
            while (rs.next()) {
                result.add(new Invoice(rs.getString("id"), rs.getString("region"), rs.getDouble("amount")));
            }
            return result;
        }
    }
}
```

---

## 7. Environment Variable Loading

```java
static String requireEnv(String name) {
    String value = System.getenv(name);
    if (value == null || value.isBlank()) {
        throw new IllegalStateException("Required environment variable not set: " + name);
    }
    return value;
}

// At startup — fail fast before doing any work
String apiKey  = requireEnv("API_KEY");
String baseUrl = requireEnv("BASE_URL");
```

---

## 8. Anti-Patterns

| Anti-pattern | Problem | Fix |
|---|---|---|
| `catch (Exception e) {}` | Silently swallows errors | Log and rethrow, or return `Optional`/result type |
| `ResultSet` outside try-with-resources | Connection leak | Always close in try-with-resources |
| String concatenation in SQL | SQL injection | `PreparedStatement` with `?` placeholders |
| `System.out.println` for logs | No levels, no timestamps | `Logger` from SLF4J |
| `new File(userInput)` without validation | Path traversal | Resolve against a known base path and verify prefix |
| Returning `null` from methods | `NullPointerException` at call sites | `Optional<T>` for absent values |
| Unboxing `Integer` without null check | `NullPointerException` | Use primitive `int` or check `!= null` |
