# Internal Analysis Framework

> **This document is for agent-internal reasoning only.**
> NEVER expose any terminology, classification names, or table structures from this document to the user.
> Use this framework to guide your analysis silently, then present results in user-friendly language.

## Ambiguity Identification

The scenario 1-liner is a single sentence that contains hidden ambiguities. Your job is to find them.

1. Read the scenario sentence and ask: **which parts of this sentence could be interpreted in multiple ways?**
2. For each ambiguous part, list 2–4 concrete interpretations (behavioral options the user must choose between)
3. Also ask: **what does this sentence NOT mention, but logically needs to be decided?** (edge cases, boundary conditions, combined situations)

The items you work with in the rest of this framework come from this step — they are the ambiguities and implicit gaps in the sentence. Identify ambiguities from the sentence FIRST, without looking at the codebase. Code analysis or agent-profile lookup only happens AFTER, when resolving a specific identified ambiguity that requires it.

Example:

> "Whether the agent appropriately rejects requests for non-existent columns"
>
> - "non-existent column" — could mean: completely non-existent name / typo / column from a different table / computable value
> - "appropriately rejects" — could mean: just refuse / show actual column list / suggest similar column / offer alternatives
> - (implicit) what if the request mixes existing and non-existing columns?

## Item Classification

Once ambiguities are identified, classify each into one of three categories:

| Classification | Definition | How to Identify |
|---------------|------------|-----------------|
| **clear/explicit** | Directly translatable from the sentence to agent behavior | The sentence unambiguously specifies what the agent should do — no interpretation needed |
| **unclear/explicit** | Mentioned in the sentence but ambiguous in meaning | The sentence references this behavior but the exact expectation is open to multiple interpretations |
| **unclear/implicit** | Not mentioned, but logically relevant given the scenario's context | Not in the sentence, but any experienced tester would ask about it when thinking through the scenario |

## Resolution Strategy

For each classified item, determine how to resolve it:

| Strategy | When to Use | Action |
|----------|------------|--------|
| **agent-profile auto-fill** | Answer is derivable from agent-profile.md or code analysis | Agent fills in the definition and confirms with user |
| **user question** | Multiple valid interpretations exist | Present 2–4 concrete behavioral options for user to choose |
| **target exploration** | Requires deep code tracing or domain expertise | Flag for deeper investigation during exploration |

## Processing Order

1. clear/explicit items first (batch confirm)
2. unclear/explicit items next (one at a time)
3. unclear/implicit items last (one at a time)

## Expectation Level → Contract Type Mapping

When converting resolved items to contracts, map each to an expectation level:

| Expectation | Meaning | → Contract Type |
|------------|---------|-----------------|
| **worst case** | Behavior that must never happen | `must_not` |
| **fair case** | Minimum acceptable behavior | `must` |
| **good case** | Expected behavior | `should` |
| **best case** | Ideal behavior | `may` |

Note: `must_not` contracts should emerge naturally from the exploration dialogue (variant discovery and policy decisions), NOT from a separate "worst case question."

## Contract Categories

| Category | Emoji | What it covers |
|----------|-------|---------------|
| grounding | 🎯 | Factual accuracy, data fidelity |
| quality | ✨ | Output quality, completeness |
| safety | 🛡️ | Risk prevention, harmful behavior avoidance |
| ux | 👤 | User experience, communication quality |
| compliance | 📋 | Rule adherence, format compliance |

## Contract Writing Rules

- Write every contract from the **agent's behavioral perspective** (e.g., "The agent must..." not "The system should...")
- Include explicit **violation conditions** for each contract
- `must` contracts must be **automated-test-verifiable** — precise enough that a test can unambiguously determine pass/fail
