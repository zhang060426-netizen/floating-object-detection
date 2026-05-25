# Phase 2B Batch4 Step 10 Disposable Sandbox Test Round2 Authorization / Gate

Status: **GO FOR SEPARATELY ASSIGNED SANDBOX-ONLY ROUND2 PARAMETER CORRECTION TEST / NO MAIN-PROJECT RUNNER / NO IMPLEMENTATION**
Date: 2026-05-25
Owner: Project Leader
Scope: Authorization boundary for one later minimal `omx exec` parameter-correction observation within the existing disposable standalone sandbox repository.

## 0. Authorization Decision Summary

```text
Step 10 direction: Local Agent Automation Bridge v1
Authorized future activity: disposable sandbox-only Round2 parameter correction test
Authorized sandbox path: E:\MM\omx-runner-sandbox
Round2 objective: retry one synthetic inbox-to-outbox observation using only help-supported omx exec / codex exec parameters
Execute Round2 during this documentation task: NO
Run omx exec / omx exec inject / omx team in the main project: NO-GO
Test omx exec inject in Round2: NO-GO
Run omx team in Round2: NO-GO unless tmux/psmux prerequisites are separately proven and separately authorized
Step 10 implementation: NOT AUTHORIZED
Step 11: NOT AUTHORIZED
External hosted-remote push: NOT DONE
```

This document authorizes only a later separately assigned Round2 observation in the disposable sandbox. It does not itself run a test, modify the sandbox, implement a bridge, authorize main-project OMX execution, or open any later lifecycle stage.

## 1. Baseline And Prior Evidence

### 1.1 Main-project authority baseline

```text
main project: E:\MM\floating-object-detection
HEAD before this Round2 authorization document: efcb053 Authorize Batch4 Step10 disposable sandbox test execution
Step 10 planning review: PASS
Step 10 read-only scan / sandbox-test planning evidence review: PASS
Disposable Sandbox Test Execution Authorization review: PASS
Step 9 stable tag:
  phase2b-batch4-step9-local-agent-orchestration-v2-stable -> b05faa8
external hosted-remote push: NOT DONE
Step 10 implementation: NOT AUTHORIZED
Step 11: NOT AUTHORIZED
main-project omx exec / omx exec inject / omx team: NO-GO
```

### 1.2 Round1 observation accepted as evidence only

The reviewed Round1 local-only result records:

```text
sandbox path: E:\MM\omx-runner-sandbox
omx exec: attempted once
task result: DID NOT COMPLETE inbox-to-outbox
failure reason: --ask-for-approval was forwarded to codex exec, was unsupported, and caused exit code 2 before synthetic task execution
synthetic outbox result: .agent_tasks/outbox/synthetic_result.md ABSENT
omx exec inject: NOT EXECUTED
omx team: NOT EXECUTED because native Windows lacked tmux/psmux on PATH
commit/tag/push/remote/additional worktree: NONE
Step 10 implementation / Step 11: NOT ENTERED
```

Round1 also demonstrated sandbox-local OMX side effects on the failed execution path, including `.omx/metrics.json`, `.omx/logs/**`, and lifecycle-created/removed state artifacts. Those effects are observation evidence and remain mandatory inventory surfaces in Round2.

### 1.3 Authority rule

Round1 evidence and all future Round2 results are observational inputs only. A successful synthetic result does not authorize Step10 implementation, main-project runner use, merge/tag/push, or Step11.

## 2. Authorized Round2 Sandbox Boundary

### 2.1 Single allowed execution root

Round2 may be executed only in the existing standalone disposable sandbox:

```text
E:\MM\omx-runner-sandbox
```

The later executor must confirm that all Round2 commands execute with the sandbox as resolved working directory and that no path targets `E:\MM\floating-object-detection`.

### 2.2 Synthetic-only restriction

Round2 may use only the sandbox's synthetic fixtures and sandbox-local evidence/output paths. It must not copy, import or reference main-project:

- source code or documentation content;
- data, database/schema or storage content;
- application/runtime/deployment/Docker configuration;
- models, weights, classes, training/inference/AI outputs;
- `.omx/**` content;
- `.agent_tasks/**` content;
- credentials, secrets, API/JWT/shared-contract payloads or `detection_result.v1` samples.

### 2.3 Git and publication restriction

Within the sandbox and main project, Round2 is prohibited from:

- creating commits;
- merging;
- creating, deleting or moving tags;
- configuring or adding remotes;
- pushing or otherwise publishing output.

## 3. Strict Main-Project NO-GO

The following remain prohibited in `E:\MM\floating-object-detection`:

- do not run `omx exec`, `omx exec inject` or `omx team` tasks, help-driven retries or behavioral tests;
- do not use the main project as a working directory, prompt source, fixture source, result path, OMX state location or temp location;
- do not modify `tools/agentctl.local.ps1`;
- do not modify `.agent_tasks/**`;
- do not modify `.ccpanes/**` or `.omx/**`;
- do not modify `web-vue/**` or `web-flask/**`;
- do not modify DB/schema/data, Docker/deployment, runtime/storage, model/weights/classes/training/inference/AI behavior, API/JWT/shared contracts or `detection_result.v1`;
- do not merge, tag or push;
- do not enter Step 10 implementation;
- do not authorize or enter Step 11.

Any later import of Round2 evidence into the main project requires a separate documentation-only task.

## 4. Round2 Minimal Execution Allowlist

A later separately assigned Round2 execution task may perform only the following within `E:\MM\omx-runner-sandbox`:

| Allowed future activity | Limit |
|---|---|
| Capture starting sandbox state | Read-only state evidence required by Section 6. |
| Run `omx exec --help` | Help comparison only; sandbox working directory and sandbox-local OMX/temp roots must be used if required to contain observed state. |
| Run `codex exec --help` | Help comparison only; identify parameters supported by delegated Codex CLI. |
| Record help comparison | Explicitly record why `--ask-for-approval` is excluded and which parameters, if any, are help-supported for one retry. |
| Run one minimal corrected `omx exec` observation | At most one retry, sandbox only, targeting the existing synthetic inbox-to-outbox observation. |
| Capture ending sandbox state and side effects | Record every created/deleted/modified path and lifecycle outcome. |

Round2 does not authorize:

- any second retry after the one corrected `omx exec` attempt;
- testing `omx exec inject`;
- running `omx team`;
- broadening synthetic task behavior beyond reading the synthetic inbox and writing the declared synthetic outbox result;
- modifying or cleaning Round1/Round2 evidence before Leader review.

If a future, separate authorization proves tmux/psmux prerequisites and specifically authorizes an `omx team` lane, that work remains outside this Round2 gate.

## 5. Parameter-Correction Requirements

The later Round2 executor must perform the following sequence:

1. Capture the complete pre-test evidence specified in Section 6.
2. Run `omx exec --help` and `codex exec --help` from or for the sandbox context and record the relevant supported option comparison.
3. Confirm explicitly that Round2 will **not** pass `--ask-for-approval` to `codex exec`.
4. If sandbox/approval control is required for the corrected retry, use only parameters whose support is established by the captured `omx exec` / `codex exec` help output.
5. If the help comparison does not establish a valid minimal invocation, record `NOT EXECUTED / PARAMETER CONTRACT UNSATISFIED` and do not run an `omx exec` retry.
6. Otherwise execute exactly one minimal `omx exec` synthetic inbox-to-outbox retry.
7. Capture all post-test evidence and result status.

The corrected retry must not conceal or discard any Round1 evidence already present in the sandbox.

## 6. Mandatory Evidence Capture

Before the help comparison, after help comparison if it writes any observable path, and before/after the one permitted corrected retry if executed, record:

| Evidence item | Required capture |
|---|---|
| Working directory | `pwd`, proving `E:\MM\omx-runner-sandbox`. |
| Working tree | `git status --short`. |
| Commit state | `git log --oneline --decorate -5`, recording unborn/no-commit state when applicable. |
| Tag state | `git tag --list`. |
| Remote state | `git remote -v`; required expected state is empty. |
| Full mutation inventory | Every created, deleted or modified file/path, classified by help comparison, corrected retry, pre-existing Round1 artifact or unexplained effect. |
| OMX lifecycle paths | All `.omx/**`, state, logs, metrics and session artifacts, including timestamp-only change and created-then-deleted paths where observable. |
| Temporary paths | Sandbox-local temp/output/cache paths and any surviving or observed transient effects. |
| Worktree state | All worktrees before and after; required expected outcome is no additional worktree. |
| Synthetic output | Whether `.agent_tasks/outbox/synthetic_result.md` is generated and its synthetic-only content/status. |
| Lifecycle prohibitions | Whether any commit, merge, tag, remote, push, main-project write, implementation action or Step11 activity occurred; required expected result is `NO`. |

All `.omx/**` side effects are reportable evidence, even when expected from Round1 or ordinary lifecycle handling.

## 7. Round2 Acceptance And Stop Conditions

| Question | Required outcome |
|---|---|
| Was Round2 confined to `E:\MM\omx-runner-sandbox`? | PASS required. |
| Were only synthetic sandbox inputs/outputs used? | PASS required. |
| Was `--ask-for-approval` excluded after help comparison? | PASS required for an executed retry. |
| Were only help-supported invocation parameters used? | PASS required for an executed retry. |
| Was at most one corrected `omx exec` retry executed? | PASS required. |
| Was `synthetic_result.md` generated? | Record PASS/FAIL observation; absence does not authorize another retry. |
| Were `.omx/**`, state, logs, temp and worktree effects inventoried? | PASS required. |
| Were commit/merge/tag/remote/push absent? | PASS required. |
| Was main-project runner use or modification absent? | PASS required. |
| Were `omx exec inject` and `omx team` excluded? | PASS required under this authorization. |
| Was implementation or Step11 authority inferred? | Must be NO. |

Fail closed and stop if:

- help comparison cannot prove a valid corrected invocation;
- an attempted retry fails for a new reason;
- a path outside the sandbox is accessed or modified;
- any unrecorded side effect, commit, merge, tag, remote or push is detected;
- any result suggests implementation or Step11 authority.

## 8. Required Round2 Result Boundary

A later Round2 execution task must return local observation evidence identifying:

- exact help commands and the supported-option comparison;
- exact corrected `omx exec` invocation if one retry is performed, with unsupported/sensitive parameters omitted or justified from help output;
- pre/post state and complete mutation inventory from Section 6;
- whether `.agent_tasks/outbox/synthetic_result.md` was generated;
- all `.omx/**`, state, logs, temp and worktree side effects;
- proof of no commit/merge/tag/remote/push;
- proof of no main-project OMX task execution or tracked modification;
- confirmation that `omx exec inject`, `omx team`, Step10 implementation and Step11 remained unexecuted/unauthorized;
- recommendation for a subsequent Leader gate review only.

The Project Leader must review this evidence before any further proposal. Round2 success remains observation evidence only.

## 9. Rollback And Retention

This Round2 authorization document adds no implementation and executes no sandbox activity. If rejected, revert only this document commit through normal reviewed Git process.

The existing sandbox and all Round1/Round2 evidence must remain available for review until a later retention/disposal decision is explicitly made. No cleanup, reset or deletion of sandbox evidence is authorized here.

The functional/control-plane rollback marker remains:

```text
phase2b-batch4-step9-local-agent-orchestration-v2-stable -> b05faa8
```

## 10. Explicit Status After This Document

```text
Round2 authorization document creation: documentation only
Round2 sandbox execution performed now: NO
Main-project omx exec / omx exec inject / omx team run now: NO
Sandbox omx exec inject run now: NO
Sandbox omx team run now: NO
tools/agentctl.local.ps1 modification: NO
.agent_tasks/** modification: NO
web-vue/** / web-flask/** modification: NO
.ccpanes/** / .omx/** modification: NO
DB / Docker / runtime / model modification: NO
Commit in sandbox: NO
Merge: NO
Tag: NO
Remote configuration: NO
Push: NO
Step 10 implementation: NOT AUTHORIZED
Step 11: NOT AUTHORIZED
```
