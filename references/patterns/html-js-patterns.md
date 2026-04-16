# HTML, CSS, and JavaScript Patterns

Load this reference when the task requires more than a trivial browser page. It provides reusable idioms and anti-patterns for no-framework tools that should stay fast, safe, and easy to hand off.

Pair with [../builders/html-css-javascript-builder.md](../builders/html-css-javascript-builder.md) for routing context and with [../rules/security-baseline.md](../rules/security-baseline.md) when the page handles untrusted input, exports, or external URLs.

---

## 1. Starter Template (Three Files)

Keep the structure obvious: `index.html`, `styles.css`, `script.js`. Everything runs from a local `file://` open or simple static hosting.

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta http-equiv="Content-Security-Policy"
        content="default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self'">
  <title>KPI Dashboard</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <header>
    <h1>Weekly KPIs</h1>
  </header>

  <main>
    <section id="summary" aria-live="polite"></section>
    <section id="chart-host"></section>
  </main>

  <script src="script.js" defer></script>
</body>
</html>
```

Use `defer` on scripts so the DOM is parsed before the script runs without blocking rendering.

---

## 2. CSS Variables Theme Block

Declare spacing, color, and typography once at the top. Everything else derives from the variables.

```css
:root {
  /* Color */
  --color-bg: #0b0d10;
  --color-fg: #e6e8ea;
  --color-muted: #8b93a0;
  --color-accent: #3aa675;
  --color-danger: #cc4b45;

  /* Spacing */
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-3: 1rem;
  --space-4: 1.5rem;
  --space-5: 2rem;

  /* Typography */
  --font-body: system-ui, -apple-system, "Segoe UI", sans-serif;
  --font-mono: "Cascadia Mono", Consolas, monospace;
  --radius: 8px;
}

@media (prefers-color-scheme: light) {
  :root {
    --color-bg: #fbfbfb;
    --color-fg: #1a1d21;
    --color-muted: #5a6169;
    --color-accent: #228b5a;
    --color-danger: #b8332d;
  }
}

body {
  margin: 0;
  padding: var(--space-4);
  background: var(--color-bg);
  color: var(--color-fg);
  font-family: var(--font-body);
}
```

---

## 3. Mobile-First Responsive

Default styles target mobile; `min-width` queries layer on wider layouts.

```css
.card {
  padding: var(--space-3);
  border-radius: var(--radius);
  background: color-mix(in oklab, var(--color-fg) 6%, transparent);
}

.grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-3);
}

@media (min-width: 640px) {
  .grid { grid-template-columns: repeat(2, 1fr); }
}

@media (min-width: 1024px) {
  .grid { grid-template-columns: repeat(4, 1fr); }
}
```

---

## 4. Safe DOM Updates

Never assign untrusted data to `innerHTML`. Use `textContent`, `createElement`, and `DocumentFragment`.

```javascript
function renderRows(rows) {
  const tbody = document.querySelector('#rows');
  const frag = document.createDocumentFragment();

  for (const row of rows) {
    const tr = document.createElement('tr');
    for (const value of [row.id, row.label, row.amount]) {
      const td = document.createElement('td');
      td.textContent = String(value ?? '');
      tr.appendChild(td);
    }
    frag.appendChild(tr);
  }

  tbody.replaceChildren(frag);
}
```

`replaceChildren` empties the node and inserts the new content in one operation. Safer and faster than `innerHTML = '' ; append(...)`.

---

## 5. CSV Parse Without A Library

Works for well-formed CSV with quoted fields. For messy real-world files, prefer `papaparse` from a local vendored copy.

```javascript
function parseCsv(text) {
  const rows = [];
  let row = [];
  let field = '';
  let inQuotes = false;

  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (inQuotes) {
      if (c === '"' && text[i + 1] === '"') { field += '"'; i++; }
      else if (c === '"') { inQuotes = false; }
      else { field += c; }
    } else {
      if (c === '"') { inQuotes = true; }
      else if (c === ',') { row.push(field); field = ''; }
      else if (c === '\n') { row.push(field); rows.push(row); row = []; field = ''; }
      else if (c === '\r') { /* skip */ }
      else { field += c; }
    }
  }
  if (field.length > 0 || row.length > 0) { row.push(field); rows.push(row); }
  return rows;
}
```

To load a CSV file the user drops on the page:

```javascript
async function loadCsvFile(file) {
  const text = await file.text();
  const rows = parseCsv(text);
  const [headers, ...data] = rows;
  return data.map(r => Object.fromEntries(headers.map((h, i) => [h, r[i] ?? ''])));
}
```

---

## 6. Safe `localStorage` Wrapper

Wrap storage so corruption does not crash the page and keys stay namespaced.

```javascript
const store = (() => {
  const prefix = 'ai-builder:';
  return {
    get(key, fallback = null) {
      try {
        const raw = localStorage.getItem(prefix + key);
        return raw ? JSON.parse(raw) : fallback;
      } catch { return fallback; }
    },
    set(key, value) {
      try { localStorage.setItem(prefix + key, JSON.stringify(value)); }
      catch { /* quota / private mode */ }
    },
    remove(key) {
      try { localStorage.removeItem(prefix + key); } catch {}
    },
  };
})();
```

---

## 7. Form Validation That Respects HTML

Use built-in validity attributes, then layer on custom messages. Do not reinvent validation on every keypress.

```html
<form id="entry" novalidate>
  <label>
    Invoice ID
    <input name="id" required pattern="^INV-\d{6}$" autocomplete="off">
  </label>
  <label>
    Amount
    <input name="amount" type="number" min="0" step="0.01" required>
  </label>
  <button type="submit">Save</button>
</form>
```

```javascript
const form = document.querySelector('#entry');
form.addEventListener('submit', (event) => {
  event.preventDefault();
  if (!form.checkValidity()) {
    form.reportValidity();
    return;
  }
  const data = Object.fromEntries(new FormData(form));
  // ... act on data ...
});
```

---

## 8. CSV Export From The Browser

```javascript
function downloadCsv(rows, filename = 'export.csv') {
  const headers = Object.keys(rows[0] ?? {});
  const lines = [
    headers.join(','),
    ...rows.map(r => headers.map(h => csvCell(r[h])).join(',')),
  ];
  const bom = '\uFEFF';                // Excel-friendly BOM
  const blob = new Blob([bom + lines.join('\r\n')], { type: 'text/csv;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const a = Object.assign(document.createElement('a'), { href: url, download: filename });
  document.body.appendChild(a); a.click(); a.remove();
  URL.revokeObjectURL(url);
}

function csvCell(value) {
  const s = value == null ? '' : String(value);
  if (/[",\r\n]/.test(s)) return '"' + s.replace(/"/g, '""') + '"';
  return s;
}
```

The BOM makes Excel open the file with UTF-8 decoding when the user double-clicks it.

---

## 9. Accessibility Baseline

- every form input has a `<label>` wrapping it or pointing at it via `for`
- interactive elements are reachable with `Tab`
- live status messages go in an `aria-live="polite"` region
- color is not the only indicator of state (add an icon or text)
- contrast meets WCAG AA (use a tool, not guesswork)

---

## 10. Anti-Patterns With Fixes

| Anti-pattern | Why it hurts | Fix |
|---|---|---|
| `innerHTML = userInput` | XSS | `textContent` or `createElement` + `textContent` |
| Inline `onclick="..."` attributes | mixes logic and markup, blocked by strict CSP | `addEventListener` in `script.js` |
| `document.write` | wipes the page if called after load | `createElement` + append |
| API keys or tokens in JS | public by definition | call a backend or read from a local, user-entered field |
| No `viewport` meta | broken on phones | include the standard viewport meta |
| Fetches with no timeout | hang forever on bad networks | wrap with `AbortController` + `setTimeout` |
| `var` + global state | implicit leaks | `const` / `let`, IIFE or ES module |
| Script tag without `defer` | blocks rendering | `<script src="..." defer>` |
| `==` instead of `===` | type coercion surprises | always `===` / `!==` |
| `alert()` for feedback | blocks UI, ugly | render a status region with `aria-live` |
| Huge synchronous loops | freezes the tab | chunk with `requestAnimationFrame` or a Worker |
| Hardcoded breakpoints | hard to tune | CSS variables and `min-width` queries |

---

## 11. Fetch With Timeout

```javascript
async function fetchJson(url, { timeoutMs = 10_000, ...init } = {}) {
  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(), timeoutMs);
  try {
    const res = await fetch(url, { ...init, signal: ctrl.signal });
    if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
    return await res.json();
  } finally {
    clearTimeout(timer);
  }
}
```

---

## 12. Claude Artifacts Pattern

Claude.ai artifacts run plain JavaScript in an isolated sandbox. Adapt the standard template to produce a single self-contained HTML file with no external dependencies.

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Tool</title>
  <style>
    /* All CSS inline — no external stylesheet */
    :root { --color-primary: #2563eb; --radius: 8px; }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: system-ui, sans-serif; padding: 1.5rem; }
  </style>
</head>
<body>
  <main id="app"></main>
  <script>
    // All JS inline — no import, no fetch to external domains
    // Use textContent, not innerHTML, for user-supplied data

    const app = document.getElementById('app');

    function render(state) {
      app.replaceChildren(); // safe DOM clear
      const h1 = document.createElement('h1');
      h1.textContent = state.title;
      app.appendChild(h1);
      // ... build DOM from state ...
    }

    render({ title: 'My Tool' });
  </script>
</body>
</html>
```

Key constraints for artifacts:
- No external `fetch` to third-party URLs — sandbox blocks most outbound requests.
- No `import` or `require` — single-file only.
- Use `textContent` and `createElement` throughout — `innerHTML` with user input is blocked by the artifact CSP.
- Inline all styles; `<link rel="stylesheet" href="...">` to external URLs will fail.
- Charts: use `<canvas>` with hand-drawn logic, or include a small self-contained library as an inline `<script>` block.

---

## Related

- Recipe: [../recipes/kpi-dashboard.md](../recipes/kpi-dashboard.md)
- Safety: [../rules/security-baseline.md](../rules/security-baseline.md)
