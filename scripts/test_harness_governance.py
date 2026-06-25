#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


def main() -> int:
    script_path = Path(".codex/hooks/skill_gate.py")
    namespace = {
        "__name__": "skill_gate_test",
        "__file__": str(script_path.resolve()),
    }
    exec(compile(script_path.read_text(encoding="utf-8"), str(script_path), "exec"), namespace)

    config = json.loads(Path(".codex/skill-gate.config.json").read_text(encoding="utf-8"))

    skill_dirs = {
        path.parent.name
        for path in Path("skills").glob("*/SKILL.md")
    }
    config_skills = set(config["skills"])
    assert skill_dirs == config_skills, {
        "missingConfig": sorted(skill_dirs - config_skills),
        "staleConfig": sorted(config_skills - skill_dirs),
    }
    for skill_id, skill_config in config["skills"].items():
        skill_root = Path("skills") / skill_id
        for read_file in skill_config.get("requiredReadFiles", []):
            assert (skill_root / read_file).is_file(), f"{skill_id}: missing requiredReadFiles entry {read_file}"
    for rule in config["rules"]:
        for skill_id in rule.get("requiredSkills", []):
            assert skill_id in config["skills"], f"{rule['id']}: unknown required skill {skill_id}"

    assert namespace["detect_phase"]("\u8fdb\u5165\u5f00\u53d1") == "development"
    assert namespace["detect_phase"]("\u8bf7\u8bc4\u5ba1\u6d4f\u89c8\u5668\u9a8c\u8bc1\u8981\u6c42") == "unknown"
    assert namespace["detect_phase"]("Please review whether we should run browser validation before release.") == "unknown"
    assert namespace["detect_phase"]("Do not run browser validation yet; discuss the gate first.") == "unknown"
    assert namespace["detect_phase"]("\u8ba8\u8bba\u662f\u5426\u8fdb\u5165\u6d4f\u89c8\u5668\u9a8c\u8bc1\u6d41\u7a0b") == "unknown"
    assert namespace["detect_phase"]("\u662f\u5426\u786e\u8ba4\u8fdb\u5165\u6d4f\u89c8\u5668\u9a8c\u8bc1\uff1f") == "unknown"
    assert namespace["detect_phase"]("\u7528\u6237\u672a\u786e\u8ba4\u8fdb\u5165\u6d4f\u89c8\u5668\u9a8c\u8bc1") == "unknown"
    assert namespace["detect_phase"]("\u7528\u6237\u786e\u8ba4\u8fdb\u5165\u6d4f\u89c8\u5668\u9a8c\u8bc1") == "browser-validation"

    assert namespace["validate_traceability_items"]([
        {
            "requirementId": "REQ-001",
            "skillId": "magus-frontend-vue-guide",
            "ruleIds": ["R1"],
            "artifact": "docs/design.md#D-001",
            "verification": "passed",
        }
    ]) == []
    assert namespace["validate_traceability_items"]([
        {
            "requirementId": "REQ-001",
            "skillId": "magus-frontend-vue-guide",
            "ruleIds": [],
            "artifact": "docs/design.md#D-001",
            "verification": "failed",
        }
    ])

    assert namespace["validate_review_issues"]([
        {
            "id": "CR-001",
            "severity": "BLOCKER",
            "evidence": "REQ-001",
            "location": "src/example.ts",
            "correction": "split type definitions",
            "verification": "typecheck",
        }
    ], config) == []
    assert namespace["validate_review_issues"]([
        {
            "id": "CR-001",
            "severity": "INFO",
            "evidence": "REQ-001",
            "location": "src/example.ts",
            "correction": "split type definitions",
            "verification": "typecheck",
        }
    ], config)
    assert namespace["validate_review_issues"]([], config)
    assert namespace["validate_review_issues"]([
        {
            "severity": "NONE",
            "reviewer": "independent-subagent",
            "reviewedArtifact": "code-review.json",
            "source": "subagent",
            "verification": "review completed",
        }
    ], config) == []
    assert namespace["validate_review_issues"]([
        {
            "severity": "NONE",
            "reviewer": "assistant",
            "reviewedArtifact": "code-review.json",
            "source": "self",
            "verification": "review completed",
        }
    ], config)
    assert namespace["validate_review_issues"]([
        {
            "severity": "NONE",
            "reviewer": "self-reviewer",
            "reviewedArtifact": "code-review.json",
            "source": "subagent",
            "verification": "review completed",
        }
    ], config)
    assert namespace["validate_review_issues"]([
        {
            "severity": "NONE",
            "reviewer": "independent-subagent",
            "reviewedArtifact": "code-review.json",
            "source": "assistant",
            "verification": "review completed",
        }
    ], config)

    browser_state = {"phase": "browser-validation", "requiredSkills": []}
    browser_missing = namespace["validate_final_output"](
        "\u7528\u6237\u786e\u8ba4\u8fdb\u5165\u6d4f\u89c8\u5668\u9a8c\u8bc1 \u622a\u56fe console network",
        browser_state,
        config,
    )
    assert any("missing user-originated confirmation" in item for item in browser_missing)
    browser_ok = namespace["validate_final_output"](
        "\u7528\u6237\u786e\u8ba4\u8fdb\u5165\u6d4f\u89c8\u5668\u9a8c\u8bc1 \u622a\u56fe console network",
        {"phase": "browser-validation", "requiredSkills": [], "browserValidationConfirmed": True},
        config,
    )
    assert browser_ok == []

    assert namespace["validate_browser_validation"]({
        "page": "/x",
        "steps": [],
        "expected": "ok",
        "actual": "ok",
        "console": [],
        "network": [],
        "screenshots": [],
        "result": "MAYBE",
    })

    skill_path = str(Path("skills/skill-reference-governance/SKILL.md").resolve())
    assert namespace["evidence_hit"](skill_path, "skill-reference-governance", skill_path) == (False, "")
    assert namespace["evidence_hit"](skill_path + "\nname: skill-reference-governance", "skill-reference-governance", skill_path) == (False, "")
    metadata_text = skill_path + "\nname: skill-reference-governance\ndescription: Use when a task needs to select, read, cite, or verify AI development skills before design, implementation, or review."
    assert namespace["evidence_hit"](metadata_text, "skill-reference-governance", skill_path) == (False, "")
    content_text = skill_path + "\n" + Path(skill_path).read_text(encoding="utf-8")
    assert namespace["evidence_hit"](content_text, "skill-reference-governance", skill_path)[0]

    receipts = namespace["build_skill_receipts"]({
        "phase": "development",
        "readEvidence": {
            "skill-reference-governance": {
                "D:/repo/skills/skill-reference-governance/SKILL.md": {
                    "seen": True,
                    "source": "PostToolUse",
                }
            }
        },
    })
    assert receipts and receipts[0]["skillId"] == "skill-reference-governance"
    assert receipts[0]["phase"] == "development"

    acceptance_lines = namespace["acceptance_guidance"](
        config,
        ["skill-reference-governance", "artifact-review-governance"],
        "initial-design",
    )
    acceptance_text = "\n".join(acceptance_lines)
    assert "Harness 最小验收卡片" in acceptance_text
    assert "skillId" in acceptance_text
    assert "ruleId" in acceptance_text
    assert "需求符合性" in acceptance_text
    assert "技能收据字段" in acceptance_text
    assert namespace["acceptance_guidance"](config, [], "unknown") == []

    available_skills = namespace["scan_available_skills"](Path.cwd(), Path.cwd())
    grilling_required, grilling_rules = namespace["select_required_skills"](
        "according to Harness, please grill my implementation plan.",
        config,
        available_skills,
    )
    assert "grilling" in grilling_required
    assert "plan-grilling" in grilling_rules

    explicit_required, explicit_rules = namespace["select_required_skills"](
        "please use $grilling on this plan",
        config,
        available_skills,
    )
    assert explicit_required == ["grilling"]
    assert explicit_rules == ["explicit:$grilling"]

    captured_state = {}
    namespace["save_state"] = lambda _root, _payload, state: captured_state.update(state)
    namespace["write_json"] = lambda _path, _data: None
    namespace["append_jsonl"] = lambda _path, _data: None
    submit_result = namespace["handle_user_prompt_submit"](
        Path(".codex"),
        {
            "session_id": "submit-test",
            "turn_id": "turn-1",
            "prompt": "根据Harness规范，设计一个菜单页面",
        },
        config,
        Path.cwd(),
        Path.cwd(),
        namespace["scan_available_skills"](Path.cwd(), Path.cwd()),
    )
    injected = submit_result["hookSpecificOutput"]["additionalContext"]
    assert "Harness 最小验收卡片" in injected
    assert "skillId" in injected
    assert "ruleId" in injected
    assert "需求符合性" in injected

    plain_result = namespace["handle_user_prompt_submit"](
        Path(".codex"),
        {
            "session_id": "submit-test",
            "turn_id": "turn-plain",
            "prompt": "你好呀",
        },
        config,
        Path.cwd(),
        Path.cwd(),
        namespace["scan_available_skills"](Path.cwd(), Path.cwd()),
    )
    plain_context = plain_result["hookSpecificOutput"]["additionalContext"]
    assert "no required skill matched" in plain_context
    assert "Harness 最小验收卡片" not in plain_context

    missing_artifact_root = Path("__missing_phase_artifact_root__")
    artifact_problems = namespace["validate_phase_artifacts"](
        missing_artifact_root,
        {"phase": "development"},
        config,
    )
    assert any("implementation-context-pack.json" in item for item in artifact_problems)
    assert any("implementation-evidence.json" in item for item in artifact_problems)

    root = Path(".codex")
    payload = {
        "session_id": "phase-artifact-test",
        "turn_id": "second-stop",
        "hook_event_name": "Stop",
        "stop_hook_active": True,
        "last_assistant_message": "\u7ec4\u4ef6\u804c\u8d23 \u7c7b\u578b\u5b9a\u4e49 \u9a8c\u8bc1",
    }
    stop_state = {
        "sessionId": "phase-artifact-test",
        "turnId": "second-stop",
        "phase": "development",
        "requiredSkills": [],
        "readEvidence": {},
        "stopBlockCount": 1,
    }
    namespace["load_state"] = lambda _root, _payload: stop_state
    namespace["save_state"] = lambda _root, _payload, _state: None
    namespace["write_json"] = lambda _path, _data: None
    namespace["append_jsonl"] = lambda _path, _data: None
    namespace["read_transcript"] = lambda _payload: ""
    result = namespace["handle_stop"](root, payload, config, missing_artifact_root, Path.cwd(), {})
    assert result.get("decision") == "block"

    skill_file = str(Path("skills/skill-reference-governance/SKILL.md").resolve())
    existing_state = {
        "sessionId": "merge-test",
        "turnId": "turn-1",
        "requiredSkills": ["skill-reference-governance", "magus-framework-ui"],
        "readEvidence": {
            "magus-framework-ui": {
                str(Path("skills/magus-framework-ui/SKILL.md").resolve()): {
                    "seen": True,
                    "source": "PostToolUse",
                }
            }
        },
        "events": [],
    }
    incoming_state = {
        "sessionId": "merge-test",
        "turnId": "turn-1",
        "requiredSkills": ["skill-reference-governance", "magus-framework-ui"],
        "readEvidence": {
            "skill-reference-governance": {
                skill_file: {
                    "seen": True,
                    "source": "PostToolUse",
                }
            }
        },
        "events": [{"hook": "PostToolUse"}],
    }
    merged_state = namespace["merge_state_for_save"](existing_state, incoming_state)
    merged_evidence = merged_state["readEvidence"]
    assert merged_evidence["skill-reference-governance"][skill_file]["seen"]
    assert merged_evidence["magus-framework-ui"][str(Path("skills/magus-framework-ui/SKILL.md").resolve())]["seen"]

    stop_lines = namespace["stop_failure_lines"](
        missing_reads={"skill-reference-governance": [skill_file]},
        output_problems=[],
        artifact_problems=[],
    )
    stop_text = "\n".join(stop_lines)
    assert "补齐阶段 required artifact" not in stop_text
    assert "读取缺失的 SKILL.md / references 文件" in stop_text

    artifact_lines = namespace["stop_failure_lines"](
        missing_reads={},
        output_problems=[],
        artifact_problems=["[development] missing required artifact: implementation-evidence.json"],
    )
    assert "补齐阶段 required artifact" in "\n".join(artifact_lines)

    output_lines = namespace["stop_failure_lines"](
        missing_reads={},
        output_problems=["[skill-reference-governance] final output missing required phrase: skillId"],
        artifact_problems=[],
    )
    assert "按技能规则修改方案" in "\n".join(output_lines)

    second_stop_state = {
        "sessionId": "phase-artifact-test",
        "turnId": "second-stop",
        "phase": "unknown",
        "requiredSkills": ["skill-reference-governance"],
        "readEvidence": {},
        "stopBlockCount": 1,
    }
    namespace["load_state"] = lambda _root, _payload: second_stop_state
    result = namespace["handle_stop"](
        root,
        {
            "session_id": "phase-artifact-test",
            "turn_id": "second-stop",
            "hook_event_name": "Stop",
            "stop_hook_active": True,
            "last_assistant_message": "skillId ruleId 技能使用证据",
        },
        config,
        Path.cwd(),
        Path.cwd(),
        namespace["scan_available_skills"](Path.cwd(), Path.cwd()),
    )
    assert result.get("decision") == "block"

    print("Python function checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
