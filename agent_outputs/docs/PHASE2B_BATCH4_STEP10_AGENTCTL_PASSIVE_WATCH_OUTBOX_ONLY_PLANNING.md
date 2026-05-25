# Phase 2B Batch4 Step 10 Agentctl Passive Watch / Outbox-Only Feasibility Planning Gate

Status: **PLANNING ONLY / PASSIVE OBSERVATION DIRECTION / NO IMPLEMENTATION AUTHORIZED**
Date: 2026-05-25
Owner: Project Leader
Scope: Documentation-only planning for a conservative `tools/agentctl.local.ps1` feasibility direction focused on passive outbox observation and review preparation.

## 0. Planning Decision Summary

```text
Step 10 direction under evaluation: agentctl passive watch / outbox-only feasibility
Why this direction now: omx exec runner route is paused after sandbox evidence
Run main-project omx exec / omx exec inject / omx team: NO-GO
Run additional Round3 omx exec runner tests now: NOT RECOMMENDED
Modify tools/agentctl.local.ps1 now: NO-GO
Step 10 implementation: NOT AUTHORIZED
Step 11: NOT AUTHORIZED
Merge / tag / external hosted-remote push: NOT AUTHORIZED
```

This document narrows Step10 feasibility work to passive visibility and evidence-preparation questions. It does not authorize any helper change, watcher, automated collect/review action, task execution, pane control, lifecycle transition or later-step entry.

## 1. Current Baseline And Authority

### 1.1 Reviewed baseline

```text
main project: E:\MM\floating-object-detection
HEAD before this planning document: fd2033f Authorize Batch4 Step10 disposable sandbox test round2
Step10 Local Agent Automation Bridge planning review: PASS
Step10 OMX read-only scan / sandbox-test planning evidence review: PASS
Round1 sandbox evidence review: PASS / observation evidence only
Round2 fixed sandbox evidence review: PASS / complete observation evidence only
Step9 stable tag:
  phase2b-batch4-step9-local-agent-orchestration-v2-stable -> b05faa8
external hosted-remote push: NOT DONE
Step10 implementation: NOT AUTHORIZED
Step11: NOT AUTHORIZED
```

### 1.2 Authority model

Tracked planning, GO, verification and closeout documents together with live Git/tag facts remain the only lifecycle authority. `.agent_tasks/**` output, any future passive watcher notification, a collected summary, a generated review prompt and any sandbox evidence remain operational or observational inputs only. None may infer PASS, implementation authority, approval, merge, tag, push or Step11 entry.

## 2. Why The OMX Exec Runner Direction Is Paused

Step10 initially evaluated OMX primitives as possible future execution/observation building blocks. The runner route is now paused because reviewed evidence shows that it does not presently provide a reliable conservative local bridge path on this Windows environment.

### 2.1 Round1 parameter compatibility failure

Round1 disposable sandbox observation attempted one synthetic `omx exec` flow. The delegated `codex exec` rejected the forwarded parameter:

```text
--ask-for-approval
```

with exit code `2` before the synthetic inbox task began. No synthetic outbox result was produced.

### 2.2 Round2 nested Windows sandbox execution failure

Round2 first compared `omx exec --help` with `codex exec --help`, removed the unsupported parameter, and performed one permitted corrected sandbox retry. The corrected invocation launched nested Codex and returned outer exit code `0`, but the task still could not complete:

```text
windows sandbox: spawn setup refresh
```

The nested process could not read the synthetic inbox file, and `.agent_tasks/outbox/synthetic_result.md` was not generated.

### 2.3 Unexplained sandbox sessions

Round2 evidence correction also classified two sandbox sessions as:

```text
UNEXPLAINED PRE-ROUND2 SANDBOX ACTIVITY
```

These sessions do not change the observed Round2 failure, but they reinforce that the runner path carries state attribution and observability risk that should not be expanded in the main project.

### 2.4 `.omx/**` write-risk finding

The main-project help/read-only scan detected transient tracked `.omx/**` side effects before they were restored:

```text
.omx/metrics.json             last_activity timestamp changed
.omx/state/hud-state.json     deleted
.omx/state/session.json       deleted
```

Sandbox runner attempts additionally created or modified sandbox-local `.omx/metrics.json`, `.omx/logs/**` and session state paths. This proves OMX calls cannot be treated as a passive no-write mechanism for the main project.

### 2.5 Current conclusion

```text
Main-project omx exec / omx exec inject / omx team: NO-GO
Round3 omx exec runner testing: NOT RECOMMENDED
Step10 implementation based on OMX runner behavior: NOT AUTHORIZED
```

## 3. Why Passive Outbox Observation Is More Conservative

A passive `agentctl` direction differs materially from an OMX runner direction:

| Concern | OMX runner direction | Passive watch / outbox-only feasibility direction |
|---|---|---|
| Starts Agent work | Intended to start or coordinate execution. | Must not start any Agent or create execution authority. |
| External/process lifecycle | Introduces nested CLI/session/runtime behavior. | Observes a pre-existing expected local result path only. |
| `.omx/**` risk | Observed state/log/metrics writes and main-project side effects. | Must not depend on OMX and must not touch `.omx/**`. |
| Permission boundary | Requires proving safe task execution semantics. | May only report file presence/absence and prepare manual-review inputs. |
| Failure behavior | Runtime/process and sandbox failures. | Timeout/missing-result notice only; no automatic retry or task launch. |
| Lifecycle progression | High risk if completion is misread as authority. | Result detection is explicitly non-authoritative and stops at Leader review. |

The intended value is reduction of manual checking, aggregation and review-prompt preparation after separately authorized agents have produced local outbox results. The intended value is **not** automated development-task execution.

## 4. Existing `agentctl` Boundary To Preserve

Current Step9-verified helper behavior already establishes the relevant boundary:

| Existing surface | Current behavior to preserve |
|---|---|
| `status`, `guard`, `next`, `dispatch` | Informational or display-only workflow guidance; no pane control or lifecycle authority. |
| `write-prompts` | Explicit local-only inbox writes only when separately intended. |
| `collect` | Explicit local-only summary generation in `.agent_tasks/outbox/**`; does not infer PASS or approval. |
| `review` | Explicit local-only `leader_review.md` preparation; does not approve or fix work. |
| Verification | `verify-backend`, `verify-frontend` and `verify-master` are write-producing and require separate authorization and explicit acknowledgement. |
| Watch behavior | Not currently implemented; any future watch proposal requires a revised separately reviewed GO Decision. |

No current helper capability is changed by this planning document.

## 5. Candidate Passive Watch / Outbox-Only Capability Range

The following are feasibility topics only. Each would require a future separate GO Decision and exact allowlist before any implementation:

| Candidate future capability | Bounded intended function | Must never do |
|---|---|---|
| `watch-outbox` / passive poll | Wait for one explicitly named expected result file under `.agent_tasks/outbox/**`, then surface found/missing/timeout status. | Must not run an Agent, write prompts, edit the result, or infer PASS. |
| Wait / timeout status | Display elapsed wait, timeout or missing-result notice for an identified expected output. | Must not auto-retry, auto-dispatch or transition lifecycle. |
| Status dashboard | Present expected task/result state, last observed result availability and manual next-step reminder. | Must not become authority or inspect prohibited state. |
| Automatic `collect` preparation | After an explicitly expected result exists, optionally invoke or prepare current local-only aggregation behavior. | Must not approve, merge, tag, push or open later stages. |
| Automatic leader-review prompt preparation | Optionally generate the existing local-only `leader_review.md` prompt after explicit result detection/collection conditions. | Must not silently review, fix, approve or authorize. |

### 5.1 Mandatory conservative rules

Any future passive design must:

- observe only specifically allowlisted `.agent_tasks/outbox/**` result paths;
- be opt-in and bounded by explicit task/result identifiers;
- perform no background task execution;
- perform no OMX invocation;
- perform no CC-Panes pane creation, navigation, injection, focus or control;
- send no prompt automatically;
- stop at notification, collection preparation or review-prompt preparation;
- retain human confirmation for every lifecycle gate;
- preserve explicit authorization for all write-producing verification;
- report timeout/missing/stale output without manufacturing a result.

## 6. Candidate Future Allowlist And Agent Need

### 6.1 Candidate implementation allowlist, if separately approved later

If a subsequent reviewed GO Decision authorizes an implementation proposal, its tracked implementation allowlist may contain only:

```text
tools/agentctl.local.ps1
```

Any tests or evidence documents would require their own explicit scope in that later decision. This planning gate does not authorize edits to the helper or any other tracked file.

### 6.2 Agent responsibility assessment

| Agent lane | Need for passive feasibility planning | Current authorization |
|---|---|---|
| Project Leader | Required for gate ownership and manual decision boundary. | Planning/review only. |
| Control-Plane Agent | Candidate for future read-only helper-boundary analysis and proposal drafting. | Not assigned by this document. |
| Docs/Test Agent | Appropriate for later evidence/checklist review. | Evidence work only after separate authorization. |
| Backend Agent | NOT REQUIRED. | No backend implementation. |
| Frontend Agent | NOT REQUIRED. | No frontend implementation. |
| AI Agent | NOT REQUIRED. | No model/inference/training work. |

## 7. Required Future Feasibility Evidence Before Any GO Decision

Before any passive-watch implementation GO Decision may be proposed, a separately authorized documentation/read-only analysis must define and justify:

1. Exact expected outbox file naming and matching contract.
2. Whether observation is a one-shot check, bounded polling loop or explicit `wait` command.
3. Timeout, cancellation, missing-result and stale-result semantics.
4. What local-only files may be created by collection or review-prompt preparation.
5. How output status is clearly labelled non-authoritative.
6. How concurrent expected results avoid ambiguity or result misattribution.
7. Why no `.omx/**`, `.ccpanes/**`, product, DB, Docker, runtime or model path can be touched.
8. Verification proving no automatic Agent run, prompt sending, pane control, lifecycle transition, merge, tag or push.
9. Rollback instructions limited to the helper-only change if a later implementation is separately approved.
10. Independent Docs/Test evidence review before any completion decision.

## 8. Explicit NO-GO

This planning activity authorizes only this documentation file. It explicitly prohibits:

- do not modify `tools/agentctl.local.ps1`;
- do not run `omx exec`, `omx exec inject` or `omx team`;
- do not modify `.agent_tasks/**` in this planning activity;
- do not modify any tracked file outside this approved planning document;
- do not modify `web-vue/**`;
- do not modify `web-flask/**`;
- do not modify `.ccpanes/**`;
- do not modify `.omx/**`;
- do not modify DB/schema/data, Docker/deployment, runtime/storage, model/weights/classes/training/inference/AI behavior, API/JWT/shared contracts or `detection_result.v1`;
- do not automatically run Agents or send prompts;
- do not automatically control CC-Panes panes;
- do not automatically approve, transition stages, merge, tag or push;
- do not enter Step10 implementation;
- do not authorize or enter Step11.

Only this new planning artifact is authorized for tracked creation:

```text
agent_outputs/docs/PHASE2B_BATCH4_STEP10_AGENTCTL_PASSIVE_WATCH_OUTBOX_ONLY_PLANNING.md
```

## 9. GO Decision Boundary

This document records a safer candidate direction only. It does not constitute a GO Decision for implementation.

Step10 implementation may be considered only after a separately reviewed GO Decision demonstrates:

- OMX runner use remains excluded from the main project;
- passive observation is bounded, opt-in and non-authoritative;
- any proposed local-only collection/review writes are declared;
- all write-producing verification remains explicitly acknowledged;
- the tracked implementation allowlist is confined to `tools/agentctl.local.ps1`;
- no Backend, Frontend or AI implementation is required;
- no `.omx/**`, `.ccpanes/**`, product, DB, Docker, runtime or model modifications are allowed;
- manual Leader gate control remains mandatory.

Until such a separate GO Decision exists:

```text
Step10 implementation: NOT AUTHORIZED
Step11: NOT AUTHORIZED
Main-project omx exec / omx exec inject / omx team: NO-GO
```

## 10. Rollback And Status

This planning document introduces no executable behavior. If rejected, rollback is limited to reverting this documentation-only commit through the normal reviewed Git process.

The protected functional/control-plane restore marker remains:

```text
phase2b-batch4-step9-local-agent-orchestration-v2-stable -> b05faa8
```

Status after this planning document:

```text
Passive watch/outbox-only implementation: NOT AUTHORIZED
tools/agentctl.local.ps1 modification: NO
.agent_tasks/** modification: NO
Main-project OMX runner execution: NO
Automatic Agent execution / prompt dispatch / pane control: NO
Merge / tag / external hosted-remote push: NOT DONE / NOT AUTHORIZED
Step10 implementation: NOT AUTHORIZED
Step11: NOT AUTHORIZED
```
