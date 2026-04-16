# PHP Builder

Use this reference for web backends, WordPress and Laravel customization, server-side scripts, and automation tasks that run on a PHP stack.

## Use It For

- Laravel or Symfony web applications and APIs
- WordPress plugin and theme customization
- Server-side scripts for form processing, report generation, or scheduled jobs
- REST API backends for internal tools
- Legacy PHP system maintenance and hardening
- CLI scripts with the PHP CLI (no web server required)
- Simple web pages with embedded PHP when a full framework is overkill

## Default Approach

- Target **PHP 8.2+** for new projects — use typed properties, enums, named arguments, and fibers where applicable.
- Use **Composer** for dependency management. Never commit `vendor/`.
- Use a framework (Laravel, Symfony, Slim) for anything beyond a simple script.
- Load secrets from environment variables (via `$_ENV` or `getenv()`) or a `.env` file via `vlucas/phpdotenv` — never hard-code credentials in source.
- Use PDO with prepared statements for all database queries — never string-concatenated SQL.

## Quality Bar

- Enable strict types: `declare(strict_types=1);` at the top of every file.
- Type-hint all function parameters and return values.
- Use `try`/`catch` with specific exception types — never catch `\Throwable` and do nothing.
- Validate and sanitize all user input: `filter_input()`, `htmlspecialchars()`, or a validation library.
- Never display raw error messages to end users — log to a file, show a generic message.

## Safety And Practicality

- SQL injection: always use PDO prepared statements.
- XSS: always `htmlspecialchars($value, ENT_QUOTES, 'UTF-8')` before echoing user content.
- CSRF: use a token for all state-mutating forms.
- File uploads: validate MIME type from file content (not the browser-supplied type), store outside the web root.
- Do not expose stack traces or `phpinfo()` in production.

## What To Deliver

- Provide `composer.json` with exact package versions.
- State the required PHP version and extensions (`ext-pdo`, `ext-mbstring`, etc.).
- Provide the exact CLI run command (`php artisan serve`, `php script.php`, etc.).
- Explain `.env` setup and which variables are required.

## Deep References

Load these when the task is non-trivial:

- [../patterns/php-patterns.md](../patterns/php-patterns.md) — file skeleton with strict types, Composer autoload, PDO prepared statements, input validation chain, error logging, `.env` loading, array utility patterns, anti-patterns.
