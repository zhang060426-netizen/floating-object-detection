# Phase 2B Batch4 Step 10 Passive Watch / Outbox-Only Helper-Only Implementation GO Decision

Status: **GO DECISION DRAFTED / REVIEW AND MERGE REQUIRED BEFORE IMPLEMENTATION / NO IMPLEMENTATION IN THIS TASK**

Decision scope: authorize a future, separately executed control-plane/helper-only implementation of bounded passive outbox observation, subject to this document being reviewed and merged first.

## 1. Decision Summary

| Item | Decision |
| --- | --- |
| Step 10 direction | `agentctl` passive watch / outbox-only helper behavior |
| This task | Documentation-only GO Decision commit |
| Future control-plane/helper implementation | **GO only after this GO Decision is reviewed and merged** |
| Tracked implementation allowlist after that gate | `tools/agentctl.local.ps1` only |
| Backend Agent | NOT REQUIRED |
| Frontend Agent | NOT REQUIRED |
| AI Agent | NOT REQUIRED |
| Docs/Test Agent | Evidence only, separately authorized |
| Main-project `omx exec` / `omx exec inject` / `omx team` | NO-GO |
| Step 10 implementation during this task | NOT AUTHORIZED |
| Step 11 | NOT AUTHORIZED |
| External hosted-remote push | NOT DONE |

This document does not modify the helper, execute a runner, or start an implementation lane. File availability observed by any future helper remains operational evidence only and never constitutes `PASS`, `GO`, approval, lifecycle completion, merge authority, tag authority, push authority, or Step 11 authority.

## 2. Baseline And Authority

| Baseline fact | Recorded state |
| --- | --- |
| HEAD before this GO Decision document | `0f16c77 Plan Batch4 Step10 agentctl passive watch feasibility` |
| Step 10 passive watch / outbox-only planning gate review | PASS |
| Step 10 passive watch / outbox-only feasibility evidence review | PASS |
| Step 9 stable tag | `phase2b-batch4-step9-local-agent-orchestration-v2-stable -> b05faa8` |
| Local tracking context before this document | `master...origin/master [ahead 4]`; `origin` points to the local Chinese-path source repository, not an external hosted remote |
| External hosted-remote publication | NOT DONE |

Tracked planning and reviewed GO/verification artifacts remain lifecycle authority. Local-only `.agent_tasks/**` reports, passive availability output, collected summaries, and prepared review prompts are inputs for human review only.

## 3. Basis For The Decision

### 3.1 OMX runner path is paused

The OMX runner direction is not the implementation path for this step:

1. Round1 sandbox observation failed before synthetic inbox-to-outbox work because `--ask-for-approval` was forwarded to `codex exec`, where it is unsupported; the attempt exited with code `2`.
2. Round2 removed that parameter and launched nested Codex, with outer `omx exec` exit code `0`, but synthetic inbox-to-outbox still did not complete. The observed failure remained `windows sandbox: spawn setup refresh`, and `synthetic_result.md` was not generated.
3. The main-project read-only scan observed transient tracked `.omx/**` side effects, including `.omx/metrics.json` modification and `.omx/state/**` deletions before restoration. Sandbox executions also produced sandbox-local OMX runtime artifacts.

Accordingly:

- main-project `omx exec`, `omx exec inject`, and `omx team` remain **NO-GO**;
- Round3 OMX runner testing is not the recommended Step 10 direction;
- no evidence currently supports main-project OMX runner use or an OMX-runner-based Step 10 implementation GO.

### 3.2 Passive outbox observation is more conservative

The proposed helper direction does not launch nested Codex, execute an Agent, control a terminal pane, or invoke OMX. It observes one predeclared outbox result path and reports bounded operational state for manual review.

This reduces risk because it:

- reads only an explicitly declared local result identity;
- stops on timeout, missing, stale, wrong-match, ambiguous, or read-error conditions;
- creates no authority from file presence or content;
- preserves all lifecycle, approval, implementation, merge, tag and push decisions for the Project Leader;
- does not require `.omx/**`, `.ccpanes/**`, product code, DB, Docker, runtime or model changes.

### 3.3 Feasibility evidence supports a helper-only proposal

The accepted Control-plane and Docs/Test feasibility evidence establishes that a future exact-path, bounded, non-authoritative observer is feasible within `tools/agentctl.local.ps1` only, provided a separately reviewed GO Decision and later implementation task enforce the boundaries in this document.

The evidence also establishes that existing `collect` and `review` behavior is write-producing preparation, not passive observation. Those actions must remain explicit, local-only and non-authoritative.

## 4. Future Implementation Authorization Gate

After this GO Decision has been separately reviewed and merged, a later implementation task may authorize changes under this exact tracked allowlist:

```text
tools/agentctl.local.ps1
```

No other tracked implementation file is permitted by this decision. Any tracked documentation, test, evidence, or helper-support file beyond that allowlist requires a separate authorization.

The implementation lane, if later activated, is:

| Lane | Future authorization after review/merge |
| --- | --- |
| Control-plane/helper implementation | GO, limited to the allowlist and minimal behavior below |
| Backend implementation | NOT REQUIRED / NO-GO |
| Frontend implementation | NOT REQUIRED / NO-GO |
| AI/model implementation | NOT REQUIRED / NO-GO |
| Docs/Test work | Evidence only, separately authorized |

Until review and merge occur, **Step 10 implementation remains NOT AUTHORIZED**.

## 5. Minimal Future Helper Behavior

A separately authorized helper implementation may add a `passive watch`, `wait-outbox`, or equivalent subcommand only when it satisfies all of the following:

1. Observe only one predeclared exact result path under `.agent_tasks/outbox/**` per invocation.
2. Validate that the normalized requested path is an exact descendant of the permitted outbox root; do not discover results by glob, basename search, or nearest match.
3. Support bounded waiting with an explicit finite timeout and terminate when the bound is reached.
4. Report an expected result as missing when the exact path does not appear under the declared observation conditions.
5. Detect a stale or pre-existing result rather than presenting it as newly available work.
6. Fail closed on wrong-match, concurrent attribution ambiguity, invalid target, or read error.
7. Treat a valid file appearance only as operational availability for manual inspection.
8. Never infer `PASS`, `GO`, approval, acceptance, lifecycle completion, merge readiness, tag readiness, push readiness, or Step 11 readiness.
9. Never automatically run an Agent or retry a producer.
10. Never invoke `omx exec`, `omx exec inject`, or `omx team`.
11. Never control a CC-Panes pane or any other interactive execution pane.
12. Never automatically send or dispatch a prompt.
13. Never automatically advance a lifecycle state.
14. Never automatically merge, tag or push.
15. Never modify product/business code, `.omx/**`, or `.ccpanes/**`.

Candidate passive operational outcomes may include:

| Outcome | Meaning | Required behavior |
| --- | --- | --- |
| `AVAILABLE` | The exact expected path satisfies the declared freshness rule. | Report for manual review only. |
| `MISSING` | A one-shot observation finds no exact expected path. | Report absence only. |
| `WAITING` | The bounded observation has not reached its deadline. | Continue polling only the exact path. |
| `TIMED_OUT` | The finite deadline expires without an accepted exact result. | Stop and report; do not retry or transition. |
| `STALE_OR_PREEXISTING` | The exact file predates or fails the freshness baseline. | Fail closed pending manual review. |
| `WRONG_MATCH` / `AMBIGUOUS` | Attribution does not match exactly or is uncertain. | Fail closed; do not select a substitute. |
| `INVALID_TARGET` / `READ_ERROR` | The requested target or read operation is unsafe or unreliable. | Stop without inference. |

## 6. Local-Only Write Boundary

Passive observation itself must be read-only and must not create or modify files.

Existing or later-authorized preparation actions remain distinct:

| Action | Permitted local-only output if separately invoked and authorized | Authority boundary |
| --- | --- | --- |
| `collect` preparation | `.agent_tasks/outbox/summary.md` | Preparation only; cannot infer result acceptance or lifecycle status. |
| `review` preparation | `.agent_tasks/inbox[/<PromptSet>]/leader_review.md` | Prompt preparation only; cannot send itself or grant approval. |

Any write-producing verification remains outside passive observation and requires explicit separate authorization and acknowledgement before execution.

## 7. Future Verification Requirements

A later, separately authorized helper implementation must demonstrate:

1. The tracked diff is confined to `tools/agentctl.local.ps1`.
2. Exact-path found, missing, timeout, stale/pre-existing, wrong-match, ambiguous, invalid-target and read-error behavior fails closed as specified.
3. Passive observation itself writes no `.agent_tasks/**`, `.omx/**`, `.ccpanes/**`, product, DB, Docker, runtime or model files.
4. Any explicit local-only `collect` or `review` preparation is independently acknowledged, records its write target, and remains non-authoritative.
5. No Agent, prompt dispatch, CC-Panes control, OMX runner invocation, lifecycle transition, merge, tag or push occurs.
6. All result evidence is reviewed manually before any further gate decision.

These requirements define a later implementation and evidence gate; they do not authorize that work in the present document-creation task.

## 8. Explicit NO-GO

For this GO Decision task, and for any future implementation unless a later authorization explicitly narrows and permits otherwise:

- do not modify `tools/agentctl.local.ps1` in this task;
- do not modify `.agent_tasks/**` in this task;
- do not modify `web-vue/**`;
- do not modify `web-flask/**`;
- do not modify `.ccpanes/**`;
- do not modify `.omx/**`;
- do not modify DB, Docker, runtime or model surfaces;
- do not run main-project or sandbox `omx exec`, `omx exec inject`, or `omx team` in this task;
- do not automatically execute an Agent;
- do not automatically send a prompt or control a pane;
- do not automatically merge, tag or push;
- do not enter Step 10 implementation before this GO Decision is reviewed and merged;
- do not enter or authorize Step 11.

## 9. Gate Outcome

This document records a **conditional GO** for a future helper-only passive watch / outbox-only implementation, restricted to `tools/agentctl.local.ps1`.

The condition is mandatory:

```text
No Step 10 helper implementation authority exists until this GO Decision is separately reviewed and merged.
```

Current state at document drafting:

```text
Main-project OMX runner: NO-GO
Step10 implementation: NOT AUTHORIZED
Step11: NOT AUTHORIZED
External hosted-remote push: NOT DONE
```
