# log-event.ps1 - PostToolUse hook (ai-control-kit)
# Appends one JSONL line per mutating tool call to .ai-control/ledger/events-YYYYMM.jsonl.
# Never blocks anything; swallows its own errors.

try {
  $reader = New-Object System.IO.StreamReader([Console]::OpenStandardInput(), (New-Object System.Text.UTF8Encoding($false)))
  $raw = $reader.ReadToEnd()
  if (-not $raw) { exit 0 }
  $j = $raw | ConvertFrom-Json

  $aiDir = Split-Path $PSScriptRoot -Parent
  $ledger = Join-Path $aiDir "ledger"
  if (-not (Test-Path $ledger)) { New-Item -ItemType Directory -Path $ledger -Force | Out-Null }
  $file = Join-Path $ledger ("events-" + (Get-Date -Format "yyyyMM") + ".jsonl")

  $target = $j.tool_input.file_path
  if (-not $target) { $target = $j.tool_input.notebook_path }
  if (-not $target) {
    $c = [string]$j.tool_input.command
    if ($c) {
      if ($c.Length -gt 200) { $c = $c.Substring(0, 200) + "..." }
      $target = $c
    }
  }

  $task = ""
  $af = Join-Path $aiDir "ACTIVE_TASK"
  if (Test-Path $af) { $task = [string](Get-Content $af -TotalCount 1) }

  $rec = @{
    ts      = (Get-Date).ToString("o")
    session = $j.session_id
    tool    = $j.tool_name
    target  = $target
    task    = $task
    cwd     = $j.cwd
  }
  Add-Content -Path $file -Value ($rec | ConvertTo-Json -Compress) -Encoding UTF8
  exit 0
}
catch { exit 0 }
