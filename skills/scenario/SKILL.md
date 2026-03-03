---
name: fluxloop-scenario
description: |
  Use for creating test scenarios, contracts, and agent wrapper setup.
  Combines code-flow analysis with Intent Discovery to extract contracts that reflect user intent.
  Frequency: when test objectives change or new scenarios are needed. Reuses existing scenarios otherwise.
  Keywords: scenario, create scenario, init, contract, contract extraction, intent discovery, wrapper, agent setup

  Auto-activates on requests like:
  - "create a scenario", "init scenario"
  - "set up a test", "configure the wrapper"
---

# FluxLoop Scenario Skill

**Scenario-First**: Agent profile check → Scenario init → Code-based scenario proposal → Intent Discovery → Contract extraction → Setup

## Output Format

> Read skills/_shared/OUTPUT_FORMAT.md

## Context Protocol

1. `fluxloop context show` → confirm project is set up and scenario state
2. `.fluxloop/test-memory/` check:
   - Load `agent-profile.md` → stale detection (compare `git_commit` vs `git rev-parse --short HEAD`)
   - Load `learnings.md` → incorporate previous insights (if exists)
   - Missing files → proceed (first run)
3. Dual Write:
   - Server: `fluxloop scenarios create/refine`
   - Local: save to `.fluxloop/test-memory/test-strategy.md`
4. On completion: verify `test-strategy.md` is current for the test skill

> Stale detection: read skills/_shared/CONTEXT_PROTOCOL.md
> Collection procedure (for inline refresh): read skills/_shared/CONTEXT_COLLECTION.md

## Prerequisite

Run `fluxloop context show` first:
- Project selected + `.fluxloop/test-memory/agent-profile.md` exists → proceed
- No project (setup missing) → Prerequisite Resolution (read skills/_shared/PREREQUISITE_RESOLUTION.md):
  - "Both project setup and agent analysis are required. Proceed with setup → context in order?"
  - Approved:
    1. Run `skills/setup/SKILL.md` inline → "Setup complete."
    2. Run `skills/context/SKILL.md` inline → "Context complete. Continuing with scenario."
    → return to Step 1
  - Denied: stop
- Project selected but no agent-profile.md (context missing) → Prerequisite Resolution:
  - "Agent analysis is required. Would you like to run context first?"
  - Approved: Run `skills/context/SKILL.md` inline → on completion return to Step 1
  - Denied: stop

## Workflow

> Each Step must be executed sequentially. Do not batch Bash/Read calls in parallel. (See CONTEXT_PROTOCOL.md)

### Step 1: Context Load + Stale Detection

- Read `.fluxloop/test-memory/agent-profile.md`:
  - Extract `git_commit` from metadata comment
  - Compare with `git rev-parse --short HEAD`
  - If different → "Code has changed since the last profile was created (previous: {old_commit} → current: {new_commit}). Would you like to update the profile?"
    - Yes → follow `_shared/CONTEXT_COLLECTION.md` procedure inline
    - No → continue with existing profile
  - If `git_commit` is `no-git` → continue without warning (stale detection unavailable)
- Read `.fluxloop/test-memory/learnings.md` (if exists):
  - Incorporate previous insights into scenario design
  - Display: "Previous learnings found: {summary}"
- Understand agent characteristics → use in Step 3 for scenario proposals

### Step 2: Scenario Initialization

```bash
fluxloop init scenario <name>
```

- Naming rules:
  - Folder name: English kebab-case only (e.g., `order-bot`)
  - Suggest 3 name candidates based on agent characteristics, allow custom input
- Common mistake: "Run from workspace root, not home directory. Check `pwd` and `fluxloop context show`."

### Step 3: Code-Flow Based Scenario Proposal

Read `agent-profile.md` and the actual codebase to propose specific, code-flow-based scenario candidates — NOT generic categories like "Happy Path", "Edge Cases", or "Advanced".

**Input**: Agent analysis from `agent-profile.md` (system prompt, tool list, key features, code flow)

**Analysis process**:
- Trace the agent's code flow: input → processing → output
- Identify specific behavioral checkpoints that need verification
- If `learnings.md` exists, reflect previous test insights in proposals

**Output**: Present 3–5 scenario candidates in a table:

| # | Scenario | What code flow it verifies |
|---|----------|---------------------------|
| 1 | {concrete scenario} | {which code path / behavior is tested} |
| 2 | {concrete scenario} | {which code path / behavior is tested} |
| ... | ... | ... |

**Guidelines for scenario proposals** (adapt to the agent type):
- Data analysis agent: "Returns correct results for user query", "Gracefully rejects request for nonexistent column"
- RAG agent: "Synthesizes answers from multiple documents", "Handles questions with no relevant documents"
- Chatbot: "Maintains context across multi-turn conversation", "Handles off-topic requests appropriately"

**User interaction**:
- User selects from the candidates or enters a custom scenario
- After selection: specify a display name (any language allowed)

> Scenarios must describe **what the agent does** in a specific code flow, not abstract test categories.
> Overly specific details (table names, column names, etc.) belong in the contract (Step 4), not the scenario level.

### Step 4: Intent Discovery & Contract Extraction

The selected scenario 1-liner often contains hidden ambiguity. This step uses the Intent Discovery framework to surface implicit expectations and extract precise contracts through structured dialogue.

> **What is a Contract?** A behavioral rule the agent must follow. Each contract has a type (`must`, `must_not`, `should`, `may`) and a category (`grounding`, `quality`, `safety`, `ux`, `compliance`). Contracts are the foundation for automated test evaluation.

#### 4-A. Initial Analysis (agent performs internally — no user confirmation needed)

Analyze the scenario 1-liner along three dimensions:

| Classification | Definition | Handling |
|---------------|------------|----------|
| **clear/explicit** | Directly translatable from sentence to code behavior | Agent fills in automatically. No user confirmation needed. |
| **unclear/explicit** | Stated in the sentence but ambiguous in meaning | Present specific behavioral options (2–4 choices) for user to select. |
| **unclear/implicit** | Not mentioned, but logically relevant when considering the code flow | Ask "What about this case?" to surface edge cases the user hasn't considered. |

Scope: analysis is limited to **agent behavior level**. Do not expand into user profiles, business context, or other external concerns.

#### 4-B. Conversational Resolution

Resolve ambiguities in order: **unclear/explicit first → unclear/implicit second**.

**Resolving unclear/explicit items**:
- For each ambiguous expression, present 2–4 concrete behavioral options
- User selects one or describes their own expectation

**Resolving unclear/implicit items**:
- Ask "What should the agent do in this case?" to naturally expose edge cases
- Limit to 2–3 questions maximum

**Worst case question** (always include):
- "What's the worst thing the agent could do in this scenario?"
- This directly elicits `must_not` contracts

**Conversation flow control**:
- If there are 3+ unclear/explicit items: resolve the top 2–3 first, then set defaults for the rest and confirm: "I've set these defaults — anything you'd like to change?"
- Limit unclear/implicit questions to 2–3 maximum (worst case question is always included)
- The entire Intent Discovery conversation should converge within **2–3 rounds**

#### 4-C. Case Quality Determination

For each resolved item, determine the expectation level:

| Case | Meaning | → Contract Type |
|------|---------|-----------------|
| **fair case** | Minimum acceptable behavior | `must` / `must_not` |
| **good case** | Expected behavior | `should` |
| **best case** | Ideal behavior | `may` |

In practice: the agent proposes fair/good/best together for each item, and the user confirms or adjusts the level (e.g., "this should be must, not should").

#### 4-D. Contract Assembly

Compile the conversation results into a contract table:

| type | category | contract |
|------|----------|----------|
| `must` | grounding | {specific contract content} |
| `must_not` | safety | {specific contract content} |
| `should` | quality | {specific contract content} |
| `may` | ux | {specific contract content} |

**Contract types**: `must`, `must_not`, `should`, `may`
**Categories**: `grounding`, `quality`, `safety`, `ux`, `compliance` (agent classifies as appropriate)

Present the assembled contract table to the user for final confirmation.

### Step 5: Contract Save (Dual Write — Local First)

**Local save**:
- Save the refined scenario description and contracts to `.fluxloop/test-memory/test-strategy.md`
- Follow the existing `test-strategy.md` template format (see `test-memory-template/test-strategy.md`)
- Populate "Active Scenarios" with: scenario name, goal (refined description), status
- Add a "Contract Summary" section with: contract count, type distribution, key contracts summary

**Server sync** (placeholder):
- Use `fluxloop scenarios create --name "..." --goal "..."` with the refined description as `--goal`
- Full contract upload to server: TBD (update this step when server contract API is finalized)
- For now: include a placeholder note — "Server contract sync will be added when the API is available"

### Step 6: Language Selection

- Select language for scenario generation
- If project-level language is already set → suggest as default, allow override
- Apply to `fluxloop scenarios create --name "..." --goal "..."` command

### Step 7: API Key Setup

- Check `.fluxloop/.env` → if exists, skip
- If missing: `fluxloop apikeys create`
- API key file location: `.fluxloop/.env` (shared across scenarios)
- Manual addition guide:
  - OpenAI: `OPENAI_API_KEY=sk-xxx`
  - Anthropic: `ANTHROPIC_API_KEY=sk-ant-xxx`

### Step 8: Wrapper Setup

Basic flow:
1. Determine if wrapper is needed (based on agent type)
2. If needed → create `wrapper.py` + update `simulation.yaml`
3. Debug test: `python -c "from agents.wrapper import run; print(run('test'))"`

> Wrapper setup detail: read skills/scenario/references/wrapper-guide.md

## Interactive Checkpoints

| Step | Interactive | Auto |
|------|------------|------|
| Step 3: Scenario selection | Ask (required) | — |
| Step 4: Intent Discovery dialogue | Ask (required, 2–3 rounds) | — |
| Step 4 end: Contract table confirmation | Ask (required) | — |
| Step 6: Language selection | Ask | Use project default |

> Min 2 required user interactions (scenario selection + contract confirmation).

## Error Handling

| Error | Response |
|-------|----------|
| No project set up | Apply Prerequisite Resolution → suggest inline setup + context execution |
| No agent profile | Apply Prerequisite Resolution → suggest inline context execution |
| `fluxloop init scenario` in home directory | "Run from workspace root, not home. Check `pwd` and `fluxloop context show`" |
| `scenarios create` failure | Check network, verify login status, confirm project is selected |
| `scenarios refine` timeout | Retry with `fluxloop scenarios refine --scenario-id <id>` |
| API key file missing | Guide: `fluxloop apikeys create` or manual `.fluxloop/.env` creation |
| Wrapper `ModuleNotFoundError` | Check `runner.target` in simulation.yaml, verify Python path |
| Wrapper `TypeError: run() missing argument` | Ensure wrapper signature: `(input_text: str, metadata: dict = None)` |
| Local path mismatch in context | `fluxloop scenarios select <id> --local-path <folder>` |
| Intent Discovery does not converge | Summarize agreements so far and ask for confirmation: "Here's what we've agreed on so far. Shall we finalize this?" |

## Next Steps

Scenario ready. Available next action:
- Run tests against the scenario (test skill)

## Quick Reference

| Step | Command |
|------|---------|
| Check | `fluxloop context show` |
| Init | `fluxloop init scenario <name>` |
| Create | `fluxloop scenarios create --name X --goal "..."` |
| Refine | `fluxloop scenarios refine --scenario-id <id>` |
| API key | `fluxloop apikeys create` |
| Git hash | `git rev-parse --short HEAD` |

> Full CLI reference: read skills/_shared/QUICK_REFERENCE.md

## Key Rules

1. Always read `agent-profile.md` first — use agent characteristics for scenario proposals
2. Always check stale detection on `agent-profile.md` before proceeding
3. Read `learnings.md` (if exists) to incorporate previous insights into scenario design
4. Scenario candidates must be code-flow-based. **Never use generic categories** (Happy Path, Edge Cases, Advanced)
5. Intent Discovery analysis scope is limited to **agent behavior level** — do not expand into user profiles or business context
6. Always include the **worst case question** during Intent Discovery to elicit `must_not` contracts
7. Intent Discovery conversation must converge within **2–3 rounds**
8. Use the template from `test-memory-template/test-strategy.md` for output format
9. Scenario folder names: English kebab-case only (`order-bot`)
10. Display names: any language allowed
11. Suggest 3 naming candidates, allow custom input
12. Run `fluxloop init scenario` from workspace root (NOT home directory)
13. Dual Write: server (`scenarios create`) and local (`test-strategy.md`) at the same time
14. On update: overwrite `test-strategy.md` entirely (not append)
