# ai-task.ps1 - file-first AI task control (ai-control-kit)
# PowerShell 5.1 compatible. Lives in <repo>/.ai-control/bin/.
#
# Usage:
#   ai-task.ps1 new -Title "..." [-Worker claude-code] [-Risk low|medium|high] [-TimeCapMinutes 60]
#   ai-task.ps1 start    -Id T-YYYYMMDD-NNN     (create worktree + branch, mark in_progress)
#   ai-task.ps1 evidence -Id T-YYYYMMDD-NNN     (collect diff/tests/handoff, mark needs_review)
#   ai-task.ps1 status                          (table of all tasks)
#   ai-task.ps1 set-status -Id T-... -To approved
#   ai-task.ps1 merge    -Id T-...              (human act: merge task branch into base)
#   ai-task.ps1 abandon  -Id T-...

param(
  [Parameter(Position=0)][string]$Command = "status",
  [string]$Id,
  [string]$Title,
  [string]$Worker = "",
  [string]$Risk = "low",
  [string]$To,
  [int]$TimeCapMinutes = 60
)

$ErrorActionPreference = "Stop"
try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch {}

$Root       = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$AiDir      = Join-Path $Root ".ai-control"
$TasksDir   = Join-Path $AiDir "tasks"
$ActiveFile = Join-Path $AiDir "ACTIVE_TASK"
$ValidStates = @("draft","in_progress","needs_review","fix_requested","approved","merged","abandoned")

function Invoke-Git([string[]]$GitArgs) {
  $prev = $ErrorActionPreference
  $ErrorActionPreference = "Continue"
  $out = & git @GitArgs 2>$null
  $code = $LASTEXITCODE
  $ErrorActionPreference = $prev
  return @{ Out = $out; Code = $code }
}

function Read-Packet([string]$TaskId) {
  $dir = Join-Path $TasksDir $TaskId
  $packetPath = Join-Path $dir "packet.md"
  if (-not (Test-Path $packetPath)) { throw "packet not found: $packetPath" }
  $lines = Get-Content $packetPath -Encoding UTF8
  if ($lines[0].Trim() -ne "---") { throw "no frontmatter in $packetPath" }
  $fm = @{}
  for ($i = 1; $i -lt $lines.Count; $i++) {
    if ($lines[$i].Trim() -eq "---") { break }
    $idx = $lines[$i].IndexOf(":")
    if ($idx -gt 0) {
      $k = $lines[$i].Substring(0, $idx).Trim()
      $v = $lines[$i].Substring($idx + 1).Trim().Trim('"')
      $fm[$k] = $v
    }
  }
  return @{ Path = $packetPath; Fm = $fm; Dir = $dir }
}

function Set-PacketField([string]$PacketPath, [string]$Key, [string]$Value) {
  $raw = Get-Content $PacketPath -Raw -Encoding UTF8
  $pattern = "(?m)^" + [regex]::Escape($Key) + ":.*$"
  if ($raw -notmatch $pattern) { throw "field '$Key' not found in packet" }
  $raw = [regex]::Replace($raw, $pattern, ($Key + ": " + $Value))
  $raw = [regex]::Replace($raw, "(?m)^updated:.*$", ("updated: " + (Get-Date -Format "yyyy-MM-dd")))
  [System.IO.File]::WriteAllText($PacketPath, $raw, (New-Object System.Text.UTF8Encoding($true)))
}

function New-Task {
  if (-not $Title) { throw "need -Title" }
  if (-not (Test-Path $TasksDir)) { New-Item -ItemType Directory -Path $TasksDir -Force | Out-Null }
  $date = Get-Date -Format "yyyyMMdd"
  $existing = @(Get-ChildItem $TasksDir -Directory -ErrorAction SilentlyContinue | Where-Object { $_.Name -like ("T-" + $date + "-*") })
  $taskId = "T-" + $date + "-" + ("{0:d3}" -f ($existing.Count + 1))
  $dir = Join-Path $TasksDir $taskId
  New-Item -ItemType Directory -Path $dir -Force | Out-Null

  $base = ""
  $r = Invoke-Git @("-C", $Root, "symbolic-ref", "--short", "HEAD")
  if ($r.Code -eq 0) { $base = ($r.Out | Select-Object -First 1) }
  if (-not $base) { $base = "main" }

  $w = $Worker
  if (-not $w) {
    $w = "claude-code"
    $py = Join-Path $AiDir "project.yaml"
    if (Test-Path $py) {
      $m = Select-String -Path $py -Pattern "^default_worker:\s*(\S+)" | Select-Object -First 1
      if ($m) { $w = $m.Matches[0].Groups[1].Value }
    }
  }

  $tpl = Get-Content (Join-Path $AiDir "templates\packet.md") -Raw -Encoding UTF8
  $tpl = $tpl.Replace("{{ID}}", $taskId).Replace("{{TITLE}}", $Title)
  $tpl = $tpl.Replace("{{WORKER}}", $w).Replace("{{RISK}}", $Risk)
  $tpl = $tpl.Replace("{{DATE}}", (Get-Date -Format "yyyy-MM-dd"))
  $tpl = $tpl.Replace("{{TIMECAP}}", [string]$TimeCapMinutes).Replace("{{BASE}}", $base)
  $packetPath = Join-Path $dir "packet.md"
  [System.IO.File]::WriteAllText($packetPath, $tpl, (New-Object System.Text.UTF8Encoding($true)))

  Write-Host ("created: " + $packetPath)
  Write-Host "next: fill in the packet (goal / scope / acceptance / test_command),"
  Write-Host ("      then: ai-task.ps1 start -Id " + $taskId)
}

function Start-Task {
  if (-not $Id) { throw "need -Id" }
  $t = Read-Packet $Id
  $r = Invoke-Git @("-C", $Root, "rev-parse", "--is-inside-work-tree")
  if ($r.Code -ne 0) { throw ("not a git repo: " + $Root + "  (git init + first commit, then retry)") }
  $base = $t.Fm["base_branch"]
  $r = Invoke-Git @("-C", $Root, "rev-parse", "--verify", $base)
  if ($r.Code -ne 0) { throw ("base branch '" + $base + "' not found") }

  $repoName = Split-Path $Root -Leaf
  $wtBase = Join-Path (Split-Path $Root -Parent) ($repoName + ".worktrees")
  if (-not (Test-Path $wtBase)) { New-Item -ItemType Directory -Path $wtBase -Force | Out-Null }
  $wt = Join-Path $wtBase $Id
  $branch = "task/" + $Id

  $r = Invoke-Git @("-C", $Root, "worktree", "add", $wt, "-b", $branch, $base)
  if ($r.Code -ne 0) { throw ("git worktree add failed (exit " + $r.Code + "). branch or worktree may already exist.") }

  Copy-Item $t.Path (Join-Path $wt "TASK_PACKET.md") -Force
  Set-Content -Path (Join-Path $wt "HANDOFF.md") -Value "# HANDOFF (AI fills this before stopping)" -Encoding UTF8

  Set-PacketField $t.Path "status" "in_progress"
  Set-PacketField $t.Path "worktree" ('"' + $wt + '"')
  Set-Content -Path $ActiveFile -Value $Id -Encoding ASCII

  Write-Host ("worktree: " + $wt)
  Write-Host ("branch:   " + $branch + "  (from " + $base + ")")
  Write-Host "next: open your AI tool INSIDE the worktree."
  Write-Host "      the task spec is TASK_PACKET.md at the worktree root."
}

function Collect-Evidence {
  if (-not $Id) { throw "need -Id" }
  $t = Read-Packet $Id
  $wt = $t.Fm["worktree"]
  if (-not $wt -or -not (Test-Path $wt)) { throw ("worktree not found for " + $Id + ". run start first.") }
  $base = $t.Fm["base_branch"]
  $stamp = Get-Date -Format "yyyyMMdd-HHmmss"
  $ev = Join-Path $t.Dir ("evidence\" + $stamp)
  New-Item -ItemType Directory -Path $ev -Force | Out-Null

  $diff    = Invoke-Git @("-C", $wt, "diff", $base)
  $stat    = Invoke-Git @("-C", $wt, "diff", "--stat", $base)
  $status  = Invoke-Git @("-C", $wt, "status", "--porcelain")
  $commits = Invoke-Git @("-C", $wt, "log", "--oneline", ($base + "..HEAD"))
  $head    = Invoke-Git @("-C", $wt, "rev-parse", "HEAD")
  Set-Content (Join-Path $ev "diff.patch")  -Value (($diff.Out    | Out-String)) -Encoding UTF8
  Set-Content (Join-Path $ev "status.txt")  -Value (($status.Out  | Out-String)) -Encoding UTF8
  Set-Content (Join-Path $ev "commits.txt") -Value (($commits.Out | Out-String)) -Encoding UTF8

  $handoff = Join-Path $wt "HANDOFF.md"
  if (Test-Path $handoff) { Copy-Item $handoff (Join-Path $ev "handoff.md") -Force }

  $testCmd = $t.Fm["test_command"]
  $testExit = $null
  if ($testCmd) {
    $prev = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    Push-Location $wt
    $testOut = & cmd.exe /d /c $testCmd 2>&1 | Out-String
    $testExit = $LASTEXITCODE
    Pop-Location
    $ErrorActionPreference = $prev
    Set-Content (Join-Path $ev "test-output.txt") -Value $testOut -Encoding UTF8
  } else {
    Set-Content (Join-Path $ev "test-output.txt") -Value "(no test_command in packet)" -Encoding UTF8
  }

  $glNote = "(gitleaks not installed - skipped)"
  if (Get-Command gitleaks -ErrorAction SilentlyContinue) {
    $prev = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    $glOut = & gitleaks detect --source $wt --no-banner 2>&1 | Out-String
    $glExit = $LASTEXITCODE
    $ErrorActionPreference = $prev
    if ($glExit -eq 0) { $glNote = "OK - no leaks found`r`n" + $glOut } else { $glNote = "WARNING - gitleaks exit " + $glExit + "`r`n" + $glOut }
  }
  Set-Content (Join-Path $ev "gitleaks.txt") -Value $glNote -Encoding UTF8

  $meta = @{
    id = $Id
    collected = (Get-Date).ToString("o")
    base = $base
    head = (($head.Out | Select-Object -First 1))
    test_command = $testCmd
    test_exit = $testExit
  }
  Set-Content (Join-Path $ev "meta.json") -Value ($meta | ConvertTo-Json) -Encoding UTF8

  Set-PacketField $t.Path "status" "needs_review"
  Write-Host ("evidence -> " + $ev)
  Write-Host ("diffstat:")
  Write-Host (($stat.Out | Out-String))
  if ($null -ne $testExit) {
    if ($testExit -eq 0) { Write-Host "tests: PASS (exit 0)" } else { Write-Host ("tests: FAIL (exit " + $testExit + ")") }
  } else { Write-Host "tests: (none defined)" }
  Write-Host ("status -> needs_review. review the evidence, then approve or request fixes:")
  Write-Host ("  ai-task.ps1 set-status -Id " + $Id + " -To approved   (or fix_requested)")
}

function Show-Status {
  $rows = @()
  $dirs = @(Get-ChildItem $TasksDir -Directory -ErrorAction SilentlyContinue)
  foreach ($d in $dirs) {
    try { $t = Read-Packet $d.Name } catch { continue }
    $rows += New-Object PSObject -Property @{
      Id = $t.Fm["id"]; Status = $t.Fm["status"]; Worker = $t.Fm["worker"]
      Risk = $t.Fm["risk"]; Updated = $t.Fm["updated"]; Title = $t.Fm["title"]
    }
  }
  if ($rows.Count -eq 0) { Write-Host "(no tasks yet - ai-task.ps1 new -Title '...')"; return }
  $rows | Sort-Object Id | Format-Table Id, Status, Worker, Risk, Updated, Title -AutoSize | Out-String | Write-Host
  if (Test-Path $ActiveFile) { Write-Host ("ACTIVE_TASK: " + (Get-Content $ActiveFile -TotalCount 1)) }
}

function Set-TaskStatus {
  if (-not $Id -or -not $To) { throw "need -Id and -To" }
  if ($ValidStates -notcontains $To) { throw ("invalid state '" + $To + "'. valid: " + ($ValidStates -join ", ")) }
  $t = Read-Packet $Id
  Set-PacketField $t.Path "status" $To
  Write-Host ($Id + " -> " + $To)
}

function Merge-Task {
  if (-not $Id) { throw "need -Id" }
  $t = Read-Packet $Id
  if ($t.Fm["status"] -ne "approved") {
    throw ("status is '" + $t.Fm["status"] + "'. human review first: ai-task.ps1 set-status -Id " + $Id + " -To approved")
  }
  $base = $t.Fm["base_branch"]
  $cur = Invoke-Git @("-C", $Root, "symbolic-ref", "--short", "HEAD")
  $curBranch = ($cur.Out | Select-Object -First 1)
  if ($curBranch -ne $base) { throw ("main checkout is on '" + $curBranch + "', switch to '" + $base + "' first") }
  $r = Invoke-Git @("-C", $Root, "merge", "--no-ff", "--no-edit", ("task/" + $Id))
  if ($r.Code -ne 0) { throw ("merge failed (exit " + $r.Code + ") - resolve manually. output: " + ($r.Out | Out-String)) }
  Set-PacketField $t.Path "status" "merged"
  if ((Test-Path $ActiveFile) -and ((Get-Content $ActiveFile -TotalCount 1) -eq $Id)) { Remove-Item $ActiveFile -Force }
  Write-Host ("merged task/" + $Id + " into " + $base)
  Write-Host "cleanup (optional, run yourself):"
  Write-Host ('  git -C "' + $Root + '" worktree remove "' + $t.Fm["worktree"] + '"')
  Write-Host ("  git -C `"" + $Root + "`" branch -d task/" + $Id)
}

function Abandon-Task {
  if (-not $Id) { throw "need -Id" }
  $t = Read-Packet $Id
  Set-PacketField $t.Path "status" "abandoned"
  if ((Test-Path $ActiveFile) -and ((Get-Content $ActiveFile -TotalCount 1) -eq $Id)) { Remove-Item $ActiveFile -Force }
  Write-Host ($Id + " -> abandoned")
  Write-Host "cleanup (optional, run yourself):"
  Write-Host ('  git -C "' + $Root + '" worktree remove --force "' + $t.Fm["worktree"] + '"')
  Write-Host ("  git -C `"" + $Root + "`" branch -D task/" + $Id)
}

switch ($Command) {
  "new"        { New-Task }
  "start"      { Start-Task }
  "evidence"   { Collect-Evidence }
  "status"     { Show-Status }
  "set-status" { Set-TaskStatus }
  "merge"      { Merge-Task }
  "abandon"    { Abandon-Task }
  default {
    Write-Host "unknown command. usage:"
    Write-Host "  ai-task.ps1 new -Title '...' [-Worker w] [-Risk r] [-TimeCapMinutes n]"
    Write-Host "  ai-task.ps1 start|evidence|merge|abandon -Id T-YYYYMMDD-NNN"
    Write-Host "  ai-task.ps1 set-status -Id T-... -To <state>"
    Write-Host "  ai-task.ps1 status"
    Write-Host ("  states: " + ($ValidStates -join " > "))
  }
}
