# Phase 2B Batch4 Step 8 Planning / Gate — Local Workflow Automation Hardening

Status: **PLANNING / GATE ONLY**
Date: 2026-05-23
Phase: Phase 2B Batch4 Step 8
Planning branch: `batch4-step8-planning`
Master HEAD baseline: `fd83686` (`Archive Batch4 Step7 stable tag`)
Latest stable tag: `phase2b-batch4-step7-record-filter-stable` -> `25c9f43`
Step 7 status: **CLOSED / STABLE / ARCHIVED**
Step 8 implementation: **NOT AUTHORIZED**
Push: **NOT DONE**
New stable tag: **NOT AUTHORIZED**

## 1. Planning Gate Decision

Selected Step 8 direction from `.agent_tasks/PROJECT_ROADMAP.md:21-26`:

```text
5. Local workflow automation hardening
```

Planning objective:

```text
Assess and gate a narrow hardening pass for the local Leader/Worker task
workflow so future steps can be planned, scanned, approved, reviewed and
verified with clearer guardrails, without entering application-feature
implementation or changing any production/business behavior.
```

This document opens only the **Planning -> Read-only scan** portion of the
required lifecycle. It does not create a GO Decision and it does not authorize
implementation.

## 2. Evidence and Stable Baseline Check

### 2.1 Governing input evidence

| Evidence | Finding |
|---|---|
| `.agent_tasks/CURRENT_STEP.md:6-13` | Stable baseline is `phase2b-batch4-step7-record-filter-stable -> 25c9f43`; master HEAD is `fd83686`; Step 7 is clean closeout. |
| `.agent_tasks/CURRENT_STEP.md:21-30` | Allowed sequence is local workflow upgrade followed by Step 8 Planning/Gate; Step 8 implementation, push, new tag, DB/Docker/runtime/model/storage and AI behavior changes are forbidden. |
| `.agent_tasks/PROJECT_ROADMAP.md:18-26` | Immediate recommendation is Local Agent Workflow Upgrade v1, and Step 8 candidate direction 5 is Local workflow automation hardening. |
| `.agent_tasks/PROJECT_ROADMAP.md:28-45` | Planning, read-only scan and GO Decision are mandatory before code; global NO-GO boundaries remain active. |
| `.agent_tasks/state.json:4-18` | Workflow is still at `workflow_upgrade_init`; `step8_implementation` is `NOT_AUTHORIZED`; local task queue/script/template/protocol validation precedes Step 8 gate progress. |
| `.agent_tasks/templates/01_planning.md:17-34` | Planning output must confirm baseline/tag/closeout, select direction, define read-only scope and NO-GO; it must not write business code, start implementation, tag or push. |
| `agent_outputs/docs/PHASE2B_BATCH4_MASTER_PLANNING_GATE.md:647-670` | Step 7 stable tag was archived at `25c9f43`; Step 8 remains not authorized and planning/gate is the only allowed next business step. |

### 2.2 Git verification performed for this planning task

The Leader verified from the source workspace before producing this artifact:

```text
git rev-parse --short HEAD
=> fd83686

git log -1 --oneline
=> fd83686 Archive Batch4 Step7 stable tag

git show-ref --tags --dereference | Select-String phase2b-batch4-step7-record-filter-stable
=> 25c9f436a2793e4ae2d0efe08b2d32055b1453c3 refs/tags/phase2b-batch4-step7-record-filter-stable
```

### 2.3 Working-tree gate note

The archived Step 7 baseline records a clean closeout. During this planning
session, the root `master` worktree already contained pre-existing local
runtime/tool-state changes (`.omx/**` and `.ccpanes/**`) before Step 8
planning output was created. Therefore:

- no planning document is written directly on `master`;
- this artifact is written in isolated worktree/branch
  `batch4-step8-planning` created from `fd83686`;
- no business-source clean-state claim is inferred from the current local
  runtime/tool-state worktree.

## 3. Why Candidate 5 Is the Best Step 8 Direction

Candidate 5 is preferred because it is the only candidate directly aligned
with the current allowed-next-action record and does not require entering a
new product implementation lane.

| Candidate | Gate assessment | Decision |
|---|---|---|
| 1. Reports page MVP | Would open a new feature lane after Word report export; it needs separate feature value/API/UI scoping and is not the recorded immediate prerequisite. | Defer. |
| 2. Video detection planning | Explicitly sensitive/high-risk and video implementation remains NO-GO without later approval. | Defer. |
| 3. Realtime detection planning | Carries stream/resource/runtime risk and realtime implementation remains NO-GO without later approval. | Defer. |
| 4. Additional QA / UI polish | Potentially useful, but it does not first close the stated local workflow-governance gap. | Defer until workflow gate is reliable. |
| **5. Local workflow automation hardening** | Matches roadmap immediate action and `state.json` workflow-init condition; can be evaluated through local, non-business, read-only evidence first. | **SELECTED.** |

Additional planning observation: the local `.agent_tasks/` queue and template
files are present in the Leader workspace, while `agentctl.local.ps1` was not
found during the planning-only inventory. This is evidence for a read-only
hardening scan; it is **not** authorization to create or modify that script.

## 4. Step 8 Planning Scope

### 4.1 In scope for this Planning / Gate artifact

- identify the local workflow hardening direction;
- capture stable baseline and gate constraints;
- define a bounded read-only scan for the existing local Agent workflow;
- define expected read-only evidence and later GO Decision requirements;
- record explicit NO-GO boundaries, risks, verification and rollback.

### 4.2 Not in scope

- creation, editing or execution of `agentctl.local.ps1`;
- editing `.agent_tasks/` control protocol, templates or worker task files,
  other than the explicitly requested Leader result summary output;
- edits to `web-vue/`, `web-flask/`, `other/model_train/detect/` or shared
  business/product documentation contracts;
- any Step 8 implementation task assignment or implementation branch work.

## 5. Authorized Read-Only Scan Scope for the Next Gate Activity

After this planning artifact is reviewed, a separate **read-only scan** may
inspect only the following local-workflow/control-plane surfaces and existing
documentation evidence:

| Scan area | Authorized read-only inspection | Required evidence output |
|---|---|---|
| Task protocol | `.agent_tasks/CURRENT_STEP.md`, `PROJECT_ROADMAP.md`, `state.json`, `inbox/*.md`, `outbox/*.md`, `templates/*.md` | File inventory, workflow transition map, missing/contradictory gate states, output-path expectations. |
| Local helper boundary | `agentctl.local.ps1` if present, or evidence that it is absent; related ignore/exclude treatment only | Existence check, intended command surface if documented, safety/approval concerns, no code creation. |
| Prior planning pattern | `agent_outputs/docs/PHASE2B_BATCH4_MASTER_PLANNING_GATE.md`, Step 7 planning/closeout/evidence documents | Baseline references, gate-order consistency, minimum required planning/verification fields. |
| Repository isolation rules | `AGENTS.md`, current branch/worktree/status/tag information through read-only Git commands | Proof that later document/code changes must use an isolated worktree/branch and that tag/push remain forbidden. |

Read-only scan restrictions:

- use read commands only (`Get-Content`, file listing, `git status`, `git log`,
  `git show`, `git diff --stat`, `git check-ignore` or equivalent);
- do not edit, create, remove, move or execute workflow/helper scripts;
- do not inspect application implementation in order to expand scope into a
  feature direction;
- do not convert scan results into a GO Decision automatically.

## 6. Expected Read-Only Scan Questions

The later read-only evidence should answer:

1. Are the documented lifecycle transitions
   `Planning -> Read-only scan -> GO Decision -> Implementation -> Review ->
   Merge -> Unified verification -> Stable tag -> Post-tag archive`
   represented consistently in the task state, templates and outbox protocol?
2. Which existing local workflow assets are already present, which are absent,
   and which are runtime-only/ignored rather than mergeable documentation?
3. Does any helper/script surface, if present, permit unsafe implicit merge,
   tag, push, implementation, destructive filesystem or external-runtime
   operations?
4. What is the narrowest future file allowlist for a **local workflow-only**
   implementation, should a separate human-approved GO Decision later be
   granted?
5. What dry-run/protocol tests could verify that worker actions remain
   low-risk and Leader/Gate confirmation is required for merge/tag/push/next
   implementation?
6. What rollback removes a future local workflow hardening change without
   disturbing the Step 7 stable application baseline?

## 7. Gate Requirements Before Any Step 8 Implementation

No Step 8 implementation may begin unless all requirements below are met in a
later activity:

1. Read-only scan evidence is delivered for the scope in Section 5.
2. Leader reviews the evidence and confirms that Candidate 5 remains bounded
   to local workflow automation only.
3. A separate **Step 8 Implementation GO Decision** is produced and explicitly
   approved before any script/template/protocol implementation.
4. The GO Decision provides an exact file allowlist, branch/worktree rule,
   permitted local test commands, rollback path and continuing NO-GO list.
5. Any request that would change product/business source, contracts, database,
   runtime, model behavior, auth semantics or `detection_result.v1` is rejected
   from this direction and requires separate planning.

Until then:

```text
Phase 2B Batch4 Step 8 Implementation: NOT AUTHORIZED
```

## 8. Explicit NO-GO

During this Planning / Gate stage and its subsequent read-only scan:

- no Step 8 implementation;
- no edits to `web-vue/**`, `web-flask/**` or `other/model_train/detect/**`;
- no new Reports page, video detection or realtime detection implementation;
- no API return-structure, database field/schema/migration/index, file storage
  structure, JWT field/auth semantic, `detection_result.v1` or evaluation
  metrics change;
- no AI/LLM, model, weight, class, training or inference behavior change;
- no Docker, runtime, deployment or storage change;
- no helper-script/template/task-protocol implementation before separate GO;
- no merge into `master`;
- no tag;
- no push.

## 9. Planning Acceptance Criteria

This Planning / Gate task is complete only when:

- [x] Current master HEAD `fd83686` and stable tag target `25c9f43` are
      recorded and verified.
- [x] Step 7 clean closeout and Step 8 `NOT_AUTHORIZED` state are identified
      from governing documents.
- [x] Exactly one roadmap candidate direction is selected with reasons and
      alternatives deferred.
- [x] An explicit read-only scan scope and evidence questions are provided.
- [x] Explicit NO-GO boundaries include business code, shared contracts,
      tag/push/merge and implementation.
- [x] Output is documentation-only and produced off `master`.

Later gates remain unchecked:

- [ ] Step 8 read-only scan evidence reviewed.
- [ ] Step 8 Implementation GO Decision explicitly approved.
- [ ] Any Step 8 implementation executed.

## 10. Risks and Mitigations

| Risk | Mitigation at this gate |
|---|---|
| Mistaking existing local runtime/tool-state dirtiness for a stable application change | Keep planning output on isolated branch/worktree and record the distinction explicitly. |
| Treating a missing helper script as approval to implement it | Record absence as scan evidence only; require separate GO Decision before creation/edit. |
| Scope drift from workflow hardening into Reports/video/realtime or application changes | Select candidate 5 exclusively and repeat NO-GO boundaries in scan and later GO records. |
| Automated workflow accidentally permitting merge/tag/push/next-step implementation | Require scan evidence of all guardrails and human approval points before any hardening implementation. |
| Committing local task-runtime output contrary to commit scope | Do not commit during this planning task; if later authorized, commit only the planning document allowed by the user. |

## 11. Verification and Rollback

Verification completed for this planning document:

- required Leader inputs and planning template read;
- Git baseline/tag read-only verification performed;
- previous Step 7 planning/archive pattern reviewed;
- local workflow asset inventory performed without editing it;
- planning output isolated from the existing `master` worktree.

Rollback for this planning-only activity:

- remove the uncommitted Step 8 planning document and local Leader result
  summary, or abandon `batch4-step8-planning`;
- no business-source rollback, DB rollback, model rollback or tag movement is
  needed because none is authorized or performed;
- the stable restore point remains
  `phase2b-batch4-step7-record-filter-stable -> 25c9f43`.

## 12. Recommended Next Step

Next allowed activity after Leader/human review:

```text
Perform a read-only scan of the local Agent workflow/control-plane surfaces
listed in Section 5 and return evidence for a separate GO Decision.
```

Not authorized as a consequence of this document:

```text
Step 8 implementation, master merge, tag creation, push, or application
feature work of any kind.
```
