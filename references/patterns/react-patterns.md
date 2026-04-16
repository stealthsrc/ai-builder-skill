# React Patterns

Load this reference when the task requires more than a trivial React component. It provides reusable idioms and anti-patterns for functional, hook-based React applications built with Vite and TypeScript.

Pair with [../builders/react-builder.md](../builders/react-builder.md) for routing context and with [../rules/security-baseline.md](../rules/security-baseline.md) when the app handles secrets, user uploads, or external API calls.

---

## 1. Vite + TypeScript Skeleton

Minimal project scaffold. Run `npm create vite@latest my-app -- --template react-ts` to generate, then customize.

```typescript
// src/main.tsx
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import App from './App.tsx';
import './styles/global.css';

const root = document.getElementById('root');
if (!root) throw new Error('Root element not found');
createRoot(root).render(<StrictMode><App /></StrictMode>);
```

```typescript
// src/App.tsx
import type { FC } from 'react';
import Dashboard from './components/Dashboard.tsx';

const App: FC = () => <Dashboard />;
export default App;
```

---

## 2. Functional Component With Props Interface

Always define prop types as an interface directly above the component.

```typescript
interface KpiCardProps {
  label: string;
  value: number | string;
  unit?: string;
  trend?: 'up' | 'down' | 'flat';
}

const KpiCard: FC<KpiCardProps> = ({ label, value, unit, trend = 'flat' }) => (
  <div className={styles.card}>
    <span className={styles.label}>{label}</span>
    <span className={styles.value}>{value}{unit && ` ${unit}`}</span>
    {trend !== 'flat' && <span className={styles[trend]}>▲</span>}
  </div>
);
```

---

## 3. useState and useEffect Idioms

Keep state minimal. Derive values from state rather than duplicating them.

```typescript
// ✓ Single source of truth: derive filteredRows from rows + filter
const [rows, setRows] = useState<Row[]>([]);
const [filter, setFilter] = useState('');
const filteredRows = rows.filter(r =>
  r.name.toLowerCase().includes(filter.toLowerCase())
);

// ✗ Don't mirror derived state into a second useState
// const [filteredRows, setFilteredRows] = useState<Row[]>([]);
```

Clean up effects that produce timers, subscriptions, or fetch aborts.

```typescript
useEffect(() => {
  const controller = new AbortController();
  fetch('/api/data', { signal: controller.signal })
    .then(r => r.json())
    .then(setData)
    .catch(err => { if (err.name !== 'AbortError') setError(err.message); });
  return () => controller.abort();  // runs on unmount or dep change
}, []);
```

---

## 4. Custom Hook Pattern

Extract reusable stateful logic into a `use*` function that returns state and handlers.

```typescript
// src/hooks/useCsvDrop.ts
interface UseCsvDropResult {
  rows: Row[];
  isDragging: boolean;
  error: string | null;
  onDragOver: React.DragEventHandler<HTMLDivElement>;
  onDrop: React.DragEventHandler<HTMLDivElement>;
}

function useCsvDrop(): UseCsvDropResult {
  const [rows, setRows] = useState<Row[]>([]);
  const [isDragging, setIsDragging] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const onDragOver: React.DragEventHandler<HTMLDivElement> = e => {
    e.preventDefault();
    setIsDragging(true);
  };

  const onDrop: React.DragEventHandler<HTMLDivElement> = e => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files[0];
    if (!file?.name.endsWith('.csv')) { setError('Only CSV files accepted.'); return; }
    const reader = new FileReader();
    reader.onload = ev => {
      try { setRows(parseCsv(ev.target?.result as string)); setError(null); }
      catch { setError('Failed to parse CSV.'); }
    };
    reader.readAsText(file);
  };

  return { rows, isDragging, error, onDragOver, onDrop };
}
```

---

## 5. Data Fetch With Loading and Error State

Standard pattern: three state variables, single fetch in useEffect.

```typescript
interface FetchState<T> { data: T | null; loading: boolean; error: string | null; }

function useFetch<T>(url: string): FetchState<T> {
  const [state, setState] = useState<FetchState<T>>({ data: null, loading: true, error: null });

  useEffect(() => {
    let cancelled = false;
    setState({ data: null, loading: true, error: null });
    fetch(url)
      .then(r => { if (!r.ok) throw new Error(`HTTP ${r.status}`); return r.json() as Promise<T>; })
      .then(data => { if (!cancelled) setState({ data, loading: false, error: null }); })
      .catch(err => { if (!cancelled) setState({ data: null, loading: false, error: err.message }); });
    return () => { cancelled = true; };
  }, [url]);

  return state;
}
```

---

## 6. Form Validation With Controlled Inputs

Use controlled inputs. Validate on submit, not on every keystroke for simple forms.

```typescript
interface FormValues { name: string; email: string; amount: string; }
type FormErrors = Partial<Record<keyof FormValues, string>>;

function validate(values: FormValues): FormErrors {
  const errors: FormErrors = {};
  if (!values.name.trim()) errors.name = 'Name is required.';
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(values.email)) errors.email = 'Invalid email.';
  if (isNaN(Number(values.amount)) || Number(values.amount) <= 0) errors.amount = 'Must be positive.';
  return errors;
}

// In the component:
const handleSubmit = (e: React.FormEvent) => {
  e.preventDefault();
  const errs = validate(values);
  if (Object.keys(errs).length) { setErrors(errs); return; }
  // submit ...
};
```

---

## 7. CSS Modules

Co-locate styles with the component using CSS modules. Use CSS variables from a global theme.

```css
/* src/styles/global.css */
:root {
  --color-primary: #2563eb;
  --color-bg: #f8fafc;
  --color-surface: #ffffff;
  --color-text: #1e293b;
  --radius: 8px;
  --shadow: 0 1px 3px rgb(0 0 0 / 0.1);
}
```

```css
/* src/components/KpiCard.module.css */
.card {
  background: var(--color-surface);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  padding: 1.5rem;
}
.value { font-size: 2rem; font-weight: 700; color: var(--color-primary); }
```

---

## 8. Error Boundary

Wrap major sections in an error boundary to prevent one broken component from crashing the whole app.

```typescript
import { Component, type ReactNode } from 'react';

interface Props { children: ReactNode; fallback?: ReactNode; }
interface State { hasError: boolean; message: string; }

class ErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false, message: '' };

  static getDerivedStateFromError(err: Error): State {
    return { hasError: true, message: err.message };
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback ?? (
        <div role="alert" style={{ padding: '1rem', color: 'red' }}>
          Something went wrong: {this.state.message}
        </div>
      );
    }
    return this.props.children;
  }
}
```

---

## 9. Anti-Patterns

| Anti-pattern | Problem | Fix |
|---|---|---|
| `dangerouslySetInnerHTML` with user input | XSS — script tags execute | Sanitize with DOMPurify or use `textContent` |
| Array index as `key` in mutable lists | React misidentifies elements on reorder/delete | Use stable unique IDs |
| State that mirrors another state | Double source of truth → stale data bugs | Derive with `useMemo` or inline computation |
| Fetching in a child that renders many times | Waterfall requests, flickering | Lift fetch to parent or use a cache (React Query) |
| `useEffect` with no cleanup for subscriptions | Memory leaks in long-lived apps | Return a cleanup function that cancels/unsubscribes |
| Secrets in `VITE_*` env vars | Ships in client bundle — visible in browser | Proxy sensitive calls through a backend or edge function |
| `any` on API response type | Type errors at runtime, not compile time | Define interface + optional zod parse |
