# Phase 2B Batch4 Step 11 Verification-Only Demo Execution Authorization

Status: **EXECUTION AUTHORIZATION DRAFT / REVIEW REQUIRED BEFORE RUN / NO IMPLEMENTATION AUTHORIZED**
Date: 2026-05-26
Owner: Project Leader
Scope: Documentation-only authorization for a later controlled local demonstration evidence run.

## 0. Decision Summary

```text
main project: E:\MM\floating-object-detection
baseline HEAD before this document:
  a55e940 Add Batch4 Step11 verification demo preflight
pre-flight review: PASS
delivery declaration boundary: ADMIN_ONLY_ISOLATED_DEMO
decision in this document: define the exact later verification-only execution scope and inputs
demo execution during this drafting task: NOT AUTHORIZED / NOT RUN
demo execution after this document: NOT AUTHORIZED until this execution authorization receives review PASS
Step 11 implementation: NOT AUTHORIZED
Step 12: NOT AUTHORIZED
external hosted-remote push: NOT DONE
tag activity: NOT DONE / NOT AUTHORIZED
```

This document authorizes no operation by its creation alone. Once separately reviewed `PASS`, it may authorize one local, non-production, evidence-producing demonstration pass over the existing implemented workflow. Any result remains verification evidence only.

## 1. Fixed Delivery Declaration Boundary

```text
SELECTED: ADMIN_ONLY_ISOLATED_DEMO
NOT CLAIMED: normal-user artifact isolation
NOT CLAIMED: cross-user direct artifact access denial
NOT CLAIMED: multi-user authorization completeness
```

The intended demonstration is limited to an isolated local environment using an administrator/demo-account route. A successful admin-only verification result may show that the selected demo journey functions for that operator; it must not be interpreted as proof of normal-user isolation.

### 1.1 Known backend limitation retained

Reviewed backend readiness evidence identified:

```text
GET /api/files/<bucket>/<path:object_key>
is JWT-protected and path-confined,
but record-owner enforcement has not been established.
```

| Boundary question | Fixed disposition for this execution authorization |
| --- | --- |
| Is normal-user artifact isolation required by this pass? | `NO` |
| Is `/api/files/**` owner enforcement represented as verified or fixed? | `NO` |
| Risk treatment | `KNOWN LIMITATION` to be recorded in execution evidence and any closeout candidate. |
| Does this known limitation authorize backend implementation in this pass? | `NO` |
| Later trigger for a backend minimal implementation GO Decision | Any later selection of `NORMAL_USER_ARTIFACT_ISOLATION_REQUIRED`, or separate evidence of a delivery-blocking backend defect. |

## 2. Fixed Local Non-Production Environment

This execution authorization is for local non-production operation only. It does not authorize deployment, external environment access, production data access or configuration redesign.

| Environment item | Fixed execution input / rule | Evidence requirement |
| --- | --- | --- |
| Environment class | Local isolated non-production development/demo environment only. | Record that no production endpoint, credentials, database or storage is used. |
| Frontend URL | `http://localhost:5173` (current project default Vite development address). | Record reachable loaded page during the later evidence run. |
| Backend/API URL | `http://localhost:5000` and API base `http://localhost:5000/api` (current project default backend/API address). | Record local backend/API availability only during authorized execution. |
| Frontend API proxy behavior | Existing Vite `/api` proxy defaults to `http://localhost:5000`; do not change this configuration for the run. | Record observed request route only if needed for evidence. |
| DB/storage scope | Local non-production DB/storage only; created detection records and artifacts must not be written into production or shared real-user data. | Record local-only assertion and generated record identity. |

Source basis for fixed default addresses, inspected read-only while drafting:

- `web-vue/vite.config.ts`: development server port `5173`; default `/api` proxy target `http://localhost:5000`.
- `web-flask/README.md`: default API base `http://localhost:5000/api`.

## 3. Fixed Account And Secret-Handling Boundary

| Account item | Execution rule |
| --- | --- |
| Required account role | A local non-production `admin/demo` account able to traverse Dashboard, image detection, record list/detail and Word export. |
| Credentials | May be used interactively only during the later authorized local run; passwords must not be written into this document or evidence artifacts. |
| Sensitive session data | Do not record JWT, cookies, authorization headers or browser storage secret values. |
| Cross-user assertion | Do not execute or claim normal-user cross-user isolation under this authorization. |
| Account unavailable | Stop the run and report `BLOCKED`; do not seed, change or repair credentials under verification-only authority. |

The execution operator must confirm the selected admin/demo role at run start without adding secret values to Git or evidence notes.

## 4. Fixed Image, Model And Threshold Inputs

| Input | Fixed rule for later execution | Evidence requirement |
| --- | --- | --- |
| Demo image | Preferred repository-local candidate: `4测试包/测试图片/1.png`. Before submission, the execution operator must confirm it is an appropriate non-sensitive sample; if it is unsuitable or unavailable, stop and record a replacement repository-local non-sensitive path before any detection request. | Record exact selected local path in local-only execution evidence; do not store private image content in tracked docs. |
| Detection model | Use the current project default published detection model as presented by the existing UI/API; do not edit model files, configuration or published-model state. Current seeded default source reference is `m_yolo26n_dev` / `YOLO26n Dev Baseline` (`yolo26n.pt`). | Record the actual model identifier/name visible in the executed flow or returned response metadata. |
| Detection threshold | Use the current default confidence threshold `0.5`; do not adjust configuration or deliberately vary the UI value for this pass. | Record the actual observed threshold in evidence or response metadata when visible. |
| Response metadata | Observe only existing UI/API-visible model, threshold, status, timing/count and record identity fields as available. | Do not infer model-quality guarantees from a single demonstration image. |

Stop condition: if a non-sensitive sample image, current default selectable model or default threshold cannot be confirmed at execution start without code/config changes, do not proceed with detection.

## 5. Data And Evidence Retention Strategy

This verification-only pass is expected to produce local non-production runtime data. These effects are acceptable only after this authorization is reviewed `PASS` and the pass is separately started under its limits.

| Data/evidence category | Allowed later execution effect | Retention rule |
| --- | --- | --- |
| Detection records | Create one or a small number of local non-production demo detection records needed to complete the journey. | Record each relevant record ID and timestamp in local-only evidence. Do not delete existing historical project data. |
| Uploaded/result artifacts | Permit local artifacts generated by the fixed detection run in the selected non-production storage. | Record their relation to the demo record where visible; no automatic cleanup required. |
| Screenshots | Capture only screens required for dashboard, detection, list/filter and detail evidence. | Store only under the local-only evidence root; redact secrets/private content. |
| Word report | Download the report for the demonstrated record and verify openability. | Store only under the local-only evidence root; record filename and file size/openability conclusion. |
| Cleanup | No automatic cleanup is required by this authorization. | Cleanup may occur only if clearly safe and recorded; never delete historical project data or broadly remove runtime state. |

## 6. Fixed Evidence Output Root And Redaction Rules

All produced demonstration evidence must remain local-only operational evidence:

```text
.agent_tasks/outbox/step11_demo_evidence/
```

Permitted local-only evidence contents:

```text
.agent_tasks/outbox/step11_demo_evidence/screenshots/
.agent_tasks/outbox/step11_demo_evidence/word_reports/
.agent_tasks/outbox/step11_demo_evidence/notes.md
.agent_tasks/outbox/step11_demo_evidence/execution_result.md
```

`.agent_tasks/**` is treated as ignored local-only operational evidence. Do not add screenshots, downloaded Word files or runtime evidence artifacts to Git.

| Evidence handling item | Required rule |
| --- | --- |
| Passwords/tokens/cookies | Never record or capture them in notes, screenshots or tracked docs. |
| Image privacy | Use only a non-sensitive sample input; do not use personal/private imagery. |
| Permitted identifiers | Record ID, timestamps, interface status, page state, selected non-sensitive filename, model/threshold metadata, downloaded report filename, file size and openability conclusion may be recorded. |
| Screenshots/report contents | Capture only what proves the workflow; redact sensitive visible values before later review or distribution. |
| Git handling | Keep all execution outputs local-only under `.agent_tasks/outbox/step11_demo_evidence/`; do not commit them. |

## 7. Verification-Only Execution Scope

After this authorization document is separately reviewed `PASS`, the later execution lane may:

1. Run the required local frontend/backend server processes using existing project behavior at the fixed local non-production addresses.
2. Run only necessary observation/verification steps needed to complete and document the journey.
3. Collect local-only evidence under Section 6.
4. Record whether the known `/api/files/**` owner-enforcement limitation remains outside the selected admin-only claim boundary.

Authorized journey:

```text
login
-> dashboard
-> image detection using the fixed local sample/default model/default threshold
-> detection record list/filter lookup
-> detection record detail
-> Word report export
-> Word report openability observation
```

| Journey phase | Required evidence output |
| --- | --- |
| Environment / login | Local-only notes confirming local non-production URLs and admin/demo role used without recording secrets. |
| Dashboard | Screenshot or recorded loaded dashboard state. |
| Detection | Selected image path, visible model/threshold metadata where available and detection result evidence. |
| Record list/filter | Filter inputs and traceable result-row evidence for the created demo record. |
| Detail | Evidence linking detail view to the same record. |
| Word download | Report filename and downloaded-file observation. |
| Word openability | Openability/readability conclusion and, if captured, redacted evidence. |
| Disposition | `execution_result.md` summarizing PASS/FAIL/BLOCKED, known limitation and next-decision recommendation. |

All observations are verification evidence only. They do not automatically authorize docs alignment, backend implementation, delivery closeout, tag, push or Step 12.

## 8. Execution Stop Conditions

Even after a later execution authorization review `PASS`, stop the run and report `BLOCKED` or `FAIL` as applicable if:

| Stop condition | Required disposition |
| --- | --- |
| The target is not clearly local non-production at the fixed frontend/backend addresses. | Stop before login or data creation. |
| An approved admin/demo account cannot be used without changing authentication state or recording secrets. | Stop; do not modify credentials. |
| `4测试包/测试图片/1.png` is not appropriate/non-sensitive and no replacement local non-sensitive image is explicitly recorded before detection. | Stop before upload/detection. |
| The default selectable model or default threshold `0.5` cannot be used without modifying code/config/model state. | Stop before detection. |
| Evidence root cannot be used locally without committing evidence artifacts or exposing secrets. | Stop before evidence-producing actions. |
| The claimed boundary changes to require normal-user artifact isolation. | Stop; prepare a separate backend minimal implementation GO Decision as needed. |
| The journey exposes a functional blocker requiring product/helper/schema/runtime/model edits. | Stop; record evidence and request a separate reviewed GO/NO-GO decision. |

## 9. Required Execution Result Record

The later executor must create a local-only:

```text
.agent_tasks/outbox/step11_demo_evidence/execution_result.md
```

It must record:

| Result field | Required record |
| --- | --- |
| Execution date/time | Local run timestamp. |
| Claim boundary | `ADMIN_ONLY_ISOLATED_DEMO`; explicitly restate that normal-user artifact isolation was not claimed. |
| Environment | Local frontend/backend/API addresses and non-production assertion. |
| Account role | Admin/demo role only, without secrets. |
| Input | Selected non-sensitive image path, observed model identifier/name and observed threshold. |
| Runtime result | Login, dashboard, detection, list/filter, detail, Word download and openability result statuses. |
| Created data | Relevant demo record ID/timestamp and evidence-artifact locations. |
| Known limitation | `/api/files/**` owner-enforcement remains a known limitation under this claim boundary. |
| Recommendation | One of: docs-only alignment review, final delivery closeout review candidate, or separate minimal GO/NO-GO decision needed. |
| Git/scope confirmation | Evidence artifacts remained local-only; no tracked code/helper change, tag or push was performed. |

## 10. Explicit NO-GO

This documentation drafting task authorizes only creation of:

```text
agent_outputs/docs/PHASE2B_BATCH4_STEP11_VERIFICATION_ONLY_DEMO_EXECUTION_AUTHORIZATION.md
```

During this drafting task:

- do not run demo, tests, builds, servers, browser sessions, API smoke operations, report downloads or Word openability checks;
- do not modify `web-vue/**`;
- do not modify `web-flask/**`;
- do not modify `tools/agentctl.local.ps1`;
- do not modify DB schema, Docker/deployment configuration, runtime configuration, model files, weights or training/inference implementation;
- do not modify `.omx/**`;
- do not modify `.ccpanes/**`;
- do not run `omx exec`, `omx exec inject` or `omx team`;
- do not create, move or replace any tag;
- do not push;
- do not enter Step 11 implementation;
- do not enter or authorize Step 12.

After later review `PASS`, the execution authorization remains constrained to local non-production server operation, the identified demo workflow, allowed local runtime/evidence effects and no product/helper/schema/config/model edits. It does not authorize `omx exec/team`, tag, push, implementation or Step 12.

## 11. Lifecycle Boundary And Completion Criteria

```text
execution authorization drafting: documentation-only
demo execution now: NOT RUN / NOT AUTHORIZED UNTIL REVIEW PASS
Step 11 implementation: NOT AUTHORIZED
Step 12: NOT AUTHORIZED
tag: NOT CREATED
external hosted-remote push: NOT DONE
```

Completion criteria for this documentation task:

- [x] `ADMIN_ONLY_ISOLATED_DEMO` is fixed and normal-user artifact isolation is excluded.
- [x] `/api/files/**` owner-enforcement risk is retained as a known limitation.
- [x] Local non-production frontend/backend/API defaults are recorded.
- [x] Admin/demo role and secret-handling boundaries are recorded.
- [x] Repository-local demo-image selection rule, default model and threshold are recorded.
- [x] Local-only evidence root and redaction rules are recorded.
- [x] Allowed later verification-only workflow and required outputs are recorded.
- [x] Stop conditions and subsequent decision boundaries are recorded.
- [x] This documentation task does not run demo/test/build/server or enter implementation.
