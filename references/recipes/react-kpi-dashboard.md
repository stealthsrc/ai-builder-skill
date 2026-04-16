# Recipe: React KPI Dashboard with CSV Drag-and-Drop

Complete Vite + React + TypeScript dashboard with CSV drag-and-drop, KPI card grid, and a Recharts line chart — no backend required.

Pair with [../builders/react-builder.md](../builders/react-builder.md) and [../patterns/react-patterns.md](../patterns/react-patterns.md).

---

## What It Does

1. Renders a drag-and-drop zone. The user drops a CSV file.
2. Parses the CSV client-side and shows four auto-calculated KPI cards (total, average, min, max of a numeric column).
3. Draws a line chart of the numeric column over the row sequence using Recharts.
4. Supports column selection so the user can switch which column drives the KPIs and chart.

---

## Project Setup

```bash
npm create vite@latest kpi-dashboard -- --template react-ts
cd kpi-dashboard
npm install recharts papaparse
npm install -D @types/papaparse
npm run dev
```

---

## File Structure

```
kpi-dashboard/
  src/
    App.tsx
    components/
      DropZone.tsx
      KpiCard.tsx
      LineChart.tsx
      ColumnPicker.tsx
    hooks/
      useCsvDrop.ts
    styles/
      global.css
      DropZone.module.css
      KpiCard.module.css
  index.html
  vite.config.ts
  package.json
  tsconfig.json
```

---

## src/styles/global.css

```css
:root {
  --color-primary:  #2563eb;
  --color-bg:       #f1f5f9;
  --color-surface:  #ffffff;
  --color-text:     #1e293b;
  --color-muted:    #64748b;
  --color-border:   #e2e8f0;
  --radius:         10px;
  --shadow:         0 1px 4px rgb(0 0 0 / 0.08);
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

body {
  background: var(--color-bg);
  color: var(--color-text);
  font-family: system-ui, sans-serif;
  min-height: 100vh;
  padding: 2rem;
}

h1 { font-size: 1.5rem; font-weight: 700; margin-bottom: 1.5rem; }
```

---

## src/hooks/useCsvDrop.ts

```typescript
import { useState } from 'react';
import Papa from 'papaparse';

export interface CsvData {
  headers: string[];
  rows: Record<string, string>[];
}

export function useCsvDrop() {
  const [data, setData]         = useState<CsvData | null>(null);
  const [isDragging, setDragging] = useState(false);
  const [error, setError]       = useState<string | null>(null);

  const onDragOver = (e: React.DragEvent) => { e.preventDefault(); setDragging(true); };
  const onDragLeave = () => setDragging(false);

  const onDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragging(false);
    const file = e.dataTransfer.files[0];
    if (!file?.name.endsWith('.csv')) { setError('Only .csv files are supported.'); return; }

    Papa.parse<Record<string, string>>(file, {
      header: true,
      skipEmptyLines: true,
      complete: result => {
        if (result.errors.length) { setError(result.errors[0]?.message ?? 'Parse error'); return; }
        setData({ headers: result.meta.fields ?? [], rows: result.data });
        setError(null);
      },
    });
  };

  return { data, isDragging, error, onDragOver, onDragLeave, onDrop };
}
```

---

## src/components/DropZone.tsx

```typescript
import type { FC } from 'react';
import styles from '../styles/DropZone.module.css';

interface Props {
  isDragging: boolean;
  onDragOver: React.DragEventHandler<HTMLDivElement>;
  onDragLeave: React.DragEventHandler<HTMLDivElement>;
  onDrop: React.DragEventHandler<HTMLDivElement>;
}

export const DropZone: FC<Props> = ({ isDragging, onDragOver, onDragLeave, onDrop }) => (
  <div
    className={`${styles.zone} ${isDragging ? styles.active : ''}`}
    onDragOver={onDragOver}
    onDragLeave={onDragLeave}
    onDrop={onDrop}
    role="region"
    aria-label="CSV drop zone"
  >
    <span>Drop a CSV file here</span>
  </div>
);
```

```css
/* src/styles/DropZone.module.css */
.zone {
  border: 2px dashed var(--color-border);
  border-radius: var(--radius);
  padding: 3rem;
  text-align: center;
  color: var(--color-muted);
  transition: border-color 0.15s, background 0.15s;
  cursor: pointer;
  margin-bottom: 2rem;
}
.zone.active { border-color: var(--color-primary); background: #eff6ff; }
```

---

## src/components/KpiCard.tsx

```typescript
import type { FC } from 'react';
import styles from '../styles/KpiCard.module.css';

interface Props { label: string; value: string; }

export const KpiCard: FC<Props> = ({ label, value }) => (
  <div className={styles.card}>
    <span className={styles.label}>{label}</span>
    <span className={styles.value}>{value}</span>
  </div>
);
```

```css
/* src/styles/KpiCard.module.css */
.card {
  background: var(--color-surface);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.label { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; color: var(--color-muted); }
.value { font-size: 2rem; font-weight: 700; color: var(--color-primary); }
```

---

## src/App.tsx

```typescript
import { useState, useMemo } from 'react';
import type { FC } from 'react';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer,
} from 'recharts';
import { useCsvDrop } from './hooks/useCsvDrop';
import { DropZone } from './components/DropZone';
import { KpiCard } from './components/KpiCard';
import './styles/global.css';

const fmt = (n: number) =>
  Number.isFinite(n) ? n.toLocaleString(undefined, { maximumFractionDigits: 2 }) : 'N/A';

const App: FC = () => {
  const { data, isDragging, error, onDragOver, onDragLeave, onDrop } = useCsvDrop();
  const [activeCol, setActiveCol] = useState('');

  const numericCols = useMemo(() =>
    (data?.headers ?? []).filter(h =>
      data!.rows.some(r => r[h] !== '' && !isNaN(Number(r[h])))
    ), [data]);

  const col = activeCol || numericCols[0] || '';

  const values = useMemo(() =>
    col ? data!.rows.map(r => Number(r[col])).filter(Number.isFinite) : [],
    [data, col]);

  const total   = values.reduce((a, b) => a + b, 0);
  const average = values.length ? total / values.length : NaN;
  const min     = Math.min(...values);
  const max     = Math.max(...values);

  const chartData = data?.rows.map((r, i) => ({ index: i + 1, value: Number(r[col]) })) ?? [];

  return (
    <main style={{ maxWidth: 960, margin: '0 auto' }}>
      <h1>KPI Dashboard</h1>

      <DropZone
        isDragging={isDragging}
        onDragOver={onDragOver}
        onDragLeave={onDragLeave}
        onDrop={onDrop}
      />

      {error && <p style={{ color: 'red', marginBottom: '1rem' }}>{error}</p>}

      {data && (
        <>
          {numericCols.length > 1 && (
            <div style={{ marginBottom: '1.5rem' }}>
              <label htmlFor="col-select">Column: </label>
              <select
                id="col-select"
                value={col}
                onChange={e => setActiveCol(e.target.value)}
                style={{ marginLeft: '0.5rem' }}
              >
                {numericCols.map(h => <option key={h} value={h}>{h}</option>)}
              </select>
            </div>
          )}

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '1rem', marginBottom: '2rem' }}>
            <KpiCard label="Total"   value={fmt(total)} />
            <KpiCard label="Average" value={fmt(average)} />
            <KpiCard label="Min"     value={fmt(min)} />
            <KpiCard label="Max"     value={fmt(max)} />
          </div>

          <div style={{ background: 'var(--color-surface)', borderRadius: 'var(--radius)', boxShadow: 'var(--shadow)', padding: '1.5rem' }}>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border)" />
                <XAxis dataKey="index" tick={{ fontSize: 12 }} />
                <YAxis tick={{ fontSize: 12 }} />
                <Tooltip />
                <Line type="monotone" dataKey="value" stroke="var(--color-primary)" dot={false} strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </>
      )}
    </main>
  );
};

export default App;
```

---

## Run

```bash
npm run dev
# Open http://localhost:5173
# Drop a CSV — columns with numeric values will power the KPIs and chart
```

---

## Validation

- Drop a CSV with at least one numeric column — KPI cards and chart should render immediately.
- If all columns are text, the column selector will be empty and KPIs will show "N/A".
- Switch columns in the dropdown — chart and KPIs update without a page reload.
- Resize the browser window — chart is responsive.

---

## Extending

| Feature | Where to add |
|---|---|
| Export chart as PNG | `useRef` on the chart container + `canvas.toDataURL` |
| Date-based X axis | Replace `index` key with a parsed date column in `chartData` |
| Multiple series | Add more `<Line>` components with different `dataKey` values |
| Dark mode | Toggle a `data-theme="dark"` attribute on `<html>` + CSS variable overrides |
