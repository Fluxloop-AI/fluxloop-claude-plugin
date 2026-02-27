---
name: fluxloop-context
description: |
  Use for scanning the codebase and creating/updating the agent profile.
  Frequency: once initially, then only when agent code changes. Stale detection handles this automatically.
  Keywords: context, profile, scan, update profile, agent info, 에이전트 파악, 프로필 업데이트, 코드베이스 스캔

  Auto-activates on requests like:
  - "에이전트 파악해줘", "scan the agent"
  - "update profile", "프로필 업데이트"
  - "what does this agent do?", "이 에이전트 뭐 하는 거야?"
---

# FluxLoop Context Skill

**Scan-Summarize-Save**: Codebase scan → Profile summary → Server upload + Local save (Dual Write)

## Output Format

> 📎 All user-facing output must follow: read skills/_shared/OUTPUT_FORMAT.md

## Context Protocol

1. `fluxloop context show` → confirm project is set up
2. `.fluxloop/test-memory/` check:
   - Exists → load `agent-profile.md` (show existing profile)
   - Missing → create `.fluxloop/test-memory/` directory (first run)
3. Dual Write:
   - Server: `fluxloop data push` (upload key files)
   - Local: save to `.fluxloop/test-memory/agent-profile.md` with metadata
4. On completion: verify `agent-profile.md` is current (`git_commit` matches)

> 📎 Full protocol: read skills/_shared/CONTEXT_PROTOCOL.md
> 📎 Collection procedure: read skills/_shared/CONTEXT_COLLECTION.md

## Prerequisite

Run `fluxloop context show` first:
- ✅ Project selected → proceed
- ❌ No project → Prerequisite Resolution (📎 read skills/_shared/PREREQUISITE_RESOLUTION.md):
  - "프로젝트 설정이 필요합니다. setup을 먼저 진행할까요?"
  - 승인 시: 📎 `skills/setup/SKILL.md`의 절차를 인라인 실행 → 완료 후 "✅ Setup 완료. 이어서 context를 진행합니다." → Step 1로 복귀
  - 거부 시: 중단

## Workflow

> ⚠️ 각 Step은 반드시 순차 실행한다. Bash/Read 호출을 병렬로 묶지 않는다. (📎 CONTEXT_PROTOCOL.md 참조)

### Step 1: Check Existing Profile

Check if `.fluxloop/test-memory/agent-profile.md` exists.

**If exists**:
- Show existing profile summary
- Display `scan_date` and `git_commit` from metadata
- Ask: "Would you like to update the profile? (Yes/No)"
  - No → keep existing profile, go to Next Steps
  - Yes → proceed to Step 2

**If missing**: "This is the first scan." → proceed to Step 2

### Step 2: Codebase Scan

> 📎 Follow the collection procedure: read skills/_shared/CONTEXT_COLLECTION.md

Scan targets:
1. README.md (or README.rst, README)
2. Agent main file (file containing system prompt, tool definitions)
3. package.json / pyproject.toml / requirements.txt (dependencies)
4. API spec files (OpenAPI, GraphQL schema, etc.)
5. Test files (to understand existing test structure)

Structure the scan results:
- Agent name, role
- LLM model / provider
- System prompt summary (3-5 lines)
- Tools / API list (table)
- Key features (bullet list)
- Dependencies (key packages / services)

### Step 3: Interactive — Additional Documents

Ask: "Do you have any reference documents? (enter path / skip)"
- Path entered → include that file in the scan
- skip → proceed

### Step 4: Intent Refine (서버에 프로젝트 컨텍스트 업로드)

Step 2에서 스캔한 결과를 바탕으로 프로젝트 intent를 정제하여 FluxLoop 서버에 전송한다.

> 💡 **Intent Refine이란?** 에이전트의 목적·기능·기술 스택을 서버가 이해할 수 있는 형태로 요약·전송하는 단계입니다. 서버가 이 정보를 분석하여 이후 시나리오 생성과 테스트 품질을 높이는 데 활용합니다.

```bash
fluxloop intent refine --intent "<에이전트의 목적과 핵심 기능을 1~3문장으로 요약>"
```

- `--intent` 파라미터: Step 2 스캔 결과(에이전트 역할, 주요 기능, 기술 스택)를 기반으로 자동 생성
- 서버가 intent를 분석/정제하여 저장 → 이후 scenario/test에서 활용됨
- 성공 응답: "✓ Intent extracted successfully"
- 실패 시: 에러 메시지 출력 후 Step 5로 진행 (intent 업로드 실패가 전체 워크플로우를 중단하지 않음)

> 📎 Staging environment: read skills/_shared/STAGING.md (staging 환경인 경우 `--staging` 플래그 추가)

### Step 5: Server Upload (Dual Write — Server)

Upload key files:

```bash
fluxloop data push README.md
fluxloop data push <agent-main-file> --bind
```

- `--bind` links the file to the current scenario (use only when a scenario is selected)
- If no scenario exists, upload to the project library without `--bind`

> **필수 결과 출력**: 업로드 완료 후 `✅ Data → N files uploaded to project library` 형식으로 출력.
> (Data 액션은 URL 없음 — POST_ACTIONS.md 참조)

### Step 6: Local Save (Dual Write — Local)

Ensure `.fluxloop/test-memory/` directory exists (create if missing).

Save to `.fluxloop/test-memory/agent-profile.md`:
- Metadata: `<!-- scan_date: {current ISO8601} | git_commit: {git rev-parse --short HEAD} -->`
- Format: follow the template from `test-memory-template/agent-profile.md`
- Replace all placeholders with actual scan results

### Step 7: Profile Summary Output

Show the generated profile to the user:
- Key info: agent name, role, LLM, number of tools, key features
- Ask: "Does this profile look correct? Let me know if anything needs to be changed."

## Error Handling

| Error | Response |
|-------|----------|
| Project not set up | Prerequisite Resolution 적용 → setup 인라인 실행 제안 |
| No README found | Fall back to other files (pyproject.toml, main file); create a limited profile |
| `fluxloop intent refine` failure | Log error, proceed to next step (best-effort — does not block workflow) |
| `fluxloop data push` failure | Check network, verify file path, confirm login status |
| `git rev-parse` failure (not a git repo) | Set `git_commit` to `no-git`; note that stale detection is unavailable |

## Next Steps

Profile ready. Available next action:
- Scenario creation tailored to the agent profile (scenario skill)

## Quick Reference

| Step | Command |
|------|---------|
| Check | `fluxloop context show` |
| Intent | `fluxloop intent refine --intent "..."` |
| Upload | `fluxloop data push <file>` |
| Upload + bind | `fluxloop data push <file> --bind` |
| Git hash | `git rev-parse --short HEAD` |

> 📎 Full CLI reference: read skills/_shared/QUICK_REFERENCE.md

## Key Rules

1. Always check existing `agent-profile.md` before scanning — avoid redundant work
2. Use the template from `test-memory-template/agent-profile.md` for output format
3. Include metadata comment (`scan_date`, `git_commit`) — required for stale detection
4. Dual Write: server upload (`data push`) and local save (`agent-profile.md`) at the same time
5. Use `--bind` only when a scenario is already selected
6. Ask for additional reference documents in interactive mode
7. If no git repo, set `git_commit: no-git` and note stale detection is unavailable
8. Show profile summary and ask for confirmation before finalizing
9. On update: overwrite the entire `agent-profile.md` (not append)
