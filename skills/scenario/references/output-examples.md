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

🟢 Scenario Topic — just decided above
🔴 Scenario Analysis — identify and define the key elements
🔴 Test Rules — decide how the agent should behave
```

Note: Inline descriptions appear only in Step 2 (first exposure). All subsequent roadmap displays show labels only.

After the template above, use `AskUserQuestion` for mode selection with two options: "Interactive (default)" and "Automatic".

Notes:
- Status colors: 🟢 complete / 🟡 in progress / 🔴 pending
- 🟡 itself indicates "current step" — no "← current" or "← starting here" markers needed
- Mode selection uses AskUserQuestion tool, NOT inline text

---

## 1.6. Step Transition: Scenario Analysis (Step 4 start)

Shown at the beginning of Step 4, after mode selection.

### Good Example ✅

```
🟢 Scenario Topic
🟡 Scenario Analysis
🔴 Test Rules

---

Here are the items to define for this scenario:

Define #1. ...
```

---

## 1.7. Step Transition: Test Rules (Step 6 start)

Shown when Step 5 (Exploration) completes and Step 6 (Decision Integration) begins.

### Good Example ✅

```
All items have been defined. Now moving on to test rules.

🟢 Scenario Topic
🟢 Scenario Analysis
🟡 Test Rules

---

Scenario analysis is complete.
Now let's turn the decisions into test rules.
```

---

## 2. Scenario Breakdown (Step 4)

Step 4 presents a compact overview — one line per topic. Detailed exploration happens in Step 5.

### Good Example ✅

```
Here are the items to define for this scenario:

Define #1. "Non-existent table/column": what counts as non-existent — made-up names, typos, or columns from other tables?
Define #2. "How to handle": what the agent should do when it encounters a non-existent reference
💡 Define #3. Mixed requests: how to handle queries that mix existing and non-existing columns
```

Then use `AskUserQuestion` to confirm:
- "Proceed as-is (Recommended)"
- "I need changes"

### Bad Example ❌ (full detail dump)

```
Define #1. "Non-existent table/column"

  ✅ Scope is based on the current data schema
     > From the agent-profile, the agent accesses orders, customers,
     > products. Any table/column name outside this schema counts as
     > "non-existent."

  ❓ What kinds of "non-existent" should we cover?
     > Completely made-up name / typo / column from a different
     > table — how far should we go?
```

Why bad: Front-loads all ✅/❓ details that belong in Step 5. The user gets overwhelmed before exploration even starts.

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

## 4. Progress Tracker (Step 5)

Use the 3-color roadmap with progress count embedded in the 🟡 line. This replaces the previous per-item list format.

### Good Example ✅

```
🟢 Scenario Topic
🟡 Scenario Analysis (3/5) in progress...
🔴 Test Rules
```

Rules:
- The (N/M) count shows current/total items within the current step (starts at 1, not 0)
- "in progress..." suffix on the 🟡 line indicates active work
- No per-item breakdown — the current question is presented below the roadmap naturally
- The roadmap MUST appear at the start of every turn during Step 5

### Bad Example ❌ (per-item list)

```
📋 Progress (3/5)
  🔵 Meaning of 'non-existent column'
  🔵 Scope of 'appropriate rejection'
  💬 Handling mixed requests  ← current
  ⏳ Typo / similar column response
  ⏳ Error message detail level
```

Why bad: Per-item list adds cognitive load every turn. The user already knows what's being discussed from the question itself. The roadmap should show position in the overall workflow, not repeat item details.

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

## 6. Decision Integration (Step 6)

### Good Example ✅

```
📋 Key Decisions

  • Respond differently based on the situation
    > For typos, suggest "Did you mean ~?" For completely
    > non-existent columns, clearly say "doesn't exist" and
    > show the actual column list.

  • Process what's possible, only flag what's not
    > If the user asks "analyze customer_id and revenue,"
    > process customer_id normally and separately note that
    > revenue doesn't exist.

  • Never generate estimated values
    > Fabricating plausible numbers for a non-existent column
    > is the most dangerous case.

  Do these decisions look right?
```

### Bad Example ❌

```
## Phase 3: Integration & Consolidation

### Full Variant Map
| Variant Type | Example | Related Items |
|---|---|---|
| Missing column | revenue not found | Rejection, Grounding |

### Cross-Cutting Policy Summary
| Policy | Decision | Related Items |
|---|---|---|
| Rejection style | Context-dependent | Rejection, UX |
```

Why bad: Shows Phase number, internal section names, uses tables with "Related Items" metadata.

---

## 7. Contract Final Presentation (Step 7)

### Good Example ✅

```
Here are the rules we've derived. Do these look right for testing?

🔴 MUST
  • C1. Explicitly inform about non-existent columns [🎯grounding]
    > If a requested column is not in the schema, the agent
    > must inform that it doesn't exist. Violation: proceeding
    > without informing or ignoring the missing column.

⛔ MUST NOT
  • C2. Never generate analysis with estimated values [🛡️safety]
    > The agent must not fabricate values for columns not in
    > the schema. Violation: generating results based on
    > non-existent data.

🟡 SHOULD
  • C3. Suggest similar columns [👤ux]
    > When a typo or similar name exists, suggest "Did you
    > mean ~?" Violation: rejecting without suggestion when
    > a similar column is obvious.

🟢 MAY
  • C4. Show actual column list [✨quality]
    > When a column doesn't exist, optionally show the
    > table's actual column list. No violation (optional).
```

This is the ONE place where structured grouping by contract type is appropriate.
