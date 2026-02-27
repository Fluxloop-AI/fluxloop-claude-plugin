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

### Step 4: Server Upload (Dual Write — Server)

Upload key files:

```bash
fluxloop data push README.md
fluxloop data push <agent-main-file> --bind
```

- `--bind` links the file to the current scenario (use only when a scenario is selected)
- If no scenario exists, upload to the project library without `--bind`

> 📎 Post-Action: read skills/_shared/POST_ACTIONS.md

### Step 5: Local Save (Dual Write — Local)

Ensure `.fluxloop/test-memory/` directory exists (create if missing).

Save to `.fluxloop/test-memory/agent-profile.md`:
- Metadata: `<!-- scan_date: {current ISO8601} | git_commit: {git rev-parse --short HEAD} -->`
- Format: follow the template from `test-memory-template/agent-profile.md`
- Replace all placeholders with actual scan results

### Step 6: Profile Summary Output

Show the generated profile to the user:
- Key info: agent name, role, LLM, number of tools, key features
- Ask: "Does this profile look correct? Let me know if anything needs to be changed."

## Error Handling

| Error | Response |
|-------|----------|
| Project not set up | Prerequisite Resolution 적용 → setup 인라인 실행 제안 |
| No README found | Fall back to other files (pyproject.toml, main file); create a limited profile |
| `fluxloop data push` failure | Check network, verify file path, confirm login status |
| `git rev-parse` failure (not a git repo) | Set `git_commit` to `no-git`; note that stale detection is unavailable |

## Next Steps

Profile ready! Continue with:
- "시나리오 만들어줘" → scenario skill (create scenarios tailored to the agent)

## Quick Reference

| Step | Command |
|------|---------|
| Check | `fluxloop context show` |
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
