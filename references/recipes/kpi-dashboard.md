# Recipe: Static KPI Dashboard (HTML/CSS/JS, No Framework)

## When To Use

The user wants a lightweight internal dashboard that reads a CSV and shows KPI cards plus a chart. It must run offline from a local folder or on any static host (SharePoint library, internal IIS, GitHub Pages).

## Route

Primary: HTML/CSS/JS. Load [../patterns/html-js-patterns.md](../patterns/html-js-patterns.md) for the CSS variable theme, safe DOM, CSV parse, and CSV export helpers.

## Assumptions

- the CSV has at least the columns `date`, `metric`, `value`
- users accept drag-and-drop or a file picker to load the data
- no sensitive information is hardcoded into the page

## File Layout

```
kpi-dashboard/
  index.html
  styles.css
  script.js
```

## `index.html`

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
    <p class="muted">Drop a CSV with columns: date, metric, value.</p>
  </header>

  <main>
    <section class="dropzone" id="drop" aria-label="CSV drop area">
      <input type="file" id="file" accept=".csv" hidden>
      <button type="button" id="pick">Choose CSV</button>
      <span id="status" aria-live="polite"></span>
    </section>

    <section class="grid" id="cards" aria-label="KPI cards"></section>
    <section class="chart">
      <h2>Trend</h2>
      <canvas id="chart" width="800" height="280" aria-label="Metric trend chart"></canvas>
    </section>
  </main>

  <script src="script.js" defer></script>
</body>
</html>
```

## `styles.css`

```css
:root {
  --color-bg: #0b0d10;
  --color-fg: #e6e8ea;
  --color-muted: #8b93a0;
  --color-accent: #3aa675;
  --color-danger: #cc4b45;
  --space-3: 1rem;
  --space-4: 1.5rem;
  --radius: 8px;
  --font-body: system-ui, -apple-system, "Segoe UI", sans-serif;
}

@media (prefers-color-scheme: light) {
  :root { --color-bg: #fbfbfb; --color-fg: #1a1d21; --color-muted: #5a6169; --color-accent: #228b5a; }
}

body {
  margin: 0; padding: var(--space-4);
  background: var(--color-bg); color: var(--color-fg);
  font-family: var(--font-body);
}

h1 { margin: 0 0 var(--space-3); }
.muted { color: var(--color-muted); }

.dropzone {
  display: flex; align-items: center; gap: var(--space-3);
  padding: var(--space-3);
  border: 1px dashed color-mix(in oklab, var(--color-fg) 30%, transparent);
  border-radius: var(--radius);
  margin: var(--space-3) 0;
}

.grid { display: grid; gap: var(--space-3); grid-template-columns: 1fr; }
@media (min-width: 640px)  { .grid { grid-template-columns: repeat(2, 1fr); } }
@media (min-width: 1024px) { .grid { grid-template-columns: repeat(4, 1fr); } }

.card {
  padding: var(--space-3); border-radius: var(--radius);
  background: color-mix(in oklab, var(--color-fg) 6%, transparent);
}
.card .label { color: var(--color-muted); font-size: 0.85rem; }
.card .value { font-size: 1.8rem; font-weight: 600; margin-top: 0.25rem; }

.chart {
  margin-top: var(--space-4); padding: var(--space-3);
  border-radius: var(--radius);
  background: color-mix(in oklab, var(--color-fg) 6%, transparent);
}
canvas { width: 100%; height: auto; }

button {
  padding: 0.5rem 0.9rem; border: 0; border-radius: 6px;
  background: var(--color-accent); color: white; cursor: pointer;
}
button:focus-visible { outline: 2px solid var(--color-fg); outline-offset: 2px; }
```

## `script.js`

```javascript
const elements = {
  drop:   document.querySelector('#drop'),
  pick:   document.querySelector('#pick'),
  file:   document.querySelector('#file'),
  status: document.querySelector('#status'),
  cards:  document.querySelector('#cards'),
  chart:  document.querySelector('#chart'),
};

elements.pick.addEventListener('click', () => elements.file.click());
elements.file.addEventListener('change', (event) => {
  const file = event.target.files?.[0];
  if (file) loadCsvFile(file);
});

['dragenter', 'dragover'].forEach(type =>
  elements.drop.addEventListener(type, (e) => { e.preventDefault(); }));

elements.drop.addEventListener('drop', (event) => {
  event.preventDefault();
  const file = event.dataTransfer.files?.[0];
  if (file) loadCsvFile(file);
});

async function loadCsvFile(file) {
  try {
    const text = await file.text();
    const rows = parseCsv(text);
    const headers = rows.shift() ?? [];
    const records = rows.map(r => Object.fromEntries(headers.map((h, i) => [h.trim(), (r[i] ?? '').trim()])));
    render(records);
    elements.status.textContent = `Loaded ${records.length} rows from ${file.name}.`;
  } catch (err) {
    elements.status.textContent = `Failed to read CSV: ${err.message}`;
  }
}

function render(records) {
  const byMetric = records.reduce((acc, row) => {
    if (!row.metric || !row.value) return acc;
    (acc[row.metric] ??= []).push({ date: row.date, value: Number(row.value) });
    return acc;
  }, {});

  renderCards(byMetric);
  const first = Object.values(byMetric)[0] ?? [];
  drawLineChart(elements.chart, first);
}

function renderCards(byMetric) {
  const frag = document.createDocumentFragment();
  for (const [metric, rows] of Object.entries(byMetric)) {
    const latest = rows.at(-1)?.value ?? 0;
    const card = document.createElement('div');
    card.className = 'card';
    const label = document.createElement('div'); label.className = 'label'; label.textContent = metric;
    const value = document.createElement('div'); value.className = 'value'; value.textContent = formatNumber(latest);
    card.append(label, value);
    frag.appendChild(card);
  }
  elements.cards.replaceChildren(frag);
}

function drawLineChart(canvas, points) {
  const ctx = canvas.getContext('2d');
  const w = canvas.width, h = canvas.height, pad = 28;
  ctx.clearRect(0, 0, w, h);
  if (!points.length) return;

  const ys = points.map(p => p.value);
  const min = Math.min(...ys), max = Math.max(...ys);
  const span = max - min || 1;
  const stepX = (w - pad * 2) / Math.max(points.length - 1, 1);

  ctx.strokeStyle = getComputedStyle(document.body).color;
  ctx.globalAlpha = 0.2;
  ctx.beginPath(); ctx.moveTo(pad, h - pad); ctx.lineTo(w - pad, h - pad); ctx.stroke();
  ctx.globalAlpha = 1;

  ctx.strokeStyle = getComputedStyle(document.documentElement).getPropertyValue('--color-accent').trim() || '#3aa675';
  ctx.lineWidth = 2;
  ctx.beginPath();
  points.forEach((p, i) => {
    const x = pad + i * stepX;
    const y = h - pad - ((p.value - min) / span) * (h - pad * 2);
    i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
  });
  ctx.stroke();
}

function formatNumber(n) {
  return new Intl.NumberFormat().format(Math.round(n * 100) / 100);
}

function parseCsv(text) {
  const rows = [];
  let row = [], field = '', inQuotes = false;
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
  if (field.length || row.length) { row.push(field); rows.push(row); }
  return rows;
}
```

## How To Run

1. Save the three files into a folder.
2. Double-click `index.html` or host the folder from any static server.
3. Drop a CSV onto the page, or click **Choose CSV**.

## Validate

- KPI cards render with the latest value per metric
- the chart draws the trend for the first metric
- the file picker and drag-and-drop both work
- closing and reopening the page shows an empty state (no secrets leak into `localStorage` by default)

## Edge Cases

- CSV with stray whitespace: header lookup is already trimmed
- non-numeric `value`: becomes `NaN`, filtered by the chart's `Number()` coercion
- very large CSV (>100k rows): parser is synchronous; for huge files swap in a vendored `papaparse`
- CSP: inline event handlers and remote scripts are blocked intentionally; keep everything in `script.js`
