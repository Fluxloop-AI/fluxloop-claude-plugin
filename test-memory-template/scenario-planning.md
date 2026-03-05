# Scenario Planning

<!-- scenario_name: {scenario_name} | created: {date} | status: in-progress -->
<!-- filename: scenario-planning.md | location: .fluxloop/scenarios/{scenario-name}/ -->

## Extracted Items

### Item: {item_name}

- **Status**: pending | resolved | skipped
- **Definition**: {precise behavioral definition once resolved}
- **Variants**:
  - {variant description}
- **Decision**: {policy decision related to this item}

<!-- Repeat "### Item: {item_name}" block for each extracted item -->

## Decisions

- **{decision title}**
  > {detailed description of what was decided and why}

## Contracts

<!-- Final contracts are recorded here after rule extraction. -->
<!-- These contracts will be transferred to test-strategy.md in the same scenario folder. -->

### 🔴 MUST

- **C{N}. {title}** [{emoji}{category}]
  > {explanation of the contract and violation conditions}

### ⛔ MUST NOT

- **C{N}. {title}** [{emoji}{category}]
  > {explanation of the contract and violation conditions}

### 🟡 SHOULD

- **C{N}. {title}** [{emoji}{category}]
  > {explanation of the contract and violation conditions}

### 🟢 MAY

- **C{N}. {title}** [{emoji}{category}]
  > {explanation of the contract and violation conditions}

## Stories

### 📖 Story {N}. {title}

- **Protagonist**: {role label} — {motivation}
- **Setting**: {context/situation}
- **Flow**: {step-by-step narrative}
- **Covers**: C1, C3, C4

<!-- Repeat "### 📖 Story {N}. {title}" block for each sub-scenario -->

## Persona Specs

### 🎭 Sub-scenario {N}. "{protagonist label}" casting spec

**Required**:
- {Trait}: {value} — {reason}
- {Trait}: {value} — {reason}

**Preferred**:
- {Trait}: {value} — {reason}

<!-- Repeat "### 🎭 Sub-scenario {N}." block for each sub-scenario -->

## Matched Personas

### Sub-scenario {N} → {preset persona name}

- **Preset ID**: {server persona id}
- **Summary**: {preset summary}
- **Required match**: {trait} ✓, {trait} ✓
- **Preferred match**: {trait} ✓, {trait} ✗

<!-- Repeat "### Sub-scenario {N} →" block for each sub-scenario -->
