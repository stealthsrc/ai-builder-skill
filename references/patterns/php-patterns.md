# PHP Patterns

Load this reference when the task requires more than a trivial PHP script. It provides reusable idioms for project setup, database access, input validation, error handling, and configuration.

Pair with [../builders/php-builder.md](../builders/php-builder.md) for routing context and with [../rules/security-baseline.md](../rules/security-baseline.md) for database access, user input handling, and file uploads.

---

## 1. Script Skeleton with Strict Types

```php
<?php
declare(strict_types=1);

require __DIR__ . '/vendor/autoload.php';

use Dotenv\Dotenv;

$dotenv = Dotenv::createImmutable(__DIR__);
$dotenv->load();
$dotenv->required(['DB_DSN', 'DB_USER', 'DB_PASS', 'API_KEY']);

function requireEnv(string $name): string {
    $value = $_ENV[$name] ?? '';
    if ($value === '') throw new RuntimeException("Missing env var: {$name}");
    return $value;
}

try {
    run();
} catch (Throwable $e) {
    error_log("[ERROR] " . $e->getMessage());
    fwrite(STDERR, "Error: " . $e->getMessage() . PHP_EOL);
    exit(1);
}

function run(): void {
    // ... main logic ...
}
```

---

## 2. PDO Prepared Statements

Always use PDO with prepared statements. Never concatenate user input into SQL.

```php
function getConnection(): PDO {
    $dsn  = requireEnv('DB_DSN');   // e.g. "mysql:host=localhost;dbname=mydb;charset=utf8mb4"
    $user = requireEnv('DB_USER');
    $pass = requireEnv('DB_PASS');

    return new PDO($dsn, $user, $pass, [
        PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
        PDO::ATTR_EMULATE_PREPARES   => false,
    ]);
}

// ✓ Safe: parameterized
function findInvoicesByRegion(PDO $pdo, string $region): array {
    $stmt = $pdo->prepare(
        'SELECT id, region, amount FROM invoices WHERE region = :region AND amount > 0'
    );
    $stmt->execute([':region' => $region]);
    return $stmt->fetchAll();
}

// ✗ Never: SQL injection
// $pdo->query("SELECT * FROM invoices WHERE region = '{$region}'");
```

---

## 3. Input Validation

```php
function validateInvoiceId(string $raw): string {
    $clean = trim($raw);
    if (!preg_match('/^INV-\d{4,10}$/', $clean)) {
        throw new InvalidArgumentException("Invalid invoice ID: {$clean}");
    }
    return $clean;
}

// For web forms — always sanitize before output
function safeOutput(string $value): string {
    return htmlspecialchars($value, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
}

// For numeric input
function positiveInt(mixed $raw): int {
    $n = filter_var($raw, FILTER_VALIDATE_INT);
    if ($n === false || $n <= 0) throw new InvalidArgumentException("Expected positive integer");
    return $n;
}
```

---

## 4. Error Logging

```php
// Log to file — never echo errors to the browser in production
ini_set('log_errors', '1');
ini_set('error_log', __DIR__ . '/logs/app.log');
ini_set('display_errors', '0');

// Custom logging helper
function appLog(string $level, string $message, array $context = []): void {
    $line = sprintf(
        "[%s] [%s] %s %s\n",
        date('Y-m-d H:i:s'),
        strtoupper($level),
        $message,
        $context ? json_encode($context) : ''
    );
    file_put_contents(__DIR__ . '/logs/app.log', $line, FILE_APPEND);
}
```

---

## 5. CSV Read and Write

```php
// Read CSV with headers
function readCsv(string $path): array {
    $rows = [];
    if (($handle = fopen($path, 'r')) === false) {
        throw new RuntimeException("Cannot open file: {$path}");
    }
    $headers = fgetcsv($handle);
    if ($headers === false) { fclose($handle); return []; }

    while (($row = fgetcsv($handle)) !== false) {
        $rows[] = array_combine($headers, $row);
    }
    fclose($handle);
    return $rows;
}

// Write CSV
function writeCsv(string $path, array $rows, array $headers): void {
    $handle = fopen($path, 'w');
    if (!$handle) throw new RuntimeException("Cannot write: {$path}");
    // UTF-8 BOM for Excel compatibility
    fwrite($handle, "\xEF\xBB\xBF");
    fputcsv($handle, $headers);
    foreach ($rows as $row) fputcsv($handle, $row);
    fclose($handle);
}
```

---

## 6. HTTP Client with cURL

```php
function httpGet(string $url, string $token, int $timeoutSec = 15): array {
    $ch = curl_init();
    curl_setopt_array($ch, [
        CURLOPT_URL            => $url,
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_TIMEOUT        => $timeoutSec,
        CURLOPT_HTTPHEADER     => ["Authorization: Bearer {$token}", "Accept: application/json"],
        CURLOPT_FAILONERROR    => false,
    ]);
    $body = curl_exec($ch);
    $code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $err  = curl_error($ch);
    curl_close($ch);

    if ($body === false) throw new RuntimeException("cURL error: {$err}");
    if ($code < 200 || $code >= 300) throw new RuntimeException("HTTP {$code}: " . substr($body, 0, 200));
    return json_decode($body, true, 512, JSON_THROW_ON_ERROR);
}
```

---

## 7. Anti-Patterns

| Anti-pattern | Problem | Fix |
|---|---|---|
| Missing `declare(strict_types=1)` | Silent type coercion | Add to every file |
| `$_GET`/`$_POST` directly in SQL | SQL injection | PDO prepared statements |
| `echo $userInput` | XSS | `htmlspecialchars()` before output |
| `mysql_*` functions | Deprecated and removed | Use PDO or MySQLi |
| `die()` / `exit()` with stack trace | Exposes internals | Log internally, show generic error |
| `include($userInput)` | Remote/local file inclusion | Never include user-controlled paths |
| Passwords in plaintext | Credential exposure | `password_hash()` / `password_verify()` |
| No `PDO::ATTR_EMULATE_PREPARES => false` | Emulated prepares do not prevent all injection | Set `false` explicitly |
