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

Write-Host "[1/5] Config parses"
Get-Content $config -Raw -Encoding UTF8 | ConvertFrom-Json | Out-Null

Write-Host "[2/5] Schemas parse"
Get-ChildItem .codex\harness\schema\*.json | ForEach-Object {
  Get-Content $_ -Raw -Encoding UTF8 | ConvertFrom-Json | Out-Null
}

Write-Host "[3/5] Example artifacts parse"
Get-Content .codex\harness\examples\pass\traceability.json -Raw -Encoding UTF8 | ConvertFrom-Json | Out-Null
Get-Content .codex\harness\examples\fail\traceability-missing-rule.json -Raw -Encoding UTF8 | ConvertFrom-Json | Out-Null

Write-Host "[4/5] Hook governance functions"
$env:PYTHONDONTWRITEBYTECODE = "1"
python3 scripts\test_harness_governance.py
if ($LASTEXITCODE -ne 0) {
  Write-Error "Python function checks failed with exit code $LASTEXITCODE"
}

Write-Host "[5/5] Existing local hook smoke"
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\test-local.ps1

Write-Host "PASS: Harness governance smoke checks completed."
