#!/usr/bin/env python3
"""Codex Skill Gate Hook.

Three gates:
1. UserPromptSubmit: select required skills and inject read/apply requirements.
2. PostToolUse: audit tool evidence that required skill files were read/referenced.
3. Stop: validate read evidence and final output; block once if the gate fails.

Important boundary:
Codex does not expose an internal "loaded_skills" field to hooks.
This hook validates observable evidence, not hidden model state.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

SURROGATE_RE = re.compile(r"[\ud800-\udfff]")
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?", re.DOTALL)
NEGATION_MARKERS = (
    "不",
    "不要",
    "不得",
    "不能",
    "不可",
    "不应",
    "不建议",
    "禁止",
    "避免",
    "无需",
    "勿",
    "must not",
    "do not",
    "don't",
    "avoid",
    "forbid",
    "forbidden",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sanitize_text(value: str) -> str:
    return SURROGATE_RE.sub("\uFFFD", value or "")


def sanitize_obj(value: Any) -> Any:
    if isinstance(value, str):
        return sanitize_text(value)
    if isinstance(value, dict):
        return {sanitize_text(str(k)): sanitize_obj(v) for k, v in value.items()}
    if isinstance(value, list):
        return [sanitize_obj(v) for v in value]
    if isinstance(value, tuple):
        return [sanitize_obj(v) for v in value]
    return value


def stdout_json(data: Any) -> str:
    # Keep hook stdout ASCII-only. Some Windows/host chains mis-decode raw UTF-8
    # hook output before Codex parses it, which turns Chinese guidance into
    # mojibake. JSON unicode escapes survive those chains safely.
    return json.dumps(sanitize_obj(data), ensure_ascii=True, separators=(",", ":"))


def read_stdin_text() -> str:
    if sys.stdin.isatty():
        return ""
    try:
        return sys.stdin.buffer.read().decode("utf-8", errors="replace")
    except Exception:
        try:
            return sys.stdin.read()
        except Exception:
            return ""


def parse_payload() -> dict[str, Any]:
    raw = sanitize_text(read_stdin_text())
    try:
        data = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        data = {"_raw": raw}
    return sanitize_obj(data) if isinstance(data, dict) else {"_raw": raw}


def hook_root() -> Path:
    # .codex/hooks/skill_gate.py -> .codex
    return Path(__file__).resolve().parents[1]


def project_root_from_payload(payload: dict[str, Any]) -> Path:
    cwd = Path(str(payload.get("cwd") or os.getcwd())).resolve()
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=str(cwd),
            text=True,
            capture_output=True,
            timeout=3,
            check=False,
        )
        if result.returncode == 0 and result.stdout.strip():
            return Path(result.stdout.strip()).resolve()
    except Exception:
        pass
    return cwd


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except Exception:
        return default


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(sanitize_obj(data), ensure_ascii=False, indent=2)
    path.write_text(sanitize_text(text) + "\n", encoding="utf-8", errors="replace")


def append_jsonl(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(sanitize_obj(data), ensure_ascii=False, separators=(",", ":"))
    with path.open("a", encoding="utf-8", errors="replace") as handle:
        handle.write(sanitize_text(line) + "\n")


def event_name(payload: dict[str, Any]) -> str:
    return str(payload.get("hook_event_name") or payload.get("hookEventName") or "UnknownHook")


def get_prompt(payload: dict[str, Any]) -> str:
    return str(payload.get("prompt") or payload.get("user_prompt") or payload.get("userPrompt") or payload.get("message") or "")


def get_last_assistant_message(payload: dict[str, Any]) -> str:
    return str(payload.get("last_assistant_message") or payload.get("lastAssistantMessage") or "")


def get_transcript_path(payload: dict[str, Any]) -> str:
    return str(payload.get("transcript_path") or payload.get("transcriptPath") or "")


def read_transcript(payload: dict[str, Any]) -> str:
    path_text = get_transcript_path(payload)
    if not path_text:
        return ""
    try:
        path = Path(path_text)
        if path.exists() and path.is_file():
            return path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""
    return ""


def state_key(payload: dict[str, Any]) -> str:
    session_id = str(payload.get("session_id") or "no-session")
    turn_id = str(payload.get("turn_id") or "no-turn")
    safe = re.sub(r"[^a-zA-Z0-9._-]+", "_", f"{session_id}__{turn_id}").strip("_")
    return safe or "default"


def state_path(root: Path, payload: dict[str, Any]) -> Path:
    return root / "hook-state" / "skill-gate" / f"{state_key(payload)}.json"


def latest_state_path(root: Path) -> Path:
    return root / "hook-state" / "skill-gate" / "latest.json"


def load_state(root: Path, payload: dict[str, Any]) -> dict[str, Any]:
    state = read_json(state_path(root, payload), None)
    if isinstance(state, dict):
        return state
    state = read_json(latest_state_path(root), None)
    if isinstance(state, dict):
        return state
    return {
        "sessionId": payload.get("session_id", ""),
        "turnId": payload.get("turn_id", ""),
        "requiredSkills": [],
        "matchedRules": [],
        "readEvidence": {},
        "stopBlockCount": 0,
        "events": [],
    }


def save_state(root: Path, payload: dict[str, Any], state: dict[str, Any]) -> None:
    path = state_path(root, payload)
    lock_path = path.with_suffix(path.suffix + ".lock")
    lock_handle = acquire_lock(lock_path)
    try:
        existing = read_json(path, None)
        merged = merge_state_for_save(existing, state) if isinstance(existing, dict) else state
        write_json(path, merged)
        write_json(latest_state_path(root), merged)
    finally:
        release_lock(lock_path, lock_handle)


def acquire_lock(lock_path: Path, timeout_seconds: float = 2.0) -> int:
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    deadline = time.monotonic() + timeout_seconds
    while True:
        try:
            return os.open(str(lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError:
            if time.monotonic() >= deadline:
                try:
                    lock_path.unlink()
                except FileNotFoundError:
                    pass
                except Exception:
                    raise
                continue
            time.sleep(0.02)


def release_lock(lock_path: Path, lock_handle: int) -> None:
    try:
        os.close(lock_handle)
    finally:
        try:
            lock_path.unlink()
        except FileNotFoundError:
            pass


def merge_state_for_save(existing: Any, incoming: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(existing, dict):
        return incoming

    merged = dict(existing)
    merged.update(incoming)
    merged["readEvidence"] = merge_read_evidence(
        existing.get("readEvidence", {}),
        incoming.get("readEvidence", {}),
    )
    merged["events"] = merge_events(existing.get("events", []), incoming.get("events", []))
    return merged


def merge_read_evidence(existing: Any, incoming: Any) -> dict[str, Any]:
    merged: dict[str, Any] = {}
    for source in [existing, incoming]:
        if not isinstance(source, dict):
            continue
        for skill_id, files in source.items():
            skill_files = merged.setdefault(str(skill_id), {})
            if not isinstance(files, dict):
                continue
            for file_path, evidence in files.items():
                skill_files[str(file_path)] = evidence
    return merged


def merge_events(existing: Any, incoming: Any) -> list[Any]:
    merged: list[Any] = []
    seen: set[str] = set()
    for source in [existing, incoming]:
        if not isinstance(source, list):
            continue
        for event in source:
            key = json.dumps(sanitize_obj(event), ensure_ascii=False, sort_keys=True)
            if key not in seen:
                seen.add(key)
                merged.append(event)
    return merged


def load_config(root: Path) -> dict[str, Any]:
    return read_json(root / "skill-gate.config.json", {"rules": [], "skills": {}})


def anti_pattern_guidance(project_root: Path, config: dict[str, Any]) -> list[str]:
    if not config.get("injectAntiPatternsEveryPrompt", False):
        return []

    rel_path = str(config.get("antiPatternsFile") or ".codex/harness/anti-patterns.md")
    path = (project_root / rel_path).resolve()
    try:
        text = path.read_text(encoding="utf-8", errors="replace").strip()
    except Exception:
        return []
    if not text:
        return []
    return [
        "AI 反模式提醒（每轮注入）：",
        text,
    ]


def normalize_slashes(text: str) -> str:
    return sanitize_text(text).replace("\\", "/")


def norm_key(text: str) -> str:
    return normalize_slashes(text).lower()


def parse_skill_frontmatter(skill_md: Path) -> dict[str, str]:
    fallback_name = skill_md.parent.name
    try:
        text = skill_md.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return {"name": fallback_name, "description": ""}
    match = FRONTMATTER_RE.match(text)
    name = fallback_name
    description = ""
    if match:
        for line in match.group(1).splitlines():
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            key = key.strip().lower()
            value = value.strip().strip("'\"")
            if key == "name" and value:
                name = value
            elif key == "description" and value:
                description = value
    return {"name": sanitize_text(name), "description": sanitize_text(description)}


def skill_roots(project_root: Path, cwd: Path) -> list[Path]:
    roots: list[Path] = []
    current = cwd.resolve()
    project_root = project_root.resolve()

    while True:
        roots.append(current / "skills")
        if current == project_root or current.parent == current:
            break
        current = current.parent

    roots.append(Path.home() / "skills")
    if os.name != "nt":
        roots.append(Path("/etc/codex/skills"))

    seen: set[str] = set()
    unique: list[Path] = []
    for root in roots:
        key = str(root.resolve()).lower() if os.name == "nt" else str(root.resolve())
        if key not in seen:
            seen.add(key)
            unique.append(root)
    return unique


def scan_available_skills(project_root: Path, cwd: Path) -> dict[str, dict[str, Any]]:
    skills: dict[str, dict[str, Any]] = {}
    for root in skill_roots(project_root, cwd):
        if not root.exists() or not root.is_dir():
            continue
        for skill_md in sorted(root.glob("*/SKILL.md")):
            meta = parse_skill_frontmatter(skill_md)
            name = meta["name"]
            # First match wins, mirroring local-to-parent-to-user priority.
            skills.setdefault(name, {
                "name": name,
                "description": meta["description"],
                "path": str(skill_md.resolve()),
                "dir": str(skill_md.parent.resolve()),
                "root": str(root.resolve()),
            })
    return skills


def resolve_skill_file(available: dict[str, dict[str, Any]], project_root: Path, skill_name: str, relative_file: str) -> str:
    relative = relative_file.replace("\\", "/").strip("/")
    skill = available.get(skill_name)
    if skill:
        return str((Path(skill["dir"]) / relative).resolve())
    return str((project_root / "skills" / skill_name / relative).resolve())


def select_required_skills(prompt: str, config: dict[str, Any], available: dict[str, dict[str, Any]]) -> tuple[list[str], list[str]]:
    prompt_lower = prompt.lower()
    required: list[str] = []
    matched_rules: list[str] = []
    harness_activated = is_harness_activated(prompt, config)

    if harness_activated:
        for rule in config.get("rules", []):
            keywords = rule.get("whenPromptMatches", [])
            if any(str(keyword).lower() in prompt_lower for keyword in keywords):
                rule_id = str(rule.get("id") or "unnamed-rule")
                matched_rules.append(rule_id)
                for skill_name in rule.get("requiredSkills", []):
                    skill_name = str(skill_name)
                    if skill_name not in required:
                        required.append(skill_name)

    # Explicit skill mentions: $skill-name or direct skill name.
    for match in re.finditer(r"\$([a-zA-Z0-9][a-zA-Z0-9._-]{1,80})", prompt):
        skill_name = match.group(1)
        if skill_name in available and skill_name not in required:
            required.append(skill_name)
            matched_rules.append(f"explicit:${skill_name}")

    return required, matched_rules


def is_harness_activated(prompt: str, config: dict[str, Any]) -> bool:
    text = prompt.lower()
    phrases = config.get("activationPhrases", [])
    if not isinstance(phrases, list):
        phrases = []
    return any(str(phrase).lower() in text for phrase in phrases)


def required_files_for(required_skills: list[str], config: dict[str, Any], available: dict[str, dict[str, Any]], project_root: Path) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    skill_cfgs = config.get("skills", {}) if isinstance(config.get("skills", {}), dict) else {}

    for skill_name in required_skills:
        skill_cfg = skill_cfgs.get(skill_name, {}) if isinstance(skill_cfgs.get(skill_name, {}), dict) else {}
        files = skill_cfg.get("requiredReadFiles", ["SKILL.md"])
        if not isinstance(files, list) or not files:
            files = ["SKILL.md"]
        result[skill_name] = [resolve_skill_file(available, project_root, skill_name, str(file)) for file in files]
    return result


def stringify(value: Any) -> str:
    try:
        return json.dumps(value, ensure_ascii=False)
    except Exception:
        return str(value)


def collect_post_tool_text(payload: dict[str, Any]) -> str:
    tool_input = payload.get("tool_input") or payload.get("toolInput") or {}
    tool_response = payload.get("tool_response") or payload.get("toolResponse") or {}
    parts = [
        str(payload.get("tool_name") or ""),
        stringify(tool_input),
        stringify(tool_response),
    ]
    return sanitize_text("\n".join(parts))


def file_evidence_snippets(file_path: str) -> list[str]:
    try:
        text = Path(file_path).read_text(encoding="utf-8", errors="replace")
    except Exception:
        return []
    snippets: list[str] = []
    in_frontmatter = False
    frontmatter_seen = False
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped == "---":
            if stripped == "---" and not frontmatter_seen:
                in_frontmatter = True
                frontmatter_seen = True
            elif stripped == "---" and in_frontmatter:
                in_frontmatter = False
            continue
        if in_frontmatter:
            continue
        if stripped.startswith("#"):
            continue
        snippets.append(stripped[:120])
        if len(snippets) >= 3:
            break
    return snippets


def evidence_hit(text: str, skill_name: str, file_path: str) -> tuple[bool, str]:
    text_n = norm_key(text)
    path_n = norm_key(file_path)
    suffix = norm_key(f"skills/{skill_name}/{Path(file_path).name}")
    skill_file_pair = skill_name.lower() in text_n and Path(file_path).name.lower() in text_n
    snippets = file_evidence_snippets(file_path)
    snippet_hits = [snippet for snippet in snippets if norm_key(snippet) in text_n]
    has_content = len(snippet_hits) >= min(2, len(snippets)) if snippets else False

    if path_n and path_n in text_n and has_content:
        return True, "full_path"
    if suffix and suffix in text_n and has_content:
        return True, "skill_path_suffix"
    if skill_file_pair and has_content:
        return True, "skill_name_file_name_and_content"
    return False, ""


def update_read_evidence_from_text(state: dict[str, Any], text: str, source: str, config: dict[str, Any], available: dict[str, dict[str, Any]], project_root: Path) -> None:
    required_skills = [str(v) for v in state.get("requiredSkills", [])]
    files_by_skill = required_files_for(required_skills, config, available, project_root)
    evidence = state.setdefault("readEvidence", {})

    for skill_name, file_paths in files_by_skill.items():
        skill_evidence = evidence.setdefault(skill_name, {})
        for file_path in file_paths:
            hit, hit_kind = evidence_hit(text, skill_name, file_path)
            if hit:
                skill_evidence[file_path] = {
                    "seen": True,
                    "source": source,
                    "evidence": hit_kind,
                    "timestamp": utc_now(),
                }


def missing_required_reads(state: dict[str, Any], config: dict[str, Any], available: dict[str, dict[str, Any]], project_root: Path) -> dict[str, list[str]]:
    required_skills = [str(v) for v in state.get("requiredSkills", [])]
    files_by_skill = required_files_for(required_skills, config, available, project_root)
    evidence = state.get("readEvidence", {}) if isinstance(state.get("readEvidence", {}), dict) else {}
    missing: dict[str, list[str]] = {}

    for skill_name, file_paths in files_by_skill.items():
        skill_evidence = evidence.get(skill_name, {}) if isinstance(evidence.get(skill_name, {}), dict) else {}
        for file_path in file_paths:
            if not skill_evidence.get(file_path, {}).get("seen"):
                missing.setdefault(skill_name, []).append(file_path)
    return missing


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
        sources = sorted({
            str(item.get("source"))
            for item in files.values()
            if isinstance(item, dict) and item.get("seen") and item.get("source")
        })
        receipts.append({
            "skillId": str(skill_id),
            "version": "unknown",
            "phase": phase,
            "loadedFiles": loaded_files,
            "evidenceSource": ",".join(sources) if sources else "unknown",
            "loadedAt": utc_now(),
        })
    return receipts


def browser_validation_confirmed(prompt: str) -> bool:
    text = prompt.lower()
    if any(token in text for token in [
        "不要",
        "不得",
        "不能",
        "暂不",
        "先不",
        "无需",
        "未确认",
        "没有确认",
        "讨论",
        "是否",
        "吗",
        "？",
        "do not",
        "don't",
        "not yet",
        "whether",
        "should we",
        "review whether",
        "discuss",
    ]):
        return False
    return any(token in text for token in [
        "用户确认进入浏览器验证",
        "确认进入浏览器验证",
        "开始浏览器验证",
        "执行浏览器验证",
        "进行浏览器验证",
        "please start browser validation",
        "please enter browser validation",
        "confirmed: start browser validation",
        "confirmed start browser validation",
        "confirm browser validation now",
    ])


def detect_phase(prompt: str) -> str:
    text = prompt.lower()
    if browser_validation_confirmed(prompt):
        return "browser-validation"
    if any(token in text for token in ["代码评审", "code review", "review code"]):
        return "code-review"
    if any(token in text for token in ["开发阶段", "进入开发", "实现", "implementation", "coding"]):
        return "development"
    if any(token in text for token in ["文档评审", "document review", "评审设计"]):
        return "document-review"
    if any(token in text for token in ["设计阶段", "初始设计", "架构"]):
        return "initial-design"
    return "unknown"


def validate_required_object_fields(item: Any, required: list[str], label: str) -> list[str]:
    problems: list[str] = []
    if not isinstance(item, dict):
        return [f"{label} must be an object"]
    for field in required:
        if not item.get(field):
            problems.append(f"{label} missing {field}")
    return problems


def validate_traceability_items(items: Any) -> list[str]:
    problems: list[str] = []
    if not isinstance(items, list):
        return ["traceability artifact must be a JSON array"]

    required = ["requirementId", "skillId", "ruleIds", "artifact", "verification"]
    for index, item in enumerate(items):
        label = f"traceability[{index}]"
        problems.extend(validate_required_object_fields(item, required, label))
        if not isinstance(item, dict):
            continue
        if not isinstance(item.get("ruleIds"), list) or not item.get("ruleIds"):
            problems.append(f"{label} ruleIds must be a non-empty array")
    return problems


def validate_requirement_atoms(items: Any) -> list[str]:
    problems: list[str] = []
    if not isinstance(items, list):
        return ["requirement atoms artifact must be a JSON array"]
    if not items:
        return ["requirement atoms artifact must not be empty"]
    required = ["id", "source", "type", "acceptanceCriteria"]
    for index, item in enumerate(items):
        label = f"requirementAtoms[{index}]"
        problems.extend(validate_required_object_fields(item, required, label))
        if isinstance(item, dict) and not isinstance(item.get("acceptanceCriteria"), list):
            problems.append(f"{label} acceptanceCriteria must be an array")
    return problems


def validate_skill_receipts(items: Any) -> list[str]:
    problems: list[str] = []
    if not isinstance(items, list):
        return ["skill receipts artifact must be a JSON array"]
    if not items:
        return ["skill receipts artifact must not be empty"]
    required = ["skillId", "version", "phase", "loadedFiles", "evidenceSource", "loadedAt"]
    for index, item in enumerate(items):
        label = f"skillReceipts[{index}]"
        problems.extend(validate_required_object_fields(item, required, label))
        if isinstance(item, dict) and (not isinstance(item.get("loadedFiles"), list) or not item.get("loadedFiles")):
            problems.append(f"{label} loadedFiles must be a non-empty array")
    return problems


def artifact_required_fields(artifact_rel: str) -> list[str]:
    if artifact_rel.endswith("requirement-atoms.json"):
        return ["id", "source", "type", "acceptanceCriteria"]
    if artifact_rel.endswith("skill-matrix.json"):
        return ["requirementId", "skillId", "ruleIds", "artifact", "verification"]
    if artifact_rel.endswith("skill-receipts.json"):
        return ["skillId", "version", "phase", "loadedFiles", "evidenceSource", "loadedAt"]
    if artifact_rel.endswith("implementation-context-pack.json"):
        return ["taskId", "sourceRequirements", "requiredSkills", "requiredRules", "verification"]
    if artifact_rel.endswith("implementation-evidence.json"):
        return ["taskId", "requirements", "skillRules", "files", "verification"]
    if artifact_rel.endswith("doc-review.json") or artifact_rel.endswith("code-review.json"):
        return ["id", "severity", "evidence", "location", "correction", "verification"]
    if artifact_rel.endswith("browser-validation.json"):
        return ["page", "steps", "expected", "actual", "console", "network", "screenshots", "result"]
    return []


def phase_artifact_guidance(config: dict[str, Any], phase: str) -> list[str]:
    phase_gates = config.get("phaseGates", {}) if isinstance(config.get("phaseGates", {}), dict) else {}
    phase_gate = phase_gates.get(phase, {}) if isinstance(phase_gates.get(phase, {}), dict) else {}
    artifacts = phase_gate.get("requiredArtifacts", []) if isinstance(phase_gate, dict) else []
    phrases = phase_gate.get("requiredFinalPhrases", []) if isinstance(phase_gate, dict) else []
    if not artifacts and not phrases:
        return []

    lines = ["", "本阶段 required artifact："]
    for artifact in artifacts:
        artifact_rel = str(artifact)
        fields = artifact_required_fields(artifact_rel)
        if fields:
            lines.append(f"- {artifact_rel}：必须包含字段 {', '.join(fields)}")
        else:
            lines.append(f"- {artifact_rel}")
    if phrases:
        lines.append("本阶段最终回答必须包含：")
        for phrase in phrases:
            lines.append(f"- {phrase}")
    return lines


def unique_strings(values: list[Any]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        text = str(value)
        if text and text not in seen:
            seen.add(text)
            result.append(text)
    return result


def skill_output_phrases(config: dict[str, Any], required_skills: list[str]) -> list[str]:
    skill_cfgs = config.get("skills", {}) if isinstance(config.get("skills", {}), dict) else {}
    phrases: list[Any] = []
    for skill_name in required_skills:
        skill_cfg = skill_cfgs.get(skill_name, {}) if isinstance(skill_cfgs.get(skill_name, {}), dict) else {}
        phrases.extend(skill_cfg.get("outputMustContain", []))
    return unique_strings(phrases)


def phase_output_phrases(config: dict[str, Any], phase: str) -> list[str]:
    phase_gates = config.get("phaseGates", {}) if isinstance(config.get("phaseGates", {}), dict) else {}
    phase_gate = phase_gates.get(phase, {}) if isinstance(phase_gates.get(phase, {}), dict) else {}
    return unique_strings(phase_gate.get("requiredFinalPhrases", []) if isinstance(phase_gate, dict) else [])


def receipt_required_fields(config: dict[str, Any]) -> list[str]:
    receipt = config.get("receipt", {}) if isinstance(config.get("receipt", {}), dict) else {}
    if not receipt.get("enabled", False):
        return []
    return unique_strings(receipt.get("requiredFields", []))


def acceptance_guidance(config: dict[str, Any], required_skills: list[str], phase: str) -> list[str]:
    """Build a compact, deterministic checklist only for turns already gated."""
    if not required_skills and phase == "unknown":
        return []

    skill_phrases = skill_output_phrases(config, required_skills)
    phase_phrases = phase_output_phrases(config, phase)
    receipt_fields = receipt_required_fields(config)

    if not skill_phrases and not phase_phrases and not receipt_fields:
        return []

    lines = [
        "",
        "本轮 Harness 最小验收卡片（只在命中门禁时注入）：",
    ]
    if receipt_fields:
        lines.append(f"- 技能收据字段：{', '.join(receipt_fields)}")
    if skill_phrases:
        lines.append(f"- 技能最终必含短语：{', '.join(skill_phrases)}")
    if phase_phrases:
        lines.append(f"- 阶段最终必含短语：{', '.join(phase_phrases)}")
    lines.extend([
        "- 最终回答建议骨架：需求符合性；组件职责/类型定义（前端适用时）；纠偏；验证；技能使用证据。",
        "- 技能使用证据内逐项写明 skillId、ruleId、读取文件、来源文件、验证证据；不要只写泛泛引用。",
        "- 如果不按照这个规范生成，最终结果无法通过审核。",
    ])
    return lines


def validate_implementation_context(item: Any) -> list[str]:
    required = ["taskId", "sourceRequirements", "requiredSkills", "requiredRules", "verification"]
    problems = validate_required_object_fields(item, required, "implementationContext")
    if isinstance(item, dict):
        for field in ["sourceRequirements", "requiredSkills", "requiredRules"]:
            if not isinstance(item.get(field), list) or not item.get(field):
                problems.append(f"implementationContext {field} must be a non-empty array")
    return problems


def validate_implementation_evidence(item: Any) -> list[str]:
    required = ["taskId", "requirements", "skillRules", "files", "verification"]
    problems = validate_required_object_fields(item, required, "implementationEvidence")
    if isinstance(item, dict):
        for field in ["requirements", "skillRules", "files"]:
            if not isinstance(item.get(field), list) or not item.get(field):
                problems.append(f"implementationEvidence {field} must be a non-empty array")
    return problems


def validate_review_issues(items: Any, config: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    if not isinstance(items, list):
        return ["review artifact must be a JSON array"]
    if not items:
        return ["review artifact must contain at least one issue or no-findings record"]

    review_cfg = config.get("reviewQuality", {}) if isinstance(config.get("reviewQuality", {}), dict) else {}
    required = [str(v) for v in review_cfg.get("requiredIssueFields", [])]
    allowed = {str(v) for v in review_cfg.get("allowedSeverities", [])}

    for index, item in enumerate(items):
        label = f"reviewIssues[{index}]"
        if not isinstance(item, dict):
            problems.extend(validate_required_object_fields(item, required, label))
            continue
        severity = str(item.get("severity", ""))
        if severity == "NONE":
            source = str(item.get("source", "")).lower()
            reviewer = str(item.get("reviewer", "")).lower()
            if item.get("reviewedArtifact") and item.get("verification") and source in {"subagent", "independent-subagent", "external-review"} and "assistant" not in reviewer and "self" not in reviewer and "self" not in source:
                continue
            problems.append(f"{label} no-findings record must come from an independent reviewer source")
            continue
        problems.extend(validate_required_object_fields(item, required, label))
        if allowed and severity not in allowed:
            problems.append(f"{label} invalid severity: {severity}")
    return problems


def validate_browser_validation(item: Any) -> list[str]:
    required = ["page", "steps", "expected", "actual", "console", "network", "screenshots", "result"]
    problems = validate_required_object_fields(item, required, "browserValidation")
    if isinstance(item, dict):
        if str(item.get("result")) not in {"PASS", "FAIL", "BLOCKED"}:
            problems.append(f"browserValidation invalid result: {item.get('result')}")
        for field in ["steps", "screenshots"]:
            if not isinstance(item.get(field), list):
                problems.append(f"browserValidation {field} must be an array")
    return problems


def validate_json_artifact(path: Path, validator: Callable[[Any], list[str]]) -> list[str]:
    if not path.exists():
        return [f"missing artifact: {path}"]
    data = read_json(path, None)
    if data is None:
        return [f"invalid json artifact: {path}"]
    return validator(data)


def schema_key_for_artifact(artifact_rel: str) -> str:
    if artifact_rel.endswith("skill-receipts.json"):
        return "skillReceipt"
    if artifact_rel.endswith("skill-matrix.json"):
        return "traceability"
    if artifact_rel.endswith("doc-review.json") or artifact_rel.endswith("code-review.json"):
        return "reviewIssue"
    if artifact_rel.endswith("browser-validation.json"):
        return "browserValidation"
    return ""


def validate_with_configured_schema(project_root: Path, config: dict[str, Any], artifact_rel: str, data: Any) -> list[str]:
    schema_key = schema_key_for_artifact(artifact_rel)
    if not schema_key:
        return []
    schema_paths = config.get("artifactSchemas", {}) if isinstance(config.get("artifactSchemas", {}), dict) else {}
    schema_rel = str(schema_paths.get(schema_key) or "")
    if not schema_rel:
        return []
    schema = read_json(project_root / schema_rel, None)
    if not isinstance(schema, dict):
        return [f"{artifact_rel} configured schema is missing or invalid: {schema_rel}"]
    required = [str(v) for v in schema.get("required", [])]
    if not required:
        return []

    targets = data if isinstance(data, list) else [data]
    problems: list[str] = []
    for index, item in enumerate(targets):
        label = f"{artifact_rel}[{index}]" if isinstance(data, list) else artifact_rel
        problems.extend(validate_required_object_fields(item, required, label))
    return problems


def validate_json_artifact_with_schema(project_root: Path, config: dict[str, Any], artifact_rel: str, path: Path, validator: Callable[[Any], list[str]]) -> list[str]:
    if not path.exists():
        return [f"missing artifact: {path}"]
    data = read_json(path, None)
    if data is None:
        return [f"invalid json artifact: {path}"]
    problems = validate_with_configured_schema(project_root, config, artifact_rel, data)
    problems.extend(validator(data))
    return problems


def validate_phase_artifacts(project_root: Path, state: dict[str, Any], config: dict[str, Any]) -> list[str]:
    phase = str(state.get("phase", "unknown"))
    phase_gates = config.get("phaseGates", {}) if isinstance(config.get("phaseGates", {}), dict) else {}
    phase_gate = phase_gates.get(phase, {}) if isinstance(phase_gates.get(phase, {}), dict) else {}
    if phase == "unknown" or not phase_gate:
        return []

    problems: list[str] = []
    for artifact in phase_gate.get("requiredArtifacts", []):
        artifact_rel = str(artifact)
        artifact_path = project_root / artifact_rel
        if not artifact_path.exists():
            problems.append(f"[{phase}] missing required artifact: {artifact_rel}")
            continue
        if artifact_rel.endswith("requirement-atoms.json"):
            problems.extend(f"[{phase}] {problem}" for problem in validate_json_artifact(artifact_path, validate_requirement_atoms))
        elif artifact_rel.endswith("skill-receipts.json"):
            problems.extend(f"[{phase}] {problem}" for problem in validate_json_artifact_with_schema(project_root, config, artifact_rel, artifact_path, validate_skill_receipts))
        elif artifact_rel.endswith("implementation-context-pack.json"):
            problems.extend(f"[{phase}] {problem}" for problem in validate_json_artifact(artifact_path, validate_implementation_context))
        elif artifact_rel.endswith("implementation-evidence.json"):
            problems.extend(f"[{phase}] {problem}" for problem in validate_json_artifact(artifact_path, validate_implementation_evidence))
        elif artifact_rel.endswith("doc-review.json") or artifact_rel.endswith("code-review.json"):
            problems.extend(f"[{phase}] {problem}" for problem in validate_json_artifact_with_schema(
                project_root,
                config,
                artifact_rel,
                artifact_path,
                lambda data: validate_review_issues(data, config),
            ))
        elif artifact_rel.endswith("browser-validation.json"):
            problems.extend(f"[{phase}] {problem}" for problem in validate_json_artifact_with_schema(project_root, config, artifact_rel, artifact_path, validate_browser_validation))
        elif artifact_rel.endswith("skill-matrix.json"):
            problems.extend(f"[{phase}] {problem}" for problem in validate_json_artifact_with_schema(project_root, config, artifact_rel, artifact_path, validate_traceability_items))
    return problems


def phrase_is_negated(text: str, phrase_start: int, config: dict[str, Any]) -> bool:
    if not config.get("allowNegatedForbiddenPhrases", True):
        return False

    try:
        window_size = int(config.get("forbiddenPhraseNegationWindow", 16))
    except Exception:
        window_size = 16

    prefix = text[max(0, phrase_start - window_size):phrase_start].lower()
    return any(marker.lower() in prefix for marker in NEGATION_MARKERS)


def contains_unnegated_phrase(text: str, phrase: str, config: dict[str, Any]) -> bool:
    if not phrase:
        return False

    start = 0
    while True:
        index = text.find(phrase, start)
        if index < 0:
            return False
        if not phrase_is_negated(text, index, config):
            return True
        start = index + len(phrase)


def validate_final_output(final_output: str, state: dict[str, Any], config: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    required_skills = [str(v) for v in state.get("requiredSkills", [])]
    skill_cfgs = config.get("skills", {}) if isinstance(config.get("skills", {}), dict) else {}
    phase = str(state.get("phase", "unknown"))

    if required_skills and config.get("requireEvidenceSection", True):
        title = str(config.get("evidenceSectionTitle") or "技能使用证据")
        if title not in final_output:
            problems.append(f"final output missing evidence section: {title}")

    for skill_name in required_skills:
        skill_cfg = skill_cfgs.get(skill_name, {}) if isinstance(skill_cfgs.get(skill_name, {}), dict) else {}
        for phrase in skill_cfg.get("outputMustContain", []):
            if str(phrase) not in final_output:
                problems.append(f"[{skill_name}] final output missing required phrase: {phrase}")
        for phrase in skill_cfg.get("outputMustNotContain", []):
            if contains_unnegated_phrase(final_output, str(phrase), config):
                problems.append(f"[{skill_name}] final output contains forbidden phrase: {phrase}")
        for pattern in skill_cfg.get("outputMustMatchRegex", []):
            try:
                if not re.search(str(pattern), final_output, re.MULTILINE):
                    problems.append(f"[{skill_name}] final output does not match regex: {pattern}")
            except re.error as exc:
                problems.append(f"[{skill_name}] invalid config regex {pattern}: {exc}")

    phase_gates = config.get("phaseGates", {}) if isinstance(config.get("phaseGates", {}), dict) else {}
    phase_gate = phase_gates.get(phase, {}) if isinstance(phase_gates.get(phase, {}), dict) else {}
    for phrase in phase_gate.get("requiredFinalPhrases", []):
        if str(phrase) not in final_output:
            problems.append(f"[{phase}] final output missing required phrase: {phrase}")

    transitions = config.get("phaseTransitions", {}) if isinstance(config.get("phaseTransitions", {}), dict) else {}
    browser_transition = transitions.get("browser-validation", {}) if isinstance(transitions.get("browser-validation", {}), dict) else {}
    if phase == "browser-validation" and browser_transition.get("requiresUserConfirmation"):
        if not state.get("browserValidationConfirmed"):
            problems.append("[browser-validation] missing user-originated confirmation evidence")
        phrase = str(browser_transition.get("confirmationPhrase", "用户确认进入浏览器验证"))
        if phrase not in final_output:
            problems.append("[browser-validation] missing user confirmation evidence")
    return problems


def stop_failure_lines(
    missing_reads: dict[str, list[str]],
    output_problems: list[str],
    artifact_problems: list[str],
) -> list[str]:
    lines = [
        "Skill Gate / 门禁三失败：继续本轮，不要结束。",
        "你必须补齐技能读取证据并修正最终方案。",
        "",
    ]
    repair_steps: list[str] = []

    if missing_reads:
        lines.append("缺失的必读技能文件：")
        for skill_name, files in missing_reads.items():
            lines.append(f"- {skill_name}")
            for file_path in files:
                lines.append(f"  - 读取：{file_path}")
        lines.append("")
        repair_steps.append("读取缺失的 SKILL.md / references 文件")

    if output_problems:
        lines.append("最终方案未满足技能验收规则：")
        for problem in output_problems:
            lines.append(f"- {problem}")
        lines.append("")
        repair_steps.extend([
            "按技能规则修改方案",
            "最终回答添加 `技能使用证据` 小节",
            "明确列出读取文件、应用规则和验证证据",
        ])

    if artifact_problems:
        lines.append("阶段产物未满足门禁规则：")
        for problem in artifact_problems:
            lines.append(f"- {problem}")
        lines.append("")
        repair_steps.append("补齐阶段 required artifact")

    if repair_steps:
        lines.append("修复要求：")
        for index, step in enumerate(dict.fromkeys(repair_steps), start=1):
            lines.append(f"{index}. {step}；")
    return lines


def compact_available(available: dict[str, dict[str, Any]]) -> list[dict[str, str]]:
    return [
        {"name": v.get("name", ""), "description": v.get("description", ""), "path": v.get("path", "")}
        for v in available.values()
    ]


def handle_user_prompt_submit(root: Path, payload: dict[str, Any], config: dict[str, Any], project_root: Path, cwd: Path, available: dict[str, dict[str, Any]]) -> dict[str, Any]:
    prompt = get_prompt(payload)
    anti_patterns = anti_pattern_guidance(project_root, config)
    harness_activated = is_harness_activated(prompt, config)
    phase = detect_phase(prompt) if harness_activated else "unknown"
    browser_confirmed = browser_validation_confirmed(prompt)
    required, matched_rules = select_required_skills(prompt, config, available)
    required_files = required_files_for(required, config, available, project_root)

    state = {
        "sessionId": payload.get("session_id", ""),
        "turnId": payload.get("turn_id", ""),
        "projectRoot": str(project_root),
        "cwd": str(cwd),
        "requiredSkills": required,
        "phase": phase,
        "browserValidationConfirmed": browser_confirmed,
        "harnessActivated": harness_activated,
        "matchedRules": matched_rules,
        "requiredFiles": required_files,
        "readEvidence": {},
        "stopBlockCount": 0,
        "events": [
            {"timestamp": utc_now(), "hook": "UserPromptSubmit", "requiredSkills": required, "matchedRules": matched_rules}
        ],
    }
    save_state(root, payload, state)

    report = {
        "timestamp": utc_now(),
        "hook": "UserPromptSubmit",
        "requiredSkills": required,
        "phase": phase,
        "browserValidationConfirmed": browser_confirmed,
        "harnessActivated": harness_activated,
        "matchedRules": matched_rules,
        "requiredFiles": required_files,
        "availableSkills": compact_available(available),
    }
    write_json(root / "hook-logs" / "latest-skill-gate-report.json", report)
    append_jsonl(root / "hook-logs" / "skill-gate-events.jsonl", report)

    if not required:
        context_lines = anti_patterns + [
            "Skill gate: no required skill matched this prompt. Continue normally.",
        ]
        return {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": "\n".join(context_lines),
            }
        }

    lines = anti_patterns + [
        "Skill Gate / 门禁一：本轮任务命中了必读技能。",
        "在输出最终方案前，必须读取并应用以下技能文件；不要只凭技能名或 description 产出方案。",
        "",
    ]
    for skill_name, file_paths in required_files.items():
        lines.append(f"- {skill_name}")
        for file_path in file_paths:
            lines.append(f"  - {file_path}")
    lines.extend([
        "",
        f"检测到阶段：{phase}",
        "最终回答必须包含 `技能使用证据` 小节，列出：",
        "1. 已读取的技能文件；",
        "2. 哪些技能规则影响了方案；",
        "3. 方案如何满足这些规则；",
        "4. 已执行或应执行的验证。",
    ])
    lines.extend(acceptance_guidance(config, required, phase))
    lines.extend(phase_artifact_guidance(config, phase))
    if phase == "browser-validation":
        lines.extend([
            "",
            "浏览器验证是显式阶段：进入浏览器验证前必须告知用户并等待确认。",
            "最终输出必须包含：用户确认进入浏览器验证。",
        ])

    return {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": "\n".join(lines),
        }
    }


def handle_post_tool_use(root: Path, payload: dict[str, Any], config: dict[str, Any], project_root: Path, cwd: Path, available: dict[str, dict[str, Any]]) -> dict[str, Any]:
    state = load_state(root, payload)
    text = collect_post_tool_text(payload)
    update_read_evidence_from_text(state, text, "PostToolUse", config, available, project_root)
    state.setdefault("events", []).append({
        "timestamp": utc_now(),
        "hook": "PostToolUse",
        "toolName": payload.get("tool_name", ""),
    })
    save_state(root, payload, state)

    report = {
        "timestamp": utc_now(),
        "hook": "PostToolUse",
        "toolName": payload.get("tool_name", ""),
        "requiredSkills": state.get("requiredSkills", []),
        "readEvidence": state.get("readEvidence", {}),
    }
    write_json(root / "hook-logs" / "latest-skill-gate-report.json", report)
    append_jsonl(root / "hook-logs" / "skill-gate-events.jsonl", report)

    # PostToolUse stdout JSON is accepted; keep it concise.
    return {
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": "Skill gate: updated observable skill-read evidence.",
        }
    }


def handle_stop(root: Path, payload: dict[str, Any], config: dict[str, Any], project_root: Path, cwd: Path, available: dict[str, dict[str, Any]]) -> dict[str, Any]:
    state = load_state(root, payload)

    if config.get("acceptTranscriptEvidence", True):
        update_read_evidence_from_text(state, read_transcript(payload), "transcript_path", config, available, project_root)

    final_output = get_last_assistant_message(payload)
    if config.get("acceptFinalClaimAsEvidence", False):
        update_read_evidence_from_text(state, final_output, "last_assistant_message", config, available, project_root)

    state["skillReceipts"] = build_skill_receipts(state)
    missing_reads = missing_required_reads(state, config, available, project_root)
    output_problems = validate_final_output(final_output, state, config)
    artifact_problems = validate_phase_artifacts(project_root, state, config)

    report = {
        "timestamp": utc_now(),
        "hook": "Stop",
        "requiredSkills": state.get("requiredSkills", []),
        "phase": state.get("phase", "unknown"),
        "requiredFiles": state.get("requiredFiles", {}),
        "readEvidence": state.get("readEvidence", {}),
        "skillReceipts": state.get("skillReceipts", []),
        "missingReads": missing_reads,
        "outputProblems": output_problems,
        "artifactProblems": artifact_problems,
        "stopHookActive": payload.get("stop_hook_active", False),
        "stopBlockCount": state.get("stopBlockCount", 0),
    }
    write_json(root / "hook-logs" / "latest-skill-gate-report.json", report)
    append_jsonl(root / "hook-logs" / "skill-gate-events.jsonl", report)

    state.setdefault("events", []).append({
        "timestamp": utc_now(),
        "hook": "Stop",
        "missingReads": missing_reads,
        "outputProblems": output_problems,
        "artifactProblems": artifact_problems,
    })

    has_required = bool(state.get("requiredSkills", []))
    has_phase_gate = state.get("phase", "unknown") != "unknown"
    failed = (has_required or has_phase_gate) and (bool(missing_reads) or bool(output_problems) or bool(artifact_problems))

    if failed:
        already_continued = bool(payload.get("stop_hook_active")) or int(state.get("stopBlockCount", 0)) >= 1
        state["stopBlockCount"] = int(state.get("stopBlockCount", 0)) + 1
        save_state(root, payload, state)

        if config.get("avoidInfiniteStopLoop", True) and already_continued and not missing_reads and not artifact_problems:
            # Stop hooks only emit JSON when they actively block. Returning an
            # event-specific informational payload here makes Codex treat stdout
            # as an invalid Stop hook response.
            return {}

        lines = stop_failure_lines(missing_reads, output_problems, artifact_problems)
        return {"decision": "block", "reason": "\n".join(lines)}

    save_state(root, payload, state)
    # A passing Stop hook should be silent. Codex validates Stop stdout against
    # the Stop-specific schema, so UserPromptSubmit/PostToolUse payloads such as
    # hookSpecificOutput are invalid here.
    return {}


def main() -> int:
    root = hook_root()
    payload = parse_payload()
    hook = event_name(payload)
    cwd = Path(str(payload.get("cwd") or os.getcwd())).resolve()
    project_root = project_root_from_payload(payload)
    config = load_config(root)
    available = scan_available_skills(project_root, cwd)

    append_jsonl(root / "hook-logs" / "skill-gate-debug.jsonl", {
        "timestamp": utc_now(),
        "hook": hook,
        "cwd": str(cwd),
        "projectRoot": str(project_root),
        "payloadKeys": sorted(payload.keys()),
        "availableSkillNames": list(available.keys()),
    })

    if hook == "UserPromptSubmit":
        result = handle_user_prompt_submit(root, payload, config, project_root, cwd, available)
    elif hook == "PostToolUse":
        result = handle_post_tool_use(root, payload, config, project_root, cwd, available)
    elif hook == "Stop":
        result = handle_stop(root, payload, config, project_root, cwd, available)
    else:
        result = {}

    if result:
        print(stdout_json(result))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        try:
            root = hook_root()
            append_jsonl(root / "hook-logs" / "skill-gate-errors.jsonl", {
                "timestamp": utc_now(),
                "error": sanitize_text(str(exc)),
            })
        finally:
            # Hooks should not break Codex if the audit script itself fails.
            raise SystemExit(0)
