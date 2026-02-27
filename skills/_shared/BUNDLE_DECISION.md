# Bundle Selection Decision Tree

Check existing data first, then offer choices to the user.

## Decision Flow

```
fluxloop bundles list --scenario-id <id>
  │
  ├─ Multiple bundles → show list, "Which bundle would you like to use?"
  │   └─ Selected → sync pull (2 commands)
  │
  ├─ One bundle → "Use existing / Create new?"
  │   ├─ Use existing → sync pull (2 commands)
  │   └─ Create new → proceed to inputs check
  │
  └─ No bundle → fluxloop inputs list --scenario-id <id>
      │
      ├─ Multiple input sets → show list, "Which input set would you like to use?"
      │   └─ Selected → bundle publish (3 commands)
      │
      ├─ One input set → "Use existing / Create new?"
      │   ├─ Use existing → bundle publish (3 commands)
      │   └─ Create new → full generation (5 commands)
      │
      └─ No input set → full generation
          fluxloop personas suggest --scenario-id <id>
          fluxloop inputs synthesize --scenario-id <id> --total-count N
          fluxloop bundles publish --scenario-id <id> --input-set-id <id>
```

## Display Format for Multiple Resources

When multiple bundles or input sets exist, show identifying information:

```
Agent: Found 3 existing bundles:
       1. v3 (stress-test, 20 inputs, 1 day ago)
       2. v2 (happy-path, 5 inputs, 3 days ago)
       3. v1 (edge-cases, 10 inputs, 7 days ago)

       Which bundle to use? Or create new?
```

Key info to display: **version/name, tag/description, count, created date**

## Simplified Flow for Comparison Tests

prompt-compare only needs a small number of inputs, so it follows a simplified flow:

```
bundles list → exists → select
             → none → inputs list → exists → select and publish
                                  → none → small-scale generation:
                                    fluxloop personas suggest --scenario-id <id>
                                    fluxloop inputs synthesize --scenario-id <id> --total-count 2
                                    fluxloop bundles publish --scenario-id <id> --input-set-id <id>
```
