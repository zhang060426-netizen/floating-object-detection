# Phase 2B Batch4 Step 10 Disposable Sandbox Test Execution Authorization / Gate

Status: **GO FOR SEPARATELY ASSIGNED SANDBOX-ONLY EXECUTION / NO MAIN-PROJECT RUNNER / NO IMPLEMENTATION**
Date: 2026-05-25
Owner: Project Leader
Scope: Authorization boundary for a later, minimal synthetic OMX behavior test in one disposable standalone repository.

## 0. Authorization Decision Summary

```text
Step 10 direction: Local Agent Automation Bridge v1
Authorized future activity: disposable sandbox test execution only
Authorized sandbox path: E:\MM\omx-runner-sandbox
Execute sandbox test during this documentation task: NO
Run omx exec / omx exec inject / omx team in the main project: NO-GO
Step 10 implementation: NOT AUTHORIZED
Step 11: NOT AUTHORIZED
External hosted-remote push: NOT DONE
```

This gate authorizes only a later separately assigned test activity confined to a disposable sandbox repository. It does not authorize creating or running that sandbox in this documentation task, changing the main project, implementing an automation bridge, or progressing to a later step.

## 1. Baseline And Authority

### 1.1 Main-project baseline at authorization drafting

```text
main project: E:\MM\floating-object-detection
HEAD before this authorization document: cea0cd6 Clarify Batch4 Step10 planning push state
Step 10 planning review: PASS
Step 10 read-only scan / sandbox-test planning evidence review: PASS
Step 9 stable tag:
  phase2b-batch4-step9-local-agent-orchestration-v2-stable -> b05faa8
local clone tracking before this document:
  master...origin/master [ahead 1]
origin meaning:
  local Chinese-path source repository, not an external hosted remote
external hosted-remote push: NOT DONE
Step 10 implementation: NOT AUTHORIZED
Step 11: NOT AUTHORIZED
```
### 1.2 Authority hierarchy

Git facts and tracked reviewed gate records remain authoritative. Local `.agent_tasks/**` inputs/results and any future sandbox output are observational inputs only. Neither process completion, generated output, OMX state, nor a passing sandbox test may create implementation permission, authorize a merge/tag/push, or open Step 11.

## 2. Evidence Supporting This Gate

This authorization is grounded in:

- `agent_outputs/docs/PHASE2B_BATCH4_STEP10_LOCAL_AGENT_AUTOMATION_BRIDGE_PLANNING.md`;
- local-only Control-Plane output `.agent_tasks/outbox/control_plane_step10_omx_readonly_scan_result.md`;
- local-only Docs/Test output `.agent_tasks/outbox/docs_step10_sandbox_plan_result.md`;
- Project Leader review accepting those two result files as planning evidence only.

The Control-Plane scan characterized installed OMX help surfaces but did not execute main-project `omx exec` or `omx team` tasks. The Docs/Test result designed an independent synthetic sandbox plan but did not create or run a sandbox.

## 3. Mandatory Safety Finding: `.omx/**` Is A Write-Risk Surface

During the main-project OMX help/read-only scan, verification detected transient tracked `.omx/**` side effects:

```text
.omx/metrics.json             last_activity timestamp changed
.omx/state/hud-state.json     deleted
.omx/state/session.json       deleted
```

Those three tracked paths were restored to the clean starting baseline, and the read-only scan did not isolate which individual command caused the effects. The safety conclusion is nevertheless binding:

1. OMX probing in the main project cannot be presumed write-free, even when the intended action is help/status discovery.
2. Future OMX behavioral validation must be confined to a disposable sandbox repository.
3. The sandbox test must inventory `.omx/**`, state, logs, worktrees and any other tool-created or tool-deleted path as first-class output.
4. Any unanticipated write or deletion is a test finding requiring review, not an acceptable invisible runtime detail.

## 4. Authorized Sandbox Boundary

### 4.1 Single allowed execution root

The only directory authorized for a later sandbox execution activity is:

```text
E:\MM\omx-runner-sandbox
```

It must be created, if later assigned, as an independent disposable Git repository. It must not be:

- a worktree, clone, branch, nested directory, linked checkout or copied subset of `E:\MM\floating-object-detection`;
- connected to main-project branches, tags, local queues or OMX state;
- treated as durable product code or an implementation branch.

### 4.2 Synthetic-only content

The sandbox may contain only minimal synthetic instructions, synthetic inbox/outbox fixtures and evidence captures necessary for the approved tests. It must not copy or reference main-project:

- source code, documentation payloads or configuration;
- data, database/schema content, storage content or datasets;
- Docker/deployment/runtime files;
- models, weights, classes, inference/training/AI outputs;
- `.omx/**` content;
- `.agent_tasks/**` content;
- credentials, tokens, secrets, API/JWT/shared-contract payloads or `detection_result.v1` samples.

Test fixture text must be created from scratch and use unmistakably synthetic tokens.

### 4.3 Repository and publication boundary

The sandbox must begin with no configured remote. The sandbox activity is prohibited from:

- creating commits;
- merging;
- creating, deleting or moving tags;
- adding a publication remote;
- pushing or publishing output anywhere.

If a later proposal requires a local-only remote fixture, it requires a separate reviewed authorization and is outside this gate.

## 5. Strict Main-Project NO-GO

The following remain prohibited in `E:\MM\floating-object-detection`:

- do not run `omx exec`, `omx exec inject` or `omx team` tasks or behavioral tests;
- do not use the main project as an OMX runner target, working directory, fixture source or state sink;
- do not modify `tools/agentctl.local.ps1`;
- do not modify `.agent_tasks/**`;
- do not modify `.ccpanes/**` or `.omx/**`;
- do not modify `web-vue/**` or `web-flask/**`;
- do not modify DB/schema/data, Docker/deployment, runtime/storage, model/weights/classes/training/inference/AI behavior, API/JWT/shared contracts or `detection_result.v1`;
- do not merge, tag or push;
- do not enter Step 10 implementation;
- do not authorize or enter Step 11.

Any future import of sandbox evidence into this main project requires a separate, documentation-only authorization and review.

## 6. Minimal Future Sandbox Execution Allowlist

Only a later expressly assigned sandbox execution may perform the following within `E:\MM\omx-runner-sandbox`:

| Allowed future sandbox activity | Limit |
|---|---|
| Create the standalone sandbox directory and initialize an isolated Git repository | Sandbox root only; no remote; no commit. |
| Create synthetic manifest/inbox/outbox/evidence files | Synthetic-only content; no main-project copies. |
| Capture pre/post state evidence | Read and record Git status/log/tag/remote data and recursive file state within the sandbox. |
| Run one minimal `omx exec` synthetic inbox-to-outbox observation | Sandbox working directory only; declared synthetic output plus fully inventoried tool state. |
| Evaluate whether `omx team` can be tested | Run only if Windows/tmux/psmux/runtime prerequisites are established within the authorized test protocol; otherwise record `NOT EXECUTED`. |
| Run a minimal `omx team` synthetic independent-task observation, only if prerequisites pass | Sandbox only, unique owned outputs, no conflict with main-project paths. |
| Record write/delete/modify side effects | Inventory all sandbox-visible paths, including tool state/log/worktree artifacts. |

Not authorized in this minimal execution scope:

- `omx exec inject` behavioral testing;
- automatic collection/review orchestration;
- failure/timeout/cancellation expansion beyond a separately reviewed follow-up assignment;
- any modification of the main project.

## 7. Required Test Cases

### 7.1 Sandbox baseline and preflight

Before any OMX runner action, the later executor must establish:

- resolved working directory equals `E:\MM\omx-runner-sandbox`;
- the repository is standalone and contains synthetic content only;
- `git remote -v` is empty;
- no commit or tag exists unless repository initialization behavior makes an unborn branch explicit;
- no path resolves into, links to, or copies from the main project;
- all intended writes and evidence locations are declared in advance.

If any preflight item fails, stop and record `NO-GO / NOT EXECUTED`.

### 7.2 Minimal `omx exec` observation

The single-run synthetic case must test only whether `omx exec` can:

1. read one explicitly named synthetic inbox fixture;
2. write one explicitly named synthetic outbox result;
3. return an observable terminal outcome;
4. leave no commit, tag, push, remote addition or gate authority;
5. expose every additional file/state/log/write/delete/modify side effect for review.

Success means only that observation evidence was captured. It is not implementation authority.

### 7.3 Conditional `omx team` observation

The later executor must first determine whether `omx team` prerequisites are available in the sandbox execution environment, including any Windows/tmux/psmux dependency needed by the installed OMX contract.

```text
If prerequisites are not satisfied:
  omx team outcome: NOT EXECUTED
  record the missing prerequisite and stop that lane safely.
```

If prerequisites are satisfied and the separately assigned execution task includes the team lane, the test may run two independent synthetic tasks with unique result outputs. It must demonstrate attribution and inventory side effects. It must not attempt implementation, main-project execution, merge, tag or push.

## 8. Mandatory Evidence Capture Per Test

For each executed test case, capture pre-test and post-test evidence in the sandbox:

| Required evidence | Requirement |
|---|---|
| `git status --short` | Record before and after each test. |
| `git log --oneline --decorate` | Record before and after each test, including unborn/no-commit state where applicable. |
| `git tag --list` | Record before and after each test. |
| `git remote -v` | Record before and after each test; expected state is empty. |
| Full file mutation inventory | Record every created, deleted or modified file/path, with classification as declared or unexpected. |
| `.omx/**`, state and logs | Record all presence, creation, modification or deletion, including timestamp-only mutation. |
| Worktree and auxiliary paths | Record any worktree, temp, task, cache, trace or process-associated directory disclosed or observed. |
| Lifecycle effects | Record whether any commit, tag, push, remote, merge, implementation action or later-step action occurred; required expected answer is `NO`. |
| `omx exec` behavior | Record whether the synthetic inbox was read and declared synthetic outbox was written. |
| `omx team` behavior | Record test evidence if prerequisites permit execution; otherwise record `NOT EXECUTED` and reason. |

Any write or deletion outside declared sandbox evidence/output paths is an observed risk requiring Leader review. It must not be erased from the evidence record merely because the sandbox is disposable.

## 9. Acceptance Criteria And Fail-Closed Rules

| Gate question | Required result |
|---|---|
| Was every executed command scoped to the sandbox? | PASS required; any main-project target is failure. |
| Were fixtures synthetic-only and independent? | PASS required. |
| Did `omx exec` produce deterministic declared synthetic evidence? | Record PASS/FAIL with full side-effect inventory. |
| Was `omx team` handled safely? | PASS with bounded sandbox evidence, or `NOT EXECUTED` with prerequisite explanation. |
| Were `.omx/**`, state, logs and worktrees inventoried? | PASS required for any executed OMX lane. |
| Did any commit, merge, tag, push or remote appear? | Must be NO; otherwise fail. |
| Did any main-project file or state change? | Must be NO; otherwise fail and stop. |
| Does output claim GO for implementation or Step11? | Must be NO; sandbox output remains observation only. |

The future sandbox execution fails closed if:

- any command points at the main project;
- any unrecorded or unexplained write occurs;
- any commit/tag/push/remote/merge action occurs;
- tool state cannot be inventoried adequately;
- results are represented as implementation authority;
- prerequisites for a lane are absent or uncertain.

## 10. Required Future Result And Review Boundary

A later sandbox execution assignment must produce a reviewable evidence result identifying:

- exact commands executed and resolved sandbox working directory;
- pre/post captures required by Section 8;
- synthetic inputs and outputs;
- complete side-effect inventory, emphasizing `.omx/**`, state, logs and worktrees;
- `omx exec` result;
- `omx team` result or `NOT EXECUTED` rationale;
- proof of no main-project modification, no commit/tag/push/remote/merge, no implementation and no Step11 action;
- a recommendation for the next gate only.

The Project Leader must review that result before any further Step10 proposal. A successful sandbox result may support a later implementation GO Decision draft, but it cannot itself authorize implementation.

## 11. Rollback And Disposal Boundary

This authorization document adds no executable implementation and creates no sandbox. If this gate is rejected, revert only this authorization-document commit through normal reviewed Git process.

For a later authorized sandbox execution:

- preserve unexpected-write evidence until review is complete;
- delete or retain `E:\MM\omx-runner-sandbox` only after a reviewed retention/disposal decision;
- never use cleanup of the sandbox as a reason to alter the main project.

The functional/control-plane rollback marker remains:

```text
phase2b-batch4-step9-local-agent-orchestration-v2-stable -> b05faa8
```

## 12. Explicit Status After This Document

```text
Authorization document creation: documentation only
Sandbox repository created now: NO
Sandbox OMX behavior tests run now: NO
Main-project omx exec / omx exec inject / omx team run now: NO
tools/agentctl.local.ps1 modification: NO
.agent_tasks/** modification: NO
web-vue/** / web-flask/** modification: NO
.ccpanes/** / .omx/** modification: NO
DB / Docker / runtime / model modification: NO
Merge: NO
Tag: NO
External hosted-remote push: NOT DONE
Step 10 implementation: NOT AUTHORIZED
Step 11: NOT AUTHORIZED
```
