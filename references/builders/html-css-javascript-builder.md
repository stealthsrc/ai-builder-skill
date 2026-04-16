# HTML CSS JavaScript Builder

Use this reference for lightweight browser-based tools and no-framework frontend work.

## Use It For

- internal dashboards and utilities
- small forms, calculators, and data-entry helpers
- static microsites or landing pages
- browser-based tools that should run from local files or simple static hosting
- requests that explicitly ask for HTML, CSS, JavaScript, or "plain frontend" without a framework

## Default Approach

- Prefer plain HTML, CSS, and JavaScript unless the user explicitly asks for a framework.
- Keep the file structure simple and obvious.
- Build something usable offline or from static hosting when possible.
- Favor progressive enhancement over unnecessary complexity.
- Make the UI feel intentional, not generic.

## Frontend Quality Bar

- Use semantic HTML with clear structure.
- Define CSS variables for color, spacing, and typography.
- Avoid default-looking layouts and generic component patterns.
- Keep JavaScript focused on user interactions, validation, and state that the page actually needs.
- Design for both desktop and mobile from the start.

## Safety And Practicality

- Do not put secrets, API keys, or privileged tokens in frontend code.
- Treat all user input as untrusted and validate it before using it in DOM updates or requests.
- Avoid unsafe patterns like injecting raw HTML unless the content is controlled and sanitized.
- If the page handles exports, uploads, or destructive actions, explain the boundaries and failure modes clearly.

## What To Deliver

- Tell the user which files to create, usually `index.html`, `styles.css`, and `script.js`.
- Keep configuration visible and easy to edit.
- Explain exactly how to open or serve the page locally.
- Include a quick validation path, especially for forms, responsive layout, and JavaScript actions.
