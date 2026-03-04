# Context Protocol

All skills (except setup) follow this protocol to manage `.fluxloop/test-memory/`.

## Common 4 Steps

> ⚠️ **Steps 0–2 must be executed sequentially.** Parallel invocations may cause sibling tool call errors, so confirm each step's result before proceeding to the next. Auxiliary commands such as `git rev-parse --short HEAD` must also run sequentially within the relevant step, not as independent calls.

0. Run `fluxloop --version` → if `command not found`, the CLI is not installed → trigger setup skill (installation step) before proceeding
1. Run `fluxloop context show` → confirm project / scenario ID
2. Check `.fluxloop/test-memory/` directory:
   - Exists → load relevant files per the mapping below
   - Missing → proceed without warning (first run; create the directory automatically)
3. Dual Write at each workflow step:
   - Server: upload / create via `fluxloop` CLI commands
   - Local: save the same information to the corresponding `.fluxloop/test-memory/` file
4. On completion → verify the files that the next skill reads are up to date

## Dual Write Principle

> Information sent to the server and saved to `.fluxloop/test-memory/` must be written **at the same moment**.
> The server is the execution environment for the CLI workflow; `.fluxloop/test-memory/` is the context bridge between skills.

## Per-Skill Read / Write Mapping

| Skill | Reads | Writes | Server Connection (CLI) |
|-------|-------|--------|------------------------|
| setup | — | — | `auth login`, `projects create/select` |
| context | — | agent-profile | `intent refine`, `data push` |
| scenario | agent-profile, learnings | test-strategy, scenario-planning-{name} | `scenarios create/refine`, `sync pull` |
| test | agent-profile, test-strategy | results-log | `sync pull`, `test --scenario` |
| evaluate | agent-profile, results-log, test-strategy | learnings, results-log | `evaluate --experiment-id` |
| prompt-compare | agent-profile, results-log | prompt-versions, results-log | `test --scenario` (×2) |

## Stale Detection (agent-profile.md only)

The scenario, test, evaluate, and prompt-compare skills check for staleness when reading `agent-profile.md`:

1. Extract `git_commit` from the metadata comment at the top of the file
2. Compare against the output of `git rev-parse --short HEAD`
3. If different → ask: "The profile looks outdated. Would you like to update it?"
   - Yes → run the procedure in `_shared/CONTEXT_COLLECTION.md` inline
   - No → continue with the existing profile

## Data Flow

```
context → agent-profile.md + intent refine (server) + data push (server)
  ↓
scenario → read agent-profile (stale? → refresh) → test-strategy.md + scenario-planning-{name}.md + scenarios create (server)
  ↓
test → read agent-profile, test-strategy (stale? → refresh) → results-log.md + test results (server)
  ↓
evaluate → read results-log → learnings.md + evaluation results (server)
  ↓
scenario → read learnings → improved scenario design (loop)
```

## Prerequisite Resolution

When inter-skill dependencies are not met, do not send a blocking message to the user.
Instead, follow the protocol defined in 📎 `skills/_shared/PREREQUISITE_RESOLUTION.md`.

Core principles:
1. Never tell the user "Please do X first"
2. Instead, confirm with "X is required. Shall I proceed?"
3. On approval, execute the prerequisite skills inline in order
4. After all prerequisite skills complete, automatically return to the originally requested skill

## SKILL.md Insertion Template

Each skill's SKILL.md should include a Context Protocol section following this pattern:

```markdown
## Context Protocol
0. `fluxloop --version` → if command not found → trigger setup (installation)
1. `fluxloop context show` → {confirm project state}
2. `.fluxloop/test-memory/` check:
   - Exists → load {files this skill reads}
   - Missing → proceed (first run)
3. Dual Write:
   - Server: {CLI commands this skill uses}
   - Local: save to {files this skill writes}
4. On completion: verify {files the next skill reads} are current

> 📎 Stale detection: read skills/_shared/CONTEXT_PROTOCOL.md
> 📎 Collection procedure: read skills/_shared/CONTEXT_COLLECTION.md
```
