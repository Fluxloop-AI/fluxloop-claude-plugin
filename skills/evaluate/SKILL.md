---
name: fluxloop-evaluate
description: |
  Use for evaluating test results, analyzing insights, and improving the agent.
  Frequency: after every test run. Core of the daily test → evaluate → fix loop.
  Keywords: evaluate, evaluation, improve, analyze results, insights, recommendations, re-test, 평가, 개선, 분석

  Auto-activates on requests like:
  - "평가해줘", "evaluate the results"
  - "에이전트 개선해줘", "improve my agent"
  - "결과 분석해줘", "analyze results"
---

# FluxLoop Evaluate Skill

**Evaluate-Analyze-Improve**: Server evaluation → Result analysis → Insight recording → Code improvement → Re-test loop

## Output Format

> 📎 All user-facing output must follow: read skills/_shared/OUTPUT_FORMAT.md

## Context Protocol

1. `fluxloop context show` → confirm project / scenario / test results exist
2. `.fluxloop/test-memory/` check:
   - Exists → load `agent-profile.md`, `results-log.md`, `test-strategy.md`
   - Missing → "Run '테스트 돌려줘' first"
3. Dual Write:
   - Server: `fluxloop evaluate --experiment-id`
   - Local: save to `.fluxloop/test-memory/learnings.md`, append to `.fluxloop/test-memory/results-log.md`
4. On completion: verify `learnings.md` is current (next scenario skill reads it)

> 📎 Full protocol: read skills/_shared/CONTEXT_PROTOCOL.md
> 📎 Collection procedure: read skills/_shared/CONTEXT_COLLECTION.md

## Prerequisite

Run `fluxloop context show` first:
- ✅ Project selected + scenario exists + test completed → proceed
- ❌ 누락된 단계 감지 → Prerequisite Resolution (📎 read skills/_shared/PREREQUISITE_RESOLUTION.md):
  - 누락 범위를 파악하고 필요한 체인을 나열한다:
    - setup 누락: "setup → context → scenario → test 순서로 진행이 필요합니다. 순서대로 진행할까요?"
    - context 누락: "context → scenario → test 순서로 진행이 필요합니다. 순서대로 진행할까요?"
    - scenario 누락: "scenario → test 순서로 진행이 필요합니다. 순서대로 진행할까요?"
    - test만 누락: "테스트 실행이 필요합니다. 먼저 진행할까요?"
  - 승인 시: 필요한 스킬을 순서대로 인라인 실행 → 각 완료 시 "✅ {스킬명} 완료." → 모두 완료 후 Step 1로 복귀
  - 거부 시: 중단

Verify test completion: check `.fluxloop/test-memory/results-log.md` has at least 1 entry, or run `fluxloop test results --scenario <name>`.

## Workflow

### Step 1: Context Load

- Read `.fluxloop/test-memory/agent-profile.md` → stale check (compare `git_commit` vs `git rev-parse --short HEAD`)
  - Stale → "프로필이 오래된 것 같은데, 업데이트 해드릴까요?"
    - Yes → run collection procedure inline (📎 read skills/_shared/CONTEXT_COLLECTION.md)
    - No → continue with existing profile
- Read `.fluxloop/test-memory/results-log.md` → identify latest experiment ID, pass/fail ratio, history
- Read `.fluxloop/test-memory/test-strategy.md` → load Evaluation Criteria

### Step 2: Server Evaluation

Trigger server-side evaluation:

```bash
fluxloop evaluate --experiment-id <id> --wait
fluxloop evaluate --experiment-id <id> --wait --timeout 900 --poll-interval 5
```

- `--wait` polls until status is `completed`, `partial`, `failed`, or `cancelled`
- When finished as `completed` or `partial` with at least one run completed → insights are generated
- If job stays `queued` >30s without `locked_at` → warn: "Workers may be down or backlog is high"

**Dual Write**:
- (Server) Evaluation results stored on server
- (Local) Append "Evaluation Results" section to the matching experiment entry in `.fluxloop/test-memory/results-log.md`:

```markdown
### Evaluation Results (added after evaluate skill runs)

| Criterion | Score | Notes |
|-----------|-------|-------|
| {criterion name} | {score} | {brief comment} |

**Insight**: {key finding from this run}

**Server link**: 🔗 {experiment URL}
```

> **필수 링크 출력**: 아래 Web Handoff 형식을 반드시 따른다. CLI 출력에서 `experiment_id`와 `project_id`를 추출하여 URL을 구성한다.

**Web Handoff** — output after evaluation:

```
✅ Evaluation → N insights 🔗 https://alpha.app.fluxloop.ai/release/experiments/exp_abc/evaluation?project=proj_123
📋 Check detailed analysis in the web app:
  - Decision: gates, budgets, baseline comparison
  - Insights: findings by category (with severity)
  - Recommendations: improvement suggestions (with priority)
  - Baseline: set the current result as baseline
```

### Step 3: Result Analysis + Insight Recording

Sync and analyze:

```bash
fluxloop sync pull --bundle-version-id <id>
fluxloop test results --scenario <name>
```

Analyze: failure patterns, warning turns, contract violations, related code locations.

Save findings to `.fluxloop/test-memory/learnings.md`:
- Format: follow `test-memory-template/learnings.md`
- **Discovered Patterns**: add Strengths / Weaknesses with new evidence
- **Applied Improvements**: add new rows to the table
- **Warnings for Next Test**: issues requiring verification
- **Open Questions**: unanswered hypotheses
- If existing content → update (preserve existing + add new evidence), never overwrite

This `learnings.md` is read by the scenario skill in the next cycle → **core of the improvement loop**.

### Step 4: Code Fix Suggestions

Based on analysis, suggest agent code modifications with specific file:line references.

> **Code changes always require user confirmation**, even in Auto mode.

| Step | Interactive | Auto |
|------|------------|------|
| Result analysis | Show + confirm | Show only |
| Code fix | Suggest → confirm (required) | Suggest → confirm (required) |
| Re-test | Ask "Re-test?" | Auto-proceed |
| Re-evaluate | Ask "Re-evaluate?" | Auto-proceed |

After edits, the hook runs `fluxloop test --smoke --quiet` automatically.

### Step 5: Re-test Guidance

If code was modified → guide to re-test:
- "테스트 돌려줘" (test skill)
- Use the same bundle for comparison consistency:
  ```bash
  fluxloop sync pull --bundle-version-id <id>
  fluxloop test --scenario <name>
  ```

### Step 6: Re-evaluate (Iteration Loop)

If unsatisfied with re-test results → repeat from Step 2:
- Run the evaluate workflow again for the same flow
- Each iteration appends to `learnings.md` Applied Improvements → tracks improvement history

## Error Handling

| Error | Response |
|-------|----------|
| Experiment ID not found | `fluxloop test results --scenario <name>` to find recent experiment ID |
| Evaluation timeout | Retry with `--timeout 900 --poll-interval 5` |
| Evaluation status `failed` / `cancelled` | Possible server issue; check status in web app |
| `.fluxloop/test-memory/results-log.md` missing | Prerequisite Resolution 적용 → test 인라인 실행 제안 |
| Worker delay (`queued` >30s without `locked_at`) | "Workers may be down or backlog is high" |

## Next Steps

Evaluation complete. Available next actions:
- Re-test with updated code (test skill)
- Compare prompt versions A vs B (prompt-compare skill)
- Improve scenario using learnings (scenario skill — reads learnings.md)

## Quick Reference

| Step | Command |
|------|---------|
| Check | `fluxloop context show` |
| Results | `fluxloop test results --scenario <name>` |
| Evaluate | `fluxloop evaluate --experiment-id <id> --wait` |
| Sync | `fluxloop sync pull --bundle-version-id <id>` |

> 📎 Full CLI reference: read skills/_shared/QUICK_REFERENCE.md

## Key Rules

1. Always run `fluxloop context show` first — route to the correct step based on state
2. Stale check `agent-profile.md` on load (`git_commit` comparison)
3. Dual Write: server evaluation results + local `results-log.md` update simultaneously
4. Code changes always require user confirmation (Auto mode included — no exceptions)
5. `learnings.md`: update (preserve existing + add new evidence); `results-log.md`: append
6. Re-test / re-evaluate loop: repeat Steps 2-6 until satisfied
7. Cite specific file:line locations when suggesting code improvements
