param(
  [Parameter(Position = 0)]
  [ValidateSet("status", "guard", "next", "dispatch", "write-prompts", "collect", "review", "verify-backend", "verify-frontend", "verify-docs", "verify-master", "init", "clean-omx")]
  [string]$Command = "status",

  [ValidateSet("planning", "go", "implementation", "review", "evidence")]
  [string]$Stage = "implementation",

  [ValidatePattern('^[0-9]+$')]
  [string]$Step = "8",

  [ValidateSet("all", "backend", "frontend", "docs-test")]
  [string]$Role = "all",

  [ValidatePattern('^$|^[A-Za-z0-9][A-Za-z0-9._-]*$')]
  [string]$PromptSet = "",

  [switch]$Overwrite,
  [switch]$AcknowledgeWriteEffects
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
$Tasks = Join-Path $Root ".agent_tasks"
$StableTag = "phase2b-batch4-step7-record-filter-stable"
$StableCommit = "25c9f43"
$Step8AuthorizedBaseline = "fbc95d0"
$GoDecisionPath = "agent_outputs/docs/PHASE2B_BATCH4_STEP8_LOCAL_WORKFLOW_HARDENING_IMPLEMENTATION_GO_DECISION.md"

function Invoke-GitRead {
  param([Parameter(Mandatory = $true)][string[]]$Arguments)

  $output = & git -C $Root @Arguments 2>&1
  if ($LASTEXITCODE -ne 0) {
    throw "git $($Arguments -join ' ') failed: $($output -join [Environment]::NewLine)"
  }
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

function Get-NextStepText {
  $number = 0
  if ([int]::TryParse($Step, [ref]$number)) {
    return [string]($number + 1)
  }
  return "the next Step"
}

function Get-StagePolicy {
  $nextStep = Get-NextStepText
  switch ($Stage) {
    "planning" {
      return [pscustomobject]@{
        Label = "Planning"
        Allowed = "Prepare or review a scoped plan and read-only scan prompts; do not implement."
        NextAction = "Complete planning review, then request an explicit GO Decision gate."
        HardStops = @("No implementation.", "No merge, tag or push.", "No Step $nextStep implementation.")
      }
    }
    "go" {
      return [pscustomobject]@{
        Label = "GO Decision"
        Allowed = "Draft or review the tracked authorization decision only within its assigned documentation scope."
        NextAction = "Require reviewed/merged GO authority before creating an implementation branch."
        HardStops = @("No implementation before reviewed/merged GO authority.", "No tag or push.", "No Step $nextStep implementation.")
      }
    }
    "implementation" {
      return [pscustomobject]@{
        Label = "Implementation"
        Allowed = "Implement only files explicitly allowlisted by the approved task; Step 8 current tracked allowlist is tools/agentctl.local.ps1 only."
        NextAction = "Return the isolated implementation branch and validation evidence for Leader review."
        HardStops = @("No merge to master, tag creation or push.", "No business, runtime, contract or model-surface expansion.", "No Step $nextStep implementation.")
      }
    }
    "review" {
      return [pscustomobject]@{
        Label = "Review"
        Allowed = "Review the authorized diff and recorded validation evidence; do not expand implementation scope."
        NextAction = "Leader decides whether a separately authorized merge/unified-verification action is warranted."
        HardStops = @("No silent fixes outside a newly authorized implementation task.", "No automatic merge, tag or push.", "No Step $nextStep implementation.")
      }
    }
    "evidence" {
      return [pscustomobject]@{
        Label = "Evidence"
        Allowed = "Record only separately authorized verification evidence and explicitly disclosed local validation outputs."
        NextAction = "Return evidence to the Leader for the next explicit gate."
        HardStops = @("No implementation changes.", "No automatic merge, tag or push.", "No Step $nextStep implementation.")
      }
    }
  }
}

function Get-RoleDefinitions {
  $definitions = @(
    [pscustomobject]@{ Id = "backend"; Name = "Backend"; File = "backend.md"; Result = "backend_result.md" },
    [pscustomobject]@{ Id = "frontend"; Name = "Frontend"; File = "frontend.md"; Result = "frontend_result.md" },
    [pscustomobject]@{ Id = "docs-test"; Name = "Docs-Test"; File = "docs.md"; Result = "docs_result.md" }
  )
  if ($Role -eq "all") { return $definitions }
  return @($definitions | Where-Object { $_.Id -eq $Role })
}

function Get-RoleScope {
  param([string]$RoleId)

  if ($Step -eq "8") {
    switch ($Stage) {
      "implementation" {
        switch ($RoleId) {
          "backend" { return "NO-GO for web-flask/** implementation or verification in this task; report any boundary concern only." }
          "frontend" { return "NO-GO for web-vue/** implementation or build verification in this task; report any boundary concern only." }
          "docs-test" { return "Do not create tracked evidence or alter documentation; a later evidence activity requires separate authorization." }
        }
      }
      "review" { return "Perform read-only review against the Step 8 single-file control-plane allowlist; do not edit tracked files." }
      "evidence" { return "Act only under a separately issued evidence authorization; do not infer permission from this prompt." }
      default { return "Perform read-only scope analysis only; Step 8 product implementation is not authorized by this stage." }
    }
  }
  return "Follow only the explicit allowlist in the assigned Step $Step $Stage task; do not infer additional write scope."
}

function Get-RolePermittedAction {
  param([string]$RoleId, [object]$Policy)

  if ($Step -eq "8" -and $Stage -eq "implementation") {
    switch ($RoleId) {
      "backend" { return "No implementation or verification action is assigned to Backend in this Step 8 control-plane task; report boundary observations only." }
      "frontend" { return "No implementation or build-verification action is assigned to Frontend in this Step 8 control-plane task; report boundary observations only." }
      "docs-test" { return "No tracked evidence or documentation edit is assigned during implementation; wait for separate evidence authorization." }
    }
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

function Show-Status {
  $branch = Invoke-GitRead -Arguments @("branch", "--show-current")
  $head = Invoke-GitRead -Arguments @("rev-parse", "HEAD")
  $changes = [string](Invoke-GitRead -Arguments @("status", "--porcelain=v1", "--untracked-files=all"))
  $stableTarget = [string](Invoke-GitRead -Arguments @("rev-list", "-n", "1", $StableTag))
  $goAtHead = Test-TrackedAtHead -Path $GoDecisionPath
  $authorizedBasePresent = Test-GitAncestor -Ancestor $Step8AuthorizedBaseline

  Write-Host "== Local Workflow Status (read-only) =="
  Write-Host "Repository: $Root"
  Write-Host "Branch: $branch"
  Write-Host "HEAD: $head"
  if ([string]::IsNullOrWhiteSpace($changes)) {
    Write-Host "Dirty status: CLEAN"
  } else {
    Write-Host "Dirty status: DIRTY"
    $changes -split "`r?`n" | ForEach-Object { Write-Host "  $_" }
  }
  Write-Host "Stable restore tag: $StableTag -> $stableTarget (expected prefix $StableCommit)"
  Write-Host "Requested lifecycle context: Step $Step / $Stage"
  Write-Host "Tracked Step 8 GO decision at HEAD: $goAtHead"
  Write-Host "Authorized implementation baseline $Step8AuthorizedBaseline is ancestor of HEAD: $authorizedBasePresent"
  if ($goAtHead -and $authorizedBasePresent) {
    Write-Host "Authorization state: Step 8 control-plane implementation may use its explicit allowlist only."
  } else {
    Write-Host "Authorization state: implementation authority is not established by live HEAD checks."
  }
  Write-Host "Hard stop: this helper does not authorize or perform merge, tag, push, or next-Step implementation."
}

function Show-Guard {
  $policy = Get-StagePolicy
  Write-Host "== Workflow Guard (read-only) =="
  Write-Host "Context: Step $Step / $($policy.Label)"
  Write-Host "Allowed now: $($policy.Allowed)"
  if ($Step -eq "8" -and $Stage -eq "implementation") {
    Write-Host "Tracked implementation allowlist: tools/agentctl.local.ps1"
    Write-Host "Local-only explicit outputs: write-prompts -> .agent_tasks/inbox/**; collect/review/task result -> .agent_tasks/outbox/** or declared inbox prompt."
  }
  Write-Host "Prohibited surfaces: web-vue/**; web-flask/**; other/model_train/detect/**; .omx/**; .ccpanes/**; .git/info/exclude; contracts, DB/schema, runtime/storage, model/AI behavior."
  Write-Host "Prohibited actions: merge to master; tag creation/movement; push; clean-omx; Step $(Get-NextStepText) implementation."
  Write-Host "Write-producing verification: verify-backend, verify-frontend, verify-master; these require separate authorization and -AcknowledgeWriteEffects."
  Write-Host "Frontend verification notice: npm build may write web-vue/dist/**."
  Write-Host "Backend verification notice: if explicitly authorized, this helper redirects APP_DB_PATH, APP_STORAGE_ROOT and AI_MODEL_ROOT to a temporary non-production sandbox."
}

function Show-Next {
  $policy = Get-StagePolicy
  Write-Host "== Permitted Next Action (read-only) =="
  Write-Host "Context: Step $Step / $($policy.Label)"
  Write-Host "Permitted next action: $($policy.NextAction)"
  Write-Host "Hard stops:"
  $policy.HardStops | ForEach-Object { Write-Host "- $_" }
}

function Show-Dispatch {
  Write-Host "== Startup Phrases (display only; no task execution or file writes) =="
  foreach ($definition in Get-RoleDefinitions) {
    $taskPath = Get-InboxDisplayPath -FileName $definition.File
    Write-Host ("{0}: You are the {0} Agent. Read {1}, obey its Step {2} {3} scope, perform no unlisted writes or later-step work, and report only as instructed." -f $definition.Name, $taskPath, $Step, $Stage)
  }
}

function Write-Prompts {
  $policy = Get-StagePolicy
  $targetDirectory = Get-InboxDirectory
  New-Item -ItemType Directory -Force -Path $targetDirectory | Out-Null

  foreach ($definition in Get-RoleDefinitions) {
    $path = Join-Path $targetDirectory $definition.File
    if ((Test-Path -LiteralPath $path) -and -not $Overwrite) {
      throw "Prompt already exists: $path. Re-run with -Overwrite only when replacing an explicitly local inbox task is intended."
    }
    $scope = Get-RoleScope -RoleId $definition.Id
    $permittedAction = Get-RolePermittedAction -RoleId $definition.Id -Policy $policy
    $hardStops = ($policy.HardStops | ForEach-Object { "- $_" }) -join "`r`n"
    $content = @"
# Step $Step $($policy.Label) Task - $($definition.Name) Agent

Lifecycle stage: `$Stage = $Stage`
Local workflow classification: generated inbox instruction only; this file is not tracked implementation authority.

## Allowed Scope
$scope

## Permitted Action
$permittedAction

## Required Guardrails
$hardStops
- Do not modify any path not explicitly assigned in this task.
- Treat live Git and tracked authorization artifacts as authoritative over stale local state.
- Treat verify-backend, verify-frontend and verify-master as write-producing verification, never as read-only scan operations.

## Return Path
If an output is explicitly required by this task, write local-only operational evidence to:
`.agent_tasks/outbox/$($definition.Result)`

Do not treat this generated prompt as authorization to merge, tag, push, or enter Step $(Get-NextStepText) implementation.
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

  "# Agent Results Summary`r`n`r`nGenerated at: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')`r`n" | Set-Content -LiteralPath $summary -Encoding UTF8
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
  Write-Host "No merge, tag, push or subsequent-step action was performed."
}

function Write-ReviewPrompt {
  $policy = Get-StagePolicy
  $inbox = Join-Path $Tasks "inbox"
  New-Item -ItemType Directory -Force -Path $inbox | Out-Null
  $review = Join-Path $inbox "leader_review.md"
  $hardStops = ($policy.HardStops | ForEach-Object { "- $_" }) -join "`r`n"
  $content = @"
# Leader Review Task - Step $Step $($policy.Label)

Review the isolated branch and local results against live Git/tracked authority.

Required checks:
1. Confirm current branch, HEAD and authorized baseline.
2. Confirm tracked modified files are inside the assigned allowlist.
3. Confirm validation commands actually run and disclosed local-only outputs.
4. Confirm write-producing verification was not mistaken for read-only status.
5. Confirm no merge, tag, push or Step $(Get-NextStepText) implementation occurred.

Hard stops:
$hardStops

Write any explicitly requested local-only decision output to `.agent_tasks/outbox/leader_result.md`.
This generated prompt does not authorize later lifecycle actions.
"@
  Set-Content -LiteralPath $review -Value $content -Encoding UTF8
  Write-Host "[WRITE] Generated local-only review prompt: .agent_tasks/inbox/leader_review.md"
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
