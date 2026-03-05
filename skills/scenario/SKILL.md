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

## Lazy-Read Rule

> **CRITICAL**: Do NOT pre-read all reference files at skill load time.
> - `skills/_shared/` files: read once at the START of Step 1 (sequentially, not in parallel).
> - `references/` files: read ONLY when you reach the Step that references them.
> - Never batch-read all files into a single Explore agent call.

## Output Format

📎 `skills/_shared/OUTPUT_FORMAT.md` — read at Step 1 start

## Context Protocol

1. `fluxloop context show` → confirm project + scenario state
2. Load `agent-profile.md` (stale detection) + `learnings.md` (if exists) from `.fluxloop/test-memory/`
3. Dual Write: server (`fluxloop scenarios create/refine`) + local (`test-strategy.md`)

📎 Stale detection: `skills/_shared/CONTEXT_PROTOCOL.md` | Collection: `skills/_shared/CONTEXT_COLLECTION.md` — read at Step 1 start

## Prerequisite

- Project + agent-profile.md exists → proceed
- Missing → follow `skills/_shared/PREREQUISITE_RESOLUTION.md` (read at Step 1 start) → inline setup/context → return to Step 1

## Workflow

> Execute each Step sequentially. Do not batch Bash/Read calls in parallel.
> Every Step must also follow the Cross-Cutting Rules at the bottom of this document.

### Step 1: Context Load + Stale Detection

**Goal**: Start from an accurate, current understanding of the target agent. If the profile is stale, downstream scenarios may be built on wrong assumptions — making the entire session's output unreliable.

**Principles**:
- This is a grounding step — be efficient. Don't turn it into a lengthy conversation.
- **Opening tone**: The first thing the user sees should feel like a natural start to a collaborative session, NOT a system boot-up log. Lead with purpose (e.g. "Let's design test scenarios for how your agent should behave in specific situations.") — context loading happens in the background, and the user only sees results (status block) not the process.
- Staleness is not just a version mismatch. When flagging it, briefly explain what *kind* of changes might invalidate previous analysis (e.g., new tools added, prompt rewritten, schema changed).
- Learnings from previous sessions (`learnings.md`) are accumulated team knowledge. Always incorporate them — they prevent re-asking questions the user already answered.

**Procedure**:
- **Shared references (one-time load)**: read the following files sequentially using the Read tool. Do this ONCE here — do not re-read in later Steps.
  1. `skills/_shared/OUTPUT_FORMAT.md`
  2. `skills/_shared/CONTEXT_PROTOCOL.md`
  3. `skills/_shared/CONTEXT_COLLECTION.md`
  4. `skills/_shared/PREREQUISITE_RESOLUTION.md`
  5. `skills/_shared/QUICK_REFERENCE.md`
- Read `agent-profile.md`: extract `git_commit`, compare with `git rev-parse --short HEAD`
  - If different → ask if user wants to update the profile
  - If `no-git` → continue without warning
- Read `learnings.md` (if exists): incorporate previous insights

### Step 2: Scenario Initialization (automatic)

**Goal**: Set up the workspace and orient the user — what was created, where they are, and what's coming next. This step transitions from scenario selection into the structured workflow.

**Principles**:
- Minimize cognitive load. The user didn't come here to think about folder names — derive them silently from agent-profile.
- Orient the user: show where they are now and what's coming next, so the workflow feels predictable rather than abrupt.

**Procedure**:
- **Internal**: derive folder name (English kebab-case) and display name from agent-profile + selected scenario
- Run `fluxloop init scenario <name>`
- **Display**: output in this template format. Replace only {placeholders}. Do NOT use tables, do NOT rearrange.

```
🎞️ {scenario-name} scenario has been created.
  > 📂 {folder-path}

Now preparing the elements needed to refine this scenario.

✅ Scenario Topic — just decided above
❌ Scenario Analysis — identify and define the key elements
❌ Test Rules — decide how the agent should behave
```

Note: The inline descriptions are only shown here (Step 2, first exposure). In all subsequent roadmap displays (Step 4/5/6), show labels only without descriptions.

- **Mode selection**: after displaying the template above, use `AskUserQuestion` tool to ask how to proceed. Options: "Interactive (default)" / "Automatic"
  - If Interactive: Step 4 shows analysis with recommendations, user chooses to accept or discuss further
  - If Automatic: agent auto-fills all items based on codebase analysis, then jumps to Step 6 for user review
- **Internal note**: Status icons: ✅ complete / ⏳ in progress / ❌ pending. "Scenario Analysis" covers Step 4 + Step 5 — mark ⏳ at Step 4, mark ✅ when Step 4 completes (if recommendations accepted) or when Step 5 completes (if opted in). "Test Rules" covers Step 6 + Step 7 + Step 8 — mark ⏳ at Step 6, mark ✅ when Step 8 completes.

### Step 3: Scenario Proposal

**Goal**: Surface the user's testing intent and taste — what they actually care about verifying in this agent. The proposals are a menu for the user to react to, not a final answer. A good proposal set makes the user quickly say "this one" or sparks them to articulate something they couldn't express from scratch.

**Principles**:
- **Profile-first, code-later.** Start from agent-profile alone — it already contains enough information (tools, data sources, responsibilities) to generate meaningful scenario candidates. Do NOT read the codebase at this stage.
- Proposals are a discovery tool, not a recommendation. Cover a diverse range of the agent's behavioral surface so the user can locate their intent by reacting to concrete options.
- Every scenario must be a **concrete situation**, not an abstract label. "When a non-existent column is requested" (O) vs. "Error handling" (X).
- Scope to **agent behavior only**. Don't drift into user profiles, business context, or system-level concerns — stay at the level of "what does the agent do in this situation."
- `learnings.md` may reveal what the user cared about in previous sessions — use it to refine the range, not to repeat the same scenarios.

**Procedure**:

- **First**: read `references/output-examples.md` § "Scenario Candidate Presentation" for formatting guidance
- Analyze `agent-profile.md` only (NO codebase reading) → propose 3–5 concrete scenarios
- Format: number + 1-line title + blockquote with concrete situation
- Reflect `learnings.md` insights if available
- **After proposals**: use the `AskUserQuestion` tool with up to 5 proposed scenarios as selectable options (no extra options — use all slots for scenarios)
- **Fallback guidance**: after the AskUserQuestion, add a text note: "If none of these fit, let me know — I can dig deeper into the codebase for more targeted proposals, or you can describe your own scenario."
- **If user requests deeper exploration:** read only the key files/paths identified in agent-profile (not the full codebase), then propose additional or refined scenarios

### Step 4: Scenario Breakdown

**Goal**: Show the user the full analysis of this scenario — what's already confirmed and what needs deciding — with recommended answers for open items. The user should see the complete picture at a glance and be able to accept recommendations quickly or opt into deeper discussion.

**Principles**:
- **Sentence-first, not code-first.** Identify ambiguities from the scenario sentence itself FIRST. Only look at agent-profile or code when resolving a specific ambiguity that requires it — and even then, target only the relevant files/paths, not the full codebase.
- **Show the full analysis, not just labels.** Each topic should tell the user what was found (✔️) or what needs deciding (❓), so they can make informed choices without a separate deep-dive step.
- **Recommend by default.** Every ❓ item gets a recommended answer with reasoning. The fast path (accept all) should be the easiest path.
- **Never expose internal terms** — classification names, resolution strategies, framework vocabulary stay invisible.

**Procedure**:

- **First**: read `references/internal-framework.md` (ambiguity identification + classification — do NOT expose terms to user) and `references/output-examples.md` § "Scenario Breakdown" for formatting guidance

1. **Analyze (internal)**: identify ambiguities in the scenario sentence using the framework — analyze the sentence FIRST without reading any code (never expose classification names). For each topic, identify confirmed facts (✅) and open questions (❓).
2. **Save**: write full analysis (with ✅/❓ details per topic) to `scenario-planning-{scenario-name}.md` at `.fluxloop/test-memory/`. This becomes the working document for Step 5.
3. **Display**: show the analysis results extracted from the saved document, organized by topic. Output in this template format. Do NOT use tables.

```
✅ Scenario Topic
⏳ Scenario Analysis
❌ Test Rules

---

Here's what I found analyzing this scenario:

**{topic name}**
  ✔️ {confirmed fact, 1 line}
  ❓ {what needs to be decided, 1 line}

**{topic name}**
  ✔️ {confirmed fact, 1 line}

**{topic name}**
  ❓ {what needs to be decided, 1 line}
  ❓ {what needs to be decided, 1 line}

💡 Recommend
  · {topic} → {recommended answer} ({reason})
  · {topic} → {recommended answer} ({reason})
  · {topic} → {recommended answer} ({reason})
```

- Group by topic. Each topic has a **bold header**, with ✔️/❓ items listed underneath. A topic may contain only ✔️, only ❓, or both.
- ✔️ items: confirmed facts (auto-filled from agent-profile or code). Show rationale in 1 line.
- ❓ items: open questions the user needs to decide — includes both explicitly stated and implicitly discovered items.
- 💡 Recommend section: covers every ❓ item. Each line shows the recommended answer with a brief reason.
- **Branching**: use `AskUserQuestion` tool with three options:
  - "Accept recommendations (Recommended)" — applies all recommend values, skips Step 5, proceeds to Step 6
  - "Discuss specific items" — user selects which ❓ items to deep-dive in Step 5
  - "Discuss all items" — enters Step 5 for all ❓ items (full exploration)
- **If "Discuss specific items"**: use a follow-up `AskUserQuestion` with `multiSelect: true` listing all ❓ items, so the user picks which ones to discuss.

### Step 5: Exploration Dialogue (opt-in)

**Goal**: Resolve selected ambiguous items into concrete behavioral expectations through deeper discussion. This step is only entered when the user opts in from Step 4 — it is skipped entirely if the user accepts all recommendations.

**Entry condition**: entered only when the user chose "Discuss specific items" or "Discuss all items" in Step 4. If the user accepted recommendations, skip directly to Step 6.

**Scope**:
- If "Discuss specific items": only iterate through the user-selected ❓ items. Non-selected ❓ items retain their Recommend values from Step 4.
- If "Discuss all items": iterate through all ❓ items (original full exploration flow).

**Principles**:
- Be Socratic, not transactional. Don't just present options and wait — present implications of each option so the user can make an informed choice. But don't lead toward a specific answer, and limit follow-up questions to one per item.
- **One question at a time.** Bundling multiple items overwhelms the user and produces shallow answers. Depth on each item matters more than speed.
- Respect user fatigue. If the user signals "enough," don't push — apply Recommend values for remaining items and move on. The goal is useful contracts, not exhaustive coverage.
- **Progress tracker every turn.** The user should always know where they are, how much is done, and how much is left. This prevents the "are we done yet?" feeling.

**Procedure**:

- **First**: read `references/output-examples.md` § "Progress Tracker", "Step 5 Selective Entry", and "Variant Presentation" for formatting guidance
- **One question at a time** — never bundle multiple items in a single turn
- **Roadmap every turn**: show the roadmap with per-item detail under the ⏳ step:
  ```
  ✅ Scenario Topic
  ⏳ Scenario Analysis
     ✓ {topic} (recommend)
     ✓ {topic}
     ▸ {topic} (N/M)
     · {topic}
  ❌ Test Rules
  ```
  Sub-item markers: `✓` done / `✓ (recommend)` pre-filled from accepted recommendation / `▸` current / `·` pending. The `(N/M)` count appears on the `▸` current item.
- For each selected item: present concrete variants (1-line title + blockquote), ask user to choose
- **Exit**: user signals "enough" → apply Recommend values for remaining items → proceed to Step 6
- **Completion**: when Step 5 completes (or is skipped), all ❓ items must have resolved values — either from Recommend acceptance or from user decisions. This resolved state is what Step 6 displays.

### Step 6: Decision Integration

**Goal**: Give the user a single, coherent view of everything decided so far. This is the last chance to catch contradictions, gaps, or misaligned assumptions before they become formalized rules.

**Principles**:
- This is a review checkpoint, not a formality. Actively look for decisions that might contradict each other when placed side by side — things that seemed fine in isolation during Step 5 may conflict in the full picture.
- Present decisions so the user can read through naturally and feel "yes, this is what I want" — not decode a structured artifact.
- If the user corrects something, reopen that specific item inline — present variants (Step 5 style), resolve, then return to this step. Don't restart the full exploration.

**Procedure**:

- **First**: read `references/output-examples.md` § "Decision Integration" for formatting guidance
- **Display**: output in this template format. Do NOT use tables.

```
All items have been defined. Now moving on to test rules.

✅ Scenario Topic
✅ Scenario Analysis
⏳ Test Rules

---

Scenario analysis is complete.
Now let's turn the decisions into test rules.
```
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

- **First**: read `references/internal-framework.md` § "Expectation Level → Contract Type" and `references/output-examples.md` § "Contract Final Presentation" for formatting guidance
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
- Local: save to `.fluxloop/test-memory/test-strategy.md` (format: see `<repo-root>/test-memory-template/test-strategy.md`)
- Server: `fluxloop scenarios create --name "..." --goal "..."`

### Step 9: Language + API Key + Wrapper

**Goal**: Ensure the testing environment is fully configured so the user can run tests immediately after this skill completes. No loose ends.

**Principles**:
- Don't ask what's already answerable. Check existing config (`.fluxloop/.env`, project defaults) before asking the user anything.
- This is a setup step, not a decision step. Keep it fast and frictionless.

**Procedure**:
- **Language**: project default → allow override
- **API Key**: `.fluxloop/.env` exists → skip; missing → `fluxloop apikeys create`
- **Wrapper**: if needed → read `references/wrapper-guide.md` at this point

## Interactive Checkpoints

Required user interactions: Step 3 (select scenario) → Step 4 (analysis review + branch) → Step 5 (per item, if opted in) → Step 6 (review decisions) → Step 7 (confirm rules). Min 3: scenario selection + analysis review + rule confirmation.

## Error Handling

| Error | Response |
|-------|----------|
| No project / no profile | Prerequisite Resolution → inline execution |
| Init in wrong directory | "Run from workspace root. Check `pwd`" |
| `scenarios create` failure | Check network, login, project selection |
| API key missing | `fluxloop apikeys create` or manual `.fluxloop/.env` |
| Wrapper errors | follow `references/wrapper-guide.md` |
| User fatigue | Set defaults for remaining items → proceed to Step 6 |

## Next Steps

Scenario ready → Run tests (test skill)

📎 CLI reference: `skills/_shared/QUICK_REFERENCE.md` (already loaded at Step 1)

## Cross-Cutting Rules

These apply to every Step. The Workflow section references this explicitly.

1. Scope: **agent behavior level only** — no user profiles or business context
2. **1-line title + dash description or blockquote detail** for all bullet items presented to the user
3. **User-friendly framing** — Frame every explanation from the user's perspective (what value they get, what they'll do next), NOT from the system's perspective (what technical operation is running). Never announce internal operations ("Starting skill…", "Checking project state…", "Loading context…"). Instead, speak naturally about the user's goal and what comes next. The user should feel they're starting a collaborative session, not watching a system boot sequence.
4. `scenario-planning-{name}.md` is intermediate; final contracts go to `test-strategy.md`
