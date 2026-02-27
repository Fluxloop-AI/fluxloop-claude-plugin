---
name: fluxloop-scenario
description: |
  Use for creating test scenarios, contracts, and agent wrapper setup.
  Frequency: when test objectives change or new scenarios are needed. Reuses existing scenarios otherwise.
  Keywords: scenario, create scenario, init, contract, wrapper, agent setup, 시나리오, 시나리오 만들기, 계약

  Auto-activates on requests like:
  - "시나리오 만들어줘", "create a scenario"
  - "init scenario", "set up a test"
  - "래퍼 설정해줘", "configure the wrapper"
---

# FluxLoop Scenario Skill

**Scenario-First**: Agent profile check → Scenario init → Contract creation → Wrapper setup → Test ready

## Context Protocol

1. `fluxloop context show` → confirm project is set up and scenario state
2. `.fluxloop/test-memory/` check:
   - Load `agent-profile.md` → stale detection (compare `git_commit` vs `git rev-parse --short HEAD`)
   - Load `learnings.md` → incorporate previous insights (if exists)
   - Missing files → proceed (first run)
3. Dual Write:
   - Server: `fluxloop scenarios create/refine`, `fluxloop sync pull`
   - Local: save to `.fluxloop/test-memory/test-strategy.md`
4. On completion: verify `test-strategy.md` is current for the test skill

> 📎 Stale detection: read skills/_shared/CONTEXT_PROTOCOL.md
> 📎 Collection procedure (for inline refresh): read skills/_shared/CONTEXT_COLLECTION.md

## Prerequisite

Run `fluxloop context show` first:
- ✅ Project selected + `.fluxloop/test-memory/agent-profile.md` exists → proceed
- ❌ No project (setup 누락) → Prerequisite Resolution (📎 read skills/_shared/PREREQUISITE_RESOLUTION.md):
  - "프로젝트 설정과 에이전트 분석이 모두 필요합니다. setup → context 순서로 진행할까요?"
  - 승인 시:
    1. 📎 `skills/setup/SKILL.md` 인라인 실행 → "✅ Setup 완료."
    2. 📎 `skills/context/SKILL.md` 인라인 실행 → "✅ Context 완료. 이어서 scenario를 진행합니다."
    → Step 1로 복귀
  - 거부 시: 중단
- ❌ Project selected but no agent-profile.md (context 누락) → Prerequisite Resolution:
  - "에이전트 분석이 필요합니다. context를 먼저 진행할까요?"
  - 승인 시: 📎 `skills/context/SKILL.md` 인라인 실행 → 완료 후 Step 1로 복귀
  - 거부 시: 중단

## Workflow

### Step 1: Context Load + Stale Detection

- Read `.fluxloop/test-memory/agent-profile.md`:
  - Extract `git_commit` from metadata comment
  - Compare with `git rev-parse --short HEAD`
  - If different → "The profile looks outdated. Would you like to update it?"
    - Yes → follow `_shared/CONTEXT_COLLECTION.md` procedure inline
    - No → continue with existing profile
  - If `git_commit` is `no-git` → continue without warning (stale detection unavailable)
- Read `.fluxloop/test-memory/learnings.md` (if exists):
  - Incorporate previous insights into scenario design
  - Display: "Previous learnings found: {summary}"
- Understand agent characteristics → use in Step 3 for scenario recommendations

### Step 2: Scenario Initialization

```bash
fluxloop init scenario <name>
```

- Naming rules:
  - Folder name: English kebab-case only (e.g., `order-bot`)
  - Suggest 3 name candidates based on agent characteristics, allow custom input
- ⚠️ Common mistake: "Run from workspace root, not home directory. Check `pwd` and `fluxloop context show`."

### Step 3: Scenario Recommendation

Suggest 3 scenarios based on `agent-profile.md`:

| # | Type | Description |
|---|------|-------------|
| 1 | **Happy Path** | Core feature verification |
| 2 | **Edge Cases** | Exception/boundary handling |
| 3 | **Advanced** | Multi-turn or domain-specific |

- Present 3 options + "Custom input" → user selects
- If `learnings.md` insights exist, reflect them in recommendations
  - Example: "Previous tests showed weak edge case handling" → prioritize Edge Cases
- After selection: specify display name (any language allowed)

### Step 4: Language Selection

- Select language for scenario generation
- If project-level language is already set → suggest as default, allow override
- Apply to `fluxloop scenarios create --name "..." --goal "..."` command

### Step 5: Contract Creation + Strategy Save (Dual Write)

**(Server)**:

```bash
fluxloop scenarios create --name "Order Accuracy Test" --goal "..."
fluxloop scenarios refine --scenario-id <id>
fluxloop sync pull   # Download contracts locally
```

After `sync pull`: "📋 You can review/edit contracts in the web app"

**(Local)**: Save to `.fluxloop/test-memory/test-strategy.md` (format: `test-memory-template/test-strategy.md`)

Fields to populate:
- Active Scenarios: scenario name, ID, goal, status=active
- Test Objectives: extracted from scenario goal
- Contract Summary: contract count, key coverage
- Evaluation Criteria: set based on scenario characteristics (default: accuracy, completeness, relevance)
- Test Configuration: turn mode (TBD), input count (TBD), wrapper path

> 📎 Post-Action: read skills/_shared/POST_ACTIONS.md

### Step 6: API Key Setup

- Check `.fluxloop/.env` → if exists, skip
- If missing: `fluxloop apikeys create`
- API key file location: `.fluxloop/.env` (shared across scenarios)
- Manual addition guide:
  - OpenAI: `OPENAI_API_KEY=sk-xxx`
  - Anthropic: `ANTHROPIC_API_KEY=sk-ant-xxx`

### Step 7: Wrapper Setup

Basic flow:
1. Determine if wrapper is needed (based on agent type)
2. If needed → create `wrapper.py` + update `simulation.yaml`
3. Debug test: `python -c "from agents.wrapper import run; print(run('test'))"`

> 📎 Wrapper setup detail: read skills/scenario/references/wrapper-guide.md

### Interactive Checkpoints

| Step | Interactive | Auto |
|------|------------|------|
| Step 3: Scenario selection | Ask (required) | Auto-select #1 |
| Step 5: Contract review | URL only | URL only |

> Max 1 required user response (scenario selection).

## Error Handling

| Error | Response |
|-------|----------|
| No project set up | Prerequisite Resolution 적용 → setup + context 인라인 실행 제안 |
| No agent profile | Prerequisite Resolution 적용 → context 인라인 실행 제안 |
| `fluxloop init scenario` in home directory | "Run from workspace root, not home. Check `pwd` and `fluxloop context show`" |
| `scenarios create` failure | Check network, verify login status, confirm project is selected |
| `scenarios refine` timeout | Retry with `fluxloop scenarios refine --scenario-id <id>` |
| API key file missing | Guide: `fluxloop apikeys create` or manual `.fluxloop/.env` creation |
| Wrapper `ModuleNotFoundError` | Check `runner.target` in simulation.yaml, verify Python path |
| Wrapper `TypeError: run() missing argument` | Ensure wrapper signature: `(input_text: str, metadata: dict = None)` |
| Local path mismatch in context | `fluxloop scenarios select <id> --local-path <folder>` |

## Next Steps

Scenario ready! Continue with:
- "테스트 돌려줘" → test skill (run tests against the scenario)

## Quick Reference

| Step | Command |
|------|---------|
| Check | `fluxloop context show` |
| Init | `fluxloop init scenario <name>` |
| Create | `fluxloop scenarios create --name X --goal "..."` |
| Refine | `fluxloop scenarios refine --scenario-id <id>` |
| Pull | `fluxloop sync pull` |
| API key | `fluxloop apikeys create` |
| Git hash | `git rev-parse --short HEAD` |

> 📎 Full CLI reference: read skills/_shared/QUICK_REFERENCE.md

## Key Rules

1. Always read `agent-profile.md` first — use agent characteristics for scenario recommendations
2. Always check stale detection on `agent-profile.md` before proceeding
3. Read `learnings.md` (if exists) to incorporate previous insights into scenario design
4. Use the template from `test-memory-template/test-strategy.md` for output format
5. Scenario folder names: English kebab-case only (`order-bot`)
6. Display names: any language allowed
7. Suggest 3 naming candidates, allow custom input
8. Run `fluxloop init scenario` from workspace root (NOT home directory)
9. Dual Write: server (`scenarios create/refine` + `sync pull`) and local (`test-strategy.md`) at the same time
10. On update: overwrite `test-strategy.md` entirely (not append)
