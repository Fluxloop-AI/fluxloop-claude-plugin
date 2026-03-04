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

  4) Enter your own
```

### Bad Example ❌

```
| # | Scenario | What code flow it verifies |
|---|----------|---------------------------|
| 1 | Non-existent column request | Tests error handling in SQL generation path |
| 2 | Multi-table join query | Tests join logic in query builder |
```

Why bad: Uses a table with internal "code flow" column. Scenario titles are abstract, not concrete situations.

---

## 2. Minimal Analysis Summary (Step 4)

### Good Example ✅

```
🔍 Analysis: ✅ 3 confirmed · ❓ 2 to discuss · 💡 1 discovered
```

### Bad Example ❌

```
Phase 1 Item Extraction results:
- clear/explicit: 3 (Resolution: agent-profile auto-fill)
- unclear/explicit: 2 (Resolution: user question)
- unclear/implicit: 1 (Resolution: target exploration)
```

Why bad: Exposes internal classification axis names, resolution strategies, and phase numbering.

---

## 3. Confirmed Items Batch Presentation (Step 4)

### Good Example ✅

```
✅ Let's start with the confirmed items:

  • Target tables are orders, customers, products
    > From the agent-profile, the agent accesses these 3 tables.
    > The scenario will operate within this scope.

  • The agent generates SQL to query data
    > When receiving a user question, it creates a SQL query,
    > executes it, and summarizes the results in natural language.

  Does this look right?
```

### Bad Example ❌

```
## Clear/Explicit Items (auto-filled from agent-profile)

| Item | Classification | Definition | Resolution Strategy |
|------|---------------|------------|-------------------|
| Target tables | clear/explicit | orders, customers, products | agent-profile auto-fill |
| Query method | clear/explicit | SQL generation | agent-profile auto-fill |

Please confirm these items.
```

Why bad: Exposes Classification, Resolution Strategy columns. Uses table format with internal metadata.

---

## 4. Progress Tracker (Step 5)

### Good Example ✅

```
📋 Progress (3/5)
  🔵 Meaning of 'non-existent column'
  🔵 Scope of 'appropriate rejection'
  💬 Handling mixed requests  ← current
  ⏳ Typo / similar column response
  ⏳ Error message detail level
```

Emoji rules:
- 🔵 Completed (use 🔵 here, since ✅ is used for "confirmed items" in Step 4)
- 💬 Currently discussing
- ⏳ Waiting

The tracker MUST appear at the start of every turn during Step 5.

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
