# Phase 2B Batch4 Step 8 Local Workflow Hardening Implementation GO Decision

Status: **GO DECISION DRAFT / CONTROL-PLANE IMPLEMENTATION CONDITIONALLY AUTHORIZED ONLY AFTER REVIEW AND MERGE**
Date: 2026-05-24
Phase: Phase 2B Batch4 Step 8
Step 8 topic: Local Workflow Hardening
Working branch: `batch4-step8-docs-workflow-go`
Current master HEAD baseline: `1a1aad8` (`Merge Phase 2B Batch4 Step8 planning`)
Stable restore point: `phase2b-batch4-step7-record-filter-stable -> 25c9f43`
Step 8 implementation before GO Decision merge: **NOT AUTHORIZED**
Push: **NOT DONE**
Step 8 tag: **NOT CREATED**

## 1. Decision Summary

```text
Backend implementation: NO-GO
Frontend implementation: NO-GO
Docs/Test evidence: GO only after implementation and separate evidence-file authorization
AI Agent: NOT REQUIRED
Control-plane implementation: CONDITIONAL GO only after this GO Decision is reviewed/merged
Candidate implementation allowlist: tools/agentctl.local.ps1 only
Step 8 implementation before this GO Decision is merged: NOT AUTHORIZED
Merge / tag / push under this drafting task: NO-GO / NOT DONE / NOT CREATED
Step 9 implementation: NOT AUTHORIZED
```

This document is a tracked, docs-only authorization decision artifact. Creating
or committing it does **not** enter Step 8 implementation. If this decision is
later reviewed and merged, it conditionally authorizes a separate, isolated
control-plane implementation activity limited to the single allowlisted helper
file in Section 5. No application, contract, runtime, local-state or evidence
file change is included in that implementation allowlist.

## 2. Baseline Reconciliation and Authority Treatment

### 2.1 Current authoritative Git baseline

| Item | Decision baseline / treatment |
|---|---|
| Current master HEAD | `1a1aad8` (`Merge Phase 2B Batch4 Step8 planning`) is the controlling HEAD baseline for this decision. |
| Planning document baseline | `fd83686` is retained only as the **historical planning baseline** at which the Step 8 planning artifact was prepared; it is not current HEAD. |
| Stable rollback anchor | `phase2b-batch4-step7-record-filter-stable -> 25c9f43` remains the application restore point. |
| Push / Step 8 tag | Push is **NOT DONE**; no Step 8 stable tag has been created or authorized. |

The tracked planning artifact is accepted as the predecessor gate document,
but any statement in it that identifies `fd83686` as current HEAD is superseded
for this decision by the planning-merged HEAD `1a1aad8`.

### 2.2 Local-only operational state is not HEAD authority

The reviewed scan outputs under `.agent_tasks/outbox/**` are inputs to this
decision because they record the local read-only scan and Leader review. The
entire `.agent_tasks/**` surface is nevertheless classified as **local-only
operational state**. It is not authoritative evidence for repository HEAD,
merged implementation scope, stable tag state or durable authorization.

Consequently:

- live Git/tracked decision artifacts govern the HEAD baseline and authorized
  tracked scope;
- stale local task-state references to `fd83686` do not require edits in this
  decision-drafting task and must not override `1a1aad8`;
- `.agent_tasks/**` is not an implementation artifact under this decision;
- any separately requested local-only task output remains outside tracked
  implementation history unless separately authorized.

## 3. Reviewed Evidence Accepted for This Decision

| Evidence | Accepted conclusion for the gate |
|---|---|
| `agent_outputs/docs/PHASE2B_BATCH4_STEP8_LOCAL_WORKFLOW_HARDENING_PLANNING.md` | Opens read-only workflow-hardening evaluation only; implementation was not authorized by planning. Its `fd83686` baseline is historical after the merge to `1a1aad8`. |
| `.agent_tasks/outbox/backend_result.md` | Backend product implementation is not needed; helper-backed backend verification is write-producing and cannot be treated as read-only scanning. |
| `.agent_tasks/outbox/frontend_result.md` | Frontend implementation is not needed; helper-backed frontend verification invokes a build that writes output and cannot be treated as read-only scanning. |
| `.agent_tasks/outbox/docs_result.md` | Requires reconciliation of the historical/current HEAD distinction, actual helper path and local-exclude treatment before any GO. Its earlier missing-scan-output observation is superseded by the Leader review. |
| `.agent_tasks/outbox/leader_result.md` | Accepts all scan results, records current HEAD `1a1aad8`, confines any future implementation to a reviewable helper artifact, and recommends GO Decision drafting only. |

The `.agent_tasks/**` sources above are supporting reviewed operational inputs,
not authoritative tracked HEAD evidence, as stated in Section 2.2.

## 4. GO / NO-GO Matrix

| Lane / Scope | Decision | Boundary |
|---|---|---|
| Backend implementation | **NO-GO** | No changes under `web-flask/**`, including backend source, tests, config, storage or generated artifacts. |
| Frontend implementation | **NO-GO** | No changes under `web-vue/**`, including frontend source, build configuration or generated output. |
| Docs/Test evidence | **GO AFTER IMPLEMENTATION, SEPARATE AUTHORIZATION REQUIRED** | A later verification-evidence artifact may be authorized separately after an authorized implementation; it is not an implementation file and is not created by this decision draft. |
| AI Agent | **NOT REQUIRED** | No model, inference, training, evaluation or multimodal/LLM behavior work. |
| Control-plane implementation | **CONDITIONAL GO AFTER THIS DECISION IS REVIEWED/MERGED** | A subsequent implementation task may change only `tools/agentctl.local.ps1` as a tracked/reviewable artifact. |
| Merge / tag / push in this drafting task | **NO-GO** | This branch may contain the decision commit only; no merge, tag creation or push is authorized here. |
| Step 9 implementation | **NO-GO / NOT AUTHORIZED** | Requires a later gate. |

## 5. Candidate Implementation Allowlist and Artifact Policy

### 5.1 Exact candidate implementation allowlist

If and only if this GO Decision is reviewed and merged, the allowed Step 8
implementation file set is exactly:

```text
tools/agentctl.local.ps1
```

No other implementation file is implicitly authorized.

### 5.2 Existing helper and tracked-delivery requirement

Read-only scan evidence establishes that `tools/agentctl.local.ps1` already
exists locally and is currently excluded by `.git/info/exclude`. Its local
presence is evidence of the current helper surface, not an already reviewed or
merged implementation.

For any future approved implementation:

- the **same exact path** `tools/agentctl.local.ps1` must be delivered as the
  sole tracked, reviewable and revertible implementation artifact;
- a local/excluded helper edit must not be accepted as durable implementation
  evidence merely because it runs locally;
- `.git/info/exclude` must not be modified to implement or evidence this Step;
- `.agent_tasks/**`, templates, protocol state, README files, application
  code and additional scripts remain outside the implementation allowlist.

### 5.3 Verification evidence is not implementation

A later proof artifact may be authorized in a separate post-implementation
task, for example:

```text
agent_outputs/docs/PHASE2B_BATCH4_STEP8_LOCAL_WORKFLOW_HARDENING_VERIFICATION_EVIDENCE.md
```

That evidence file is **not** authorized for creation or modification by this
GO Decision drafting task, and it is not part of the implementation allowlist.
Separate authorization is required before it is written.

## 6. Future Helper-Hardening Requirements

A later implementation activity, once authorized by review/merge of this
decision, must remain local-workflow/control-plane only and should address the
reviewed helper risks without expanding file scope:

1. Distinguish non-mutating inspection/status behavior from operations that
   create directories, task outputs or build/test artifacts.
2. Retain explicit failure propagation for authorized verification actions.
3. Retain human/Leader gates for implementation, merge, tag, push and any
   subsequent step; the helper must not silently certify or perform them.
4. Treat cleanup operations that could restore/discard runtime state as
   destructive and outside implicit workflow execution.
5. Keep product behavior, application code, shared contracts, model behavior
   and local task-state files unchanged.

Any required solution that cannot be completed within
`tools/agentctl.local.ps1` only is **NO-GO** under this decision and must return
for a revised allowlist decision before editing additional paths.

## 7. Verification Command Classification and Guardrails

Reviewed static evidence establishes that these helper operations are
**write-producing verification**, not read-only scan operations:

| Helper operation | Write-side-effect classification | Decision treatment |
|---|---|---|
| `verify-backend` | May create Python/pytest artifacts and may initialize local backend DB/storage paths unless invocation is isolated. | Must never be represented or invoked as a read-only scan. Future use requires explicit verification authorization and side-effect containment. |
| `verify-frontend` | Invokes the frontend build and may write `web-vue/dist/**`. | Must never be represented or invoked as a read-only scan. Future use requires explicit verification authorization. |
| `verify-master` | Aggregates backend/frontend verification effects and therefore can write artifacts in both lanes. | Must never be represented or invoked as a read-only scan. Future use requires explicit verification authorization and containment. |

This GO Decision drafting task does not execute any helper, build or test
command. Later validation commands and any evidence output must be explicitly
scoped in the separately authorized implementation/review activity.

## 8. Explicit NO-GO Boundaries

The following are explicitly prohibited by this decision-drafting task and by
the candidate implementation unless a new gate expressly changes scope:

- `web-vue/**`;
- `web-flask/**`;
- `other/model_train/detect/**`;
- DB schema, migration, index or data files;
- Docker, deployment, runtime or storage structure;
- model, weights, classes, inference, training or AI behavior;
- API, JWT, auth/login, `detection_result.v1` or metrics contract;
- `.omx/**`;
- `.ccpanes/**`;
- `.git/info/exclude`;
- `.agent_tasks/**`, unless separately authorized as local-only task output and
  never treated as the tracked implementation artifact;
- merge, tag creation or push;
- Step 9 implementation.

In addition, before this GO Decision is reviewed/merged:

```text
Phase 2B Batch4 Step 8 Implementation: NOT AUTHORIZED
```

## 9. Required Later Review / Verification Evidence

After a separately authorized helper implementation, a later separately
authorized evidence task must demonstrate at minimum:

1. the implementation diff changes `tools/agentctl.local.ps1` only;
2. the helper is present as a tracked/reviewable implementation artifact, not
   solely an excluded local file;
3. read-only/status behavior does not trigger workflow-directory or application
   output writes;
4. `verify-backend`, `verify-frontend` and `verify-master` are clearly treated
   as write-producing verification rather than scan operations;
5. business/application source, database, runtime/storage, model and shared
   contracts remain unchanged;
6. merge/tag/push and any later-step action remain separately gated;
7. rollback can be achieved by reverting the single helper implementation
   commit, without disturbing the stable application restore point.

This section specifies future proof requirements only; it does not authorize
verification commands or an evidence-file write in the present drafting task.

## 10. Risks and Mitigations

| Risk | Mitigation required by this decision |
|---|---|
| Historical `fd83686` local metadata is mistaken for current HEAD | Treat `fd83686` as planning history only; use tracked/live baseline `1a1aad8`. |
| Locally excluded executable is changed without reviewability | Permit future implementation only when `tools/agentctl.local.ps1` is the sole tracked/reviewable artifact. |
| Verification is misused as read-only inspection | Explicitly classify all three verify operations as write-producing and require separate authorization for execution. |
| Scope expands into application behavior or operational state | Enforce single-file implementation allowlist and explicit NO-GO list. |
| Decision drafting is mistaken for implementation authorization | Maintain hard stop until this document is reviewed/merged and implementation is separately performed in its scoped activity. |

## 11. Rollback and Current Authorization State

Rollback anchor for application/product behavior remains unchanged:

```text
phase2b-batch4-step7-record-filter-stable -> 25c9f43
```

Rollback treatment:

- this docs-only GO Decision commit can be reverted or abandoned independently
  before merge, with no application/model/database rollback required;
- any later authorized helper implementation must be a narrow revertible
  single-file change;
- no stable-tag move, new tag or push is permitted by this document.

Current authorization state at completion of this draft:

```text
Step 8 planning: MERGED at master HEAD 1a1aad8
Step 8 GO Decision: DRAFTED ON ISOLATED DOCS/WORKFLOW BRANCH ONLY
Step 8 implementation: NOT AUTHORIZED UNTIL GO DECISION REVIEW/MERGE
Backend implementation: NO-GO
Frontend implementation: NO-GO
Docs/Test evidence: GO AFTER IMPLEMENTATION AND SEPARATE AUTHORIZATION ONLY
AI Agent: NOT REQUIRED
Candidate implementation allowlist after decision review/merge: tools/agentctl.local.ps1 only
Merge: NOT PERFORMED / NO-GO IN THIS TASK
Step 8 stable tag: NOT CREATED
Push: NOT DONE
Step 9 implementation: NOT AUTHORIZED
```