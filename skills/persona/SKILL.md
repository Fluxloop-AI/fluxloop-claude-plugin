---
name: fluxloop-persona
description: |
  Create project-level persona pool from agent-profile.
  Flow: context load → existing check → size recommendation → strategy → casting query → server matching → review → save.
  Frequency: once per project, then when agent capabilities change significantly.
  Keywords: persona, user type, casting, persona pool, user profile
---

# FluxLoop Persona Skill

**Flow**: Profile check → Existing check → Size recommendation → Strategy → Casting query → Server matching → Review → Save

## Lazy-Read Rule

> **CRITICAL**: Do NOT pre-read all reference files at skill load time.
> - `skills/_shared/` files: read once at the START of Step 1 (sequentially, not in parallel).
> - Never batch-read all files into a single Explore agent call.

## Output Format

📎 `skills/_shared/OUTPUT_FORMAT.md` — read at Step 1 start

## Context Protocol

1. `fluxloop context show` → confirm project + state
2. Load `agent-profile.md` (stale detection) + `learnings.md` (if exists) from `.fluxloop/test-memory/`
3. Local only: save to `.fluxloop/test-memory/persona-pool.md` (no server sync in this version)

📎 Stale detection: `skills/_shared/CONTEXT_PROTOCOL.md` | Collection: `skills/_shared/CONTEXT_COLLECTION.md` — read at Step 1 start

## Prerequisite

- Project + agent-profile.md exists → proceed
- Missing → follow `skills/_shared/PREREQUISITE_RESOLUTION.md` (read at Step 1 start) → inline setup/context → return to Step 1

## User-Facing Roadmap

Internal steps are grouped into user-facing phases. **Never expose step numbers** (Step 1, Step 3, etc.) to the user.

| User-Facing Phase | Internal Steps | Auto/Interactive |
|---|---|---|
| Agent Review | Step 1 + Step 2 | Auto |
| Team Size | Step 3 | Interactive |
| Role Design | Step 4 + Step 5 | Interactive |
| Casting | Step 6 | Auto |
| Final Review | Step 7 + Step 8 | Interactive |

### Roadmap Display

Show the roadmap at the **start of every user-visible phase** (Team Size, Role Design, Casting, Final Review). The Agent Review phase completes silently before the first roadmap appears.

Template (Korean — this is user-facing output, skill is always used in Korean context):

```
✅ Agent Review — profile confirmed
⏳ Team Size — decide how many personas to create
❌ Role Design — define each persona's characteristics
❌ Casting — match server profiles
❌ Final Review — review and save
```

Status icons: ✅ complete / ⏳ in progress / ❌ pending.
Inline descriptions appear only on **first display**. Subsequent displays show labels only.
⏳ itself indicates the current phase — no extra markers like "← current" needed.

## Workflow

> Execute each Step sequentially. Do not batch Bash/Read calls in parallel.
> Every Step must also follow the Cross-Cutting Rules at the bottom of this document.

### Step 1: Context Load + Stale Detection

**Goal**: Start from an accurate, current understanding of the target agent.

**Principles**:
- This is a grounding step — be efficient. Don't turn it into a lengthy conversation.
- **Opening tone**: "Let's create user personas for your agent." — context loading happens in the background, and the user only sees results (status block) not the process.
- **First-encounter explanation** (only if persona-pool.md does NOT exist yet): after the status block, explain what a persona is in 2-3 sentences. Cover these points in natural language:
  1. A persona is a fictional user who would realistically use the agent (give a concrete example, e.g. "a marketer who is great with Excel but has never touched SQL").
  2. Creating multiple personas with different backgrounds lets you test how the agent handles diverse situations.
- Learnings from previous sessions (`learnings.md`) are accumulated team knowledge. Always incorporate them.

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
- Output status block (OUTPUT_FORMAT pattern)

### Step 2: Existing Asset Check

**Goal**: If personas already exist, offer to reuse/extend. If not, start fresh.

**Procedure**:
- Check `.fluxloop/test-memory/persona-pool.md` existence
- **If exists**:
  - Show existing summary (how many personas, key characteristics)
  - Use `AskUserQuestion` with options: "Add to existing personas" / "Modify specific personas" / "Start from scratch"
- **If missing**: proceed to Step 3 (first-encounter explanation was already shown in Step 1)

### Step 3: Size Recommendation

**Goal**: Recommend how many personas to create, based on agent-profile analysis.

**Principles**:
- Ground the recommendation in concrete analysis, not arbitrary numbers.
- Keep it concise — 1-2 sentences of reasoning + a number.

**Procedure**:
- **Display roadmap** (first appearance — with inline descriptions)
- Analyze `agent-profile.md` for:
  - Tool count and variety
  - Feature breadth (simple query → complex pipeline)
  - Branching complexity (HITL gates, approval flows, etc.)
  - Data source count
- Output: 1-2 sentence rationale + recommended count (e.g. "4-5 personas")
- Use `AskUserQuestion` to confirm the count or let the user specify a different number

### Step 4: Generation Strategy

**Goal**: Present shared conditions + control variables in natural language, recommend diverse vs. similar composition.

**Principles**:
- Present everything in natural language. Never expose 6-trait terminology to the user.
- Recommend a direction (diverse vs. similar) with reasoning, but always present the alternative.
- Difficulty is internally derived from other variable combinations — never expose it.

**Classification criteria** — use these to decide what goes where:
- **Shared**: attributes that must be identical across all personas to keep the test controlled. If varying this attribute would change _what_ the agent does (not _how_ it responds), it belongs here.
- **Variable**: attributes that should differ across personas to test the agent's adaptability. If varying this attribute changes _how_ the user interacts with the agent, it belongs here.
- **Random**: attributes that don't meaningfully affect test outcomes. Assign randomly for natural diversity.

The specific items in each category are **derived from the agent-profile** — they are NOT fixed. Different agents will have entirely different shared conditions and variables.

**Procedure**:
- **Display roadmap** (labels only — inline descriptions already shown in Step 3)
- Analyze `agent-profile.md` → classify attributes into Shared / Variable / Random using the criteria above
- Determine recommended direction (diverse/similar) with rationale
- Output format — each item includes a 1-line value + blockquote explaining why it was classified this way:

  ```
  🔒 Shared Conditions

  - {attribute 1}: {value}
    > {Why this is shared — how it controls the test}

  - {attribute 2}: {value}
    > {Why this is shared}

  🎛️ Variables per Persona

  - {attribute 3}: {range or options}
    > {Why this varies — what aspect of agent adaptability it tests}

  - {attribute 4}: {range or options}
    > {Why this varies}

  🎲 Random
  - {attribute} — or "None"
  ```

- Present alternative: "If you prefer a similar composition: ..."
- **Internal mapping (NOT exposed to user)**: map natural language expressions to 6 traits

  | User Expression | 6 Traits Mapping |
  |---|---|
  | Data/tech proficiency | Tech Savvy (low/mid/high) |
  | Personality type | Archetype (cautious_user, trust_seeker, power_user...) |
  | Failure behavior | Signal (confusion_loop, abandonment_risk, compliance_friction...) |
  | Patience | Patience (low/mid/high) |
  | Vertical/domain (shared) | Vertical |
  | (internal allocation) | Difficulty (Easy/Medium/Hard) — auto-determined from other variable combinations |

- Use `AskUserQuestion` to confirm or modify the strategy

### Step 5: Casting Query Generation

**Goal**: Convert the confirmed strategy into casting queries.

**Principles**:
- Each persona gets a 1-2 sentence situation description + parameter tags.
- The situation description is the core differentiator between personas — control variable combinations must be woven into concrete scenarios.

**Procedure**:
- For each persona, generate:
  - 1-2 sentence natural language situation description (matching personality, behavior_patterns, pain_points)
  - Parameter tags: `type difficulty tech_familiarity patience vertical [capability] [signal_family]`
- **Required**: situation description + vertical
- **Optional**: difficulty, patience, tech_familiarity, capability, signal_family, type
- Generate control variable distribution table (for internal verification, optionally shown to user)
- Display each persona:

  ```
  **1.**
  {situation description}
  `{parameter tags}`

  **2.**
  {situation description}
  `{parameter tags}`
  ...
  ```

- Use `AskUserQuestion` to confirm or request modifications

### Step 6: Casting Query Execution (Server Matching)

**Goal**: Execute casting queries against the server DB to find matching persona presets.

**Procedure (pre)**:
- **Display roadmap** (labels only)

**Pre-flight check** (once, before any query execution):
1. Check `.env` exists (plugin root) → if missing: "Server matching requires a `.env` file. Set these 3 keys: SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, OPENAI_API_KEY"
2. Run `python -c "import httpx"` → if fails: "Install httpx: `pip install httpx`"
3. If both fail → skip Step 6 entirely, inform user, proceed to Step 7 (review without matching results)

**Execution**:
- Use `scripts/test_persona_casting.py` script (included in the plugin repo)
- Command: `python scripts/test_persona_casting.py --json "{query}"`
- Environment: auto-loads from root `.env` (script falls back to `parent.parent/.env`)
- Default scope: `admin` (admin presets only)
- Path resolution: relative to plugin root — reference the script within the plugin directory even when running from a different project

**For each casting query**: run individually → parse JSON result

**Display results**:
  ```
  ▶ Persona 1: {1-line summary}
    Query: "{full casting query}"

    Match results (top 3):
    • #1 {name} ({type}) — score: {vector_score:.4f}
      > {searchable_description first 120 chars}
    • #2 {name} ({type}) — score: {vector_score:.4f}
      > {searchable_description first 120 chars}
    • #3 ...
  ```

**Match quality assessment**:
- If top score is too low (< 0.7) → suggest query rewrite
- If top results don't match intent → suggest tag adjustments

**Error handling**:
- API error → display error message, skip that query, continue with next
- Total failure → skip Step 6, proceed to review without matching results

### Step 7: Persona Review

**Goal**: Synthesize casting queries + server matching results for user review/modification.

**Principles**:
- Summary first, details on demand. Don't overwhelm with all details at once.
- Allow granular modifications (individual persona replace/edit/add/delete).

**Procedure**:
- **Display roadmap** (labels only)
1. List all personas as 1-line summary (Persona N + key characteristic + top match name/score)
2. Use `AskUserQuestion`: "Select a persona to see details (or 'all')"
3. Show selected persona details: situation description + casting query tags + matching results
4. Handle modification requests:
   - Replace/edit a specific persona → re-run Step 6 for that persona to verify matching
   - Add new persona → generate query, run matching
   - Delete a persona → confirm and remove
5. When all confirmed → proceed to Step 8

### Step 8: Save

**Goal**: Save the confirmed persona pool locally.

**Procedure**:
- Save to `.fluxloop/test-memory/persona-pool.md`
- Format:

  ```markdown
  <!-- generated_date: {ISO8601} | git_commit: {hash} | persona_count: {N} -->
  # Persona Pool

  ## Persona 1: {1-line summary}
  > {1-2 sentence natural language situation description}

  `{casting query tags}`

  **Server match**: {top 1 name} (score: {score}) | {top 2 name} (score: {score})

  ## Persona 2: {1-line summary}
  ...
  ```

- Display confirmation message: "{N} user personas have been saved."
- Show Next Steps block:

  ```
  ⏭️ Next Steps
    • Create test scenarios using these personas (scenario)
    • Re-generate personas after updating the profile (persona)
  ```

## Error Handling

| Error | Response |
|-------|----------|
| No project / no profile | Prerequisite Resolution → inline execution |
| `.env` missing for server matching | Skip Step 6, proceed without matching |
| `httpx` not installed | Skip Step 6, proceed without matching |
| Script execution failure | Display error, skip that query, continue |
| `git rev-parse` failure (not a git repo) | Set `git_commit` to `no-git`; note stale detection unavailable |

## Next Steps

Persona pool ready → Create test scenarios (scenario skill)

📎 CLI reference: `skills/_shared/QUICK_REFERENCE.md` (already loaded at Step 1)

## Cross-Cutting Rules

These apply to every Step. The Workflow section references this explicitly.

1. **Never expose 6-trait terminology to the user.** All trait references (Tech Savvy, Archetype, Signal, Patience, Vertical, Difficulty) stay internal. Present everything in natural, context-appropriate language.
2. **Difficulty is always hidden.** It is auto-determined from other variable combinations — never mention it to the user.
3. All Steps execute sequentially (no parallel execution).
4. Domain terms: explain in 1-2 sentences on first encounter.
5. Use **1-line title + blockquote detail** pattern for all items presented to the user.
6. **User-friendly framing** — never announce internal operations. Speak naturally about the user's goal and what comes next.
7. **Never expose internal step numbers** (Step 1, Step 3, etc.) to the user. Use the roadmap phases instead.
8. **Treat personas as people.** Use people-counters (e.g. Korean "명", not object-counter "개"). Identifiers stay as `Persona 1`, `Persona 2` etc. — never assign fictional names.
