# Phase 2B Batch4 Step 9 Planning / Gate - Local Agent Orchestration v2

Status: **PLANNING / GATE ONLY**
Date: 2026-05-24
Phase: Phase 2B Batch4 Step 9
Recommended direction: **Local Agent Orchestration v2**
Planning branch: `batch4-step9-planning`
Current master HEAD baseline: `b8b3f16` (`Archive Batch4 Step8 stable tag`)
Latest stable tag: `phase2b-batch4-step8-local-workflow-stable -> 3c00a1e`
Step 8 status: **CLOSED / VERIFIED / STABLE TAG ARCHIVED**
Step 9 implementation: **NOT AUTHORIZED**
New stable tag: **NOT CREATED / NOT AUTHORIZED**
Push: **NOT DONE**
Step 10: **NOT AUTHORIZED**

## 1. Planning Gate Decision

Selected Step 9 direction:

```text
Local Agent Orchestration v2
```

Planning objective:

```text
Plan a bounded second iteration of the local CC-Panes + tracked
`tools/agentctl.local.ps1` workflow so that stage-specific task creation,
short agent dispatch, result collection and Leader review require fewer manual
long-prompt copy/paste operations, while preserving explicit human gates and
keeping application/product behavior unchanged.
```

This document creates only the Step 9 **Planning / Gate** artifact. It does not
authorize a read-write implementation task, does not modify the existing
helper and does not open Step 10.

## 2. Current Baseline and Step 8 Clean Closeout

### 2.1 Authoritative baseline

| Item | Current evidence / planning treatment |
|---|---|
| Current `master` HEAD | `b8b3f16` (`Archive Batch4 Step8 stable tag`) |
| Step 8 evidence merge / tag commit | `3c00a1e` (`Merge Phase 2B Batch4 Step8 local workflow verification evidence`) |
| Step 8 stable tag | `phase2b-batch4-step8-local-workflow-stable -> 3c00a1e` |
| Step 8 implementation merge | `c6befa3` (`Merge Phase 2B Batch4 Step8 control-plane workflow hardening`) |
| Step 8 implementation artifact | `tools/agentctl.local.ps1` only |
| Prior application stable restore point | `phase2b-batch4-step7-record-filter-stable -> 25c9f43` |
| Current working tree before planning branch creation | Clean on `master` |
| Push | **NOT DONE** |
| Step 9 implementation | **NOT AUTHORIZED** |
| Step 10 | **NOT AUTHORIZED** |

### 2.2 Step 8 closeout accepted as prerequisite

The following Step 8 records establish the gate prerequisite for planning only:

- `PROJECT_CONTEXT.md` and `README.md` record Step 8 as `VERIFIED / STABLE TAG CREATED` and limit the next allowed action to Step 9 Planning / Gate.
- `agent_outputs/docs/PHASE2B_BATCH4_MASTER_PLANNING_GATE.md` records the same tag, clean verification and Step 9 hard stop.
- `agent_outputs/docs/PHASE2B_BATCH4_STEP8_LOCAL_WORKFLOW_HARDENING_CLOSEOUT.md` and `..._VERIFICATION_EVIDENCE.md` record that the tracked Step 8 implementation was limited to `tools/agentctl.local.ps1`, with informational helper verification PASS and no application/contract/runtime/model change.

Planning conclusion:

```text
Step 8 is cleanly closed and stable-tag archived.
Step 9 Planning / Gate may begin.
Step 9 implementation remains NOT AUTHORIZED until a later reviewed GO Decision.
```

## 3. Why Continue with Local Agent Orchestration v2

Step 8 delivered a narrow, tracked helper that reduces manual workflow effort
without modifying product code. Step 9 should continue that direction because
the remaining observed problem is still local workflow orchestration quality,
not application functionality.

### 3.1 Decision drivers

1. Reduce repeated copying of long web/UI prompts while keeping workflow output reviewable.
2. Correct lifecycle drift: operational guidance must reflect current Git/docs/state rather than stale Step 8 implementation defaults.
3. Preserve strict human-controlled merge/tag/push and next-step gates.

### 3.2 Local v2 versus AO / Maestro / external orchestrator

| Option | Planning assessment | Step 9 decision |
|---|---|---|
| Extend existing `agentctl.local.ps1` with CC-Panes as the operating UI | Builds on the tracked Step 8 artifact and proven local review flow; allows narrowly auditable scope and rollback; requires no new orchestrator authority or dependency. | **RECOMMENDED FOR PLANNING.** |
| Adopt AO / Maestro / another external orchestrator | Would introduce a new integration/authority surface, configuration and lifecycle behavior not required to resolve the evidenced stale-state/manual-prompt gap; would materially expand scope before local v2 is evaluated. | **NO-GO FOR THIS STEP 9 DIRECTION.** |

This decision is a scope-control conclusion, not a general product comparison:
Step 9 does not investigate, integrate or replace tooling with AO, Maestro or
any external orchestrator. CC-Panes remains the human-facing operating
interface, and `agentctl.local.ps1` remains the bounded local control-plane
candidate.

## 4. Current `agentctl.local.ps1` Capability and Observed Gap

### 4.1 Capabilities already present from Step 8

Read-only review of `tools/agentctl.local.ps1` confirms these current command
surfaces:

| Current capability | Source evidence | Planning finding |
|---|---|---|
| `status` | `Show-Status` plus command switch | Reports branch/HEAD/dirty state and authority guidance without implicit task writes. |
| `guard` | `Show-Guard` | Reports allowlist, prohibited surfaces/actions and write-producing verification warnings. |
| Stage-aware `next` | `Get-StagePolicy` / `Show-Next` | Has policies for `planning`, `go`, `implementation`, `review`, `evidence`. |
| `dispatch` | `Show-Dispatch` | Emits short Backend / Frontend / Docs-Test startup phrases without writing task files. |
| `write-prompts` | `Write-Prompts` | Explicitly writes scoped local-only inbox prompts. |
| `collect` | `Collect-Results` | Explicitly writes a local-only outbox summary and does no lifecycle action. |
| `review` | `Write-ReviewPrompt` | Explicitly writes a local-only Leader review prompt with hard stops. |
| Verification guard | `Assert-WriteVerificationAuthorized` and `verify-*` routes | Treats `verify-backend`, `verify-frontend`, `verify-master` as write-producing verification requiring acknowledgement. |
| Destructive guard | `init` / `clean-omx` command cases | Blocks implicit initialization and runtime-state discard behavior. |

### 4.2 Confirmed stale lifecycle/state limitation

The current helper remains oriented to the closed Step 8 implementation state:

| Observation | Direct helper evidence | Step 9 planning implication |
|---|---|---|
| Default stage is stale | Parameter default is `[string]$Stage = "implementation"`. | Running informational commands without explicit stage still displays implementation context after Step 8 closeout. |
| Default step is stale | Parameter default is `[string]$Step = "8"`. | It cannot naturally represent Step 9 planning without the caller supplying arguments. |
| Stable/authorization facts are Step 8-specific | `$StableTag` points to the Step 7 stable tag, `$Step8AuthorizedBaseline = "fbc95d0"`, and `$GoDecisionPath` names the Step 8 GO Decision. | Current status output is not a general lifecycle/state resolver and must not be treated as current Git authority for Step 9. |
| Role prompt behavior is Step 8-specific | `Get-RoleScope` / `Get-RolePermittedAction` contain Step 8 implementation branches. | Prompt generation needs lifecycle/state-driven scope selection before reuse for future steps. |

Current-state decision:

```text
Git and tracked closeout documents are authoritative: Step 8 is closed and
Step 9 is planning-only. Existing `agentctl` default Step 8 / implementation
output is a candidate deficiency for Step 9 planning, not authorization to edit
or run implementation.
```

## 5. Proposed Step 9 Target Capability Scope

A later GO Decision may consider only a bounded local-orchestration improvement
after read-only evidence validates the design. Candidate target capabilities:

| Candidate capability | Planning target behavior | Gate note |
|---|---|---|
| Stage-complete `write-prompts` | Generate standardized local-only inbox task files for `planning`, `read-only`, `go`, `implementation`, `review` and `evidence` contexts, with stage-appropriate allowlists and NO-GO text. | Must distinguish prompt generation writes from informational commands. |
| `dispatch` | Output a fixed short launch phrase per applicable Agent and current approved task/stage. | Must not execute or control a CC-Panes pane automatically. |
| `collect` | Aggregate explicitly available local-only outbox results for Leader review. | Must not infer PASS, merge, tag or next implementation. |
| `review` | Generate a Leader review task grounded in the current authorized stage and discovered evidence set. | Must not auto-approve or auto-merge. |
| State/Git/docs-aware `next` | Determine the permitted next gate using live Git HEAD/tag state and tracked planning/GO/evidence/closeout records, with local state treated only as operational input. | Must resolve the current Step 8-default/stale-context gap. |
| Correct lifecycle `status` / `guard` | Display the current stable tag, closed Step state and upcoming planning-only authority rather than defaulting to the previous implementation lane. | Must be non-mutating and evidence-backed. |
| Optional `watch` | Monitor local outbox changes only and surface review readiness. | Optional; must never merge, tag, push, control panes or enter implementation. |

### 5.1 Deliberately retained interface and exclusions

- **Retain:** CC-Panes as the runtime/user interaction surface.
- **Retain:** a local, tracked and reviewable `tools/agentctl.local.ps1` workflow boundary if later authorized.
- **Exclude:** AO / Maestro / external orchestrator integration.
- **Exclude:** automatic CC-Panes pane creation, navigation, prompt injection or control.
- **Exclude:** automatic merge, tag, push or Step 10 implementation.

## 6. Agent Lane Assessment

| Agent lane | Step 9 planning / scan requirement | Implementation decision at this gate |
|---|---|---|
| Project Leader / Control-plane | **REQUIRED** for evidence synthesis, lifecycle-state authority policy, exact candidate allowlist and later GO Decision. | **NO IMPLEMENTATION AUTHORIZED.** |
| Backend Agent | **LIMITED READ-ONLY SCAN ONLY IF NEEDED** to confirm future `verify-backend` safety classification remains correctly isolated and no backend code is needed. | **NO-GO** for `web-flask/**`. |
| Frontend Agent | **LIMITED READ-ONLY SCAN ONLY IF NEEDED** to confirm future `verify-frontend` remains explicitly write-producing and no frontend code is needed. | **NO-GO** for `web-vue/**`. |
| Docs/Test Agent | **REQUIRED** for checklist design, tracked-state evidence requirements and later verification/closeout documentation planning. | **DOCS/TEST EVIDENCE ONLY AFTER SEPARATE AUTHORIZATION; no implementation now.** |
| AI Agent | **NOT REQUIRED**. No model, inference, training, evaluation or multimodal/LLM work is involved. | **NO-GO.** |

## 7. Authorized Read-Only Scan Design for the Next Gate Activity

After this planning document is reviewed/merged, a separate read-only scan may
be authorized to determine whether a narrowly scoped Step 9 GO Decision is
justified. The scan must not modify `tools/agentctl.local.ps1` or local task
state.

### 7.1 Read-only scan work packages

| Scan work package | Read-only inputs | Required evidence output |
|---|---|---|
| Lifecycle authority mapping | `PROJECT_CONTEXT.md`, `README.md`, Step 8 planning/GO/evidence/closeout docs, tags/HEAD through read-only Git | Define authoritative facts for closed Step 8, Step 9 planning, future stage transitions and how stale outputs are detected. |
| Current helper capability/gap scan | `tools/agentctl.local.ps1` static inspection only | Inventory current command surfaces; map hard-coded Step 8/default implementation behavior; assess design options for Step 9 state/Git/docs-aware lifecycle resolution. |
| Prompt/dispatch flow scan | Existing helper source and tracked documentation patterns only | Specify required `planning` / `read-only` / `go` / `implementation` / `review` / `evidence` generated task structures and fixed startup phrase contract. |
| Collect/review/watch safety scan | Existing helper source and archived workflow evidence | Define explicit local-output writes; determine whether optional outbox-only `watch` is safe and useful without automation side effects. |
| Boundary verification scan | Git path/diff/tag/status read commands and explicit NO-GO list | Prove no business/product/contract/runtime/model scope is required and propose an exact later file allowlist. |

### 7.2 Read-only scan restrictions

Allowed inspection activities only:

```text
Get-Content / Select-String / Get-ChildItem for listed workflow documentation and helper source
git status / git log / git show / git diff --name-status / git diff --check / git tag --points-at / git show-ref
static source comparison and written scan-result drafting only when separately authorized
```

Forbidden during the scan:

```text
executing tools/agentctl.local.ps1 write-producing commands
modifying tools/agentctl.local.ps1
modifying .agent_tasks/**
modifying docs unless the scan-result file path is explicitly authorized
running build/test/verify-backend/verify-frontend/verify-master
controlling CC-Panes panes
merge / tag / push / Step 9 implementation / Step 10 implementation
```

### 7.3 Required scan questions

The read-only evidence must answer:

1. What source of truth should select current Step and lifecycle stage: Git tags/HEAD plus tracked docs, an explicit config/state artifact, command parameters, or a bounded combination?
2. How will `agentctl` avoid displaying stale Step 8 implementation authorization now that Step 8 is closed and Step 9 is planning-only?
3. What exact prompt schemas are required for `planning`, `read-only`, `go`, `implementation`, `review` and `evidence`?
4. How should `dispatch` reference generated tasks without automatically writing prompts or controlling CC-Panes?
5. How should `collect` and `review` operate on local-only outbox/inbox files while preserving tracked Git/docs authority?
6. Is optional outbox-only `watch` justified and how is it proven to have no merge/tag/push/pane-control/later-step effects?
7. What is the narrowest future tracked implementation file allowlist, and what separately authorized evidence/doc files would be needed?

## 8. GO Decision Prerequisites Before Any Step 9 Implementation

Step 9 implementation remains prohibited unless a later activity completes all
of the following:

1. Merge/review this planning artifact as the planning gate record.
2. Complete an explicitly authorized read-only scan covering Section 7.
3. Reconcile the stale Step 8 implementation/default status behavior against the current `b8b3f16` / stable-tag archived state.
4. Decide the authoritative lifecycle/state selection approach with concrete failure handling and no implicit state writes.
5. Produce a separate tracked Step 9 Implementation GO Decision with:
   - exact implementation file allowlist;
   - command/function scope;
   - CC-Panes and external-orchestrator boundary;
   - permitted validation commands and handling of any local-only disposable output;
   - explicit merge/tag/push/Step 10 gates;
   - rollback plan.
6. Confirm all requested work remains local control-plane only and requires no application, contract, runtime or model changes.

Until those gates are completed:

```text
Phase 2B Batch4 Step 9 Implementation: NOT AUTHORIZED
```

## 9. Explicit NO-GO

During Step 9 Planning / Gate and any subsequent separately authorized
read-only scan, the following remain prohibited:

- no Step 9 implementation;
- no edits to `tools/agentctl.local.ps1`;
- no edits to `.agent_tasks/**`;
- no edits to `web-vue/**` or `web-flask/**`;
- no edits to `.ccpanes/**` or `.omx/**`;
- no edits to `other/model_train/detect/**`;
- no DB schema, migration, index or data-file changes;
- no Docker, deployment, runtime or storage-structure changes;
- no model, weight, class, training, inference, AI/LLM or evaluation behavior changes;
- no API response, JWT, auth/login, `detection_result.v1` or metrics contract changes;
- no AO / Maestro / external orchestrator integration;
- no automatic or manual CC-Panes pane control as part of this direction;
- no automatic merge, tag or push capability;
- no merge, tag or push action under this planning task;
- no Step 10 implementation.

## 10. Planning Acceptance Criteria

This Step 9 Planning / Gate artifact is complete only when:

- [x] Current master baseline `b8b3f16` and Step 8 stable tag target `3c00a1e` are recorded.
- [x] Step 8 `CLOSED / VERIFIED / STABLE TAG ARCHIVED` status and clean working-tree prerequisite are recorded.
- [x] Local Agent Orchestration v2 is identified as the recommended direction and external orchestrator integration is explicitly excluded.
- [x] Current helper capabilities and the stale Step 8/default implementation context limitation are captured from source evidence.
- [x] Candidate target capabilities include stage-aware prompt/dispatch/collect/review/next behavior and optional safe outbox-only `watch` evaluation.
- [x] Agent lane needs, read-only scan design, GO prerequisites, rollback and NO-GO boundaries are recorded.
- [x] Push remains `NOT DONE`, stable tagging for Step 9 remains uncreated/unauthorized, and Step 10 remains `NOT AUTHORIZED`.
- [x] This planning branch changes only the specified planning document.

Future gates remain pending:

- [ ] Step 9 planning artifact reviewed/merged.
- [ ] Step 9 read-only scan separately authorized and completed.
- [ ] Step 9 Implementation GO Decision produced/reviewed/merged.
- [ ] Step 9 implementation authorized or executed.

## 11. Risks and Mitigations

| Risk | Mitigation required by this planning gate |
|---|---|
| The existing helper presents stale Step 8 implementation context as though it were current authority. | Treat Git/tags/tracked docs as authoritative; require read-only scan and GO Decision to design state-aware correction before implementation. |
| Prompt reduction unintentionally turns into automated lifecycle execution. | Separate prompt generation/summary display from decisions; explicitly prohibit merge/tag/push/Step 10 automation. |
| Local-only `.agent_tasks/**` files are mistaken for durable authorization. | Keep local outputs operational-only; require tracked decision artifacts for gate authority. |
| Optional watch feature becomes background automation or pane control. | Evaluate outbox-only observation in read-only scan; keep pane control and lifecycle actions NO-GO. |
| Scope grows into new orchestrator adoption or application changes. | Keep CC-Panes + helper as selected planning direction; exclude AO/Maestro/external integration and all business/runtime/model/contracts. |

## 12. Verification and Rollback Baseline

### 12.1 Planning document verification

This docs-only planning task requires:

```text
git status --short
git log --oneline --decorate -10
git diff --name-status
git diff --check
git show --name-status --oneline HEAD after the planning commit
```

No helper command, build/test command or write-producing verification command
is run to create this planning artifact.

### 12.2 Rollback baseline

Stable rollback baseline entering Step 9 planning:

```text
phase2b-batch4-step8-local-workflow-stable -> 3c00a1e
```

Planning rollback:

- abandon or revert the isolated Step 9 planning commit before merge if the direction is rejected;
- no helper, business-code, DB, runtime, model or tag rollback is required because those changes are prohibited in this task;
- no new stable tag is created during Step 9 Planning / Gate.

## 13. Recommended Next Step

After review of this planning artifact, the only eligible continuation is a
separately scoped read-only scan for **Local Agent Orchestration v2** as defined
in Section 7.

```text
Allowed next direction: Phase 2B Batch4 Step 9 read-only scan / gate evidence only.
Not allowed: Step 9 implementation, Step 10 implementation, helper edits, external orchestrator integration, pane automation, merge/tag/push or application work.
```