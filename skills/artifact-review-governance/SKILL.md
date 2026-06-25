---
name: artifact-review-governance
description: Use when reviewing design documents, code, browser validation evidence, or correction records for AI-generated development work.
---

# Artifact Review Governance

## Rules

- Reviews must be issue-level, not generic advice.
- Each issue must include `id`, `severity`, `evidence`, `location`, `correction`, and `verification`.
- Code review must check requirement fit, design fit, skill fit, and best practices.
- Frontend review must check 组件职责 and 类型定义 when applicable.
- Browser validation must include page, steps, expected, actual, console, network, screenshots, and result.
- Browser validation is an explicit phase; the assistant must tell the user it is entering browser validation and wait for confirmation before that phase.
