# Harness Governance MVP Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a simple, file-based AI development Harness that forces skill references, records evidence, validates generated artifacts, and blocks low-evidence final outputs.

**Architecture:** Extend the existing Codex hook package instead of introducing a service, database, or queue. Keep governance data in JSON files under `.codex/`, keep scripts in Python with no third-party runtime dependency, and make every stage verifiable by local PowerShell smoke tests.

**Tech Stack:** Python standard library, Codex hooks, JSON config/state files, PowerShell smoke scripts.

---

## Scope

This plan builds a minimal Harness that constrains AI coding behavior through observable evidence. It does not attempt to inspect the model's hidden internal state.

In scope:

- Skill registry validation.
- Skill read receipt generation.
- Phase-aware governance checks.
- Requirement to skill to artifact traceability.
- Document, code, and browser validation evidence schemas.
- Lightweight review quality checks.
- Local smoke tests for pass and fail cases.

Out of scope for MVP:

- Web UI.
- Database storage.
- Remote service.
- Multi-agent orchestration.
- Full AST parsing for every language.
- Browser automation runner implementation.

## Required Skills For Harness Construction

The Harness itself should enforce these skill categories:

- `skill-reference-governance`: governs skill registry, required reads, receipts, and rule-level citations.
- `artifact-review-governance`: governs design review, code review, browser validation, correction records, and verification evidence.
- Domain skills such as `frontend-architecture`, `frontend-vue-guide`, `framework-ui`, `type-definition-standard`, and `module-development-standard`: these are consumed by projects and validated by the Harness.

For this repository, the two governance skills must be created as real `skills/*/SKILL.md` files because the Harness will be tested in realistic skill-loading scenarios.

## File Structure

Create or modify these files:

- Modify `.codex/skill-gate.config.json`
  - Add `artifactSchemas`, `phaseGates`, `reviewQuality`, and `receipt` sections.
- Modify `.codex/hooks/skill_gate.py`
  - Add receipt generation, phase gate checks, traceability checks, and review quality checks.
- Create `.codex/harness/schema/skill-receipt.schema.json`
  - Documents required receipt fields.
- Create `.codex/harness/schema/traceability.schema.json`
  - Documents requirement to skill to artifact mapping fields.
- Create `.codex/harness/schema/review-issue.schema.json`
  - Documents issue-level review fields.
- Create `.codex/harness/schema/browser-validation.schema.json`
  - Documents browser validation evidence fields.
- Create `.codex/harness/examples/pass/final-answer.md`
  - Example final response that satisfies evidence requirements.
- Create `.codex/harness/examples/fail/final-answer-missing-evidence.md`
  - Example final response that should fail.
- Create `.codex/harness/examples/pass/traceability.json`
  - Example traceability map.
- Create `.codex/harness/examples/fail/traceability-missing-rule.json`
  - Example traceability map that should fail.
- Create `scripts/test-harness-governance.ps1`
  - Runs deterministic local pass and fail checks.
- Modify `README.md`
  - Explain the new Harness workflow and commands.

## Confirmed Product Decisions

These decisions are confirmed by the user and must be followed during implementation:

1. Governance skills are real skill files, not config-only concepts.
2. Missing required artifacts must block directly.
3. Browser validation is an explicit phase. Before entering it, the assistant must tell the user that the workflow is entering browser validation and wait for user confirmation.

---

### Task 1: Extend Harness Config With Phase Gates

**Files:**

- Modify: `.codex/skill-gate.config.json`

- [ ] **Step 1: Add phase gate config**

Add these top-level sections while preserving existing `rules` and `skills`:

```json
{
  "receipt": {
    "enabled": true,
    "requiredFields": [
      "skillId",
      "version",
      "loadedFiles",
      "evidenceSource",
      "phase",
      "loadedAt"
    ]
  },
  "phaseGates": {
    "initial-design": {
      "requiredArtifacts": [
        ".codex/harness/artifacts/requirement-atoms.json",
        ".codex/harness/artifacts/skill-matrix.json",
        ".codex/harness/artifacts/skill-receipts.json"
      ],
      "requiredFinalPhrases": [
        "需求原子",
        "技能矩阵",
        "技能使用证据"
      ]
    },
    "document-review": {
      "requiredArtifacts": [
        ".codex/harness/artifacts/doc-review.json"
      ],
      "requiredFinalPhrases": [
        "需求一致性",
        "技能规则",
        "纠偏"
      ]
    },
    "development": {
      "requiredArtifacts": [
        ".codex/harness/artifacts/implementation-context-pack.json",
        ".codex/harness/artifacts/implementation-evidence.json"
      ],
      "requiredFinalPhrases": [
        "组件职责",
        "类型定义",
        "验证"
      ]
    },
    "code-review": {
      "requiredArtifacts": [
        ".codex/harness/artifacts/code-review.json"
      ],
      "requiredFinalPhrases": [
        "需求符合性",
        "设计符合性",
        "最佳实践"
      ]
    },
    "browser-validation": {
      "requiredArtifacts": [
        ".codex/harness/artifacts/browser-validation.json"
      ],
      "requiredFinalPhrases": [
        "用户确认进入浏览器验证",
        "截图",
        "console",
        "network"
      ]
    }
  },
  "phaseTransitions": {
    "browser-validation": {
      "requiresUserConfirmation": true,
      "confirmationPhrase": "用户确认进入浏览器验证"
    }
  },
  "reviewQuality": {
    "requiredIssueFields": [
      "id",
      "severity",
      "evidence",
      "location",
      "correction",
      "verification"
    ],
    "allowedSeverities": [
      "BLOCKER",
      "MAJOR",
      "MINOR"
    ]
  }
}
```

- [ ] **Step 2: Run JSON parse check**

Run:

```powershell
Get-Content .codex\skill-gate.config.json -Raw -Encoding UTF8 | ConvertFrom-Json | Out-Null
```

Expected: command exits with code 0.

### Task 2: Add Artifact Schemas

**Files:**

- Create: `.codex/harness/schema/skill-receipt.schema.json`
- Create: `.codex/harness/schema/traceability.schema.json`
- Create: `.codex/harness/schema/review-issue.schema.json`
- Create: `.codex/harness/schema/browser-validation.schema.json`

- [ ] **Step 1: Create skill receipt schema**

Create `.codex/harness/schema/skill-receipt.schema.json`:

```json
{
  "required": [
    "skillId",
    "version",
    "phase",
    "loadedFiles",
    "evidenceSource",
    "loadedAt"
  ],
  "properties": {
    "skillId": "registered skill name",
    "version": "skill version or unknown when the skill file has no version",
    "phase": "initial-design, document-review, development, code-review, browser-validation, or unknown",
    "loadedFiles": "array of absolute file paths observed by PostToolUse or transcript evidence",
    "evidenceSource": "tool event, transcript, or final output claim",
    "loadedAt": "UTC timestamp"
  }
}
```

- [ ] **Step 2: Create traceability schema**

Create `.codex/harness/schema/traceability.schema.json`:

```json
{
  "required": [
    "requirementId",
    "skillId",
    "ruleIds",
    "artifact",
    "verification"
  ],
  "properties": {
    "requirementId": "stable requirement atom id such as REQ-001",
    "skillId": "registered skill name",
    "ruleIds": "array of concrete skill rule ids or stable section ids",
    "artifact": "file path, design section, code path, or validation evidence path",
    "verification": "command, review issue id, browser evidence id, or explicit blocked reason"
  }
}
```

- [ ] **Step 3: Create review issue schema**

Create `.codex/harness/schema/review-issue.schema.json`:

```json
{
  "required": [
    "id",
    "severity",
    "evidence",
    "location",
    "correction",
    "verification"
  ],
  "properties": {
    "id": "stable issue id such as DOC-001 or CR-001",
    "severity": "BLOCKER, MAJOR, or MINOR",
    "evidence": "requirement id, skill rule, file path, screenshot, console error, or network record",
    "location": "document section, file path, line number, or browser step",
    "correction": "specific change required",
    "verification": "specific command or manual validation step after correction"
  }
}
```

- [ ] **Step 4: Create browser validation schema**

Create `.codex/harness/schema/browser-validation.schema.json`:

```json
{
  "required": [
    "page",
    "steps",
    "expected",
    "actual",
    "console",
    "network",
    "screenshots",
    "result"
  ],
  "properties": {
    "page": "validated URL or route",
    "steps": "ordered interaction steps",
    "expected": "expected behavior",
    "actual": "observed behavior",
    "console": "console error and warning summary",
    "network": "failed request summary",
    "screenshots": "screenshot paths",
    "result": "PASS, FAIL, or BLOCKED"
  }
}
```

- [ ] **Step 5: Parse all schema files**

Run:

```powershell
Get-ChildItem .codex\harness\schema\*.json | ForEach-Object { Get-Content $_ -Raw -Encoding UTF8 | ConvertFrom-Json | Out-Null }
```

Expected: command exits with code 0.

### Task 3: Generate Skill Receipts From Observed Evidence

**Files:**

- Modify: `.codex/hooks/skill_gate.py`
- Test using: `scripts/test-local.ps1`

- [ ] **Step 1: Add receipt creation helper**

Add a function near existing evidence helpers:

```python
def build_skill_receipts(state: dict[str, Any]) -> list[dict[str, Any]]:
    receipts: list[dict[str, Any]] = []
    evidence = state.get("readEvidence", {})
    if not isinstance(evidence, dict):
        return receipts

    phase = str(state.get("phase", "unknown"))
    for skill_id, files in sorted(evidence.items()):
        if not isinstance(files, dict):
            continue
        loaded_files = [
            file_path
            for file_path, item in sorted(files.items())
            if isinstance(item, dict) and item.get("seen")
        ]
        if not loaded_files:
            continue
        receipts.append({
            "skillId": str(skill_id),
            "version": "unknown",
            "phase": phase,
            "loadedFiles": loaded_files,
            "evidenceSource": "PostToolUse",
            "loadedAt": utc_now(),
        })
    return receipts
```

- [ ] **Step 2: Save receipts when Stop runs**

In `handle_stop`, after read evidence is updated, write receipts into state:

```python
state["skillReceipts"] = build_skill_receipts(state)
```

Then save state with the existing `save_state(...)` call.

- [ ] **Step 3: Run local smoke test**

Run:

```powershell
.\scripts\test-local.ps1
```

Expected: output reaches `Done. Report: .codex\hook-logs\latest-skill-gate-report.json`.

- [ ] **Step 4: Inspect receipt state**

Run:

```powershell
.\scripts\show-report.ps1
```

Expected: latest state contains `skillReceipts` with at least one skill and one loaded file after the local fake read evidence.

### Task 4: Add Traceability Artifact Validation

**Files:**

- Modify: `.codex/hooks/skill_gate.py`
- Create: `.codex/harness/examples/pass/traceability.json`
- Create: `.codex/harness/examples/fail/traceability-missing-rule.json`

- [ ] **Step 1: Create pass traceability example**

Create `.codex/harness/examples/pass/traceability.json`:

```json
[
  {
    "requirementId": "REQ-001",
    "skillId": "frontend-architecture",
    "ruleIds": [
      "HARD-GATE:开发前配置确认"
    ],
    "artifact": "docs/design.md#D-001",
    "verification": "check-traceability passed"
  }
]
```

- [ ] **Step 2: Create fail traceability example**

Create `.codex/harness/examples/fail/traceability-missing-rule.json`:

```json
[
  {
    "requirementId": "REQ-001",
    "skillId": "frontend-architecture",
    "ruleIds": [],
    "artifact": "docs/design.md#D-001",
    "verification": "missing rule id should fail"
  }
]
```

- [ ] **Step 3: Add traceability validation helper**

Add:

```python
def validate_traceability_items(items: Any) -> list[str]:
    problems: list[str] = []
    if not isinstance(items, list):
        return ["traceability artifact must be a JSON array"]

    required = ["requirementId", "skillId", "ruleIds", "artifact", "verification"]
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            problems.append(f"traceability[{index}] must be an object")
            continue
        for field in required:
            if not item.get(field):
                problems.append(f"traceability[{index}] missing {field}")
        if not isinstance(item.get("ruleIds"), list) or not item.get("ruleIds"):
            problems.append(f"traceability[{index}] ruleIds must be a non-empty array")
    return problems
```

- [ ] **Step 4: Add artifact file validator helper**

Add:

```python
def validate_json_artifact(path: Path, validator: Callable[[Any], list[str]]) -> list[str]:
    if not path.exists():
        return [f"missing artifact: {path}"]
    data = read_json(path, None)
    if data is None:
        return [f"invalid json artifact: {path}"]
    return validator(data)
```

Also add this import:

```python
from typing import Callable
```

- [ ] **Step 5: Run direct Python validation through the hook script**

Because helpers are internal, run the existing local test after wiring validation into `Stop` in Task 5.

### Task 5: Add Phase Gate Checks Without Overblocking Normal Chat

**Files:**

- Modify: `.codex/hooks/skill_gate.py`

- [ ] **Step 1: Add phase detection helper**

Add:

```python
def detect_phase(prompt: str) -> str:
    text = prompt.lower()
    if any(token in text for token in ["浏览器验证", "browser validation", "runtime validation"]):
        return "browser-validation"
    if any(token in text for token in ["代码评审", "code review", "review code"]):
        return "code-review"
    if any(token in text for token in ["开发阶段", "实现", "implementation", "coding"]):
        return "development"
    if any(token in text for token in ["文档评审", "document review", "评审设计"]):
        return "document-review"
    if any(token in text for token in ["设计阶段", "初始设计", "方案", "架构"]):
        return "initial-design"
    return "unknown"
```

- [ ] **Step 2: Store phase during prompt submit**

In `handle_user_prompt_submit`, after prompt is read:

```python
state["phase"] = detect_phase(prompt)
```

- [ ] **Step 3: Add final phrase check for detected phase**

In `validate_final_output`, after skill phrase checks:

```python
phase = str(state.get("phase", "unknown"))
phase_gates = config.get("phaseGates", {}) if isinstance(config.get("phaseGates", {}), dict) else {}
phase_gate = phase_gates.get(phase, {}) if isinstance(phase_gates.get(phase, {}), dict) else {}
for phrase in phase_gate.get("requiredFinalPhrases", []):
    if phrase and phrase not in final_output:
        problems.append(f"[{phase}] final output missing required phrase: {phrase}")
```

- [ ] **Step 4: Block missing artifacts for detected phases**

In `handle_stop`, check every configured `requiredArtifacts` path when `phase != "unknown"` and the config explicitly sets a phase gate. Missing required artifacts must be blocking problems.

Use this behavior:

```python
phase = str(state.get("phase", "unknown"))
phase_gates = config.get("phaseGates", {}) if isinstance(config.get("phaseGates", {}), dict) else {}
phase_gate = phase_gates.get(phase, {}) if isinstance(phase_gates.get(phase, {}), dict) else {}
if phase != "unknown" and phase_gate:
    for artifact in phase_gate.get("requiredArtifacts", []):
        artifact_path = project_root / str(artifact)
        if not artifact_path.exists():
            final_problems.append(f"[{phase}] missing required artifact: {artifact}")
```

- [ ] **Step 5: Require browser validation confirmation phrase**

In `validate_final_output`, when `phase == "browser-validation"`, require the final output to contain the configured confirmation phrase:

```python
transitions = config.get("phaseTransitions", {}) if isinstance(config.get("phaseTransitions", {}), dict) else {}
browser_transition = transitions.get("browser-validation", {}) if isinstance(transitions.get("browser-validation", {}), dict) else {}
if phase == "browser-validation" and browser_transition.get("requiresUserConfirmation"):
    phrase = str(browser_transition.get("confirmationPhrase", "用户确认进入浏览器验证"))
    if phrase not in final_output:
        problems.append("[browser-validation] missing user confirmation evidence")
```

- [ ] **Step 6: Run existing local smoke**

Run:

```powershell
.\scripts\test-local.ps1
```

Expected: the existing fake final answer still passes because it includes configured skill phrases.

### Task 6: Add Review Quality Checks

**Files:**

- Modify: `.codex/hooks/skill_gate.py`
- Create: `.codex/harness/examples/pass/final-answer.md`
- Create: `.codex/harness/examples/fail/final-answer-missing-evidence.md`

- [ ] **Step 1: Add issue quality helper**

Add:

```python
def validate_review_issues(items: Any, config: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    if not isinstance(items, list):
        return ["review artifact must be a JSON array"]

    review_cfg = config.get("reviewQuality", {}) if isinstance(config.get("reviewQuality", {}), dict) else {}
    required = [str(v) for v in review_cfg.get("requiredIssueFields", [])]
    allowed = {str(v) for v in review_cfg.get("allowedSeverities", [])}

    for index, item in enumerate(items):
        if not isinstance(item, dict):
            problems.append(f"reviewIssues[{index}] must be an object")
            continue
        for field in required:
            if not item.get(field):
                problems.append(f"reviewIssues[{index}] missing {field}")
        severity = str(item.get("severity", ""))
        if allowed and severity not in allowed:
            problems.append(f"reviewIssues[{index}] invalid severity: {severity}")
    return problems
```

- [ ] **Step 2: Create pass final answer example**

Create `.codex/harness/examples/pass/final-answer.md`:

```markdown
## 方案

本轮已覆盖需求原子、技能矩阵、组件职责、类型定义和验证。

## 技能使用证据

- 已读取 frontend-architecture/SKILL.md
- 已按组件职责和类型定义规则生成验证方案
```

- [ ] **Step 3: Create fail final answer example**

Create `.codex/harness/examples/fail/final-answer-missing-evidence.md`:

```markdown
## 方案

我已经参考了相关规范，整体没问题。
```

- [ ] **Step 4: Add final output example checks to PowerShell test**

Implement in `scripts/test-harness-governance.ps1` in Task 8.

### Task 7: Add Governance Skill Files

**Files:**

- Create: `skills/skill-reference-governance/SKILL.md`
- Create: `skills/artifact-review-governance/SKILL.md`

- [ ] **Step 1: Create skill reference governance skill**

Create `skills/skill-reference-governance/SKILL.md`:

```markdown
---
name: skill-reference-governance
description: Use when a task needs to select, read, cite, or verify AI development skills before design, implementation, or review.
---

# Skill Reference Governance

## Rules

- Skills must come from the configured registry or discovered `skills/*/SKILL.md` files.
- A final answer may not claim a skill was used unless observable read evidence exists.
- A valid skill receipt contains skillId, version, phase, loadedFiles, evidenceSource, and loadedAt.
- Design and implementation outputs must cite concrete rule ids or stable section ids.
- Missing required reads are blocking.
```

- [ ] **Step 2: Create artifact review governance skill**

Create `skills/artifact-review-governance/SKILL.md`:

```markdown
---
name: artifact-review-governance
description: Use when reviewing design documents, code, browser validation evidence, or correction records for AI-generated development work.
---

# Artifact Review Governance

## Rules

- Reviews must be issue-level, not generic advice.
- Each issue must include id, severity, evidence, location, correction, and verification.
- Code review must check requirement fit, design fit, skill fit, and best practices.
- Frontend review must check component responsibilities and type definitions when applicable.
- Browser validation must include page, steps, expected, actual, console, network, screenshots, and result.
```

- [ ] **Step 3: Update config for governance skills**

Add config entries after the files exist:

```json
"skill-reference-governance": {
  "requiredReadFiles": [
    "SKILL.md"
  ],
  "outputMustContain": [
    "skillId",
    "ruleId",
    "技能使用证据"
  ],
  "outputMustNotContain": [
    "我大概参考了"
  ],
  "outputMustMatchRegex": []
}
```

Expected: `scripts/test-local.ps1` continues to pass.

### Task 8: Add Local Harness Governance Test Script

**Files:**

- Create: `scripts/test-harness-governance.ps1`

- [ ] **Step 1: Create deterministic test script**

Create `scripts/test-harness-governance.ps1`:

```powershell
$ErrorActionPreference = "Stop"
$OutputEncoding = [System.Text.UTF8Encoding]::new($false)
[Console]::OutputEncoding = $OutputEncoding

$root = Get-Location
$hook = Join-Path $root ".codex\hooks\skill_gate.py"
$config = Join-Path $root ".codex\skill-gate.config.json"

if (-not (Test-Path $hook)) {
  Write-Error "Cannot find hook: $hook"
}
if (-not (Test-Path $config)) {
  Write-Error "Cannot find config: $config"
}

Write-Host "[1/4] Config parses"
Get-Content $config -Raw -Encoding UTF8 | ConvertFrom-Json | Out-Null

Write-Host "[2/4] Schemas parse"
Get-ChildItem .codex\harness\schema\*.json | ForEach-Object {
  Get-Content $_ -Raw -Encoding UTF8 | ConvertFrom-Json | Out-Null
}

Write-Host "[3/4] Existing local hook smoke"
.\scripts\test-local.ps1

Write-Host "[4/4] Report exists"
$report = ".codex\hook-logs\latest-skill-gate-report.json"
if (-not (Test-Path $report)) {
  Write-Error "Expected report not found: $report"
}

Write-Host "PASS: Harness governance smoke checks completed."
```

- [ ] **Step 2: Run the test**

Run:

```powershell
.\scripts\test-harness-governance.ps1
```

Expected: final line is `PASS: Harness governance smoke checks completed.`

### Task 9: Update README With The New Workflow

**Files:**

- Modify: `README.md`

- [ ] **Step 1: Add Harness workflow section**

Add:

```markdown
## Harness Governance MVP

The Harness uses local Codex hooks to enforce observable governance evidence:

1. `UserPromptSubmit` selects required skills and detects the workflow phase.
2. `PostToolUse` records observable skill read evidence.
3. `Stop` validates required reads, final-answer phrases, phase requirements, and evidence sections.

The MVP remains file-based:

- Config: `.codex/skill-gate.config.json`
- Hook: `.codex/hooks/skill_gate.py`
- State: `.codex/hook-state/skill-gate/`
- Logs: `.codex/hook-logs/`
- Schemas: `.codex/harness/schema/`
- Examples: `.codex/harness/examples/`

Run local validation:

```powershell
.\scripts\test-harness-governance.ps1
```

Governance intent:

- Skills must be read before they can be claimed.
- Requirements must map to skill rules and artifacts.
- Reviews must be issue-level and include correction plus verification.
- Frontend work must explicitly cover component responsibilities, type definitions, and validation.
```

- [ ] **Step 2: Verify README renders as plain Markdown**

Run:

```powershell
Get-Content README.md -Raw -Encoding UTF8 | Out-Null
```

Expected: command exits with code 0.

### Task 10: Final Verification

**Files:**

- No new files.

- [ ] **Step 1: Run the governance smoke test**

Run:

```powershell
.\scripts\test-harness-governance.ps1
```

Expected: `PASS: Harness governance smoke checks completed.`

- [ ] **Step 2: Show latest hook report**

Run:

```powershell
.\scripts\show-report.ps1
```

Expected:

- `latest-skill-gate-report.json` exists.
- `latest.json` exists.
- latest state contains required skills, read evidence, and skill receipts after the smoke flow.

- [ ] **Step 3: Manual acceptance check**

Confirm these acceptance criteria:

- A prompt that matches configured keywords injects required skill read instructions.
- A missing required skill read blocks at Stop.
- A detected phase with missing required artifacts blocks at Stop.
- A final answer missing `技能使用证据` blocks at Stop.
- A frontend/development phase answer must include `组件职责`, `类型定义`, and `验证`.
- Browser validation final output must include evidence that the user confirmed entering browser validation.
- Local tests can be run without network access.

## Expected Result

After this plan is implemented, the repository will provide a simple Harness that can:

- Detect required skills from prompts.
- Require observable skill file reads.
- Produce skill receipts from evidence.
- Enforce phase-specific output requirements.
- Validate traceability and review artifact shape.
- Keep the workflow local, auditable, and easy to extend.

## Self-Review

Spec coverage:

- Skill reference governance is covered by Tasks 1, 3, 4, 5, and 7.
- Artifact review governance is covered by Tasks 2, 6, 8, and 9.
- Simplicity and no overdesign are covered by the file-based architecture and no external dependencies.
- Product choices are fixed in the Confirmed Product Decisions section.

Placeholder scan:

- No unresolved placeholder markers or vague implementation placeholders are intentionally left in the executable tasks.

Type consistency:

- The plan consistently uses `skillReceipts`, `phaseGates`, `reviewQuality`, `traceability`, and `browser-validation` naming.
