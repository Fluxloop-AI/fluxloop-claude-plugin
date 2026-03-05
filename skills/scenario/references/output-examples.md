# Output Examples

> This document provides formatting examples for the scenario skill.
> All user-facing output must follow the "1-line title + blockquote detail" pattern.
> Reference this document when presenting information to the user.

## Common Formatting Rule

Every bullet item follows this pattern:

```
• {1-line title}
  > {Detailed explanation in 1-3 lines. Describes what this means
  > concretely for the user's agent and scenario.}
```

---

## 1. Scenario Candidate Presentation (Step 3)

### Good Example ✅

```
Which situation should we test?

  1) How the agent responds when a non-existent column is requested
     > The user asks "show me average revenue", but the orders
     > table has no revenue column.

  2) Whether the agent can handle queries spanning multiple tables
     > "Show me customer order rankings" — requires joining
     > customers and orders tables for aggregation.

  3) How the agent interprets an ambiguous question
     > "Analyze recent data" — which table, what time range,
     > and what kind of analysis are all unspecified.

  Above are initial proposals based on the agent profile.
```

Then use `AskUserQuestion` with up to 5 proposed scenarios as selectable options (use all slots for scenarios, no extra options).

After the AskUserQuestion, add a text note: "If none of these fit, let me know — I can dig deeper into the codebase for more targeted proposals, or you can describe your own scenario."

### Bad Example ❌

```
| # | Scenario | What code flow it verifies |
|---|----------|---------------------------|
| 1 | Non-existent column request | Tests error handling in SQL generation path |
| 2 | Multi-table join query | Tests join logic in query builder |
```

Why bad: Uses a table with internal "code flow" column. Scenario titles are abstract, not concrete situations.

### Bad Example ❌ (chatbot-style option list)

```
Please select one of the following:

  - Select a scenario above — let me know by number
  - Enter your own scenario — if you already have a situation in mind
  - Request codebase analysis — for more targeted proposals based on actual code
```

Why bad: Mechanical chatbot tone. Turns a natural conversation into a formal menu. Use `AskUserQuestion` tool instead of inline option lists.

---

## 1.5. Scenario Roadmap (Step 2, after init)

### Good Example ✅

```
🎞️ {scenario-name} scenario has been created.
  > 📂 {folder-path}

Now preparing the elements needed to refine this scenario.

✅ Scenario Topic — just decided above
❌ Scenario Analysis — identify and define the key elements
❌ Test Rules — decide how the agent should behave
❌ Detailed Scenarios — create simulation stories covering all rules
❌ Persona Casting — match server personas to each story
```

Note: Inline descriptions appear only in Step 2 (first exposure). All subsequent roadmap displays show labels only.

After the template above, use `AskUserQuestion` for mode selection with two options: "Interactive (default)" and "Automatic".

Notes:
- Status icons: ✅ complete / ⏳ in progress / ❌ pending
- ⏳ itself indicates "current step" — no "← current" or "← starting here" markers needed
- Mode selection uses AskUserQuestion tool, NOT inline text

---

## 1.6. Step Transition: Scenario Analysis (Step 4 start)

Shown at the beginning of Step 4, after mode selection.

### Good Example ✅

```
✅ Scenario Topic
⏳ Scenario Analysis
❌ Test Rules
❌ Detailed Scenarios
❌ Persona Casting

---

Here's what I found analyzing this scenario:

✔️ ...
```

---

## 1.7. Step Transition: Test Rules (Step 6 start)

Shown when Step 5 (Exploration) completes and Step 6 (Rule Extraction) begins.

### Good Example ✅

```
All items have been defined. Here are the test rules.

✅ Scenario Topic
✅ Scenario Analysis
⏳ Test Rules
❌ Detailed Scenarios
❌ Persona Casting

---

Decisions have been converted into test rules.
```

---

## 2. Scenario Breakdown (Step 4)

Step 4 shows the full analysis organized by topic: ✔️ confirmed items with rationale, ❓ open items with what needs deciding, and a 💡 Recommend section with suggested answers. The user can accept recommendations to proceed quickly or opt into deeper discussion.

### Good Example ✅

```
Here's what I found analyzing this scenario:

**Data Access**
  ✔️ the agent reads CSV files via pandas to check available columns

**Column Handling**
  ✔️ a column existence check already exists before analysis
  ❓ Similar Column Suggestion — suggest "did you mean X?" when a similar column name exists?
  ❓ Partial Request — when some columns exist and others don't, reject all or process what's available?

**Response**
  ✔️ the agent returns results/errors in JSON format
  ❓ Rejection Timing — reject immediately on request, or fail after attempting analysis?
  ❓ Error Tone — tone of the rejection message (technical error vs. friendly guidance)

💡 Recommend
  · Rejection Timing → reject immediately (avoid unnecessary computation)
  · Similar Column Suggestion → suggest similar columns (handle user typos)
  · Partial Request → process available + flag missing (flexible response)
  · Error Tone → friendly guidance (fits data analysis context)
```

Then use `AskUserQuestion` with three options:
- "Accept recommendations (Recommended)"
- "Discuss specific items"
- "Discuss all items"

### Bad Example ❌ (labels only, no analysis)

```
Here are the items to define for this scenario:

Define #1. "Non-existent table/column": what counts as non-existent — made-up names, typos, or columns from other tables?
Define #2. "How to handle": what the agent should do when it encounters a non-existent reference
Define #3. Mixed requests: how to handle queries that mix existing and non-existing columns
```

Why bad: Shows only topic labels without analysis results. User can't see what's confirmed vs. what needs deciding, and has no recommended starting point.

### Bad Example ❌ (status-first grouping)

```
🔍 Analysis: ✅ 3 confirmed · ❓ 2 to discuss · 💡 1 discovered

✅ Confirmed:
  • Target tables are orders, customers, products
  • The agent generates SQL to query data

❓ To discuss:
  • Meaning of "non-existent"
  • Scope of "appropriate handling"
```

Why bad: Groups by status, not by topic. User can't see the full picture of each concept.

### Bad Example ❌ (codebase facts)

```
✅ Confirmed:
  • run_sql returns errors in structured format
  • describe_table does not throw on missing tables
  • list_tables returns empty array
```

Why bad: Lists technical facts gathered from the codebase instead of analyzing ambiguities in the scenario sentence.

---

## 3. Step 5 Selective Entry

Step 5 is opt-in. When the user selects "Discuss specific items" in Step 4, only the chosen ❓ items are explored. Non-selected items retain their Recommend values and appear as `✓ (recommend)` in the progress tracker.

### Good Example ✅ (selective entry — 2 of 4 items selected)

```
✅ Scenario Topic
⏳ Scenario Analysis
   ✓ Rejection Timing (recommend)
   ▸ Similar Column Suggestion (1/2)
   · Partial Request
   ✓ Error Tone (recommend)
❌ Test Rules
❌ Detailed Scenarios
❌ Persona Casting
```

The `(recommend)` marker tells the user which items were pre-filled from Step 4's recommendations vs. which were discussed.

### Good Example ✅ (all items selected)

```
✅ Scenario Topic
⏳ Scenario Analysis
   ✓ Rejection Timing
   ▸ Similar Column Suggestion (2/4)
   · Partial Request
   · Error Tone
❌ Test Rules
❌ Detailed Scenarios
❌ Persona Casting
```

When all items are selected, no `(recommend)` markers appear — all items go through full exploration.

### Bad Example ❌ (recommend items shown as pending)

```
✅ Scenario Topic
⏳ Scenario Analysis
   · Rejection Timing
   ▸ Similar Column Suggestion (1/4)
   · Partial Request
   · Error Tone
❌ Test Rules
❌ Detailed Scenarios
❌ Persona Casting
```

Why bad: Non-selected items appear as `·` (pending), making it look like they still need work. Items that already have accepted Recommend values should show `✓ (recommend)`.

---

## 4. Progress Tracker (Step 5)

Show the roadmap with per-item detail nested under the ⏳ step. Sub-item markers use a lighter visual weight than the top-level icons to maintain hierarchy.

### Good Example ✅

```
✅ Scenario Topic
⏳ Scenario Analysis
   ✓ Define #1. Non-existent scope
   ✓ Define #2. Handling method
   ▸ Define #3. Mixed requests (3/5)
   · Define #4. Typo detection
   · Define #5. Error message level
❌ Test Rules
❌ Detailed Scenarios
❌ Persona Casting
```

Rules:
- Sub-item markers: `✓` done / `✓ (recommend)` pre-filled from accepted recommendation / `▸` current / `·` pending — lighter than top-level ✅⏳❌ to show hierarchy
- The `(N/M)` count on `▸` reflects only the items being discussed (not recommend-accepted items). Starts at 1, not 0.
- The roadmap MUST appear at the start of every turn during Step 5

### Bad Example ❌ (heavy emoji per sub-item)

```
✅ Scenario Topic
⏳ Scenario Analysis
   ✅ Define #1. Non-existent scope
   ✅ Define #2. Handling method
   ⏳ Define #3. Mixed requests (3/5)
   ❌ Define #4. Typo detection
   ❌ Define #5. Error message level
❌ Test Rules
❌ Detailed Scenarios
❌ Persona Casting
```

Why bad: Same emoji weight at both levels — no visual hierarchy. Sub-items compete with top-level roadmap for attention.

---

## 5. Variant Presentation (Step 5)

### Good Example ✅

```
❓ Let's define "appropriate rejection."

  Here are some possible cases:

  • Completely non-existent column
    > "Show me average revenue" — the orders table has no
    > revenue column at all. How should the agent communicate
    > this?

  • Typo / similar name
    > "Sort by total" — total doesn't exist, but total_price
    > does. Should it reject outright, or suggest "Did you
    > mean total_price?"

  • Column from a different table
    > "Group orders by category" — category is in the products
    > table, not orders. Should it join automatically or
    > inform the user about the table mismatch?

  Which case matters most to you?
```

### Bad Example ❌

```
## 2-2. Variant Expansion for Item "Rejection Behavior"

| Variant Type | Example | Related Items |
|-------------|---------|---------------|
| Missing column | revenue not in schema | Rejection, Error Handling |
| Typo | total vs total_price | Rejection, Suggestion |
```

Why bad: Shows internal sub-step number (2-2), uses "Variant Expansion" label, table format with "Related Items" metadata.

---

## 6. Rule Extraction (Step 6)

### Good Example ✅

```
Decisions have been converted into test rules.

**Column Handling**
  • Suggest "did you mean ~?" for typos
    → 🟡 C1. Suggest similar columns

  • Clearly say "doesn't exist" for unknown columns
    → 🔴 C2. Explicitly inform about non-existent columns

**Response**
  • Never fabricate values for missing columns
    → ⛔ C3. Never generate analysis with estimated values

  • Process available columns, flag missing ones separately
    → 🟡 C4. Process available + flag missing

Do these rules look right for testing?
```

### Bad Example ❌ (grouped by contract type, not topic)

```
🔴 MUST
  • C1. Explicitly inform about non-existent columns [🎯grounding]
    > ...
⛔ MUST NOT
  • C2. Never generate analysis with estimated values [🛡️safety]
    > ...
```

Why bad: Groups by contract type (MUST/SHOULD) instead of topic. User loses the connection between decisions and rules. Also verbose with blockquote details.

---

## 7. Detailed Scenario Generation (Step 7)

Step 7 creates sub-scenarios that collectively cover all confirmed contracts. Each sub-scenario has a protagonist whose behavior drives the story.

### Good Example ✅

```
Test rules are confirmed. Now creating sub-scenarios for simulation.

✅ Scenario Topic
✅ Scenario Analysis
✅ Test Rules
⏳ Detailed Scenarios
❌ Persona Casting

---

Here are 3 sub-scenarios that cover all 4 rules:

📖 Sub-scenario 1. The Typo-Prone Analyst
  > Protagonist: Junior data analyst — rushing to prepare a report before a meeting
  > Setting: The analyst has a list of column names from memory, some misspelled
  > Flow: Asks for "revnue" and "total_pric" — the agent must detect near-matches and suggest corrections rather than failing silently
  > Covers: C1, C2

📖 Sub-scenario 2. The Multi-Table Explorer
  > Protagonist: Product manager — wants a cross-functional view combining orders and customer data
  > Setting: Requests metrics that span multiple tables without specifying joins
  > Flow: Asks "show me customer order rankings" — agent must handle the implicit join or inform about table boundaries
  > Covers: C3, C4

📖 Sub-scenario 3. The Partial Request
  > Protagonist: Marketing lead — needs a quick snapshot but asks for a mix of valid and invalid columns
  > Setting: Some requested columns exist, others don't
  > Flow: Asks for "revenue, order_date, campaign_id" where campaign_id doesn't exist — agent must process what's available and flag what's missing
  > Covers: C1, C4

Coverage check: ✅ All 4 rules covered by 3 sub-scenarios.
```

Then use `AskUserQuestion` with options: "Proceed (Recommended)" / "I need changes".

---

## 8. Persona Spec Definition (Step 8)

Step 8 converts each protagonist into casting conditions using server preset traits, classified as Required or Preferred.

### Good Example ✅

```
Sub-scenarios are set. Now defining casting conditions for each protagonist.

✅ Scenario Topic
✅ Scenario Analysis
✅ Test Rules
✅ Detailed Scenarios
⏳ Persona Casting
   ▸ Persona spec
   · Casting call

---

🎭 Sub-scenario 1. "Junior data analyst" casting spec

  Required:
    · Tech Savvy: low — typos are core to the story; a proficient user wouldn't make them
    · Signal: confusion_loop — repeated failed attempts drive the test flow

  Preferred:
    · Patience: mid — stays long enough to see correction suggestions
    · Vertical: general-consumer — not domain-specific

🎭 Sub-scenario 2. "Product manager" casting spec

  Required:
    · Archetype: power_user — expects cross-table queries to "just work"
    · Signal: compliance_friction — pushes boundaries of what the agent supports

  Preferred:
    · Tech Savvy: mid — understands data concepts but not SQL syntax
    · Difficulty: Medium — moderate challenge level

🎭 Sub-scenario 3. "Marketing lead" casting spec

  Required:
    · Patience: low — wants quick results, may abandon if too many errors
    · Signal: abandonment_risk — partial failures might cause early exit

  Preferred:
    · Archetype: trust_seeker — needs confidence that partial results are reliable
```

Then use `AskUserQuestion` with options: "Proceed to casting call (Recommended)" / "I need changes".

---

## 9. Casting Call — Server Persona Matching (Step 9)

Step 9 matches server preset personas against the casting specs from Step 8.

### Good Example ✅

```
Casting specs are ready. Now matching from server persona pool.

✅ Scenario Topic
✅ Scenario Analysis
✅ Test Rules
✅ Detailed Scenarios
⏳ Persona Casting
   ✓ Persona spec
   ▸ Casting call

---

🎭 Sub-scenario 1. "Junior data analyst"
  → Match: **Confused Novice** (A beginner who frequently misunderstands terminology)
  ✅ Required: Tech Savvy: low ✓, Signal: confusion_loop ✓
  ℹ️ Preferred: Patience: mid ✓, Vertical: general-consumer ✓

🎭 Sub-scenario 2. "Product manager"
  → Match: **Demanding Executive** (Expects immediate, comprehensive answers)
  ✅ Required: Archetype: power_user ✓, Signal: compliance_friction ✓
  ℹ️ Preferred: Tech Savvy: mid ✓, Difficulty: Medium ✗ (preset is Hard)

🎭 Sub-scenario 3. "Marketing lead"
  → Match: **Impatient Browser** (Low tolerance for delays or repeated errors)
  ✅ Required: Patience: low ✓, Signal: abandonment_risk ✓
  ℹ️ Preferred: Archetype: trust_seeker ✗ (preset is cautious_user)
```

Then use `AskUserQuestion` with options: "Confirm personas (Recommended)" / "Re-suggest (exclude current)" / "I'll adjust specs".
