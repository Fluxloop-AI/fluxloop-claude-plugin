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

The selected scenario 1-liner often contains hidden ambiguity. This step uses a **document-driven, 4-phase progressive exploration** to surface implicit expectations and extract precise contracts through structured dialogue.

> **What is a Contract?** A behavioral rule the agent must follow. Each contract has a type (`must`, `must_not`, `should`, `may`) and a category (`grounding`, `quality`, `safety`, `ux`, `compliance`). Contracts are the foundation for automated test evaluation.

**Working Document**: `scenario-planning.md` serves as the shared memory, context anchor, and to-do tracker throughout Phases 1–4. Create it at `.fluxloop/test-memory/scenario-planning.md` using the template from `test-memory-template/scenario-planning.md`. Update it after every phase. This document prevents context loss between turns and allows the user to review progress at any time.

Scope: analysis is limited to **agent behavior level**. Do not expand into user profiles, business context, or other external concerns.

#### Phase 1: Item Extraction

Analyze the scenario 1-liner and extract all behavioral items into three classifications:

| Classification | Definition | Discrimination Criteria | Handling |
|---------------|------------|------------------------|----------|
| **clear/explicit** | Directly translatable from sentence to code behavior | The sentence unambiguously specifies what the agent should do — no interpretation needed | Agent fills in automatically via agent-profile |
| **unclear/explicit** | Stated in the sentence but ambiguous in meaning | The sentence mentions this behavior but the exact expectation is open to multiple interpretations | Present specific behavioral options (2–4 choices) for user to select |
| **unclear/implicit** | Not mentioned, but logically relevant when considering the code flow | Not in the sentence, but any experienced tester would ask about it given the agent's code flow | Ask "What about this case?" to surface edge cases |

For each item, determine its resolution strategy:

| Strategy | When to Use | Action |
|----------|------------|--------|
| **agent-profile auto-fill** | Answer is derivable from agent-profile.md or code analysis | Agent fills in the definition and confirms with user |
| **user question** | Multiple valid interpretations exist | Present 2–4 concrete behavioral options for user to choose |
| **target exploration** | Rare: requires deep code tracing or domain expertise | Flag for deeper investigation in Phase 2 |

**Agent actions**:
1. Classify all items from the scenario 1-liner
2. Determine resolution strategy for each item
3. Order items: clear/explicit → unclear/explicit → unclear/implicit
4. Create `scenario-planning.md` with all extracted items
5. Present a summary to the user: item count per classification, resolution strategy overview

> ⚠️ **STOP**: Create the file and present the summary. STOP and wait for user acknowledgment before proceeding to Phase 2.

#### Phase 2: Deep Exploration per Item (×N)

Explore each item one at a time, in the order established in Phase 1. Each item goes through 4 sub-steps:

**2-1. Clear Definition**
- Establish the precise behavioral definition for this item
- For agent-profile auto-fill items: present the auto-filled definition for quick confirmation

**2-2. Variant Expansion**
- Expand into concrete cases and variations (present as a table)
- Example: "User asks for column X" → variants: column exists, column doesn't exist, column name is misspelled, etc.

**2-3. Upper-Level Policy Questions**
- From the variants, identify design tensions that require policy decisions
- Formulate as clear policy questions: "When X happens, should the agent do A or B?"
- Include the **worst case question** when relevant: "What's the worst thing the agent could do here?"

**2-4. Confirm & Update**
- User confirms definitions, selects variants, answers policy questions
- Update `scenario-planning.md` with resolved information

> ⚠️ **Critical Principles**:
> - **ONE item per turn. Do NOT bundle multiple items.**
> - **For clear/explicit items**: auto-fill definition + quick confirm. No deep exploration needed — skip 2-2 and 2-3.
> - **If user says "enough" or "this is enough"**: proceed directly to Phase 3 with items explored so far. Set agent-profile-based defaults for remaining items.
> - **Retroactive updates allowed**: later insights may update earlier items — update the document accordingly.

#### Phase 3: Integration & Consolidation

After all items are explored (or user signals "enough"), integrate findings into a coherent picture:

**Full Variant Map**: consolidate all variants across items

| Variant Type | Example | Related Items |
|-------------|---------|---------------|
| {type} | {concrete example} | {item names} |

**Cross-Cutting Policy Summary**: consolidate all policy decisions

| Policy | Decision | Related Items |
|--------|----------|---------------|
| {description} | {resolved decision} | {item names} |

**Policy Conflict Resolution**: if policies from different items conflict:
- Present both sides explicitly
- Provide a recommendation with reasoning
- Ask the user to confirm the resolution

**Risk Behavior List**: collect all identified risk behaviors from Phase 2

Record all integration results in the "Intermediate Results" section of `scenario-planning.md`.

> ⚠️ **STOP**: Present integration results and wait for user confirmation before proceeding to Phase 4.

#### Phase 4: Expectation Level → Contract

Map each resolved item to a contract with an expectation level:

| Expectation | Meaning | → Contract Type |
|------------|---------|-----------------|
| **worst case** | Behavior that must never happen | `must_not` |
| **fair case** | Minimum acceptable behavior | `must` |
| **good case** | Expected behavior | `should` |
| **best case** | Ideal behavior | `may` |

**Contract Presentation Format** — group by type with emoji indicators:

**🔴 MUST**
- **C{N}. {title}** [{emoji}{category}]
  > {explanation from agent's behavioral perspective, including violation conditions}

**⛔ MUST NOT**
- **C{N}. {title}** [{emoji}{category}]
  > {explanation from agent's behavioral perspective, including violation conditions}

**🟡 SHOULD**
- **C{N}. {title}** [{emoji}{category}]
  > {explanation from agent's behavioral perspective, including violation conditions}

**🟢 MAY**
- **C{N}. {title}** [{emoji}{category}]
  > {explanation from agent's behavioral perspective, including violation conditions}

**Category emoji mapping**: grounding 🎯, quality ✨, safety 🛡️, ux 👤, compliance 📋

**Formatting rules**:
- Write every contract from the **agent's behavioral perspective** (e.g., "The agent must..." not "The system should...")
- Include explicit **violation conditions** for each contract
- `must` contracts must be written at an **automated-test-verifiable level** — precise enough that a test can unambiguously determine pass/fail

Record final contracts in the "Contracts" section of `scenario-planning.md`.

> ⚠️ **STOP**: Present contracts for final confirmation before proceeding to Step 5.

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
| Phase 1: Item extraction summary | Inform (user acknowledges) | — |
| Phase 2: Per-item exploration | Ask (required, per item) | clear/explicit: auto-fill + confirm |
| Phase 3: Integration confirmation | Ask (required) | Agent performs consolidation |
| Phase 4: Contract confirmation | Ask (required) | — |
| Step 6: Language selection | Ask | Use project default |

> Min 3 required user interactions (scenario selection + at least 1 item exploration + contract confirmation).

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
| Intent Discovery taking too long | Detect user fatigue → summarize explored items, set agent-profile-based defaults for remaining items, proceed to Phase 3 |

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
7. Intent Discovery explores ONE item at a time in depth. Do NOT dump all analysis questions at once. Use `scenario-planning.md` as the working document throughout.
8. Use the template from `test-memory-template/test-strategy.md` for output format
9. Scenario folder names: English kebab-case only (`order-bot`)
10. Display names: any language allowed
11. Suggest 3 naming candidates, allow custom input
12. Run `fluxloop init scenario` from workspace root (NOT home directory)
13. Dual Write: server (`scenarios create`) and local (`test-strategy.md`) at the same time
14. On update: overwrite `test-strategy.md` entirely (not append)
15. Resolution strategy: agent-profile auto-fill first → user question → target exploration (exceptional)
16. Phase 2 clear/explicit items: auto-fill and quick confirm. Do NOT deep-explore clear items.
17. If user says "this is enough", proceed directly to Phase 3.
18. `scenario-planning.md` is an intermediate document. Final contracts go to `test-strategy.md` in Step 5.
