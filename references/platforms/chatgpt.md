# ChatGPT

Use this reference when the skill is consumed from ChatGPT, either as a Custom GPT, a Project, or through the OpenAI Apps SDK / Agents SDK.

## Three Practical Deployment Modes

### 1. Custom GPT (GPT Builder)

Paste the content of `dist/chatgpt-custom-gpt.md` into the Custom GPT "Instructions" field. Upload the files below as knowledge attachments:

- `SKILL.md`
- `AGENTS.md`
- `references/rules/output-and-safety.md`
- `references/rules/security-baseline.md`
- `references/rules/risk-trigger-matrix.md`
- every file under `references/builders/`

Keep file count minimal. If the 20-file cap is a constraint, zip `references/` into a single archive and attach it.

### 2. Project (ChatGPT Projects)

Upload the same files as project files and set the project's system prompt to the content of `dist/chatgpt-custom-gpt.md`. Projects share the instruction across every conversation in the project, which is a good fit for a routing skill.

### 3. OpenAI Apps SDK / Agents SDK

Use `agents/openai.yaml` as the distribution manifest. The `instructions` field is the full skill contract, the `starter_prompts` field seeds the first-turn UI, and the `default_prompt` field is the canonical trigger.

For an Apps SDK app, map the skill like this:

- `instructions` from `agents/openai.yaml` becomes the app's system prompt
- `SKILL.md` and `references/` ship as attached documents or tool-accessible files
- tools that execute code or touch the filesystem should request confirmation for any action in the risk trigger matrix

## Why ChatGPT Is Different From Codex CLI

ChatGPT cannot read files from disk the way Codex, Claude Code, Gemini CLI, or Antigravity can. It only sees what you attach or paste. That changes the packaging model:

- the skill must be bundled, not discovered from a repo checkout
- progressive disclosure has to happen inside the instructions, not through on-disk file reads
- references have to be attached as knowledge files or folded into the system prompt

Keep the system prompt short and lean on knowledge files for depth.

## Safety Posture

ChatGPT tool use is broad but opaque. For this skill that means:

- never claim a command was executed unless the tool response confirms it
- never fabricate file paths, row counts, or validation results
- recommend dry-runs, explicit backup steps, and test-on-a-copy guidance for every destructive workflow
- surface risk signals explicitly from `references/rules/risk-trigger-matrix.md`

## Official References

- OpenAI Apps SDK: https://platform.openai.com/docs/apps-sdk
- OpenAI Agents SDK: https://platform.openai.com/docs/agents-sdk
- Custom GPTs (GPT Builder): https://help.openai.com/en/articles/8554407
- ChatGPT Projects: https://help.openai.com/en/articles/10169521
