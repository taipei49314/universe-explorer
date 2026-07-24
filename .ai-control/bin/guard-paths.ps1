# guard-paths.ps1 - PreToolUse hook (ai-control-kit)
# Blocks writes to forbidden paths and forbidden shell commands.
# Reads hook JSON from stdin. Exit 2 = block (stderr shown to the AI). Fail-open on internal errors.

try {
  $reader = New-Object System.IO.StreamReader([Console]::OpenStandardInput(), (New-Object System.Text.UTF8Encoding($false)))
  $raw = $reader.ReadToEnd()
  if (-not $raw) { exit 0 }
  $j = $raw | ConvertFrom-Json

  $polPath = Join-Path (Split-Path $PSScriptRoot -Parent) "policies.json"
  if (-not (Test-Path $polPath)) { exit 0 }
  $pol = Get-Content $polPath -Raw -Encoding UTF8 | ConvertFrom-Json

  $tool = $j.tool_name

  if (@("Write", "Edit", "NotebookEdit") -contains $tool) {
    $p = $j.tool_input.file_path
    if (-not $p) { $p = $j.tool_input.notebook_path }
    if (-not $p) { exit 0 }
    $norm = ($p -replace "/", "\")
    $norm = [regex]::Replace($norm, "\\{2,}", "\")
    foreach ($a in $pol.allowed_write_overrides) {
      if ($norm -like $a) { exit 0 }
    }
    foreach ($f in $pol.forbidden_write_paths) {
      if ($norm -like $f) {
        [Console]::Error.WriteLine("ai-control guard: write BLOCKED by policy pattern '$f' -> $p  (see .ai-control/policies.md)")
        exit 2
      }
    }
  }
  elseif ($tool -eq "Bash") {
    $cmd = [string]$j.tool_input.command
    if ($cmd) {
      foreach ($pat in $pol.forbidden_command_patterns) {
        if ($cmd -match $pat) {
          [Console]::Error.WriteLine("ai-control guard: command BLOCKED by policy pattern '$pat'. Merge/push/reset on protected refs are HUMAN actions (see .ai-control/policies.md)")
          exit 2
        }
      }
    }
  }
  exit 0
}
catch {
  [Console]::Error.WriteLine("ai-control guard: internal error, failing open: $_")
  exit 0
}
