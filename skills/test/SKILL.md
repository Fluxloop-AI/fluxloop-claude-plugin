---
name: fluxloop-test
description: |
  Use for running tests against scenarios — includes data selection, bundle management, and test execution.
  Frequency: the most common entry point. Run repeatedly during the test-evaluate-fix loop.
  Keywords: test, run test, test my agent, simulation, run simulation, generate test data, synthesize inputs, 테스트, 테스트 돌려, 시뮬레이션

  Auto-activates on requests like:
  - "테스트 돌려줘", "run the test"
  - "test my agent", "시뮬레이션 실행"
  - "generate test data", "테스트 데이터 만들어줘"
---

# FluxLoop Test Skill

**Select-Check-Execute**: Data selection → Pre-check (every path) → Test execution → Result recording (Dual Write)

## Output Format

> 📎 All user-facing output must follow: read skills/_shared/OUTPUT_FORMAT.md

## Context Protocol

1. `fluxloop context show` → confirm project + scenario are set up
2. `.fluxloop/test-memory/` check:
   - Load `agent-profile.md` → stale detection (compare `git_commit` vs `git rev-parse --short HEAD`)
   - Load `test-strategy.md` → understand test objectives and config
   - Missing files → proceed (first run); if `agent-profile.md` missing, guide to context skill
3. Dual Write:
   - Server: `fluxloop test --scenario <name>` (results stored on server, experiment ID generated)
   - Local: append to `.fluxloop/test-memory/results-log.md`
4. On completion: verify `results-log.md` has the new entry for the evaluate skill

> 📎 Stale detection: read skills/_shared/CONTEXT_PROTOCOL.md
> 📎 Collection procedure (for inline refresh): read skills/_shared/CONTEXT_COLLECTION.md

## Prerequisite

Run `fluxloop context show` first:
- ✅ Project selected + scenario exists → proceed
- ❌ 누락된 단계 감지 → Prerequisite Resolution (📎 read skills/_shared/PREREQUISITE_RESOLUTION.md):
  - 누락 범위를 파악하고 필요한 체인을 나열한다:
    - setup 누락: "setup → context → scenario 순서로 진행이 필요합니다. 순서대로 진행할까요?"
    - context 누락: "context → scenario 순서로 진행이 필요합니다. 순서대로 진행할까요?"
    - scenario만 누락: "scenario 생성이 필요합니다. 먼저 진행할까요?"
  - 승인 시: 필요한 스킬을 순서대로 인라인 실행 → 각 완료 시 "✅ {스킬명} 완료." → 모두 완료 후 Step 1로 복귀
  - 거부 시: 중단

## Workflow

### Step 1: Context Load

- Read `.fluxloop/test-memory/agent-profile.md`:
  - Stale detection (compare `git_commit` vs `git rev-parse --short HEAD`)
  - If stale → "The profile looks outdated. Would you like to update it?"
    - Yes → follow `_shared/CONTEXT_COLLECTION.md` procedure inline
    - No → continue with existing profile
  - If `git_commit` is `no-git` → continue without warning
  - Understand agent characteristics (tools, features, dependencies)
- Read `.fluxloop/test-memory/test-strategy.md` (if exists):
  - Understand test objectives, evaluation criteria, test configuration
  - Use wrapper path info from test-strategy in Step 3 pre-check
- If `test-strategy.md` missing: "test-strategy.md not found. You can still run a test, but running the scenario skill first provides better context."

### Step 2: Bundle/Input Selection

> 💡 **용어 설명** (세션에서 처음 등장 시 반드시 사용자에게 전달):
> - **Bundle**: 테스트 입력과 페르소나를 하나로 묶은 스냅샷. 동일 조건으로 반복 테스트할 수 있게 해줍니다.
> - **Input Set**: AI가 생성한 테스트 입력 데이터 모음. Bundle로 발행해야 테스트에 사용 가능합니다.
> - **Persona**: 테스트에서 사용할 가상 사용자 유형 (예: "급한 고객", "처음 이용하는 사용자").

> 📎 Bundle selection decision tree: read skills/_shared/BUNDLE_DECISION.md

Run `fluxloop bundles list --scenario-id <id>` and follow the decision tree:

| Bundle State | Input Set State | Path |
|--------------|----------------|------|
| Multiple | - | User selects → Step 3 |
| One | - | "Use existing / Create new?" → Step 3 or generation |
| None | Multiple | User selects → `bundles publish` → Step 3 |
| None | One | "Use existing / Create new?" → Step 3 or generation |
| None | None | Full generation → Step 3 |

When showing multiple resources, include: **version/name, tag/description, count, created date**

**Full generation path:**

```bash
fluxloop personas suggest --scenario-id <id>
fluxloop inputs synthesize --scenario-id <id>    # --timeout 300 for large, --total-count 2 for quick
# (Interactive only) fluxloop inputs qc → fluxloop inputs refine
fluxloop bundles publish --scenario-id <id> --input-set-id <id>
```

> ⚠️ Do NOT run `fluxloop test` here — always proceed to Step 3 first. (E-M2 fix)

### Step 3: Pre-check (mandatory for ALL paths)

This step ensures no path skips essential checks. (L-H1 fix)

1. **Wrapper check**: Verify `.fluxloop/scenarios/<name>/agents/wrapper.py` or `runner.target` in `configs/simulation.yaml`
   - Not configured → "Wrapper setup is needed. See the scenario skill's wrapper guide."
2. **Turn mode selection**: "Multi-turn? (yes/no), max turns? (default: 8)"
   > 💡 **Multi-turn이란?** 에이전트와 여러 번 주고받는 대화를 시뮬레이션합니다. Single-turn은 1회 질문-응답만 테스트하고, Multi-turn은 맥락을 유지하며 연속 대화하는 능력을 검증합니다.
   - If `test-strategy.md` has previous settings → suggest as default
3. **Provider selection** (multi-turn only): "Provider? (openai/anthropic)"

### Step 4: Data Sync

```bash
fluxloop sync pull --bundle-version-id <id>
```

> ⚠️ Never use `--pull` option — `sync pull` and `test` must run as separate commands.

### Step 5: Test Execution (Dual Write)

**(Server)**:

Single-turn:
```bash
fluxloop test --scenario <name>
```

Multi-turn:
```bash
! fluxloop test --scenario <name> --multi-turn --max-turns <N>
```

> 📎 Multi-turn rules: read skills/_shared/MULTITURN.md

**(Local)**: Append to `.fluxloop/test-memory/results-log.md` (format: `test-memory-template/results-log.md`)

Fields to populate:
- Date, scenario name
- Experiment ID: `exp_xxx`
- Bundle: `bundle_version_id`
- Input count: N
- Turn mode: single / multi-turn
- Pass / Fail: N / M
- Duration: Ns
- Evaluation Results: (leave empty — evaluate skill fills this)
- Insight: (leave empty — evaluate skill fills this)
- Server link: experiment URL

> **필수 링크 출력**: 테스트 완료 후 CLI 출력에서 `experiment_id`를 추출하여 아래 형식으로 반드시 출력:
> `✅ Test → exp_xxx (N runs) 🔗 https://alpha.app.fluxloop.ai/release/experiments/{experiment_id}/evaluation?project={project_id}`

### Step 6: Results Review

```bash
fluxloop test results --scenario <name>
```

Display result summary to the user.

> 📎 CLI options: read skills/test/references/cli-commands.md

## Error Handling

| Error | Response |
|-------|----------|
| No project set up | Prerequisite Resolution 적용 → setup~scenario 체인 인라인 실행 제안 |
| No scenario | Prerequisite Resolution 적용 → scenario 인라인 실행 제안 |
| `Sync API key not set` | "Run `fluxloop apikeys create` or check `.fluxloop/.env`" |
| `Inputs file not found` | "Run `fluxloop sync pull --bundle-version-id <id>` first" |
| `No personas found` | "Run `fluxloop personas suggest --scenario-id <id>` first" |
| `Synthesis timed out` | "Use `--timeout 300` or reduce `--total-count`" |
| `ModuleNotFoundError` in test | "Check `runner.target` in simulation.yaml, ensure wrapper is in Python path" |
| Agent returns None | "Ensure wrapper returns string, not None" |

## Next Steps

Test complete. Available next actions:
- Analyze results and generate insights (evaluate skill)
- Compare prompt versions A vs B (prompt-compare skill)

## Quick Reference

| Step | Command |
|------|---------|
| Check | `fluxloop context show` |
| Bundles | `fluxloop bundles list --scenario-id <id>` |
| Inputs | `fluxloop inputs list --scenario-id <id>` |
| Personas | `fluxloop personas suggest --scenario-id <id>` |
| Synthesize | `fluxloop inputs synthesize --scenario-id <id>` |
| QC | `fluxloop inputs qc --scenario-id <id> --input-set-id <id>` |
| Refine | `fluxloop inputs refine --scenario-id <id> --input-set-id <id>` |
| Publish | `fluxloop bundles publish --scenario-id <id> --input-set-id <id>` |
| Sync | `fluxloop sync pull --bundle-version-id <id>` |
| Test | `fluxloop test --scenario <name>` |
| Multi-turn | `! fluxloop test --scenario <name> --multi-turn --max-turns <N>` |
| Results | `fluxloop test results --scenario <name>` |
| Git hash | `git rev-parse --short HEAD` |

> 📎 Full CLI reference: read skills/_shared/QUICK_REFERENCE.md

## Key Rules

1. Always read `agent-profile.md` first — check stale detection before proceeding
2. Read `test-strategy.md` (if exists) for test objectives and configuration
3. NEVER skip Step 3 (Pre-check) regardless of which bundle path was taken (L-H1 fix)
4. NEVER run `fluxloop test` as part of bundle selection (E-M2 fix) — always go through Pre-check first
5. Use `sync pull` + `test` separately — NEVER use `--pull` option
6. Multi-turn commands must start with `!` prefix
7. Use explicit IDs (`--bundle-version-id`, `--scenario-id`) — **CLI 테이블 출력은 UUID를 잘라서 표시할 수 있으므로, 사용 전 반드시 36자(`xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`) 검증. 36자 미만이면 list 명령 재실행하여 전체 ID 확보 후 사용.**
8. Dual Write: server (test results + experiment ID) and local (`results-log.md`) at the same time
9. Use the template from `test-memory-template/results-log.md` for output format
10. Append to `results-log.md` (most recent at top) — do NOT overwrite
