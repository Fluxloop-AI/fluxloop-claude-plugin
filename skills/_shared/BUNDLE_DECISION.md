# Bundle Selection Decision Tree

Check existing data first, then offer choices to the user.

## Decision Flow

```
fluxloop bundles list --scenario-id <id> --format json
  │
  ├─ Multiple bundles → show list, "Which bundle would you like to use?"
  │   └─ Selected → sync pull (2 commands)
  │
  ├─ One bundle → "Use existing / Create new?"
  │   ├─ Use existing → sync pull (2 commands)
  │   └─ Create new → proceed to inputs check
  │
  └─ No bundle → fluxloop inputs list --scenario-id <id> --format json
      │
      ├─ Multiple input sets → show list, "Which input set would you like to use?"
      │   └─ Selected → bundle publish (3 commands)
      │
      ├─ One input set → "Use existing / Create new?"
      │   ├─ Use existing → bundle publish (3 commands)
      │   └─ Create new → full generation (5 commands)
      │
      └─ No input set → full generation (must display results after each step)
          1. fluxloop personas suggest --scenario-id <id>
             → ✅ Personas → N generated + name list
          2. fluxloop inputs synthesize --scenario-id <id> --total-count N
             → ✅ Input Set → {id} (N inputs) 🔗 URL + content summary
             → On 409 (`DATA_CONTEXT_NOT_READY`/`DATA_SUMMARY_MISSING`/`DATA_SUMMARY_STALE`), follow the CLI guidance message and retry the same command
          3. fluxloop bundles publish --scenario-id <id> --input-set-id <id>
             → ✅ Bundle → v1 ({id}) 🔗 URL
```

## ID Extraction

Always use `--format json` when running list commands to extract IDs. Table output may truncate UUIDs depending on terminal width, so parse the full ID safely from JSON output.

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
bundles list --format json → exists → select
             → none → inputs list --format json → exists → select and publish
                                  → none → small-scale generation (must display results after each step):
                                    1. fluxloop personas suggest --scenario-id <id>
                                       → ✅ Personas → N generated + name list
                                    2. fluxloop inputs synthesize --scenario-id <id> --total-count 2
                                       → ✅ Input Set → {id} (N inputs) 🔗 URL + content summary
                                       → On 409 (`DATA_CONTEXT_NOT_READY`/`DATA_SUMMARY_MISSING`/`DATA_SUMMARY_STALE`), follow the CLI guidance message and retry the same command
                                    3. fluxloop bundles publish --scenario-id <id> --input-set-id <id>
                                       → ✅ Bundle → v1 ({id}) 🔗 URL
```
