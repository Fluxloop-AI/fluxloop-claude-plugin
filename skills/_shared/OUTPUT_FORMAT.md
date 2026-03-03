# Output Format Guide

All skills must follow this formatting guide when presenting information to the user.
The goal: users should instantly see **where they are**, **what to do**, and **what happened**.

## Core Principles

1. **Section separation** — use dividers between major sections
2. **Icon prefixes** — each information type has a designated icon
3. **Indentation** — commands and details are indented under their parent section
4. **Minimal prose** — bullet points over paragraphs; one line per fact
5. **First-encounter explanation** — When using domain terms (Happy Path, Bundle, Contract, Input Set, Multi-turn, etc.) for the first time in a session, **always explain them in 1-2 sentences**. Explain concretely in the context of the user's agent.
6. **Link mandatory** — All actions that create or reference server resources must include a `🔗` link. Instead of vague guidance like "check the web app", **output the full URL directly**.

## Section Dividers

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ← thick: skill title only
────────────────────────────────────  ← thin: between sections
```

- Thick divider (`━`): appears above AND below the skill title (top of output only)
- Thin divider (`─`): separates every major section from the next

## Icon Reference

| Icon | Usage | Example |
|------|-------|---------|
| 🚀 | Skill title | `🚀 FluxLoop Getting Started Guide` |
| 📋 | Status / current state | `📋 Current Status` |
| ▶ | Action step (user must do something) | `▶ Step 1: Install CLI` |
| 👉 | Command to run | `👉 uv pip install fluxloop-cli` |
| ✅ | Completed / success | `✅ Login → user@example.com` |
| ❌ | Missing / failed | `❌ FluxLoop CLI: not installed` |
| ⏭️ | Next steps | `⏭️ Next Steps` |
| 💡 | Tip or note | `💡 Run from the workspace root` |
| ⚠️ | Warning | `⚠️ Do not use the --pull option` |
| 🔗 | Link | `🔗 https://alpha.app.fluxloop.ai/...` |
| 📊 | Results / data | `📊 Test Results` |
| 🔄 | In progress / loading | `🔄 Running evaluation...` |

## Output Templates

### 1. Skill Header

Every skill output starts with:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚀 {Skill Title}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 2. Status Block

Show current state immediately after the header:

```
📋 Current Status
  • Project: {name} ({details})
  • FluxLoop CLI: ✅ installed (v1.2.3) | ❌ not installed
  • Auth: ✅ logged in (user@email.com) | ❌ not authenticated
  • Scenario: ✅ {name} | ❌ none
```

- Use `✅` / `❌` inline for boolean states
- Indent details with `  • ` (2-space + bullet)

### 3. Action Steps

Each step the user needs to act on:

```
────────────────────────────────────

▶ Step {N}: {Step Title}

  {One-line explanation if needed}

  👉 {command to run}
```

- One thin divider before each step
- `👉` marks the exact command or action the user must perform
- Keep explanation to 1 line max; **however, add 1-2 sentences of explanation when a domain term appears for the first time** (Core Principles #5)

### 4. Selection Prompt

When the user must choose between options:

```
────────────────────────────────────

▶ Step {N}: {Selection Title}

  1) {Option A} — {brief description}
  2) {Option B} — {brief description}
  3) {Option C} — {brief description}
  4) Enter manually

  👉 Select a number or enter manually:
```

### 5. Result / Completion

After a CLI action completes:

```
✅ {Action} → {summary} 🔗 {url}
```

> **Required**: When creating or referencing server resources (Project, Scenario, Input Set, Bundle, Experiment, Evaluation), extract the ID from CLI output and construct a link using the URL patterns below.
>
> | Resource | URL Pattern |
> |----------|-------------|
> | Project | `https://alpha.app.fluxloop.ai/simulate/scenarios?project={project_id}` |
> | Scenario | `https://alpha.app.fluxloop.ai/simulate/scenarios/{scenario_id}?project={project_id}` |
> | Input Set | `https://alpha.app.fluxloop.ai/simulate/scenarios/{scenario_id}/inputs/{input_set_id}?project={project_id}` |
> | Bundle | `https://alpha.app.fluxloop.ai/simulate/scenarios/{scenario_id}/bundles/{bundle_version_id}?project={project_id}` |
> | Experiment | `https://alpha.app.fluxloop.ai/release/experiments/{experiment_id}/evaluation?project={project_id}` |
>
> Only omit the link for actions without a URL (e.g., Data actions). See `skills/_shared/POST_ACTIONS.md` for full examples.

### 6. Next Steps Block

Always end a skill with:

```
────────────────────────────────────

⏭️ Next Steps
  • "{user command}" → {what it does}
  • "{user command}" → {what it does}
```

### 7. Warning / Tip (inline)

Insert anywhere relevant:

```
  💡 {helpful tip}
  ⚠️ {warning message}
```

## Full Example: Setup Skill

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚀 FluxLoop Getting Started Guide
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Current Status
  • Project: pluto-duck (Python 3.13.2, uv available)
  • FluxLoop CLI: ❌ not installed

────────────────────────────────────

▶ Step 1: Install CLI

  uv is available, so we'll use it for installation:

  👉 uv pip install fluxloop-cli

────────────────────────────────────

▶ Step 2: Login

  Authenticate after installation. When a device code is displayed, enter it in your browser.

  👉 fluxloop auth login --no-wait && fluxloop auth login --resume

────────────────────────────────────

▶ Step 3: Create/Select Project

  After login, create a new project or select an existing one.

────────────────────────────────────

⏭️ Available Next Actions
  • Codebase scan & agent profile generation (context)
  • Test scenario setup (scenario)
  • Run simulation (test)
  • Result analysis & improvement (evaluate)
```

## Full Example: Evaluate Skill

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚀 FluxLoop Evaluation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Current Status
  • Scenario: Order Accuracy Test
  • Experiment: exp_abc (10 runs)
  • Profile: ✅ up-to-date (a1b2c3d)

────────────────────────────────────

🔄 Running server evaluation...

✅ Evaluation → 3 insights 🔗 https://alpha.app.fluxloop.ai/...

────────────────────────────────────

📊 Result Analysis

  | Criterion   | Score | Notes                    |
  |-------------|-------|--------------------------|
  | Accuracy    | 8/10  | Order items correct      |
  | Completeness| 6/10  | Frequent option omission |

  💡 Key finding: Consistent error pattern detected in option menu handling

────────────────────────────────────

▶ Improvement Suggestion

  `agents/order_bot.py:42` — Missing multi-select handling in option parsing logic

  👉 Apply the fix? (Yes/No)

────────────────────────────────────

⏭️ Available Next Actions
  • Re-test after fix (test)
  • Prompt A/B comparison (prompt-compare)
```

## Rules

1. **Every skill output** must start with the Skill Header (thick divider + title)
2. **Every section transition** must have a thin divider
3. **Never output plain text without structure** — even a single-step result needs the header + status + result format
4. **Commands the user must run** are always marked with `👉`
5. **Link mandatory** — When creating or referencing server resources, use the `✅ Action → summary 🔗 URL` format and **always output the full URL**. See the "Result / Completion" section above for URL patterns.
6. **First-encounter explanation** — Explanation of 1-2 sentences is required when using a domain term for the first time. Do not assume terms are self-explanatory from the user's perspective.
7. **Keep prose minimal** — Use bullet lists after explanations; however, Core Principles #5 (first-encounter explanation) is an exception
8. **Status block** appears right after the header, before any action steps
