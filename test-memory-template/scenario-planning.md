# Scenario Planning

<!-- scenario_name: {scenario_name} | created: {date} | status: in-progress -->

## Extracted Items

### Item: {item_name}

- **Classification**: clear/explicit | unclear/explicit | unclear/implicit
- **Discrimination Criteria**: {why this item falls into this classification}
- **Resolution Strategy**: agent-profile auto-fill | user question | target exploration
- **Status**: pending | resolved | skipped
- **Definition**: {precise behavioral definition once resolved}
- **Variants**: {list of concrete cases/variations}
- **Policy**: {upper-level policy decisions related to this item}

<!-- Repeat "### Item: {item_name}" block for each extracted item -->

## Intermediate Results

### Full Variant Map

| Variant Type | Example | Related Items |
|-------------|---------|---------------|
| {type} | {concrete example} | {item names} |

### Cross-Cutting Policy Summary

| Policy | Decision | Related Items |
|--------|----------|---------------|
| {policy description} | {resolved decision} | {item names} |

### Risk Behavior List

- {risk behavior description} → related item: {item_name}

## Contracts

<!-- Final contracts are recorded here after Phase 4 confirmation. -->
<!-- These contracts will be transferred to test-strategy.md in Step 5. -->

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
