$ErrorActionPreference = "Stop"
$OutputEncoding = [System.Text.UTF8Encoding]::new($false)
[Console]::OutputEncoding = $OutputEncoding

$root = Get-Location
$hook = Join-Path $root ".codex\hooks\skill_gate.py"
$configPath = Join-Path $root ".codex\skill-gate.config.json"

if (-not (Test-Path $hook)) {
  Write-Error "Cannot find hook: $hook. Run this script from the project root."
}

if (-not (Test-Path $configPath)) {
  Write-Error "Cannot find config: $configPath. Run this script from the project root."
}

$config = Get-Content $configPath -Raw -Encoding UTF8 | ConvertFrom-Json

Write-Host "[1/3] UserPromptSubmit"
$userPayload = @{
  session_id = "local-test-session"
  turn_id = "local-test-turn"
  transcript_path = ""
  cwd = $root.Path
  hook_event_name = "UserPromptSubmit"
  model = "gpt-5.5"
  permission_mode = "default"
  prompt = "Design a Harness skill gate for AI 开发 技能治理 with independent 子agent review."
} | ConvertTo-Json -Depth 20
$userPayload | python3 $hook

Write-Host "[2/3] PostToolUse - observed skill read evidence"
$skillReferencePath = Join-Path $root "skills\skill-reference-governance\SKILL.md"
$artifactReviewPath = Join-Path $root "skills\artifact-review-governance\SKILL.md"
$skillReferenceContent = Get-Content $skillReferencePath -Raw -Encoding UTF8
$artifactReviewContent = Get-Content $artifactReviewPath -Raw -Encoding UTF8
$postPayload = @{
  session_id = "local-test-session"
  turn_id = "local-test-turn"
  transcript_path = ""
  cwd = $root.Path
  hook_event_name = "PostToolUse"
  model = "gpt-5.5"
  permission_mode = "default"
  tool_name = "Bash"
  tool_input = @{
    command = "Get-Content skills\skill-reference-governance\SKILL.md; Get-Content skills\artifact-review-governance\SKILL.md"
  }
  tool_response = @{
    output = @"
$skillReferencePath
$skillReferenceContent
$artifactReviewPath
$artifactReviewContent
"@
  }
} | ConvertTo-Json -Depth 20
$postPayload | python3 $hook

Write-Host "[3/3] Stop - fake final answer"
$mustContain = @()
$mustContain += $config.skills.'skill-reference-governance'.outputMustContain
$mustContain += $config.skills.'artifact-review-governance'.outputMustContain
$finalLines = @()
$finalLines += "## Plan"
$finalLines += ($mustContain -join " ")
$finalLines += ""
$finalLines += "## $($config.evidenceSectionTitle)"
$finalLines += "- Read skill-reference-governance/SKILL.md"
$finalLines += "- Read artifact-review-governance/SKILL.md"

$stopPayload = @{
  session_id = "local-test-session"
  turn_id = "local-test-turn"
  transcript_path = ""
  cwd = $root.Path
  hook_event_name = "Stop"
  model = "gpt-5.5"
  permission_mode = "default"
  stop_hook_active = $false
  last_assistant_message = ($finalLines -join "`n")
} | ConvertTo-Json -Depth 20
$stopPayload | python3 $hook

Write-Host "Done. Report: .codex\hook-logs\latest-skill-gate-report.json"
