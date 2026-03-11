# Prerequisite Resolution Protocol

When a prerequisite is missing during skill execution, do not tell the user "Please do X first" and stop.
Instead, follow the procedure below to execute prerequisite skills inline.

## Dependency Chain

```
setup → context → persona → scenario → test → evaluate
```

## Resolution Procedure

1. **Check CLI installation**: Run `fluxloop --version` → if `command not found`, start from the setup skill's installation step
2. **Identify missing scope**: Use `fluxloop context show` + local file existence to identify where to start
3. **User confirmation**: List the required prerequisite steps and confirm at once
   - 1 missing: "{skill_name} has not been completed yet. Shall I proceed with it first?"
   - Multiple missing: "{skill_A} → {skill_B} need to be run in order. Shall I proceed sequentially?"
4. **On approval**: Execute the required skills inline in order
   - Follow each skill's SKILL.md procedure
   - On each completion: "✅ {skill_name} complete — {one-sentence summary of what the skill did}. Continuing with {next}."
     - Example: "✅ Setup complete — CLI installed and project connected. Continuing with context."
     - Example: "✅ Context complete — Analyzed agent code and generated profile. Continuing with scenario."
   - After all prerequisites complete: automatically return to Step 1 of the originally requested skill
5. **On rejection**: Stop the current skill and only inform which prerequisite skills are needed

## Inline Execution Rules

- Execute only the **core procedure** of prerequisite skills — skip closing guidance ("Next, you can try X")
- If an error occurs during prerequisite execution → report the error to the user and **stop entirely** (do not proceed to the original skill)
- The setup skill requires user interaction (login, project selection), so keep those steps as-is
- A single confirmation covers all required prerequisite skills executed in order (do not re-confirm for each skill)

## Status Check Criteria

| Check Target | How to Check | Required Skill if Missing |
|--------------|-------------|--------------------------|
| CLI installation | `fluxloop --version` → command not found | setup (installation step) |
| Project setup | `fluxloop context show` → no project | setup (auth/project step) |
| Agent profile | `.fluxloop/test-memory/agent-profile.md` absent | context |
| Persona pool | `.fluxloop/test-memory/persona-pool.md` absent | persona |
| Scenario | `fluxloop context show` → no scenario | scenario |
| Test results | `.fluxloop/test-memory/results-log.md` absent or 0 entries | test |

## Skip Messages (when already completed)

When a prerequisite is already met and inline execution is triggered, skip the skill and notify with a single line.

| Status | Message |
|--------|---------|
| setup (installation) complete | "✅ fluxloop-cli installed (vX.X.X) — skipping installation step" |
| setup (project) complete | "✅ Project connected (proj_xxx) — skipping setup" |
| context complete (up-to-date) | "✅ Agent profile is current (scanned {N} days ago) — skipping context" |
| context complete (stale) | "⚠️ Profile is outdated (code changes detected) — update recommended (optional)" |
| persona complete | "✅ Persona pool exists ({N} personas) — skipping persona" |
| scenario complete | "✅ Active scenario exists ({scenario_name}) — skipping scenario" |
| test complete | "✅ Recent test results exist (exp_xxx) — proceeding directly to evaluation" |
