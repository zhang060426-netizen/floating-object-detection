# Phase 2B Batch4 Step 9 Local Agent Orchestration v2 Implementation GO Decision

Status: **GO DECISION DRAFT / CONTROL-PLANE IMPLEMENTATION CONDITIONALLY AUTHORIZED ONLY AFTER REVIEW AND MERGE**
Date: 2026-05-24
Phase: Phase 2B Batch4 Step 9
Topic: Local Agent Orchestration v2
Working branch: `batch4-step9-docs-workflow-go`
Current master HEAD baseline: `0b0adfd` (`Merge Phase 2B Batch4 Step9 planning`)
Stable restore point: `phase2b-batch4-step8-local-workflow-stable -> 3c00a1e`
Step 9 implementation before this decision is separately reviewed/merged: **NOT AUTHORIZED**
Step 9 tag: **NOT CREATED / NOT AUTHORIZED**
Push: **NOT DONE / NOT AUTHORIZED**
Step 10: **NOT AUTHORIZED**

## 1. Decision Summary

```text
Backend implementation: NO-GO
Frontend implementation: NO-GO
AI Agent: NOT REQUIRED
Docs/Test: GO only for separately authorized decision/evidence documents; no implementation scope
Control-plane implementation: CONDITIONAL GO only after this GO Decision is separately reviewed/merged
Candidate implementation allowlist: tools/agentctl.local.ps1 only
This drafting task: documentation only; no helper change and no implementation entered
Merge / tag / push in this drafting task: NO-GO / NOT CREATED / NOT DONE
Step 10: NOT AUTHORIZED
```

This is the separately authorized **Docs/Workflow decision-document** activity requested after completion of the Step 9 Backend, Frontend and Docs/Test read-only scans. Creating this tracked draft does **not** implement Local Agent Orchestration v2 and does not authorize the current branch to edit the helper, local task state, application code or lifecycle state. A later implementation task may be opened only after separate review/merge of this decision and must remain within the exact allowlist in Section 5.

## 2. Reconciled Baseline and Authority Treatment

### 2.1 Current tracked baseline

| Item | Decision baseline / treatment |
|---|---|
| Current `master` HEAD | `0b0adfd` (`Merge Phase 2B Batch4 Step9 planning`) is the current merged planning baseline observed by all three completed scans. |
| Planning document authored baseline | `b8b3f16` (`Archive Batch4 Step8 stable tag`) is retained as historical planning-input context only; it is superseded for live-state reporting by `0b0adfd`. |
| Stable rollback anchor | `phase2b-batch4-step8-local-workflow-stable -> 3c00a1e` remains the stable restored control-plane baseline entering this decision. |
| Current lifecycle state | Step 8 is **CLOSED / VERIFIED / STABLE TAG ARCHIVED**; Step 9 has merged planning evidence, but implementation was not authorized by planning. |
| Step 9 tag / push / Step 10 | No Step 9 stable tag is authorized or created; push remains not done; Step 10 remains not authorized. |

### 2.2 Local read-only scan outputs are inputs, not authorization

The reviewed scan results were produced as local operational evidence:

```text
.agent_tasks/outbox/backend_step9_readonly_result.md
.agent_tasks/outbox/frontend_step9_readonly_result.md
.agent_tasks/outbox/docs_step9_checklist_result.md
```

They are accepted as decision inputs because they record the separately completed read-only checks. However, `.agent_tasks/**` remains local-only operational state and is not a tracked implementation artifact, not durable Git authority and not permission to implement, verify, merge, tag, push or enter Step 10. Live Git facts and tracked planning/decision/evidence/closeout records remain authoritative.

## 3. Reviewed Evidence Accepted for This Decision

| Evidence | Accepted conclusion for this gate |
|---|---|
| `agent_outputs/docs/PHASE2B_BATCH4_STEP9_LOCAL_AGENT_ORCHESTRATION_V2_PLANNING.md` | Defines Step 9 as Local Agent Orchestration v2 planning/gate only, identifies stale helper lifecycle context, and requires a later GO Decision with an exact allowlist before implementation. |
| `.agent_tasks/outbox/backend_step9_readonly_result.md` | Confirms live baseline `0b0adfd`, Step 8 stable tag `3c00a1e`, stale Step 8 helper context, write-producing backend verification classification, Backend implementation **NO-GO**, AI Agent **NOT REQUIRED**, and helper-only candidate scope. |
| `.agent_tasks/outbox/frontend_step9_readonly_result.md` | Confirms live baseline and stale dispatch/stage presentation risk; requires stage-correct display-only dispatch and explicit `read-only` context; Frontend implementation is **NO-GO**; helper-only candidate scope is sufficient. |
| `.agent_tasks/outbox/docs_step9_checklist_result.md` | Confirms sufficient read-only evidence for a GO Decision, requires fail-closed Git/tag/tracked-document authority handling, recommends the helper-only allowlist, excludes optional `watch` from the minimal correction, and reserves Docs/Test for separately authorized decision/evidence records only. |
| `agent_outputs/docs/PHASE2B_BATCH4_STEP8_LOCAL_WORKFLOW_HARDENING_IMPLEMENTATION_GO_DECISION.md` and later Step 8 closeout/evidence records | Establish the prior helper-only control-plane pattern, write-producing verification treatment and stable Step 8 rollback anchor without opening application or model scope. |

## 4. GO / NO-GO Matrix

| Lane / Scope | Decision | Boundary |
|---|---|---|
| Backend implementation | **NO-GO / NOT REQUIRED** | No changes under `web-flask/**`; no backend/API/JWT/auth/DB/storage/contract change is needed or permitted. |
| Frontend implementation | **NO-GO / NOT REQUIRED** | No changes under `web-vue/**`; no UI/API consumption/build/product change is needed or permitted. |
| AI Agent | **NOT REQUIRED / NO-GO** | No model, weights, classes, inference, training, evaluation or multimodal/LLM behavior is implicated. |
| Docs/Test | **GO ONLY FOR SEPARATELY AUTHORIZED DECISION/EVIDENCE DOCUMENTS** | This GO Decision draft is authorized as documentation only. A later evidence/closeout document requires its own authorization and is not implementation. |
| Control-plane implementation | **CONDITIONAL GO ONLY AFTER THIS DECISION IS REVIEWED/MERGED** | Any later implementation activity may modify exactly `tools/agentctl.local.ps1` and no additional file. |
| Current docs/workflow drafting task | **DOC-ONLY GO** | Add this decision artifact only; do not edit or execute the helper or any protected/local-state surface. |
| Merge / tag / push in this task | **NO-GO** | No merge, tag or push is performed or authorized by this drafting branch. |
| Step 10 | **NO-GO / NOT AUTHORIZED** | No Step 10 planning or implementation is opened by this document. |

## 5. Exact Candidate Implementation Allowlist

If and only if this decision is separately reviewed and merged, a separate Step 9 implementation task may be considered with exactly this tracked file allowlist:

```text
tools/agentctl.local.ps1
```

No other implementation file is included. In particular:

- this decision document is a documentation/gate artifact, not implementation;
- any later verification-evidence or closeout document is separately authorized Docs/Test scope, not implementation;
- `.agent_tasks/**` remains local-only workflow state and is never part of tracked implementation authority;
- an implementation need outside `tools/agentctl.local.ps1` is automatically **NO-GO** under this decision and must return for a revised decision before any edit.

## 6. Bounded Later Implementation Requirements Within the Single File

Only after the review/merge gate, a separately assigned helper-only implementation may address the read-only scan findings within `tools/agentctl.local.ps1` as follows:

| Candidate behavior | Required boundary |
|---|---|
| Lifecycle-correct `status`, `guard` and `next` output | Determine current eligibility from live Git/tag facts plus tracked gate/GO/evidence/closeout records; explicit requested context must not manufacture authority; stale/conflicting/absent authority must fail closed to NO-GO/read-only guidance. |
| Stage-complete local prompt policy | Support the six explicit task contexts `planning`, `read-only`, `go`, `implementation`, `review`, `evidence`, each with stage-appropriate allowlists and hard-stop language. |
| Fixed short `dispatch` output | Display a role/task/stage/result instruction grounded in current authority; it must be copyable by a human but must not create/control a CC-Panes pane, write prompts implicitly or enter implementation. |
| Explicit `write-prompts`, `collect` and `review` outputs | Any local-only `.agent_tasks/**` output must be opt-in, declared as operational-only and incapable of authorizing implementation, verification, merge, tag, push or later-step progression. |
| Verification guard preservation | `verify-backend`, `verify-frontend` and `verify-master` remain write-producing operations requiring separate authorization and disclosed effects; they are never read-only scans. |

Minimal-scope decision on optional features:

```text
Optional outbox-only watch behavior is NOT AUTHORIZED in the minimal Step 9 implementation scope.
It is unnecessary to correct stale authority resolution and missing read-only stage coverage.
Any later request for watch requires a revised separately reviewed decision.
```

## 7. Authority, Safety and CC-Panes Boundary

Any later authorized helper-only implementation must preserve this authority hierarchy:

1. Live Git branch/HEAD/tag observations establish repository-state facts.
2. Tracked planning, GO Decision, verification evidence and closeout/archive records establish lifecycle permission and exact file allowlists.
3. Explicit command parameters may request display/task context only; they must not override missing or conflicting tracked authority.
4. `.agent_tasks/**` inputs/outputs are operational convenience files only and must never grant tracked authority.
5. Any conflict, missing prerequisite or stale local/default context fails closed to read-only/NO-GO guidance.

CC-Panes and integration boundary:

```text
CC-Panes remains a human-facing operating interface only.
No helper behavior may automatically create, navigate, focus, inject prompts into or otherwise control CC-Panes panes.
AO, Maestro and all external orchestrator integration are NO-GO for Step 9.
No helper behavior may merge, tag, push or enter Step 10.
```

## 8. Explicit NO-GO Surfaces and Actions

### 8.1 Prohibited in this documentation-drafting task

This branch may add the GO Decision document only. It must not modify or execute:

```text
tools/agentctl.local.ps1
.agent_tasks/**
web-flask/**
web-vue/**
other/model_train/detect/**
.ccpanes/**
.omx/**
runtime/**
DB/schema/data files
Docker/deployment/storage-structure files
API/JWT/auth/login/detection_result/metrics/model contract surfaces
```

It must not perform implementation, helper/build/test/verification execution, CC-Panes control, external-orchestrator integration, merge, tag, push or Step 10 work.

### 8.2 Prohibited in any later implementation unless a new decision changes scope

A later implementation authorized from this decision remains prohibited from changing every surface above except the single allowlisted helper path `tools/agentctl.local.ps1`. In particular, Backend, Frontend and AI implementation remain NO-GO, and Docs/Test documents remain separately authorized evidence/decision activities rather than implementation scope.

## 9. Future Validation / Evidence Requirements (Not Executed Here)

This document specifies future proof obligations only. It does not authorize helper execution, builds, tests, verification output, evidence-file creation or implementation in the present task.

After a separately authorized helper-only implementation, a separately authorized review/evidence activity must prove at minimum:

1. implementation diff changes only `tools/agentctl.local.ps1`;
2. the helper parses successfully and the authorized lifecycle changes are reviewable;
3. current merged-planning state (`master@0b0adfd` plus Step 8 stable tag `3c00a1e`) produces NO-GO until this GO authority is actually reviewed/merged and an implementation task is opened;
4. live-authority conflict/missing-record cases fail closed rather than exposing stale Step 8 implementation permission;
5. `planning`, `read-only`, `go`, `implementation`, `review` and `evidence` contexts retain explicit stage boundaries;
6. display-only informational paths and dispatch do not write local task state or control CC-Panes;
7. any separately authorized write-producing local prompt/result validation is disclosed and does not establish tracked authority;
8. Backend/Frontend verification remains classified as write-producing and is not represented as read-only inspection;
9. no protected application, model, runtime, contract, `.ccpanes/**` or `.omx/**` surface changed;
10. merge, tag, push and Step 10 remain separately gated.

## 10. Required Review and Lifecycle Sequence

| Sequence | Allowed activity | Hard stop |
|---|---|---|
| Current activity | Draft this single tracked GO Decision document on `batch4-step9-docs-workflow-go`. | No helper edit/execution; no implementation; no merge/tag/push; no Step 10. |
| Separate Leader review | Review this documentation artifact against planning and the three read-only results. | Review alone does not authorize changing files outside a separately issued task. |
| Separate GO merge decision | If accepted, merge this document only under separate authorization. | Merge is not performed by this drafting task; no tag/push is implied. |
| Separate implementation task | After merged GO authority, optionally edit only `tools/agentctl.local.ps1` in an isolated implementation branch/worktree. | Any additional file need is NO-GO and requires a new decision. |
| Separate review/evidence activity | Review the helper-only diff and create only separately authorized evidence documentation. | No silent implementation fix; no tag/push/Step 10. |
| Later closeout/tag decision | Consider lifecycle closeout/tag only after reviewed evidence and new authorization. | Push and Step 10 remain prohibited until expressly opened. |

## 11. Risks and Mitigations

| Risk | Required mitigation |
|---|---|
| Closed Step 8 defaults appear to grant current implementation authority. | Resolve live lifecycle from Git/tag plus tracked documents; fail closed when authority is absent or inconsistent. |
| Local prompts/results are misread as durable permission. | Classify `.agent_tasks/**` as local operational state only and require tracked reviewed authority for each gate. |
| Dispatch convenience becomes pane automation or implicit execution. | Keep output display-only and prohibit all CC-Panes pane control and lifecycle actions. |
| Scope expands into application/model/runtime changes. | Enforce the exact helper-only candidate allowlist and explicit Backend/Frontend/AI NO-GO decisions. |
| Optional functionality enlarges an otherwise minimal correction. | Exclude `watch` from this minimal scope; require a new decision if later justified. |
| Decision drafting is mistaken for implementation entry. | Keep current task document-only and record implementation as not entered/not authorized before separate review/merge. |

## 12. Rollback and Current Authorization State

Rollback baseline entering this decision:

```text
phase2b-batch4-step8-local-workflow-stable -> 3c00a1e
```

Rollback treatment:

- abandon or revert only this isolated docs-only decision commit if the decision is rejected before any separately authorized merge;
- no helper, application, database, runtime, model or contract rollback is required for this drafting task because those edits are prohibited;
- any future authorized Step 9 helper implementation must be independently revertible as a single-file helper change;
- no Step 9 stable tag or push is created or authorized here.

Current authorization state at completion of this draft:

```text
Step 9 planning: MERGED at master HEAD 0b0adfd
Step 9 GO Decision: DRAFTED ON ISOLATED DOCS/WORKFLOW BRANCH ONLY
Step 9 implementation: NOT ENTERED / NOT AUTHORIZED BEFORE SEPARATE REVIEW AND MERGE
Candidate implementation allowlist after separate review/merge: tools/agentctl.local.ps1 only
Backend implementation: NO-GO
Frontend implementation: NO-GO
AI Agent: NOT REQUIRED
Docs/Test: separately authorized decision/evidence documents only; no implementation
Helper modification/execution in this task: NOT PERFORMED / NOT AUTHORIZED
.agent_tasks/** modification in this task: NOT PERFORMED / NOT AUTHORIZED
Business code / .ccpanes/** / .omx/** modification: NOT PERFORMED / NOT AUTHORIZED
Merge: NOT PERFORMED / NOT AUTHORIZED IN THIS TASK
Step 9 stable tag: NOT CREATED / NOT AUTHORIZED IN THIS TASK
Push: NOT DONE / NOT AUTHORIZED IN THIS TASK
Step 10: NOT AUTHORIZED / NOT ENTERED
```

## 13. Post-Tag Archive Addendum (2026-05-25)

The authorization block above records the state of this GO Decision at drafting time. Its bounded helper-only implementation was subsequently reviewed, merged and closed through tracked evidence before stable tagging.

```text
Step 9 status: VERIFIED / STABLE TAG CREATED
Step 9 stable tag: phase2b-batch4-step9-local-agent-orchestration-v2-stable -> b05faa8
current tag commit: b05faa8
implementation merge commit: bf90654 Merge Phase 2B Batch4 Step9 control-plane orchestration v2
verified implementation artifact: tools/agentctl.local.ps1 only
post-tag archive commit at start of this docs update: NOT CREATED
post-tag archive outcome: this docs-only archive commit advances HEAD beyond the tag commit after commit
push: NOT DONE
new tag created by this archive update: NO
business code modified after tag: NO
tools/agentctl.local.ps1 modified after tag: NO
FLOATING_OBJECT_PROJECT_CONTEXT_MASTER.md: NOT FOUND; NOT CREATED
Step 10: NOT AUTHORIZED
next allowed step: Phase 2B Batch4 Step 10 Planning / Gate only; direct implementation is NOT AUTHORIZED
```

This post-tag archive addendum does not widen the GO Decision, modify its sole implementation artifact, push, create another tag, or authorize Step 10 implementation.
