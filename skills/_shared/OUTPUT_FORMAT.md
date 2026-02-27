# Output Format Guide

All skills must follow this formatting guide when presenting information to the user.
The goal: users should instantly see **where they are**, **what to do**, and **what happened**.

## Core Principles

1. **Section separation** — use dividers between major sections
2. **Icon prefixes** — each information type has a designated icon
3. **Indentation** — commands and details are indented under their parent section
4. **Minimal prose** — bullet points over paragraphs; one line per fact

## Section Dividers

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ← thick: skill title only
────────────────────────────────────  ← thin: between sections
```

- Thick divider (`━`): appears above AND below the skill title (top of output only)
- Thin divider (`─`): separates every major section from the next

## Icon Reference

| Icon | Usage | Example |
|------|-------|---------|
| 🚀 | Skill title | `🚀 FluxLoop 시작 가이드` |
| 📋 | Status / current state | `📋 현재 상태` |
| ▶ | Action step (user must do something) | `▶ Step 1: CLI 설치` |
| 👉 | Command to run | `👉 uv pip install fluxloop-cli` |
| ✅ | Completed / success | `✅ Login → user@example.com` |
| ❌ | Missing / failed | `❌ FluxLoop CLI: 미설치` |
| ⏭️ | Next steps | `⏭️ 다음 단계` |
| 💡 | Tip or note | `💡 workspace root에서 실행하세요` |
| ⚠️ | Warning | `⚠️ --pull 옵션은 사용하지 마세요` |
| 🔗 | Link | `🔗 https://alpha.app.fluxloop.ai/...` |
| 📊 | Results / data | `📊 테스트 결과` |
| 🔄 | In progress / loading | `🔄 평가 진행 중...` |

## Output Templates

### 1. Skill Header

Every skill output starts with:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚀 {Skill Title}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 2. Status Block

Show current state immediately after the header:

```
📋 현재 상태
  • 프로젝트: {name} ({details})
  • FluxLoop CLI: ✅ 설치됨 (v1.2.3) | ❌ 미설치
  • 인증: ✅ 로그인됨 (user@email.com) | ❌ 미인증
  • 시나리오: ✅ {name} | ❌ 없음
```

- Use `✅` / `❌` inline for boolean states
- Indent details with `  • ` (2-space + bullet)

### 3. Action Steps

Each step the user needs to act on:

```
────────────────────────────────────

▶ Step {N}: {Step Title}

  {One-line explanation if needed}

  👉 {command to run}
```

- One thin divider before each step
- `👉` marks the exact command or action the user must perform
- Keep explanation to 1 line max; omit if the step title is self-explanatory

### 4. Selection Prompt

When the user must choose between options:

```
────────────────────────────────────

▶ Step {N}: {Selection Title}

  1) {Option A} — {brief description}
  2) {Option B} — {brief description}
  3) {Option C} — {brief description}
  4) 직접 입력

  👉 번호를 선택하거나 직접 입력하세요:
```

### 5. Result / Completion

After a CLI action completes:

```
✅ {Action} → {summary} 🔗 {url}
```

This follows the existing POST_ACTIONS.md format — no change needed.

### 6. Next Steps Block

Always end a skill with:

```
────────────────────────────────────

⏭️ 다음 단계
  • "{user command}" → {what it does}
  • "{user command}" → {what it does}
```

### 7. Warning / Tip (inline)

Insert anywhere relevant:

```
  💡 {helpful tip}
  ⚠️ {warning message}
```

## Full Example: Setup Skill

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚀 FluxLoop 시작 가이드
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 현재 상태
  • 프로젝트: pluto-duck (Python 3.13.2, uv 사용 가능)
  • FluxLoop CLI: ❌ 미설치

────────────────────────────────────

▶ Step 1: CLI 설치

  uv가 있으니 이걸로 설치합니다:

  👉 uv pip install fluxloop-cli

────────────────────────────────────

▶ Step 2: 로그인

  설치 후 인증합니다. device code가 출력되면 브라우저에서 입력하세요.

  👉 fluxloop auth login --no-wait && fluxloop auth login --resume

────────────────────────────────────

▶ Step 3: 프로젝트 생성/선택

  로그인 후 프로젝트를 만들거나 기존 프로젝트를 선택합니다.

────────────────────────────────────

⏭️ 다음으로 가능한 작업
  • 코드베이스 스캔 & 에이전트 프로필 생성 (context)
  • 테스트 시나리오 설정 (scenario)
  • 시뮬레이션 실행 (test)
  • 결과 분석 & 개선 (evaluate)
```

## Full Example: Evaluate Skill

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚀 FluxLoop 평가
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 현재 상태
  • 시나리오: Order Accuracy Test
  • 실험: exp_abc (10 runs)
  • 프로필: ✅ 최신 (a1b2c3d)

────────────────────────────────────

🔄 서버 평가 실행 중...

✅ Evaluation → 3 insights 🔗 https://alpha.app.fluxloop.ai/...

────────────────────────────────────

📊 결과 분석

  | Criterion   | Score | Notes          |
  |-------------|-------|----------------|
  | Accuracy    | 8/10  | 주문 항목 정확 |
  | Completeness| 6/10  | 옵션 누락 빈번 |

  💡 주요 발견: 옵션 메뉴 처리에서 일관된 패턴의 오류 감지

────────────────────────────────────

▶ 개선 제안

  `agents/order_bot.py:42` — 옵션 파싱 로직에서 다중 선택 처리 누락

  👉 수정을 적용할까요? (Yes/No)

────────────────────────────────────

⏭️ 다음으로 가능한 작업
  • 수정 후 재테스트 (test)
  • 프롬프트 A/B 비교 (prompt-compare)
```

## Rules

1. **Every skill output** must start with the Skill Header (thick divider + title)
2. **Every section transition** must have a thin divider
3. **Never output plain text without structure** — even a single-step result needs the header + status + result format
4. **Commands the user must run** are always marked with `👉`
5. **POST_ACTIONS.md `✅` format** is unchanged — it integrates naturally into this system
6. **Keep prose minimal** — if it takes more than 2 lines to explain, use a bullet list
7. **Status block** appears right after the header, before any action steps
