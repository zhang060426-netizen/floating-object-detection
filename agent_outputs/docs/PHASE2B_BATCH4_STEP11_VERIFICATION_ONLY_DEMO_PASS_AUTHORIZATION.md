# Phase 2B Batch4 Step 11 Verification-Only Demo Pass Authorization / Evidence Template

Status: **VERIFICATION-ONLY DEMO PASS AUTHORIZATION DRAFT / NO IMPLEMENTATION AUTHORIZED**
Date: 2026-05-26
Owner: Project Leader
Scope: Documentation-only authorization template for a later controlled, non-production demonstration evidence pass.

## 0. Decision Summary

```text
Step 11 planning review: PASS
Step 11 delivery-readiness evidence review: PASS
Delivery readiness status: NEEDS_VERIFICATION
Decision in this document: authorize a later verification-only demo evidence pass
Run demo/test/build/server while drafting this document: NO
Enter Step 11 implementation: NO-GO
External hosted-remote push: NOT DONE
Create tag: NO-GO
Step 12: NOT AUTHORIZED
```

This document defines the evidence boundary and template for a separately executed Step 11 verification-only demonstration pass. It does not itself execute that pass, prove delivery readiness, authorize product or helper changes, or authorize a later lifecycle step.

## 1. Current Baseline And Reviewed Evidence

```text
main project: E:\MM\floating-object-detection
branch: master
HEAD before this authorization document: ac2c3f7 Add Batch4 Step11 system finalization planning
Step 10 stable tag:
  phase2b-batch4-step10-passive-watch-stable
  -> 150967c3b793b0432692932f1e308829be779493
Step 11 planning review: PASS
Step 11 delivery-readiness evidence review: PASS
external hosted-remote push: NOT DONE
Step 11 implementation: NOT AUTHORIZED
Step 12: NOT AUTHORIZED
```

Reviewed delivery-readiness evidence establishes:

1. The candidate end-to-end demonstration route is present in existing source/evidence:

   ```text
   login -> dashboard -> image detection -> record list/filter -> detail -> Word export
   ```

2. Backend evidence identified a conditional security concern: `GET /api/files/<bucket>/<path:object_key>` is protected by JWT and path scope, but record-owner enforcement has not been established.
3. Frontend evidence did not identify a proven functional blocker, but final evidence still lacks a fixed demonstration image, live screenshots and Word download/openability confirmation.
4. Docs/Test evidence correctly classifies final delivery as blocked pending controlled demonstration verification, without authorizing implementation.

## 2. Authorization Purpose And Boundary

This authorization is limited to a later, explicitly controlled **verification-only demo pass** whose purpose is to gather evidence about the already implemented system. It may establish whether final delivery requires:

- documentation-only alignment;
- a separately reviewed minimal backend implementation GO Decision; or
- final delivery closeout planning after successful evidence review.

Every result produced under this authorization is evidence for manual Project Leader review only. Evidence does not automatically authorize implementation, closeout, tagging, push, Step 12, or any lifecycle transition.

## 3. Required Delivery Claim Selection

Before the verification-only pass starts, the Project Leader must record exactly one intended delivery-claim boundary:

| Selection | Permitted claim | File-serving owner-enforcement treatment | Selected value |
| --- | --- | --- | --- |
| `ADMIN_ONLY_ISOLATED_DEMO` | Demonstration uses a designated non-production isolated environment and an authorized admin/demo operator only. It does not claim normal-user artifact isolation. | The missing record-owner enforcement for direct `/api/files/**` artifact access is recorded as a known limitation and must not be represented as fixed. | `PENDING SELECTION` |
| `NORMAL_USER_ARTIFACT_ISOLATION_REQUIRED` | Final delivery must demonstrate that normal users cannot retrieve other users' uploaded/result artifacts. | Existing backend evidence triggers a potential delivery blocker. Verification may record/reproduce the gap but cannot fix it; a separate minimal implementation GO Decision is required before claiming readiness. | `PENDING SELECTION` |

Prohibited interpretation:

```text
An admin-only demonstration must not be used to assert multi-user artifact isolation.
Observed functionality must not be used to waive a required authorization guarantee.
```

## 4. Mandatory Pre-Flight Fixing Of Verification Inputs

No controlled demo execution may begin until each item below has an explicit recorded value and handling boundary.

| Required pre-flight item | Required record | Result |
| --- | --- | --- |
| Non-production environment | Environment identifier, frontend URL, backend/API identity, storage/database isolation statement and confirmation that no production system is targeted. | `PENDING` |
| Delivery claim boundary | One selection from Section 3 with owner-enforcement implication acknowledged. | `PENDING` |
| Test account role | Approved non-production account role and permissions required for the selected demo route; record no passwords, tokens or secrets. | `PENDING` |
| Fixed demo image | One designated non-sensitive image reference and permitted evidence-handling rule. | `PENDING` |
| Fixed model | Published/permitted model identifier or visible model name selected for the demo. | `PENDING` |
| Fixed threshold | Detection confidence threshold selected for the run. | `PENDING` |
| Data retention policy | Retain-or-cleanup decision for created record, uploaded/result artifacts, screenshots and downloaded Word evidence, with owner authorization. | `PENDING` |
| Evidence location | Approved non-production local evidence location and redaction rule. | `PENDING` |

If any pre-flight item is missing, the verification-only run status is `BLOCKED` and the operator must not improvise inputs or change system configuration to proceed.

## 5. Authorized Verification-Only Demo Journey

Once the pre-flight manifest is complete and separately approved for execution, the later pass may run exactly this controlled journey:

```text
login
-> dashboard
-> image detection using the fixed image/model/threshold
-> detection record list/filter lookup
-> detection record detail
-> Word report export from the detail page
```

| Step | Verification action | Required observable evidence | Result field |
| --- | --- | --- | --- |
| 0. Pre-flight | Record the Section 4 manifest and delivery claim boundary. | Complete manifest with no secrets and explicit retention rule. | `PENDING / PASS / BLOCKED` |
| 1. Login | Authenticate using the approved non-production test account. | Successful authenticated navigation state; role noted without exposing credentials or token. | `PENDING / PASS / FAIL / BLOCKED` |
| 2. Dashboard | Navigate to the Dashboard and wait for its reviewable loaded state. | Screenshot or data evidence identifying the loaded summary state and run context. | `PENDING / PASS / FAIL / BLOCKED` |
| 3. Image detection | Submit the fixed image using the fixed model and threshold. | Result status, selected model/threshold, output rendering and traceable indication that a record is available. | `PENDING / PASS / FAIL / BLOCKED` |
| 4. Record list/filter | Locate the created record through the records list and an appropriate filter scenario. | Filter values plus evidence of one matching record tied to the detection step. | `PENDING / PASS / FAIL / BLOCKED` |
| 5. Detail | Open the same identified record. | Detail-page evidence correlated to the record from Step 4. | `PENDING / PASS / FAIL / BLOCKED` |
| 6. Word export | From that detail page, export the Word report. | Downloaded `.docx` filename and association with the demonstrated record. | `PENDING / PASS / FAIL / BLOCKED` |
| 7. Word openability | Open or otherwise validate the downloaded Word artifact under the authorized verification environment. | Evidence that the report opens/readably renders, with sensitive content redacted where required. | `PENDING / PASS / FAIL / BLOCKED` |
| 8. Disposition | Reconcile results, known limitations and evidence retention. | Completed evidence table and recommendation for docs-only, implementation-GO or delivery-closeout lane. | `PENDING / PASS / FAIL / BLOCKED` |

## 6. Evidence Capture Template

| Evidence ID | Required evidence | Minimum content | Handling rule | Result / reference |
| --- | --- | --- | --- | --- |
| `EV-00` | Pre-flight manifest | Environment, claim boundary, account role, image, model, threshold and retention policy. | Exclude passwords, bearer tokens and production identifiers. | `PENDING` |
| `EV-01` | Login evidence | Authenticated state after login. | Do not capture entered secret values. | `PENDING` |
| `EV-02` | Dashboard evidence | Dashboard screenshot and/or data observation in loaded state. | Identify run context; redact sensitive data. | `PENDING` |
| `EV-03` | Detection setup evidence | Fixed image reference, model and threshold. | Use approved non-sensitive image only. | `PENDING` |
| `EV-04` | Detection success evidence | Result rendering/status plus record-correlation information. | Do not overclaim model quality from one example. | `PENDING` |
| `EV-05` | Record list/filter evidence | Filter input and matching record entry. | Correlate to `EV-04`. | `PENDING` |
| `EV-06` | Detail evidence | Same-record detail view and rendered result evidence. | Correlate to `EV-05`. | `PENDING` |
| `EV-07` | Word report download evidence | Download occurrence and filename. | Retain only in authorized evidence location. | `PENDING` |
| `EV-08` | Word openability evidence | Open/readability result for the `.docx`. | Redact report contents as needed. | `PENDING` |
| `EV-09` | Authorization-claim disposition | Whether owner-enforcement condition is triggered by the selected delivery claim and observed behavior. | Do not infer a security guarantee that was not tested or implemented. | `PENDING` |
| `EV-10` | Final recommendation | Docs-only alignment, minimal implementation GO Decision, or final delivery closeout eligibility. | Project Leader review required. | `PENDING` |

## 7. Backend File-Serving Owner-Enforcement Decision Template

Known evidence condition:

```text
GET /api/files/<bucket>/<path:object_key>
has JWT and path-scope enforcement, but current readiness evidence did not establish record-owner enforcement.
```

| Decision question | Answer field |
| --- | --- |
| Which delivery claim boundary was selected? | `PENDING` |
| Does the selected claim require normal-user artifact isolation? | `PENDING: YES / NO` |
| Was any direct artifact access behavior exercised in the verification pass? | `PENDING: YES / NO / NOT AUTHORIZED` |
| Is the condition a declared known limitation for admin-only isolated demonstration? | `PENDING: YES / NO / NOT APPLICABLE` |
| Is a backend minimal implementation GO Decision required before delivery can proceed? | `PENDING: YES / NO` |

Decision rule:

| Verification disposition | Required next lane |
| --- | --- |
| `ADMIN_ONLY_ISOLATED_DEMO` selected, verification route passes, limitation recorded without claiming normal-user isolation. | Consider docs-only alignment and final delivery closeout review. |
| `NORMAL_USER_ARTIFACT_ISOLATION_REQUIRED` selected, owner enforcement remains unestablished or failure is evidenced. | Stop delivery closeout and draft a separate minimal backend implementation GO Decision. |
| Any unrelated functional blocker is evidenced in the demo route. | Stop and draft a separate narrowly scoped GO/NO-GO review; no automatic fix. |

## 8. Result Classification And Follow-On Decision

| Result classification | Meaning | Authorized follow-on consideration |
| --- | --- | --- |
| `PASS / DOCS_ONLY_ALIGNMENT` | The fixed demo route succeeds under the declared boundary; remaining gaps are operator guidance, README/context or evidence archive wording. | Propose a separately reviewed docs-only closeout/alignment update. |
| `PASS / FINAL_DELIVERY_CLOSEOUT_CANDIDATE` | Required evidence is complete, claim boundary is respected and no blocking defect is identified. | Propose final delivery closeout review; no automatic tag, push or Step 12 action. |
| `BLOCKED / BACKEND_MINIMAL_GO_REQUIRED` | Normal-user artifact isolation is required or the demo exposes a backend delivery blocker needing code change. | Prepare a separate minimal Step11 implementation GO Decision with exact file scope and tests. |
| `BLOCKED / VERIFICATION_INPUTS_INCOMPLETE` | Environment, account, image, model, threshold, retention or evidence controls are absent. | Complete verification prerequisites only; do not implement. |
| `FAIL / NEW_DEFECT_OBSERVED` | Controlled journey fails for an evidenced functional reason outside an approved change scope. | Stop; prepare separate review and authorization decision. |

This template does not preselect any result.

## 9. Explicit NO-GO

This documentation task authorizes only creation of:

```text
agent_outputs/docs/PHASE2B_BATCH4_STEP11_VERIFICATION_ONLY_DEMO_PASS_AUTHORIZATION.md
```

While drafting and committing this document:

- do not run the demonstration journey;
- do not run tests, builds, servers, browser/demo sessions, API smoke operations or download validation;
- do not modify `web-vue/**`;
- do not modify `web-flask/**`;
- do not modify `tools/agentctl.local.ps1`;
- do not modify `.agent_tasks/**`;
- do not modify `.omx/**`;
- do not modify `.ccpanes/**`;
- do not modify DB schema, database state, Docker/deployment surfaces, runtime/storage configuration or model/weight/training/inference surfaces;
- do not run `omx exec`, `omx exec inject` or `omx team`;
- do not create, move or replace any tag;
- do not push;
- do not enter Step 11 implementation;
- do not enter or authorize Step 12.

A later verification-only execution may be proposed under this template only after explicit review of its pre-flight values and runtime/data effects. It remains evidence collection, not product implementation or lifecycle authority.

## 10. Rollback And Lifecycle Boundary

This artifact changes documentation only. If rejected, rollback is limited to reverting this documentation commit through normal reviewed Git handling. No product/helper/runtime rollback applies because this task must not alter product behavior.

```text
verified rollback reference retained:
  phase2b-batch4-step10-passive-watch-stable
  -> 150967c3b793b0432692932f1e308829be779493
external hosted-remote push: NOT DONE
Step 11 implementation: NOT AUTHORIZED
Step 12: NOT AUTHORIZED
```

## 11. Documentation-Task Completion Checklist

- [x] Current Step 11 baseline and reviewed readiness status recorded.
- [x] Delivery claim boundary requires explicit selection.
- [x] Non-production environment, account, image, model, threshold and retention fields defined.
- [x] Controlled demo journey limited to the existing delivery path.
- [x] Dashboard, detection, list/filter, detail, Word download and Word openability evidence fields defined.
- [x] Backend file-serving owner-enforcement trigger decision recorded.
- [x] Possible docs-only, implementation-GO and final-delivery-closeout outcomes distinguished.
- [x] Verification evidence explicitly remains non-authoritative for implementation or Step 12.
- [x] NO-GO prohibits code/helper/runtime/model/tag/push/OMX/demo/test/build/server actions in this documentation task.
