---
name: fluxloop-scenario
description: |
  Create test scenarios and behavioral rules for agent testing.
  Flow: scenario selection → structured dialogue → rule extraction → save.
  Frequency: when test objectives change or new scenarios are needed.
  Keywords: scenario, create scenario, init, contract, wrapper, agent setup
---

# FluxLoop Scenario Skill

**Flow**: Profile check → Scenario init → Proposal → Analysis → Exploration → Integration → Rules → Save

## Output Format

> Read skills/_shared/OUTPUT_FORMAT.md

## Context Protocol

1. `fluxloop context show` → confirm project + scenario state
2. Load `agent-profile.md` (stale detection) + `learnings.md` (if exists) from `.fluxloop/test-memory/`
3. Dual Write: server (`fluxloop scenarios create/refine`) + local (`test-strategy.md`)

> Stale detection: read skills/_shared/CONTEXT_PROTOCOL.md | Collection: read skills/_shared/CONTEXT_COLLECTION.md

## Prerequisite

- Project + agent-profile.md exists → proceed
- Missing → read skills/_shared/PREREQUISITE_RESOLUTION.md → inline setup/context → return to Step 1

## Workflow

> Execute each Step sequentially. Do not batch Bash/Read calls in parallel.
> Every Step must also follow the Cross-Cutting Rules at the bottom of this document.

### Step 1: Context Load + Stale Detection

**Goal**: Start from an accurate, current understanding of the target agent. If the profile is stale, downstream scenarios may be built on wrong assumptions — making the entire session's output unreliable.

**Principles**:
- This is a grounding step — be efficient. Don't turn it into a lengthy conversation.
- Staleness is not just a version mismatch. When flagging it, briefly explain what *kind* of changes might invalidate previous analysis (e.g., new tools added, prompt rewritten, schema changed).
- Learnings from previous sessions (`learnings.md`) are accumulated team knowledge. Always incorporate them — they prevent re-asking questions the user already answered.

**Procedure**:
- Read `agent-profile.md`: extract `git_commit`, compare with `git rev-parse --short HEAD`
  - If different → ask if user wants to update the profile
  - If `no-git` → continue without warning
- Read `learnings.md` (if exists): incorporate previous insights

### Step 2: Scenario Initialization (automatic)

**Goal**: Set up the workspace so the user can focus on scenario design, not file management. This step should feel invisible — the user just sees a one-line confirmation.

**Principles**:
- Minimize cognitive load. The user didn't come here to think about folder names — derive them silently from agent-profile.
- Keep the confirmation to exactly one line. No folder paths, no technical details unless the user asks.

**Procedure**:
- **Internal**: derive folder name from agent-profile (English kebab-case)
- Run `fluxloop init scenario <name>` → inform user that the folder was created (one line)

### Step 3: Scenario Proposal

**Goal**: Surface the user's testing intent and taste — what they actually care about verifying in this agent. The proposals are a menu for the user to react to, not a final answer. A good proposal set makes the user quickly say "this one" or sparks them to articulate something they couldn't express from scratch.

**Principles**:
- Proposals are a discovery tool, not a recommendation. Cover a diverse range of the agent's behavioral surface so the user can locate their intent by reacting to concrete options.
- Every scenario must be a **concrete situation**, not an abstract label. "When a non-existent column is requested" (O) vs. "Error handling" (X).
- Derive scenarios from the agent's actual code — where it branches, where it calls external tools, where it makes judgment calls. Generic testing categories are useless here.
- Scope to **agent behavior only**. Don't drift into user profiles, business context, or system-level concerns — stay at the level of "what does the agent do in this situation."
- `learnings.md` may reveal what the user cared about in previous sessions — use it to refine the range, not to repeat the same scenarios.

**Procedure**:

> Read references/output-examples.md § "Scenario Candidate Presentation"

- Analyze `agent-profile.md` + codebase → propose 3–5 concrete scenarios
- Format: number + 1-line title + blockquote with concrete situation
- Reflect `learnings.md` insights if available
- User selects or enters custom scenario, then specifies a display name

### Step 4: Analysis + Confirmed Items

**Goal**: Map out the unknown territory. The user should see clearly what's already decided and what still needs discussion — so the upcoming exploration (Step 5) feels scoped and predictable, not open-ended.

**Principles**:
- The analysis serves the user, not the framework. Classify internally, but present only what matters to the user: "these are settled, these need your input."
- Confirmed items are not just informational — they're alignment checkpoints. If the user disagrees with something marked "confirmed," catch it now before it becomes a wrong assumption in the contracts.
- Keep the summary minimal. One status line + confirmed items batch. The user should grasp the full picture in under 10 seconds.
- **Never expose internal terms** — classification names, resolution strategies, framework vocabulary stay invisible.

**Procedure**:

> Read references/internal-framework.md (classification — do NOT expose terms to user)
> Read references/output-examples.md § "Minimal Analysis Summary" and "Confirmed Items"

- **Internal**: classify items using the framework (never expose classification names)
- **Output (a)**: minimal summary line — `🔍 Analysis: ✅ N confirmed · ❓ N to discuss · 💡 N discovered`
- **Output (b)**: batch-present confirmed items (1-line title + blockquote) → ask for confirmation
- Create `scenario-planning-{scenario-name}.md` at `.fluxloop/test-memory/`

### Step 5: Exploration Dialogue

**Goal**: Resolve every ambiguous item into a concrete behavioral expectation — whether through user decision or accepted defaults. By the end, no item remains undecided: each one has a specific expectation attached to it.

**Principles**:
- Be Socratic, not transactional. Don't just present options and wait — present implications of each option so the user can make an informed choice. But don't lead toward a specific answer, and limit follow-up questions to one per item.
- **One question at a time.** Bundling multiple items overwhelms the user and produces shallow answers. Depth on each item matters more than speed.
- Respect user fatigue. If the user signals "enough," don't push — set sensible defaults for remaining items and move on. The goal is useful contracts, not exhaustive coverage.
- **Progress tracker every turn.** The user should always know where they are, how much is done, and how much is left. This prevents the "are we done yet?" feeling.

**Procedure**:

> Read references/output-examples.md § "Progress Tracker" and "Variant Presentation"

- **One question at a time** — never bundle multiple items in a single turn
- **Progress tracker every turn**: `📋 Progress (N/M)` with 🔵 done / 💬 current / ⏳ waiting
- For each item: present concrete variants (1-line title + blockquote), ask user to choose
- **Exit**: user signals "enough" → set defaults for remaining items → proceed to Step 6

### Step 6: Decision Integration

**Goal**: Give the user a single, coherent view of everything decided so far. This is the last chance to catch contradictions, gaps, or misaligned assumptions before they become formalized rules.

**Principles**:
- This is a review checkpoint, not a formality. Actively look for decisions that might contradict each other when placed side by side — things that seemed fine in isolation during Step 5 may conflict in the full picture.
- Present decisions so the user can read through naturally and feel "yes, this is what I want" — not decode a structured artifact.
- If the user corrects something, reopen that specific item inline — present variants (Step 5 style), resolve, then return to this step. Don't restart the full exploration.

**Procedure**:

> Read references/output-examples.md § "Decision Integration"

- Consolidate decisions using 1-line title + blockquote (NO tables, NO metadata)
- End with confirmation prompt — corrections reopen specific items

### Step 7: Rule Extraction + Confirmation

**Goal**: Transform human decisions into machine-testable contracts. Every contract must be precise enough that an automated test can unambiguously determine pass or fail — no room for interpretation.

**Principles**:
- Be precise, not verbose. Strip out subjective language ("appropriately", "well", "sufficiently") — if a word requires human judgment to evaluate, the contract is not testable.
- Write from the **agent's behavioral perspective** ("The agent must..."), not system perspective ("The system should...").
- `must_not` contracts are the highest-stakes rules. They should emerge naturally from decisions made in Step 5 (where the user identified dangerous behaviors), not be invented here as an afterthought.
- This is still a confirmation step. If a decision doesn't translate well into a rule, reopen that item inline — present variants (Step 5 style), resolve, then return to this step.

**Procedure**:

> Read references/internal-framework.md § "Expectation Level → Contract Type"
> Read references/output-examples.md § "Contract Final Presentation"

- **Internal**: convert decisions to contracts using expectation level mapping
- **Output**: contracts grouped by 🔴 MUST / ⛔ MUST NOT / 🟡 SHOULD / 🟢 MAY (bullet + blockquote)
- Each contract: title, category emoji, violation conditions
- Update `scenario-planning-{scenario-name}.md` with final contracts

### Step 8: Save (Dual Write)

**Goal**: Persist the confirmed contracts so they're immediately usable for testing. The user should feel "done" after this step — no manual copy-paste or file management needed.

**Principles**:
- Both writes (local + server) must succeed. If one fails, inform the user clearly and offer a retry — don't silently skip.
- Overwrite `test-strategy.md` entirely. This file represents the current truth, not an append log.

**Procedure**:
- Local: save to `.fluxloop/test-memory/test-strategy.md` (use `test-memory-template/test-strategy.md` format)
- Server: `fluxloop scenarios create --name "..." --goal "..."`

### Step 9: Language + API Key + Wrapper

**Goal**: Ensure the testing environment is fully configured so the user can run tests immediately after this skill completes. No loose ends.

**Principles**:
- Don't ask what's already answerable. Check existing config (`.fluxloop/.env`, project defaults) before asking the user anything.
- This is a setup step, not a decision step. Keep it fast and frictionless.

**Procedure**:
- **Language**: project default → allow override
- **API Key**: `.fluxloop/.env` exists → skip; missing → `fluxloop apikeys create`
- **Wrapper**: if needed → read references/wrapper-guide.md

## Interactive Checkpoints

Required user interactions: Step 3 (select scenario) → Step 4 (batch confirm) → Step 5 (per item) → Step 6 (review decisions) → Step 7 (confirm rules). Min 3: scenario selection + exploration + rule confirmation.

## Error Handling

| Error | Response |
|-------|----------|
| No project / no profile | Prerequisite Resolution → inline execution |
| Init in wrong directory | "Run from workspace root. Check `pwd`" |
| `scenarios create` failure | Check network, login, project selection |
| API key missing | `fluxloop apikeys create` or manual `.fluxloop/.env` |
| Wrapper errors | read references/wrapper-guide.md |
| User fatigue | Set defaults for remaining items → proceed to Step 6 |

## Next Steps

Scenario ready → Run tests (test skill)

> CLI reference: read skills/_shared/QUICK_REFERENCE.md

## Cross-Cutting Rules

These apply to every Step. The Workflow section references this explicitly.

1. Scope: **agent behavior level only** — no user profiles or business context
2. **1-line title + blockquote detail** for all bullet items presented to the user
3. **Each Step starts with user-facing explanation** — what it does + what user needs to do
4. `scenario-planning-{name}.md` is intermediate; final contracts go to `test-strategy.md`
