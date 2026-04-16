# React Builder

Use this reference for lightweight React applications: internal tools, KPI dashboards, admin panels, data entry apps, and vibe-coded UIs that need component state but not a full framework.

## Use It For

- Internal dashboards and admin UIs
- Data entry forms with validation and conditional logic
- Multi-step workflows and wizards
- Client-side tools that read files, call APIs, and display results
- Vibe-coded prototypes that need more structure than plain HTML/JS
- Tools where reusable components will be composed from a small set

## Default Approach

- Use **Vite** as the build tool — fast cold starts, instant HMR, minimal config.
- Default to **functional components with hooks** — no class components.
- Use **TypeScript** unless the user asks for JavaScript.
- Default to plain **CSS modules** for styling unless the user asks for Tailwind.
- Avoid Redux, Zustand, or other state managers unless the user's request clearly needs shared state across many components.
- Use React Query / TanStack Query for server-state when there are multiple API calls.

## Project Setup

```
vite.config.ts      – minimal Vite config
src/
  main.tsx          – React root, ReactDOM.createRoot
  App.tsx           – top-level component and routing (if needed)
  components/       – shared UI components
  hooks/            – custom hooks
  lib/              – pure utilities
  styles/           – global CSS variables, resets
index.html          – Vite entry point
package.json
tsconfig.json
```

## Quality Bar

- Use `strict: true` in tsconfig and no `any` escapes.
- Type all props with interfaces or type aliases.
- Keep components small and focused — one concern per component.
- Extract repeated JSX patterns into components when they appear three or more times.
- Use `key` props correctly in lists — always a stable unique ID, never array index for mutable lists.
- Avoid direct DOM manipulation — let React manage the DOM.

## Safety And Practicality

- Do not put secrets, API keys, or privileged tokens in React source — they ship to the browser.
- Use `VITE_` prefix for environment variables that must be client-visible, and document their purpose.
- Validate all external data (API responses, CSV uploads, URL params) before rendering.
- Sanitize any user-supplied content before injecting it into the DOM — prefer `textContent` over `dangerouslySetInnerHTML`.

## What To Deliver

- Provide `package.json` with exact dependencies and a `dev` script.
- Provide `tsconfig.json` and `vite.config.ts`.
- Provide the exact install and run commands (`npm install && npm run dev`).
- Explain the component structure briefly so the user can navigate the code.
- Include a quick validation path — what to open in a browser and what to check.

## Deep References

Load these when the task is non-trivial:

- [../patterns/react-patterns.md](../patterns/react-patterns.md) — Vite + TypeScript skeleton, functional component and custom hook idioms, `useState`/`useEffect`/`useRef` patterns, data fetch with loading and error state, form validation, CSS modules, error boundary, anti-patterns.
- [../recipes/react-kpi-dashboard.md](../recipes/react-kpi-dashboard.md) — Vite React dashboard with CSV drag-and-drop, KPI card grid, and a Recharts line chart.
