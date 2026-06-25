---
name: skill-reference-governance
description: Use when a task needs to select, read, cite, or verify AI development skills before design, implementation, or review.
---

# Skill Reference Governance

## Rules

- Skills must come from the configured registry or discovered `skills/*/SKILL.md` files.
- A final answer may not claim a skill was used unless observable read evidence exists.
- A valid skill receipt contains `skillId`, `version`, `phase`, `loadedFiles`, `evidenceSource`, and `loadedAt`.
- Design and implementation outputs must cite concrete `ruleId` values or stable section ids.
- Missing required reads are blocking.
- Claims such as "I referenced the standard" are invalid without `skillId`, file evidence, rule evidence, and verification evidence.
