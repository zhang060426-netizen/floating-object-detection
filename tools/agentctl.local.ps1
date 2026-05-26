param(
  [Parameter(Position = 0)]
  [ValidateSet("status", "guard", "next", "dispatch", "watch-outbox", "write-prompts", "collect", "review", "verify-backend", "verify-frontend", "verify-docs", "verify-master", "init", "clean-omx")]
  [string]$Command = "status",

  [ValidateSet("planning", "read-only", "go", "implementation", "review", "evidence")]
  [string]$Stage = "read-only",

  [ValidatePattern('^[0-9]+$')]
  [string]$Step = "9",

  [ValidateSet("all", "control-plane", "backend", "frontend", "docs-test")]
  [string]$Role = "all",

  [ValidatePattern('^$|^[A-Za-z0-9][A-Za-z0-9._-]*$')]
  [string]$PromptSet = "",

  [switch]$Overwrite,
  [switch]$AcknowledgeWriteEffects,

  [Alias("ResultPath")]
  [string]$Path = "",

  [ValidateRange(0, 86400)]
  [int]$TimeoutSeconds = 0,

  [ValidateRange(1, 86400)]
  [int]$PollIntervalSeconds = 2
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
$Tasks = Join-Path $Root ".agent_tasks"
$StableTag = "phase2b-batch4-step8-local-workflow-stable"
$StableCommit = "3c00a1e"
$AuthorizedStep = "9"
$Step9AuthorizedBaseline = "5f21599"
$PlanningPath = "agent_outputs/docs/PHASE2B_BATCH4_STEP9_LOCAL_AGENT_ORCHESTRATION_V2_PLANNING.md"
$GoDecisionPath = "agent_outputs/docs/PHASE2B_BATCH4_STEP9_LOCAL_AGENT_ORCHESTRATION_V2_IMPLEMENTATION_GO_DECISION.md"
$ImplementationAllowlist = "tools/agentctl.local.ps1"

function Invoke-GitRead {
  param([Parameter(Mandatory = $true)][string[]]$Arguments)

  $output = & git -C $Root @Arguments 2>&1
  if ($LASTEXITCODE -ne 0) {
    throw "git $($Arguments -join ' ') failed: $($output -join [Environment]::NewLine)"
  }
  return (($output | ForEach-Object { [string]$_ }) -join [Environment]::NewLine).Trim()
}

function Get-GitValueOrEmpty {
  param([Parameter(Mandatory = $true)][string[]]$Arguments)

  $output = & git -C $Root @Arguments 2>$null
  if ($LASTEXITCODE -ne 0) { return "" }
  return (($output | ForEach-Object { [string]$_ }) -join [Environment]::NewLine).Trim()
}

function Test-GitAncestor {
  param([string]$Ancestor)

  & git -C $Root merge-base --is-ancestor $Ancestor HEAD 2>$null
  return ($LASTEXITCODE -eq 0)
}

function Test-TrackedAtHead {
  param([string]$Path)

  & git -C $Root cat-file -e "HEAD:$Path" 2>$null
  return ($LASTEXITCODE -eq 0)
}

function Get-LifecycleAuthority {
  $stableTarget = [string](Get-GitValueOrEmpty -Arguments @("rev-list", "-n", "1", $StableTag))
  $planningAtHead = Test-TrackedAtHead -Path $PlanningPath
  $goAtHead = Test-TrackedAtHead -Path $GoDecisionPath
  $planningText = if ($planningAtHead) { Get-GitValueOrEmpty -Arguments @("show", "HEAD:$PlanningPath") } else { "" }
  $goText = if ($goAtHead) { Get-GitValueOrEmpty -Arguments @("show", "HEAD:$GoDecisionPath") } else { "" }
  $planningContextPresent = $planningText.Contains("Step 9 implementation remains NOT AUTHORIZED until a later reviewed GO Decision.")
  $goAllowlistMatches = $goText.Contains("tools/agentctl.local.ps1 only")
  $goSafetyBoundariesPresent = ($goText -match 'Step 10:[^\r\n]*NOT AUTHORIZED') -and $goText.Contains("Optional outbox-only watch behavior is NOT AUTHORIZED")
  $authorizedBasePresent = Test-GitAncestor -Ancestor $Step9AuthorizedBaseline
  $stableMatches = (-not [string]::IsNullOrWhiteSpace($stableTarget)) -and $stableTarget.StartsWith($StableCommit, [System.StringComparison]::OrdinalIgnoreCase)
  $requestedStepMatches = ($Step -eq $AuthorizedStep)
  $implementationEligible = $requestedStepMatches -and $planningAtHead -and $planningContextPresent -and $goAtHead -and $goAllowlistMatches -and $goSafetyBoundariesPresent -and $authorizedBasePresent -and $stableMatches
  $observations = @()
  if (-not $requestedStepMatches) { $observations += "requested Step $Step does not match current tracked GO authority for Step $AuthorizedStep" }
  if (-not $planningAtHead) { $observations += "tracked Step 9 planning record missing at HEAD" }
  elseif (-not $planningContextPresent) { $observations += "tracked Step 9 planning lifecycle prerequisite is missing or conflicting" }
  if (-not $goAtHead) { $observations += "tracked Step 9 GO Decision missing at HEAD" }
  elseif (-not $goAllowlistMatches) { $observations += "tracked Step 9 GO Decision helper-only allowlist is missing or conflicting" }
  elseif (-not $goSafetyBoundariesPresent) { $observations += "tracked Step 9 GO Decision watch/Step 10 hard stops are missing or conflicting" }
  if (-not $authorizedBasePresent) { $observations += "merged Step 9 GO baseline $Step9AuthorizedBaseline is not an ancestor of HEAD" }
  if (-not $stableMatches) { $observations += "stable rollback tag is missing or does not target $StableCommit" }
  if (-not $requestedStepMatches) {
    $summary = "NO-GO: requested Step $Step does not match current tracked GO authority for Step $AuthorizedStep; no Step $Step implementation task or write scope is authorized."
    $eligibleNextGate = "Read-only only: Step $Step implementation is not authorized; return to separately gated Step $AuthorizedStep authority handling."
  } elseif ($implementationEligible) {
    $summary = "Step 9 merged GO authority is present; any separately assigned implementation is helper-only."
    $eligibleNextGate = "Separately assigned Step 9 helper-only implementation/review within $ImplementationAllowlist only; this display does not itself authorize a write."
  } else {
    $summary = "NO-GO/read-only: required Step 9 tracked/Git/tag authority is missing or conflicting."
    $eligibleNextGate = "Read-only reconciliation of missing/conflicting tracked authority before any implementation."
  }
  return [pscustomobject]@{
    StableTarget = $stableTarget
    AuthorizedStep = $AuthorizedStep
    RequestedStepMatches = $requestedStepMatches
    PlanningAtHead = $planningAtHead
    PlanningContextPresent = $planningContextPresent
    GoAtHead = $goAtHead
    GoAllowlistMatches = $goAllowlistMatches
    GoSafetyBoundariesPresent = $goSafetyBoundariesPresent
    AuthorizedBasePresent = $authorizedBasePresent
    StableMatches = $stableMatches
    ImplementationEligible = $implementationEligible
    Observations = $observations
    Summary = $summary
    EligibleNextGate = $eligibleNextGate
  }
}

function Get-NextStepText {
  $number = 0
  if ([int]::TryParse($Step, [ref]$number)) {
    return [string]($number + 1)
  }
  return "the next Step"
}

function Get-StagePolicy {
  param([Parameter(Mandatory = $true)][object]$Authority)

  switch ($Stage) {
    "planning" {
      return [pscustomobject]@{
        Label = "Planning"
        Allowed = "Prepare or review scoped planning only under an explicit planning assignment; do not implement."
        NextAction = "Submit planning for a separately reviewed gate decision; the requested planning view does not reopen a completed gate."
        HardStops = @("No implementation.", "No merge, tag or push.", "No Step 10 implementation.")
      }
    }
    "read-only" {
      return [pscustomobject]@{
        Label = "Read-only Scan"
        Allowed = "Inspect repository and tracked authority only; do not edit tracked files or produce write-producing verification effects."
        NextAction = "Return read-only findings to the Leader for an explicit gate; do not infer implementation authority from local results."
        HardStops = @("No implementation or implicit local task writes.", "Do not run write-producing verification as a read-only scan.", "No merge, tag, push or Step 10 implementation.")
      }
    }
    "go" {
      return [pscustomobject]@{
        Label = "GO Decision"
        Allowed = "Draft or review a tracked authorization decision only within separately assigned documentation scope."
        NextAction = "Require reviewed and merged tracked GO authority plus a separately issued implementation task before edits."
        HardStops = @("No implementation from a draft or local prompt.", "No automatic merge, tag or push.", "No Step 10 implementation.")
      }
    }
    "implementation" {
      $allowed = if ($Authority.ImplementationEligible) {
        "Only under a separately issued implementation task, edit the tracked allowlist: $ImplementationAllowlist."
      } else {
        "NO-GO for implementation: tracked/Git/tag authority is incomplete, conflicting or does not match requested Step $Step; use read-only reconciliation only."
      }
      $fileBoundary = if ($Authority.RequestedStepMatches) {
        "No file outside $ImplementationAllowlist."
      } else {
        "No implementation task or implementation file is authorized for requested Step $Step."
      }
      $nextAction = if ($Authority.ImplementationEligible) {
        "Return the isolated helper-only branch and disclosed validation evidence for separate Leader review."
      } else {
        "No implementation action is permitted for requested Step $Step; perform read-only reconciliation only."
      }
      return [pscustomobject]@{
        Label = "Implementation"
        Allowed = $allowed
        NextAction = $nextAction
        HardStops = @($fileBoundary, "No merge, tag, push, pane control or automatic lifecycle transition.", "No Step 10 implementation.")
      }
    }
    "review" {
      return [pscustomobject]@{
        Label = "Review"
        Allowed = "Review the authorized diff and recorded evidence only; review output does not approve, merge or widen implementation scope."
        NextAction = "Return review findings for a separately authorized evidence or lifecycle decision."
        HardStops = @("No silent implementation fixes.", "No automatic merge, tag or push.", "No Step 10 implementation.")
      }
    }
    "evidence" {
      return [pscustomobject]@{
        Label = "Evidence"
        Allowed = "Record only separately authorized evidence and explicitly disclosed local-only outputs; do not change implementation."
        NextAction = "Return evidence to the Leader for the next explicit decision gate."
        HardStops = @("No implementation changes.", "No automatic merge, tag or push.", "No Step 10 implementation.")
      }
    }
  }
}

function Get-RoleDefinitions {
  $definitions = @(
    [pscustomobject]@{ Id = "control-plane"; Name = "Control-Plane"; File = "control_plane.md"; Result = "control_plane_result.md" },
    [pscustomobject]@{ Id = "backend"; Name = "Backend"; File = "backend.md"; Result = "backend_result.md" },
    [pscustomobject]@{ Id = "frontend"; Name = "Frontend"; File = "frontend.md"; Result = "frontend_result.md" },
    [pscustomobject]@{ Id = "docs-test"; Name = "Docs-Test"; File = "docs.md"; Result = "docs_result.md" }
  )
  if ($Role -eq "all") { return $definitions }
  return @($definitions | Where-Object { $_.Id -eq $Role })
}

function Get-RoleScope {
  param([string]$RoleId, [Parameter(Mandatory = $true)][object]$Authority)

  switch ($Stage) {
    "implementation" {
      if ($RoleId -eq "control-plane" -and $Authority.ImplementationEligible) {
        return "Tracked implementation allowlist: $ImplementationAllowlist only. No other tracked implementation or local authority state is assigned."
      }
      return "NO-GO for tracked implementation in the $RoleId lane; report boundary observations only and do not edit application, documentation or runtime surfaces."
    }
    "read-only" { return "Read-only inspection and reporting only; no tracked edit or write-producing verification is assigned in this prompt." }
    "planning" { return "Planning analysis only when separately assigned; do not edit implementation artifacts or infer later authority." }
    "go" { return "GO Decision drafting/review only when separately assigned in tracked documentation scope; no helper or product implementation." }
    "review" { return "Review only the separately submitted authorized diff/evidence; do not silently fix or expand scope." }
    "evidence" { return "Evidence output only when separately assigned; no implementation or lifecycle transition is authorized." }
  }
}

function Get-RolePermittedAction {
  param([string]$RoleId, [object]$Policy, [Parameter(Mandatory = $true)][object]$Authority)

  if ($Stage -eq "implementation" -and $RoleId -ne "control-plane") {
    return "No implementation is assigned to this lane for Step 9 helper-only work; report NO-GO boundary observations only."
  }
  return $Policy.Allowed
}

function Get-InboxDirectory {
  $inbox = Join-Path $Tasks "inbox"
  if ([string]::IsNullOrWhiteSpace($PromptSet)) { return $inbox }
  return Join-Path $inbox $PromptSet
}

function Get-InboxDisplayPath {
  param([string]$FileName)

  if ([string]::IsNullOrWhiteSpace($PromptSet)) {
    return ".agent_tasks/inbox/$FileName"
  }
  return ".agent_tasks/inbox/$PromptSet/$FileName"
}

function Write-WatchOutcome {
  param(
    [Parameter(Mandatory = $true)][string]$Outcome,
    [Parameter(Mandatory = $true)][string]$Reason,
    [Parameter(Mandatory = $true)][int]$ExitCode
  )

  Write-Host "Outcome: $Outcome"
  Write-Host "Reason: $Reason"
  Write-Host "Authority: operational availability only; no PASS, GO, approval or lifecycle completion is inferred."
  Write-Host "Side effects: none; no collect/review, prompt dispatch, Agent run, OMX call, pane control, lifecycle transition, merge, tag or push."
  return $ExitCode
}

function Get-OutboxWatchPathState {
  param([Parameter(Mandatory = $true)][string]$LiteralPath)

  try {
    if (-not (Test-Path -LiteralPath $LiteralPath)) { return "MISSING" }
    if (Test-Path -LiteralPath $LiteralPath -PathType Leaf) { return "FILE" }
    return "WRONG_MATCH"
  } catch {
    return "READ_ERROR"
  }
}

function Watch-Outbox {
  Write-Host "== Passive Outbox Watch (read-only) =="
  Write-Host "Requested exact path: $(if ([string]::IsNullOrWhiteSpace($Path)) { '<not supplied>' } else { $Path })"
  Write-Host "TimeoutSeconds: $TimeoutSeconds"
  Write-Host "PollIntervalSeconds: $PollIntervalSeconds"

  if ([string]::IsNullOrWhiteSpace($Path)) {
    return (Write-WatchOutcome -Outcome "INVALID_PATH" -Reason "An explicit exact result path is required." -ExitCode 2)
  }
  if ($Path.IndexOfAny([char[]]"*?[]") -ge 0) {
    return (Write-WatchOutcome -Outcome "AMBIGUOUS" -Reason "Wildcard or matching syntax is not permitted; supply one exact result path." -ExitCode 2)
  }

  try {
    $candidate = if ([System.IO.Path]::IsPathRooted($Path)) {
      [System.IO.Path]::GetFullPath($Path)
    } else {
      [System.IO.Path]::GetFullPath((Join-Path $Root $Path))
    }
    $outboxRoot = [System.IO.Path]::GetFullPath((Join-Path $Tasks "outbox"))
  } catch {
    return (Write-WatchOutcome -Outcome "INVALID_PATH" -Reason "The requested result path cannot be normalized safely." -ExitCode 2)
  }

  $outboxPrefix = $outboxRoot.TrimEnd([char[]]"\/") + [System.IO.Path]::DirectorySeparatorChar
  if (-not $candidate.StartsWith($outboxPrefix, [System.StringComparison]::OrdinalIgnoreCase)) {
    return (Write-WatchOutcome -Outcome "INVALID_PATH" -Reason "The exact result path must be a descendant of .agent_tasks/outbox/." -ExitCode 2)
  }
  Write-Host "Resolved exact path: $candidate"

  $initialState = Get-OutboxWatchPathState -LiteralPath $candidate
  switch ($initialState) {
    "FILE" {
      return (Write-WatchOutcome -Outcome "STALE_OR_PREEXISTING" -Reason "The exact result file existed before passive observation began." -ExitCode 3)
    }
    "WRONG_MATCH" {
      return (Write-WatchOutcome -Outcome "WRONG_MATCH" -Reason "The exact target exists but is not a result file." -ExitCode 2)
    }
    "READ_ERROR" {
      return (Write-WatchOutcome -Outcome "READ_ERROR" -Reason "The exact target could not be inspected reliably." -ExitCode 2)
    }
  }

  if ($TimeoutSeconds -eq 0) {
    return (Write-WatchOutcome -Outcome "MISSING" -Reason "The exact result file is absent at the one-shot observation boundary." -ExitCode 4)
  }

  $deadline = [DateTime]::UtcNow.AddSeconds($TimeoutSeconds)
  while ($true) {
    $remainingMilliseconds = [int][Math]::Ceiling(($deadline - [DateTime]::UtcNow).TotalMilliseconds)
    if ($remainingMilliseconds -le 0) {
      return (Write-WatchOutcome -Outcome "TIMED_OUT" -Reason "The bounded wait expired before the exact result file appeared." -ExitCode 5)
    }

    $pollMilliseconds = [Math]::Min(($PollIntervalSeconds * 1000), $remainingMilliseconds)
    Start-Sleep -Milliseconds $pollMilliseconds
    if ([DateTime]::UtcNow -ge $deadline) {
      return (Write-WatchOutcome -Outcome "TIMED_OUT" -Reason "The bounded wait expired before the exact result file was observed." -ExitCode 5)
    }
    switch (Get-OutboxWatchPathState -LiteralPath $candidate) {
      "FILE" {
        return (Write-WatchOutcome -Outcome "OBSERVED" -Reason "The exact result file appeared after passive observation began and is available for manual inspection only." -ExitCode 0)
      }
      "WRONG_MATCH" {
        return (Write-WatchOutcome -Outcome "WRONG_MATCH" -Reason "The exact target appeared but is not a result file." -ExitCode 2)
      }
      "READ_ERROR" {
        return (Write-WatchOutcome -Outcome "READ_ERROR" -Reason "The exact target could not be inspected reliably." -ExitCode 2)
      }
    }
  }
}

function Show-Status {
  $authority = Get-LifecycleAuthority
  $branch = Invoke-GitRead -Arguments @("branch", "--show-current")
  $head = Invoke-GitRead -Arguments @("rev-parse", "HEAD")
  $changes = [string](Invoke-GitRead -Arguments @("status", "--porcelain=v1", "--untracked-files=all"))

  Write-Host "== Local Agent Orchestration Status (read-only) =="
  Write-Host "Repository: $Root"
  Write-Host "Branch: $branch"
  Write-Host "HEAD: $head"
  if ([string]::IsNullOrWhiteSpace($changes)) {
    Write-Host "Dirty status: CLEAN"
  } else {
    Write-Host "Dirty status: DIRTY"
    $changes -split "`r?`n" | ForEach-Object { Write-Host "  $_" }
  }
  Write-Host "Stable rollback tag: $StableTag -> $($authority.StableTarget) (expected prefix $StableCommit; match=$($authority.StableMatches))"
  Write-Host "Tracked Step 9 planning at HEAD / prerequisite matches: $($authority.PlanningAtHead) / $($authority.PlanningContextPresent)"
  Write-Host "Tracked Step 9 merged GO Decision at HEAD: $($authority.GoAtHead)"
  if ($authority.RequestedStepMatches) {
    Write-Host "Tracked GO helper allowlist / safety boundaries match: $($authority.GoAllowlistMatches) / $($authority.GoSafetyBoundariesPresent)"
  } else {
    Write-Host "Tracked Step $($authority.AuthorizedStep) GO details are not exposed as permission for requested Step $Step."
  }
  Write-Host "Merged GO baseline $Step9AuthorizedBaseline is ancestor of HEAD: $($authority.AuthorizedBasePresent)"
  Write-Host "Requested display/task context: Step $Step / $Stage (request does not confer authority)"
  Write-Host "Authority state: $($authority.Summary)"
  if ($authority.ImplementationEligible) {
    Write-Host "Current tracked implementation allowlist: $ImplementationAllowlist only"
  } else {
    $authority.Observations | ForEach-Object { Write-Host "Authority issue: $_" }
  }
  Write-Host "Hard stop: this helper does not authorize or perform merge, tag, push, pane control, or Step 10 implementation."
}

function Show-Guard {
  $authority = Get-LifecycleAuthority
  $policy = Get-StagePolicy -Authority $authority
  Write-Host "== Workflow Guard (read-only) =="
  Write-Host "Requested context: Step $Step / $($policy.Label) (display context only)"
  Write-Host "Current authority: $($authority.Summary)"
  Write-Host "Allowed in requested context: $($policy.Allowed)"
  if ($authority.RequestedStepMatches) {
    Write-Host "Step 9 tracked implementation allowlist: $ImplementationAllowlist only"
  } else {
    Write-Host "Requested Step $Step implementation write scope: NONE (NO-GO; current tracked GO authority is Step $($authority.AuthorizedStep) only)."
  }
  Write-Host "Local-only explicit outputs: write-prompts -> .agent_tasks/inbox/**; collect/task result -> .agent_tasks/outbox/**; review -> .agent_tasks/inbox/**. These do not grant authority."
  Write-Host "Prohibited surfaces: web-vue/**; web-flask/**; other/model_train/detect/**; .omx/**; .ccpanes/**; contracts, DB/schema, runtime/storage, model/AI behavior."
  Write-Host "Prohibited actions: merge to master; tag creation/movement; push; CC-Panes pane control; automatic lifecycle transitions; Step 10 implementation."
  Write-Host "Write-producing verification: verify-backend, verify-frontend, verify-master; these require separate authorization and -AcknowledgeWriteEffects."
  Write-Host "Frontend verification notice: npm build may write web-vue/dist/**."
  Write-Host "Backend verification notice: if separately authorized, this helper redirects APP_DB_PATH, APP_STORAGE_ROOT and AI_MODEL_ROOT to a temporary non-production sandbox."
}

function Show-Next {
  $authority = Get-LifecycleAuthority
  $policy = Get-StagePolicy -Authority $authority
  Write-Host "== Permitted Next Action (read-only) =="
  Write-Host "Requested context: Step $Step / $($policy.Label) (request does not confer authority)"
  Write-Host "Current tracked authority: $($authority.Summary)"
  Write-Host "Authority-derived eligible gate: $($authority.EligibleNextGate)"
  Write-Host "Context-specific next action: $($policy.NextAction)"
  Write-Host "Hard stops:"
  $policy.HardStops | ForEach-Object { Write-Host "- $_" }
}

function Show-Dispatch {
  $authority = Get-LifecycleAuthority
  $policy = Get-StagePolicy -Authority $authority
  Write-Host "== Startup Phrases (display only; no writes and no pane control) =="
  Write-Host "Authority: $($authority.Summary)"
  if (-not $authority.RequestedStepMatches) {
    Write-Host "NO-GO: no startup phrase is emitted for unauthorized Step $Step; this helper will not dispatch implementation outside current tracked authority."
    return
  }
  foreach ($definition in Get-RoleDefinitions) {
    $taskPath = Get-InboxDisplayPath -FileName $definition.File
    Write-Host ("{0}: Read {1}; execute only the separately assigned Step {2} {3} scope; keep output at .agent_tasks/outbox/{4} only if requested; no unlisted writes, pane control, merge/tag/push, or Step 10 work." -f $definition.Name, $taskPath, $Step, $policy.Label, $definition.Result)
  }
}

function Write-Prompts {
  $authority = Get-LifecycleAuthority
  $policy = Get-StagePolicy -Authority $authority
  if (($Stage -eq "implementation") -and (-not $authority.RequestedStepMatches)) {
    throw "[NO-GO] write-prompts refused: requested Step $Step implementation does not match current tracked GO authority for Step $($authority.AuthorizedStep). No implementation task file was generated."
  }
  $targetDirectory = Get-InboxDirectory
  New-Item -ItemType Directory -Force -Path $targetDirectory | Out-Null

  foreach ($definition in Get-RoleDefinitions) {
    $path = Join-Path $targetDirectory $definition.File
    if ((Test-Path -LiteralPath $path) -and -not $Overwrite) {
      throw "Prompt already exists: $path. Re-run with -Overwrite only when replacing an explicitly local inbox task is intended."
    }
    $scope = Get-RoleScope -RoleId $definition.Id -Authority $authority
    $permittedAction = Get-RolePermittedAction -RoleId $definition.Id -Policy $policy -Authority $authority
    $hardStops = ($policy.HardStops | ForEach-Object { "- $_" }) -join "`r`n"
    $content = @"
# Step $Step $($policy.Label) Task - $($definition.Name) Agent

Lifecycle stage: `$Stage = $Stage`
Local workflow classification: generated local-only inbox instruction; this file is operational convenience state, not tracked implementation authority.
Current tracked authority summary: $($authority.Summary)

## Authority Hierarchy
1. Live Git branch/HEAD/tag facts establish repository state.
2. Tracked planning, GO Decision, verification and closeout/archive records establish lifecycle permission and allowlists.
3. Explicit task/view parameters request context only and never override missing or conflicting tracked authority.
4. `.agent_tasks/**` inputs/outputs are local-only operational state and never grant tracked authority.

## Allowed Scope
$scope

## Permitted Action
$permittedAction

## Output Boundary
If an output is explicitly required by this task, write local-only operational output only to:
`.agent_tasks/outbox/$($definition.Result)`
No local output may infer PASS, approve work, or transition a lifecycle stage.

## Required Guardrails
$hardStops
- Step 9 implementation allowlist, when separately authorized and applicable to this role, is $ImplementationAllowlist only.
- Do not modify any path not explicitly assigned in this task.
- Treat verify-backend, verify-frontend and verify-master as write-producing verification requiring separate authorization and explicit acknowledgement; never treat them as read-only scans.
- Do not create, navigate, focus, inject into or control CC-Panes panes.
- Do not implement watch; any future watch request requires a revised separately reviewed decision.

This generated prompt does not authorize merge, tag, push, automatic lifecycle action, or Step 10 implementation.
"@
    Set-Content -LiteralPath $path -Value $content -Encoding UTF8
    Write-Host "[WRITE] Wrote local-only inbox prompt: $(Get-InboxDisplayPath -FileName $definition.File)"
  }
}

function Collect-Results {
  $outbox = Join-Path $Tasks "outbox"
  New-Item -ItemType Directory -Force -Path $outbox | Out-Null
  $summary = Join-Path $outbox "summary.md"
  $entries = @("leader", "backend", "frontend", "docs", "control_plane")

  "# Agent Results Summary`r`n`r`nGenerated at: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')`r`n`r`nLocal-only aggregation: this summary does not infer PASS, approve work, transition stages, merge, tag, push or authorize Step 10.`r`n" | Set-Content -LiteralPath $summary -Encoding UTF8
  foreach ($name in $entries) {
    $file = Join-Path $outbox "${name}_result.md"
    Add-Content -LiteralPath $summary -Encoding UTF8 -Value "`r`n---`r`n## $name result`r`n"
    if (Test-Path -LiteralPath $file) {
      Get-Content -LiteralPath $file | Add-Content -LiteralPath $summary -Encoding UTF8
    } else {
      Add-Content -LiteralPath $summary -Encoding UTF8 -Value "_No result file found._"
    }
  }
  Write-Host "[WRITE] Collected local-only result summary: .agent_tasks/outbox/summary.md"
  Write-Host "No PASS decision, approval, transition, merge, tag, push or Step 10 action was inferred or performed."
}

function Write-ReviewPrompt {
  $authority = Get-LifecycleAuthority
  $policy = Get-StagePolicy -Authority $authority
  $targetDirectory = Get-InboxDirectory
  New-Item -ItemType Directory -Force -Path $targetDirectory | Out-Null
  $review = Join-Path $targetDirectory "leader_review.md"
  $reviewPath = Get-InboxDisplayPath -FileName "leader_review.md"
  $hardStops = ($policy.HardStops | ForEach-Object { "- $_" }) -join "`r`n"
  $content = @"
# Leader Review Task - Step $Step $($policy.Label)

This is a local-only review prompt. It is not tracked authority and cannot infer PASS, approval, lifecycle transition, merge, tag, push or Step 10 authority.
Current tracked authority summary: $($authority.Summary)

Authority hierarchy: live Git/tag facts first; tracked planning/GO/evidence/closeout records second; explicit parameters are requested context only; `.agent_tasks/**` is operational state only.

Required checks:
1. Confirm current branch, HEAD, rollback tag and merged GO baseline.
2. Confirm tracked modified files remain inside $ImplementationAllowlist only when implementation is separately assigned.
3. Confirm validation commands actually run and all local-only outputs are disclosed.
4. Confirm write-producing verification was not mistaken for read-only status and still requires acknowledgement.
5. Confirm no pane control, watch, merge, tag, push or Step 10 implementation occurred.

Hard stops:
$hardStops

Write any explicitly requested local-only decision output only to `.agent_tasks/outbox/leader_result.md`.
Do not silently fix implementation or authorize later lifecycle actions from this prompt.
"@
  Set-Content -LiteralPath $review -Value $content -Encoding UTF8
  Write-Host "[WRITE] Generated local-only review prompt: $reviewPath"
}
function Assert-WriteVerificationAuthorized {
  param([string]$VerificationName, [string]$EffectMessage)

  if (-not $AcknowledgeWriteEffects) {
    Write-Error "[BLOCKED] $VerificationName is write-producing verification, not a read-only query. It requires separate authorization and explicit -AcknowledgeWriteEffects. $EffectMessage"
    exit 2
  }
  Write-Warning "[WRITE-PRODUCING] $VerificationName explicitly acknowledged. $EffectMessage"
}

function Invoke-BackendVerification {
  Assert-WriteVerificationAuthorized -VerificationName "verify-backend" -EffectMessage "A temporary non-production DB/storage/model/cache sandbox will be created."
  $sandbox = Join-Path ([System.IO.Path]::GetTempPath()) ("agentctl-backend-verify-" + [Guid]::NewGuid().ToString("N"))
  $storage = Join-Path $sandbox "storage"
  $modelRoot = Join-Path $sandbox "models"
  $cacheRoot = Join-Path $sandbox "pycache"
  New-Item -ItemType Directory -Force -Path $storage, $modelRoot, $cacheRoot | Out-Null
  $savedEnvironment = @{}
  foreach ($name in @("APP_DB_PATH", "APP_STORAGE_ROOT", "AI_MODEL_ROOT", "PYTHONPYCACHEPREFIX", "TEMP", "TMP")) {
    $savedEnvironment[$name] = [Environment]::GetEnvironmentVariable($name, "Process")
  }
  try {
    $env:APP_DB_PATH = Join-Path $storage "app.sqlite3"
    $env:APP_STORAGE_ROOT = $storage
    $env:AI_MODEL_ROOT = $modelRoot
    $env:PYTHONPYCACHEPREFIX = $cacheRoot
    $env:TEMP = $sandbox
    $env:TMP = $sandbox
    Write-Host "[WRITE] Backend verification sandbox: $sandbox"
    Push-Location (Join-Path $Root "web-flask")
    try {
      & python -m compileall . | Out-Host
      if ($LASTEXITCODE -ne 0) { return [int]$LASTEXITCODE }
      & python -m pytest -p no:cacheprovider | Out-Host
      return [int]$LASTEXITCODE
    } finally {
      Pop-Location
    }
  } finally {
    foreach ($name in $savedEnvironment.Keys) {
      $prior = $savedEnvironment[$name]
      if ($null -eq $prior) {
        [Environment]::SetEnvironmentVariable($name, $null, "Process")
      } else {
        [Environment]::SetEnvironmentVariable($name, [string]$prior, "Process")
      }
    }
  }
}

function Invoke-FrontendVerification {
  Assert-WriteVerificationAuthorized -VerificationName "verify-frontend" -EffectMessage "npm build may write web-vue/dist/**."
  Push-Location (Join-Path $Root "web-vue")
  try {
    & npm.cmd run build | Out-Host
    return [int]$LASTEXITCODE
  } finally {
    Pop-Location
  }
}

function Invoke-DocsCheck {
  Write-Host "[READ-ONLY] Running Git whitespace/diff inspection only; no verification outputs are generated by this command."
  & git -C $Root diff --name-status | Out-Host
  if ($LASTEXITCODE -ne 0) { return [int]$LASTEXITCODE }
  & git -C $Root diff --check | Out-Host
  return [int]$LASTEXITCODE
}

function Invoke-MasterVerification {
  Assert-WriteVerificationAuthorized -VerificationName "verify-master" -EffectMessage "It includes backend sandbox writes and frontend web-vue/dist/** build output."
  $backendExit = Invoke-BackendVerification
  if ($backendExit -ne 0) { return [int]$backendExit }
  return [int](Invoke-FrontendVerification)
}

try {
  switch ($Command) {
    "status" { Show-Status }
    "guard" { Show-Guard }
    "next" { Show-Next }
    "dispatch" { Show-Dispatch }
    "watch-outbox" { $watchExitCode = Watch-Outbox; exit $watchExitCode }
    "write-prompts" { Write-Prompts }
    "collect" { Collect-Results }
    "review" { Write-ReviewPrompt }
    "verify-backend" { exit (Invoke-BackendVerification) }
    "verify-frontend" { exit (Invoke-FrontendVerification) }
    "verify-docs" { exit (Invoke-DocsCheck) }
    "verify-master" { exit (Invoke-MasterVerification) }
    "init" {
      Write-Error "[BLOCKED] init previously created local workflow directories implicitly. Use explicit write-prompts, collect or review only when that write is intended."
      exit 2
    }
    "clean-omx" {
      Write-Error "[BLOCKED] clean-omx would restore/discard runtime state and is intentionally disabled by workflow hardening."
      exit 2
    }
  }
} catch {
  Write-Error $_
  exit 1
}
