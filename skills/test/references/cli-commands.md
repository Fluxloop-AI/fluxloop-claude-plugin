# Test CLI Commands Reference

## API Key File

- Location: `.fluxloop/.env` (shared by all scenarios)
- Created by: `fluxloop apikeys create`
- Manual additions:
  - OpenAI: `OPENAI_API_KEY=sk-xxx`
  - Anthropic: `ANTHROPIC_API_KEY=sk-ant-xxx`

## Test Command Options

| Option | Description |
|--------|-------------|
| `--scenario <name>` | Specify scenario to test |
| `--multi-turn` | Enable multi-turn mode (requires `!` prefix) |
| `--max-turns <N>` | Maximum turns in multi-turn (default: 8) |
| `--supervisor-provider <provider>` | Use `anthropic` for Anthropic supervisor |

## Result Commands

| Command | Description |
|---------|-------------|
| `fluxloop test results --scenario <name>` | Formatted output |
| `fluxloop test results --scenario <name> --raw` | Raw markdown |

## Important Notes

- **Never use `--pull`** — always run `fluxloop sync pull` and `fluxloop test` as separate commands
- **Verify full UUID** — ensure IDs are the complete 36-character format (`xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`)
