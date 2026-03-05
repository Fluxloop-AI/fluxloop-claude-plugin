**English** | [한국어](README.ko.md)

# FluxLoop Claude Code Plugin

A Claude Code plugin for automated AI agent testing and evaluation.

## 🚀 Installation

### Step 1: Add Marketplace

```
/plugin marketplace add Fluxloop-AI/fluxloop-claude-plugin
```

### Step 2: Install Plugin

```
/plugin install fluxloop@fluxloop
```

That's it! Now just talk to Claude naturally.

---

## ⭐ Skills — Test Your Agent with Natural Language

FluxLoop consists of 6 specialized skills. Just speak naturally and the right skill activates automatically.

### 🗣️ Usage (Natural Language)

| Intent | Example | Activated Skill |
|--------|---------|-----------------|
| Initial setup | "set up fluxloop" | setup |
| Scan / update agent | "scan my agent" | context |
| Create scenario | "create a scenario" | scenario |
| Run test | "run the test" | test |
| Evaluate / improve | "evaluate my results" | evaluate |
| Compare prompts | "compare prompts" | prompt-compare |

### Skill Workflow

**First time setup (once per project):**
```
setup → context → scenario → test → evaluate
```

**Daily loop (most of your time here):**
```
test → evaluate → (fix code) → test → evaluate → ...
```

> setup and context are automatically skipped when already complete.
> You can jump straight to "run the test" — FluxLoop detects the current state and handles the rest.

**No commands to memorize. No manual steps. Just ask.**

---

## 📋 Requirements

- **FluxLoop Account**: [alpha.app.fluxloop.ai](https://alpha.app.fluxloop.ai)
- **Python 3.11+**: Required for FluxLoop CLI

> 💡 **The setup skill installs FluxLoop CLI for you!** Just say "set up fluxloop" and everything gets configured automatically.

---

## 🔧 Example Conversation

```
You: "set up fluxloop"
Claude: [setup skill] Installing CLI, authenticating, and configuring the project...
      ✅ Setup complete → Say "scan my agent" to proceed.

You: "scan my agent"
Claude: [context skill] Scanning codebase and generating agent profile...
      ✅ Profile saved → Say "create a scenario" to proceed.

You: "run the test"
Claude: [test skill] Checking scenario and data, then running tests...
      ✅ Test completed! 47/50 passed (94%)
      → Say "evaluate my results" to analyze.
```

---

## 🧪 Evaluation

FluxLoop provides server-side evaluation powered by AI insights.

Simply say **"evaluate my results"** — the **evaluate** skill handles everything automatically.

For direct CLI usage, see the [documentation](https://docs.fluxloop.ai).

---

## 🪝 Hooks (Optional)

Auto-run smoke tests after file edits (only when FluxLoop is set up):

```json
{
  "hooks": [
    {
      "type": "PostToolUse",
      "matcher": "Write|Edit",
      "command": "if [ -f .fluxloop/context.json ] && command -v fluxloop >/dev/null 2>&1; then fluxloop test --smoke --quiet; fi"
    }
  ]
}
```

> The hook only runs when FluxLoop CLI is installed and the project is initialized.

---

## 📁 Project Structure

```
your-project/
├── .fluxloop/
│   ├── project.json          # Project connection info
│   ├── context.json          # Current scenario pointer
│   ├── .env                  # API key
│   ├── scenarios/
│   │   └── my-test/
│   │       ├── agents/       # Agent wrappers
│   │       ├── configs/      # Configuration files
│   │       ├── .state/
│   │       │   └── contracts/  # Scenario contracts (YAML)
│   │       ├── inputs/       # Test inputs
│   │       ├── experiments/  # Test results
│   │       ├── scenario-planning.md  # Scenario design working doc
│   │       └── test-strategy.md      # Test objectives & contracts
│   └── test-memory/          # Shared context across skills (auto-generated)
│       ├── agent-profile.md  # Agent profile & metadata
│       ├── prompt-versions.md # Prompt version history
│       ├── results-log.md    # Test results log
│       └── learnings.md      # Insights & improvements
```

> Default config files are `configs/scenario.yaml`, `configs/input.yaml`, and `configs/simulation.yaml`.
> `setting.yaml` and `fluxloop.yaml` remain supported for legacy compatibility.

## 🔗 Links

- **FluxLoop Web**: <a href="https://alpha.app.fluxloop.ai" target="_blank">alpha.app.fluxloop.ai</a>
- **Documentation**: <a href="https://docs.fluxloop.ai" target="_blank">docs.fluxloop.ai</a>

## 📄 License

MIT License
