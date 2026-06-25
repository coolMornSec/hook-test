$ErrorActionPreference = "Stop"
$report = Join-Path (Get-Location) ".codex\hook-logs\latest-skill-gate-report.json"
$state = Join-Path (Get-Location) ".codex\hook-state\skill-gate\latest.json"

if (Test-Path $report) {
  Write-Host "===== latest-skill-gate-report.json ====="
  Get-Content $report -Raw
} else {
  Write-Host "No report found: $report"
}

if (Test-Path $state) {
  Write-Host "===== latest state ====="
  Get-Content $state -Raw
} else {
  Write-Host "No state found: $state"
}
