# Context Collection Procedure

## Collection Steps

1. **Codebase scan**: README, agent main file, package.json/pyproject.toml, API specs, test files
2. **Generate summary**: Agent name, role, system prompt, tools/API list, key features, dependencies
3. **Interactive mode**: `"Do you have any reference documents? (enter path / skip)"`
4. **Server upload**:
   ```bash
   fluxloop data push README.md
   fluxloop data push docs/api-spec.md --bind  # --bind links to the current scenario
   ```
5. **Local save**: Save the collected results to `.fluxloop/test-memory/agent-profile.md` with metadata

## agent-profile.md Metadata Format

Include metadata as an HTML comment at the top of the file:

```
<!-- scan_date: 2024-01-15T10:30:00Z | git_commit: a1b2c3d -->
```

## Stale Detection Criteria

- If `git_commit` differs from the current `git rev-parse --short HEAD`, the profile is considered stale
- On stale detection: "The profile looks outdated. Would you like to update it?"
  - Yes → run the collection procedure above
  - No → continue with the existing profile
