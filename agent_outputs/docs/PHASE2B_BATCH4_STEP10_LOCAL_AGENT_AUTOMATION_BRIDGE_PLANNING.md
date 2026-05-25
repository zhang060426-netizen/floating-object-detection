# Phase 2B Batch4 Step 10 Local Agent Automation Bridge v1 Planning / Gate

Status: **PLANNING ONLY / NO IMPLEMENTATION AUTHORIZED**
Date: 2026-05-25
Owner: Project Leader
Scope: Documentation-only feasibility and gate planning for a bounded local Agent automation bridge built on existing CC-Panes, OMX and `tools/agentctl.local.ps1`.

## 0. Planning Decision Summary

```text
Step 10 recommended direction: Local Agent Automation Bridge v1
Decision in this document: PLAN / EVALUATE ONLY
Use omx exec/team for main-project implementation tasks now: NO-GO
Modify tools/agentctl.local.ps1 now: NO-GO
Modify .agent_tasks/** now: NO-GO
Create Step 10 stable tag now: NO
Push: NOT DONE
Step 11: NOT AUTHORIZED
```

Step 10 may evaluate how a local runner could reduce manual prompt/result copy-paste while retaining the existing human-reviewed gate sequence. This document does not authorize a runner, execute an Agent task, widen write authority, or enter implementation.

## 1. Current Baseline

### 1.1 Live baseline observed before this planning document

The requested pre-planning Git inspection established:

```text
branch: master
HEAD before Step 10 planning document: c892e344cc24c22cf835e1fa47ef9a2bacf4e4d6
HEAD subject: Archive Batch4 Step9 stable tag
working tree before Step 10 planning document: clean
latest Step 9 stable tag:
  phase2b-batch4-step9-local-agent-orchestration-v2-stable -> b05faa8
push: NOT DONE
Step 10 implementation: NOT AUTHORIZED
```

The authoritative source baseline is the archived Step 9 state recorded in:

- `PROJECT_CONTEXT.md` (Step 9 post-tag archive);
- `README.md` (Step 9 post-tag archive);
- `agent_outputs/docs/PHASE2B_BATCH4_MASTER_PLANNING_GATE.md` (Step 9 post-tag archive at its closing section);
- `agent_outputs/docs/PHASE2B_BATCH4_STEP9_LOCAL_AGENT_ORCHESTRATION_V2_CLOSEOUT.md` (post-tag addendum);
- `agent_outputs/docs/PHASE2B_BATCH4_STEP9_LOCAL_AGENT_ORCHESTRATION_V2_VERIFICATION_EVIDENCE.md` (post-tag addendum).

### 1.2 Baseline interpretation

The latest safe rollback marker is the Step 9 stable tag, not this planning file. Step 10 begins only as a documentation gate above a verified control-plane baseline. No inference may be made that an automation bridge exists or that it may execute work in this repository.

## 2. Step 9 Clean Closeout State

Step 9 is fully closed and provides the entry boundary for this planning activity:

```text
Step 9 scope: Local Agent Orchestration v2 / control-plane helper only
Step 9 status: CLOSED / VERIFIED / STABLE TAG ARCHIVED
implementation merge commit: bf90654
verification evidence / stable tag target: b05faa8
verified implementation artifact: tools/agentctl.local.ps1 only
final verification before tag: PASS
Step 10 negative checks: PASS / NO-GO retained
.agent_tasks/** modification during final informational/negative verification: NO
tools/agentctl.local.ps1 modified after tag: NO
business code modified after tag: NO
push: NOT DONE
Step 10 implementation: NOT AUTHORIZED
```

The Step 9 evidence is material to Step 10 because it confirms the present helper fails closed for unauthorized future-step implementation requests, does not automate pane control/merge/tag/push, and does not treat `.agent_tasks/**` output as authority.

## 3. Step 10 Recommended Direction

Recommended direction:

```text
Local Agent Automation Bridge v1
```

Purpose: evaluate a narrow bridge that could eventually invoke already-authorized local Agent tasks and retrieve their outputs with less user copy/paste, using existing local components:

- CC-Panes remains the human-facing operating surface;
- OMX is evaluated as an execution/inspection primitive only;
- `tools/agentctl.local.ps1` remains the possible bounded control-plane entry point;
- `.agent_tasks/inbox/**` and `.agent_tasks/outbox/**` remain candidate local operational queue boundaries;
- Git-tracked planning, GO decisions, verification and closeout records remain the only lifecycle authority.

This direction is preferable only if it can preserve all existing gates and default to fail-closed behavior. It is not a decision to implement automation.

## 4. Why AO / Maestro Is Not Used Now

Direct AO / Maestro integration is not appropriate for Step 10 planning:

1. **Scope discipline:** the open question is whether existing local tools already provide sufficient bounded automation; adding an orchestration layer before that evidence would expand scope prematurely.
2. **Authority clarity:** Step 9 deliberately made tracked Git/gate artifacts authoritative and local operational outputs non-authoritative. A new external controller would introduce additional lifecycle/state interpretation risk before the local model is proven.
3. **UI/control risk:** automatic external control of CC-Panes panes is explicitly prohibited for this step.
4. **Rollback simplicity:** a possible future single-helper change is far easier to review and revert than an external orchestration integration.
5. **Evidence first:** behavior of OMX single-task, multi-worker, injection and read-only primitives must be characterized in an isolated sandbox before evaluating any broader platform.

Therefore AO / Maestro remains outside Step 10, with no integration task, dependency, runtime, configuration or pane automation authorized.

## 5. Why OMX Primitives Must Be Evaluated

OMX surfaces are candidates, not approved dependencies of a runner. Each must be assessed against a fail-closed local workflow:

| OMX surface | Question to evaluate | Potential benefit | Required safety finding before any GO |
|---|---|---|---|
| `omx exec` | Can it run one non-interactive Agent task with deterministic exit/result reporting? | Candidate `run-agent` primitive that removes manual prompt paste. | Must prove isolated task scope, explicit working directory, result capture, timeout/cancel handling and no undeclared main-repo writes. |
| `omx exec inject` | Can it append a bounded instruction to a running authorized task? | Candidate controlled follow-up/correction path. | Must prove it targets only an explicitly identified run, records injected instructions, cannot silently widen authority, and is not used as pane control. |
| `omx team` | Can it safely start multiple bounded workers for independent tasks? | Candidate `run-team` primitive for future parallel read-only or separately authorized lanes. | Must prove role/file isolation, deterministic collection, conflict behavior and that a worker cannot infer merge/tag/push or next-step authority. |
| `omx sparkshell` | Can it execute bounded read-only inspection commands without introducing write effects? | Candidate scan/verification helper for status and evidence gathering. | Must classify commands by write effect; only genuinely read-only scans may be considered. |
| `omx state`, `trace`, code-intel and `wiki` | Can these help observe run status and context without becoming authority? | Candidate progress/status/context evidence surfaces. | Must remain observational or explicitly local/supporting; tracked gates and Git facts remain authoritative. No `.omx/**` modification in this planning task. |

Evaluation must distinguish CLI availability/help/contract discovery from runtime behavior. Runtime behavior testing belongs only in a disposable sandbox test repository under a separately reviewed test plan; it must not use this main project to execute `omx exec` or `omx team`.

## 6. Current `agentctl` v2 Capability and Gaps

### 6.1 Capabilities already present at the Step 9 stable baseline

Inspection of `tools/agentctl.local.ps1` and Step 9 evidence shows the current helper already provides:

| Existing capability | Current boundary |
|---|---|
| `status`, `guard`, `next` | Read/display lifecycle and safety information; a request does not confer authority. |
| Six lifecycle stages | `planning`, `read-only`, `go`, `implementation`, `review`, `evidence`. |
| `dispatch` | Displays startup phrases only; no pane control. |
| `write-prompts` | Explicitly writes local-only inbox prompt files when separately intended. |
| `collect` | Explicitly aggregates local-only outbox results and does not infer PASS, approval or lifecycle transition. |
| `review` | Explicitly creates a local-only review prompt; it does not approve or silently fix work. |
| Role vocabulary | `control-plane`, `backend`, `frontend`, `docs-test`. |
| Verification classification | `verify-backend`, `verify-frontend`, and `verify-master` are write-producing and require explicit acknowledgement; `verify-docs` is Git diff/whitespace inspection only. |
| Fail-closed future-step protection | Unauthorized Step 10 implementation directions are rejected or displayed as NO-GO. |
| Safety exclusions | No automatic lifecycle transition, merge, tag, push, CC-Panes pane control or Step 10 implementation. |

### 6.2 Gaps relevant to the proposed bridge

The current helper intentionally does **not** provide:

- a process-owning `run-agent` operation for one authorized task;
- a `run-team` operation or worker lifecycle coordination;
- `omx exec inject` integration or an auditable follow-up instruction path;
- a passive/controlled `watch-outbox` operation;
- a `wait` operation with timeout, exit-code and terminal-state semantics;
- an `auto-review` orchestration that triggers collection/review while stopping before any approval or Git lifecycle action;
- run identifiers, concurrency/conflict policy, cancellation policy or crash recovery evidence;
- validated integration with OMX state/trace/code-intel/wiki;
- sandbox-backed proof that OMX execution primitives preserve the repository and gate boundaries.

These are planning gaps, not implementation defects. Filling any gap would require a later GO Decision with an explicit allowlist.

## 7. Step 10 Candidate Capability Range

The candidate capability range is limited to feasibility analysis and future design:

| Candidate future capability | Intended bounded function | Planning outcome required now | Not authorized now |
|---|---|---|---|
| `run-agent` | Start one explicitly authorized local task via a proven non-interactive mechanism. | Define invocation, input/output contract, timeout/cancel and failure behavior. | No helper edit and no task execution in the main project. |
| `run-team` | Start several independent explicitly authorized tasks after conflict/scope checks. | Define role isolation, concurrency limit and result ownership. | No worker launch in the main project. |
| `wait` | Poll an identified execution until terminal result/timeout. | Define terminal states and non-authoritative evidence format. | No monitoring automation installed. |
| `watch-outbox` | Detect new outbox result files and surface them for collection. | Determine whether polling can be bounded and non-mutating by default. | No watch behavior; Step 9 recorded it as not implemented. |
| `auto-review` | On successful explicit completion, run collect/review preparation only. | Define separation between result collection, review prompt creation and a Leader decision. | No automatic approval, merge, tag, push or next-step opening. |
| context/status assist | Optionally consume OMX observational surfaces for reporting. | Decide what is evidence vs tracked authority. | No `.omx/**` changes or authority transfer. |

### 7.1 Non-negotiable future design rule

Even if later approved, an automation bridge may at most automate **execution convenience and evidence preparation** for a separately authorized task. It must never:

- create its own implementation permission;
- infer GO/PASS from a completed process or outbox file;
- merge branches;
- create/move tags;
- push;
- open a later step;
- automatically operate CC-Panes panes.

## 8. Agent Need Assessment

No Agent is authorized to execute Step 10 work by this document. If a later **read-only feasibility scan** or **sandbox validation plan** is separately approved, the minimal responsibility split is:

| Agent lane | Needed for Step 10 planning/feasibility? | Permitted future contribution, only after separate authorization | Reason |
|---|---:|---|---|
| Project Leader | YES | Gate ownership, evidence review, GO/NO-GO decision. | Maintains lifecycle authority and final manual decision boundary. |
| Control-Plane Agent | YES, for future read-only/sandbox evidence only | Characterize OMX behavior and draft bounded helper capability proposal. | This is a control-plane question, not product implementation. |
| Docs/Test Agent | YES, for future evidence review only | Define/read results, safety matrix, sandbox acceptance evidence and gate record. | Preserves reviewer separation and verifiable closeout discipline. |
| Backend Agent | NO | None in the current scope. Consult only if a later proposal touches backend verification/write classification, which is currently prohibited. | No backend/API/runtime changes are proposed. |
| Frontend Agent | NO | None in the current scope. Consult only if a later proposal touches frontend build/write classification, which is currently prohibited. | No UI or CC-Panes UI automation is proposed. |
| AI Agent | NO | None in the current scope. | No model, inference, training, multimodal or dataset surface is involved. |

The candidate bridge must not be justified by dispatching unused application/AI lanes.

## 9. Read-Only Scan Task Design

Before any implementation GO Decision, a separately authorized read-only evidence pass should answer whether the necessary interfaces exist and how they behave at the contract level.

### 9.1 Read-only scan objective

Produce a documentation-only capability matrix for:

- installed OMX version and locally available command/help surfaces;
- help/usage contract for `omx exec`, `omx exec inject`, `omx team`, `omx sparkshell`, `omx state`, `omx trace`, code-intel and wiki surfaces where available;
- current `agentctl.local.ps1` command/stage/role boundary;
- existing `.agent_tasks/inbox/**` / `.agent_tasks/outbox/**` queue semantics as recorded by tracked evidence, without writing those directories.

### 9.2 Scan rules

| Rule | Requirement |
|---|---|
| Repository write boundary | No writes in this main project; in particular no `.agent_tasks/**`, `.omx/**`, `.ccpanes/**`, helper, product or docs writes during the scan except a separately authorized tracked evidence document after review. |
| OMX execution boundary | Do not execute `omx exec` or `omx team` against this project; discover interface/usage only. |
| Sparkshell boundary | Treat `omx sparkshell` as unproven until isolated testing confirms its read-only behavior; do not use it for a command that may write output/state. |
| State/context boundary | Any OMX state/trace/code-intel/wiki observation is supporting evidence only; no surface supersedes Git/tracked gate records. |
| Result format | Record command availability, documented input/output, observed write risk, unanswered question and proposed sandbox test. |
| Stop condition | Stop at capability evidence and a reviewed recommendation; do not modify the helper or dispatch tasks. |

### 9.3 Proposed read-only evidence output

A future separately authorized evidence file could record:

```text
agent_outputs/docs/PHASE2B_BATCH4_STEP10_LOCAL_AGENT_AUTOMATION_BRIDGE_READONLY_SCAN.md
```

That path is a recommendation only. It is not created or authorized by this planning document.

## 10. Sandbox Test Repository Design Recommendation

### 10.1 Need for a sandbox repository

A disposable sandbox test repository is recommended before any GO Decision because command availability alone cannot prove:

- whether `omx exec` behaves non-interactively and exposes deterministic completion;
- whether injection is targeted, auditable and scope-safe;
- whether team execution writes coordination/runtime state or permits conflicting workers;
- whether sparkshell is read-only for the proposed command set;
- which directories/state surfaces are written in normal, failure, timeout and cancellation cases.

No such behavioral test may be performed in the main project during this step.

### 10.2 Isolation design

The sandbox should be a separate disposable Git repository, not a worktree of the project and not a copy of application secrets/data. Suggested contents:

```text
sandbox-agent-bridge/
  README.md                         # synthetic task and gate rules only
  tools/agentctl.fixture.ps1        # minimal disposable fixture, if separately approved
  .agent_tasks/inbox/               # synthetic prompt inputs only
  .agent_tasks/outbox/              # synthetic result outputs only
  evidence/                         # command transcript and before/after snapshots
```

Isolation requirements:

- no `web-vue/**`, `web-flask/**`, model, runtime, DB, credentials or real dataset content;
- no linkage to main-project branches/tags;
- before/after snapshots of tracked/untracked files and tool-created state;
- explicit deletion/retention decision for sandbox artifacts after evidence review;
- test output imported into the main project only through a separately authorized documentation evidence activity.

### 10.3 Candidate sandbox test matrix

| Test lane | Synthetic test | Expected acceptance condition |
|---|---|---|
| Single runner | One fake inbox task through candidate `omx exec` flow. | Deterministic run identity, terminal result and declared output only; no implicit authority. |
| Injection | Append a harmless correction to an identified running synthetic task. | Instruction is auditable, targets only that run and cannot alter gate/write scope. |
| Team | Two independent synthetic read-only/result tasks. | Results attributable per worker; no shared-file overwrite; conflict case fails closed. |
| Read-only command | Candidate sparkshell invocation for harmless repository inspection. | Before/after snapshot proves no unexpected file/state mutation for the allowed command. |
| Status/context | Observe state/trace/code-intel/wiki availability where present. | Supporting telemetry is distinguishable from tracked authority and its writes, if any, are disclosed. |
| Failure/timeout | Synthetic timeout, non-zero exit and cancellation. | Runner reports explicit terminal state; no automatic retry/approval/merge/tag/push. |
| Collection/review | Synthetic successful outputs followed by proposed collection/review flow. | Can prepare review evidence only; requires Leader decision and performs no lifecycle transition. |

### 10.4 Sandbox evidence threshold

A future GO Decision should be refused unless the sandbox evidence identifies every file/state write, proves failure/timeout behavior, and demonstrates the non-automation boundaries for merge/tag/push/pane control/later-step authorization.

## 11. Queue Boundary: `.agent_tasks/inbox/**` and `.agent_tasks/outbox/**`

It is reasonable to continue evaluating the existing queue directories as the bridge boundary because Step 9 already treats them as local-only operational inputs/outputs:

| Queue area | Candidate future use | Authority rule |
|---|---|---|
| `.agent_tasks/inbox/**` | Explicit task instructions prepared only after authorization. | A file in inbox does not authorize implementation or execution. |
| `.agent_tasks/outbox/**` | Agent result/evidence return channel. | A file in outbox does not imply PASS, approval, merge or next-step entry. |

However:

- this planning document does not change or populate either directory;
- any future automated watcher must be opt-in, bounded and separately reviewed;
- tracked gate documents and Git facts continue to outrank any local queue state;
- any future use must preserve auditability of which task was authorized, started, injected, completed, collected and reviewed.

## 12. Automatic Collect / Review Feasibility Boundary

A future bridge may be worth evaluating if it can, after an explicitly authorized Agent run reaches a terminal result:

1. identify the matching outbox result;
2. prepare an aggregation equivalent to current explicit `collect`;
3. prepare a review prompt equivalent to current explicit `review`;
4. surface both to the Project Leader for a manual decision.

This is the maximum acceptable automation target for Step 10 feasibility. It must **not** automatically:

- mark evidence as PASS;
- approve a diff;
- update lifecycle authority;
- create implementation instructions for an unauthorized step;
- merge;
- tag;
- push.

If result-to-review automation cannot preserve those separations, the bridge direction is a NO-GO.

## 13. GO Decision Prerequisites

Step 10 may be proposed for implementation only after a new, separately reviewed and merged GO Decision demonstrates all of the following:

| Prerequisite | Required evidence |
|---|---|
| Stable baseline preserved | Step 9 stable tag remains a valid rollback point; main-project working tree is clean before any future GO implementation branch. |
| Interface characterization | Documentation-only read-only scan identifies installed OMX commands, invocation contracts and unknowns. |
| Sandbox proof | Disposable test-repo evidence covers single execution, injection if proposed, team if proposed, sparkshell classification, status/context surfaces, failure/timeout and collect/review boundary. |
| Write-effect inventory | Every command and state/output path is categorized as read-only or write-producing; no hidden `.omx/**`, `.agent_tasks/**`, `.ccpanes/**` or product write is overlooked. |
| Authority model | Git/tracked gate artifacts remain sole authority; task queue, OMX state/trace/wiki, process completion and review preparation remain non-authoritative. |
| Minimal implementation allowlist | A future GO Decision explicitly states the smallest tracked file/test/docs allowlist; it must not silently include application, model, runtime, DB, Docker or CC-Panes surfaces. |
| Failure safety | Timeout, cancellation, crashed process, stale outbox, worker conflict and injected-scope violation all fail closed. |
| Human control | Automatic merge/tag/push/pane control/later-step authorization remain prohibited; Leader review remains mandatory. |
| Reviewer separation | A Docs/Test or equivalent independent review evaluates sandbox evidence and any future control-plane diff before closeout. |
| Rollback | Future implementation rollback and cleanup procedure is written before implementation begins. |

Until every prerequisite is met, the decision is:

```text
Can Step 10 enter implementation? NO
```

## 14. Explicit NO-GO

The following are prohibited by this planning gate:

- do not directly use `omx exec`, `omx exec inject` or `omx team` to execute main-project implementation tasks;
- do not enter Step 10 implementation;
- do not modify `tools/agentctl.local.ps1`;
- do not modify `.agent_tasks/**`;
- do not modify `web-vue/**`;
- do not modify `web-flask/**`;
- do not modify `.ccpanes/**`;
- do not modify `.omx/**`;
- do not modify DB/schema/data, Docker/deployment, runtime/storage, model/weights/classes/training/inference/AI behavior, API/JWT/shared contracts or `detection_result.v1`;
- do not integrate AO or Maestro;
- do not automatically create, focus, navigate, inject into or otherwise control CC-Panes panes;
- do not automate merge, tag or push;
- do not create a Step 10 stable tag during planning;
- do not authorize or enter Step 11.

Only this documentation-only planning artifact is authorized in this activity:

```text
agent_outputs/docs/PHASE2B_BATCH4_STEP10_LOCAL_AGENT_AUTOMATION_BRIDGE_PLANNING.md
```

## 15. Rollback Baseline

This document introduces no implementation to roll back. If planning is rejected, revert/remove only this planning-document commit under the normal reviewed Git process.

The protected functional/control-plane restore marker remains:

```text
phase2b-batch4-step9-local-agent-orchestration-v2-stable -> b05faa8
```

No rollback action is performed by this planning task.

## 16. Stable Tag, Push and Later-Step Status

```text
Step 10 stable tag: NOT CREATED / NOT AUTHORIZED DURING PLANNING
push: NOT DONE
Step 11: NOT AUTHORIZED
```

The next permitted activity after this planning document is review of the planning gate and, only if separately authorized, a documentation-only read-only capability scan and/or sandbox-test design/evidence activity. No implementation follows automatically.

## 17. Planning Acceptance Checklist

- [x] Current baseline recorded from clean pre-planning Git state.
- [x] Step 9 closed/verified/stable-tag-archived status recorded.
- [x] Recommended Step 10 direction is Local Agent Automation Bridge v1.
- [x] AO / Maestro exclusion rationale recorded.
- [x] OMX candidate surfaces and proof requirements identified.
- [x] Current `agentctl` v2 capabilities and gaps recorded.
- [x] Candidate future capability range bounded.
- [x] Agent need assessment limits work to appropriate future control-plane/docs-test evidence roles.
- [x] Read-only scan design recorded without running an Agent.
- [x] Disposable sandbox test repository design recommended.
- [x] GO Decision prerequisites and fail-closed default recorded.
- [x] Queue and auto-review boundaries preserve tracked authority.
- [x] Explicit NO-GO, rollback baseline, no-tag/no-push and Step 11 NO-GO recorded.
- [x] No implementation is authorized by this document.
