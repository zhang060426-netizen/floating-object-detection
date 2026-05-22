# Phase 2B Batch4 Step 5 Word Report Planning / Gate

Status: PLANNING ONLY
Date: 2026-05-22
Phase: Phase 2B Batch4 Step 5
Current branch: `batch4-step5-word-planning`
Current stable baseline: `phase2b-batch4-step4-detail-readability-stable`
Current stable baseline target: `66349abc9ba3f8ad4a31afe85d5430a52b0a4393`
Step 4 status: CLOSED / VERIFIED / TAGGED
Step 5 Implementation: NOT AUTHORIZED
Step 5 stable tag: NOT CREATED
Push: NOT DONE

## 1. Current Stable Baseline

The current restore baseline is:

```text
master latest stable baseline: phase2b-batch4-step4-detail-readability-stable
stable commit: 66349abc9ba3f8ad4a31afe85d5430a52b0a4393
stable tag object: annotated tag resolves to commit 66349abc9ba3f8ad4a31afe85d5430a52b0a4393
Step 4: CLOSED / VERIFIED / TAGGED
Step 5: NOT AUTHORIZED
push: NOT DONE
```

Step 4 closed the detection-record detail readability enhancement. The current safe product chain is:

```text
login -> image detection -> save record -> records list -> record detail
```

Step 5 planning should continue from the record-detail link and avoid opening unrelated product surfaces by default. In particular, Step 5 planning must not authorize DB schema changes, video/realtime work, complex async jobs, batch report generation, custom report templates, Dashboard implementation, model changes, Docker changes, runtime/storage changes, push, or tag creation.

## 2. Step 5 Candidate Direction Comparison

| Candidate | Description | Fit with current chain | Risk | Verification cost | Rollback safety | Default DB/schema need | Recommendation |
|---|---|---:|---:|---:|---:|---:|---|
| Word report export MVP | Export one Word report from one detection record detail using existing record/detail data and safe image reads when available. | High | Low-Medium | Medium | High | No | Recommended |
| Dashboard statistics overview | Add aggregate cards/charts for records, targets, model usage, and status trends. | Medium | Medium | Medium-High | Medium | Maybe, depending on aggregate needs | Defer; broader surface than current record-detail chain |
| Video detection MVP | Add video upload/detection flow and record handling. | Low for current chain | High | High | Low-Medium | Maybe | Defer; explicitly not default for Step 5 |
| Realtime detection planning | Plan future camera/realtime capture and inference pathway. | Low | Low if docs-only, high if implemented | Medium | High for docs-only | No for planning | Defer; not the closest next feature |
| Model management preface | Prepare model lifecycle, active model display, upload/selection, or metadata plans. | Medium-Low | Medium | Medium | Medium | Maybe | Defer; separate module boundary and not record-detail continuation |

### Candidate assessment

1. **Word report export MVP** is the nearest continuation because Step 4 improved the record detail page and the report can be generated from the same record data already displayed there. It is also naturally scoped to one record, one action, and one downloadable artifact.
2. **Dashboard statistics overview** is useful but moves from one-record inspection to cross-record aggregation. It is more likely to need new endpoints, aggregation semantics, and broader frontend layout decisions.
3. **Video detection MVP** would open new inference, upload, storage, runtime, and potentially async-task risks. It violates the default Step 5 constraints.
4. **Realtime detection planning** can remain documentation-only, but it is not as valuable as a directly adjacent MVP and should not be the next implementation gate.
5. **Model management preface** is important later, but it touches model lifecycle boundaries and is less directly connected to the current record-detail flow.

## 3. Recommended Step 5 Direction

Recommended Step 5:

```text
Phase 2B Batch4 Step 5 - Word Report Export MVP
```

Recommended objective:

```text
Add a small, reversible, single-record Word report export from the detection record detail page, using existing detection-record data and existing image paths only when they can be safely resolved/read.
```

This document is only the Planning / Gate artifact. It does not authorize implementation.

## 4. Recommended Reasons

Word Report Export MVP is preferred because:

- it is the closest extension of the current stable chain: record detail already gathers the report source data;
- it can be constrained to a single detection record and one export action;
- it does not require DB schema changes by default;
- it does not require video, realtime, Dashboard, batch reporting, custom templates, or complex async tasks;
- it can preserve `detection_result.v1` by summarizing existing data instead of mutating detection output semantics;
- it has clear verification: backend unit/API checks, frontend build/smoke checks, generated `.docx` openability/content checks, and scope guard checks;
- it is easy to roll back by reverting a narrow backend/frontend report-export diff if later authorized;
- it provides user-visible value without replacing the current model, changing storage layout, or changing existing record APIs.

The main risk is document-generation dependency and image embedding behavior. The recommended mitigation is to confirm the backend's existing dependency policy and implement the smallest possible server-side export endpoint only after a separate GO Decision. If a new dependency is required later, it must be explicitly listed in that GO Decision and verified through local install/build evidence.

## 5. MVP Scope

If a later Step 5 Implementation GO Decision is created, the recommended MVP should be limited to exporting one `.docx` report for one existing detection record.

Required report content:

- record ID;
- file name;
- detection time;
- model information;
- detection status;
- target count;
- confidence statistics;
- elapsed/timing information;
- detection target table;
- original image and result image only if the current paths can be safely resolved and read;
- `detection_result.v1` summary.

Recommended behavior:

- export starts from the detection record detail page;
- backend returns a downloadable `.docx` file for the selected record;
- missing optional fields render as explicit safe placeholders such as `N/A` or `未记录`;
- missing/unreadable images do not fail the whole report unless the record itself is unavailable;
- report content is derived from existing persisted record/detail data;
- report generation is synchronous for one record only unless later evidence proves it is unsafe;
- no persistent report artifact is required by default; generated file may be streamed directly;
- generated filename should be deterministic enough for smoke checks, for example `detection-report-<record_id>.docx`;
- authentication should follow existing detection-record detail access rules.

Recommended candidate implementation surface, if later authorized:

- backend route/service for one-record Word export under existing detection/report boundary;
- frontend detail-page export button and download handling;
- optional lightweight report utility if it keeps backend route code small;
- tests/checks for missing fields, missing images, and generated response headers/content.

No implementation is authorized by this planning document.

## 6. Allowed Scope Suggestions

Recommended allowed scope for a future GO Decision:

### Backend, narrow implementation candidate

Potential files only after explicit GO:

- `web-flask/routes/detection.py` or a narrowly named report route under the existing backend routing style;
- `web-flask/services/detection_service.py` for record lookup reuse only if needed;
- optional new `web-flask/services/report_service.py` or similar if it isolates Word generation cleanly;
- `web-flask/requirements.txt` only if the GO Decision explicitly authorizes a document-generation dependency;
- backend tests under `web-flask/tests/**` only for report-export behavior.

Backend implementation should remain additive:

- add one endpoint for single-record report export;
- reuse existing record detail lookup and file path helpers;
- stream/return `.docx` with correct content type and attachment headers;
- preserve all existing detection APIs and response structures;
- preserve DB schema and `detection_result.v1` semantics.

### Frontend, narrow implementation candidate

Potential files only after explicit GO:

- `web-vue/src/views/DetectionRecordDetail.vue` for an export button/action;
- `web-vue/src/api/detection.ts` for a one-record export request helper;
- `web-vue/src/types/detection.ts` only if a typed helper is necessary and additive;
- optional existing download/request utility if already present.

Frontend implementation should remain additive:

- add one visible export action on the record detail page;
- show loading/error feedback for export request;
- download the returned `.docx` without changing detail display semantics;
- preserve current route, list-to-detail navigation, image display, and JSON collapse behavior.

### Docs/Test

Allowed documentation/test planning:

- GO Decision document;
- verification checklist;
- closeout/evidence archive after implementation if later authorized;
- manual smoke instructions for generated Word report content.

### Read-only scan allowance before GO

A future Step 5 GO Decision should be preceded by read-only scans only. The scans may inspect backend route/service/file helper patterns and frontend detail/API/download patterns, but must not modify business code.

## 7. Forbidden Scope

Step 5 planning and any default future Step 5 implementation must not include:

- business-code changes during this planning task;
- `web-vue/**` changes during this planning task;
- `web-flask/**` changes during this planning task;
- DB schema changes;
- migration scripts;
- Dockerfile changes;
- `docker-compose.yml` changes;
- runtime/storage structure changes;
- model weight changes;
- model class/category changes;
- model training changes;
- model replacement;
- `detection_result.v1` semantic changes;
- image detection main-flow semantic changes;
- auth/login semantic changes;
- record create/list/detail response-shape breaking changes;
- Dashboard implementation;
- video detection implementation;
- realtime detection implementation;
- batch report generation;
- custom Word templates;
- asynchronous report task queue;
- scheduled report jobs;
- persistent report management module;
- user-configurable report designer;
- external report service integration;
- broad UI redesign;
- push;
- tag creation;
- commit during this planning task.

## 8. Recommended Agent Division

| Agent | Recommended Step 5 responsibility |
|---|---|
| Docs/Test Agent | Own this Planning / Gate document, future GO Decision, verification checklist, evidence archive, and scope guard. |
| Backend Agent | Perform read-only scan first; if later authorized, own one-record Word generation endpoint/service and backend tests. |
| Frontend Agent | Perform read-only scan first; if later authorized, own detail-page export action and download handling only. |
| AI Agent | No implementation role; no model, training, class, weight, inference-chain, video, or realtime changes. |

Recommended default decision:

```text
Docs/Test planning: AUTHORIZED for this document only
Backend read-only scan: RECOMMENDED BEFORE GO, NOT IMPLEMENTATION
Frontend read-only scan: RECOMMENDED BEFORE GO, NOT IMPLEMENTATION
Backend implementation: NOT AUTHORIZED
Frontend implementation: NOT AUTHORIZED
AI implementation: NOT AUTHORIZED
```

## 9. Backend Read-only Scan Questions

Before any Step 5 Implementation GO Decision, Backend Agent should answer these questions with file/line evidence and no code changes:

1. Which existing endpoint returns a single detection record detail, and can the report endpoint reuse its service lookup path?
2. What exact fields are returned for record ID, filename/original filename, created/detection time, status, model info, target count, timing, original image path/url, result image path/url, and `detection_result`?
3. Are original/result image references stored as safe relative paths, public URLs, or filesystem paths, and which helper resolves them?
4. Can current file helper logic safely prevent path traversal when resolving images for embedding?
5. Is there already a dependency capable of `.docx` generation? If not, what is the smallest dependency candidate and what install/build risk does it introduce?
6. What response pattern is used for file download/streaming in the Flask app, if any?
7. What authentication/authorization decorator or request context must protect the export endpoint?
8. What backend tests already cover record detail and file access, and where should report-export tests be placed if later authorized?
9. What should happen if a record exists but one or both images are missing/unreadable?
10. Can generation remain synchronous for one record under expected MVP report size?

## 10. Frontend Read-only Scan Questions

Before any Step 5 Implementation GO Decision, Frontend Agent should answer these questions with file/line evidence and no code changes:

1. Where is the detection record detail page action area/header, and what is the least disruptive place for an export button?
2. Which API helper currently fetches a single detection record detail?
3. Does the frontend already have a blob download helper or existing download pattern?
4. How does the request wrapper handle `responseType: 'blob'` or raw Axios response options?
5. Which existing loading/error UI patterns should an export action reuse?
6. Which record fields are already normalized/displayed on the detail page and should match report labels?
7. How are original/result images currently rendered and resolved?
8. What compatibility behavior exists for missing `detection_result`, missing timing, empty detections, and missing images?
9. What frontend build/type checks should prove the export action does not regress detail display?
10. Can the export UI be added without changing routes, list behavior, detection flow, or existing detail layout semantics?

## 11. Verification Requirements

A future authorized Step 5 implementation should be accepted only after evidence covers all items below.

### Planning / Gate verification for this task

- only `agent_outputs/docs/PHASE2B_BATCH4_STEP5_WORD_REPORT_PLANNING.md` is added/modified;
- no `web-vue/**` changes;
- no `web-flask/**` changes;
- no DB/Docker/runtime/storage/model changes;
- `git diff --check` passes;
- git status/diff evidence is recorded in the final response;
- Step 5 Implementation remains `NOT AUTHORIZED`.

### Future implementation verification, if separately authorized

1. Backend checks:
   - backend tests for successful `.docx` export from an existing record;
   - backend tests or manual evidence for missing optional fields;
   - backend tests or manual evidence for missing/unreadable images;
   - response headers include Word `.docx` content type or safe attachment behavior;
   - record-not-found returns existing error style;
   - path traversal is not possible through image references.
2. Frontend checks:
   - `npm.cmd run build` or `npm run build` from `web-vue/`;
   - detail page still loads an existing record;
   - export button triggers a `.docx` download for one record;
   - export loading/error states are visible and non-blocking;
   - missing `detection_result` / empty detections / missing images do not crash the detail page.
3. Report content smoke:
   - generated `.docx` opens in Word-compatible tooling;
   - report includes record ID, filename, time, model, status, count, confidence stats, timing, target table, safe image inclusion when available, and `detection_result.v1` summary;
   - missing image placeholders are acceptable and explicit.
4. Scope guard:
   - no DB schema changes;
   - no Dockerfile or compose changes;
   - no runtime/storage layout changes;
   - no model/weights/classes/training changes;
   - no video/realtime/Dashboard/batch/custom-template implementation;
   - existing detection APIs remain backward compatible;
   - `detection_result.v1` preserved.
5. Git checks:
   - `git diff --check`;
   - `git status --short --branch`;
   - `git diff --stat`;
   - `git diff --name-status`.

## 12. Rollback Baseline

Rollback baseline for any future Step 5 implementation should be:

```text
rollback baseline: phase2b-batch4-step4-detail-readability-stable
rollback baseline commit: 66349abc9ba3f8ad4a31afe85d5430a52b0a4393
rollback baseline meaning: Step 4 closed, verified, and tagged; Step 5 implementation not started
```

If Step 5 is later implemented and must be reverted:

- revert only Step 5 implementation commits and Step 5 verification/closeout docs;
- preserve the Step 4 stable tag unless separately authorized;
- no DB rollback should be required under the recommended default scope;
- no Docker/runtime/storage/model rollback should be required;
- if a document-generation dependency was added under a later GO Decision, remove it by reverting that authorized Step 5 commit.

## 13. Step 5 Implementation Authorization State

```text
Step 5 Planning / Gate: OPENED BY THIS DOCUMENT
Recommended Step 5: Word Report Export MVP
Step 5 Implementation: NOT AUTHORIZED
Backend implementation: NOT AUTHORIZED
Frontend implementation: NOT AUTHORIZED
AI implementation: NOT AUTHORIZED
DB schema changes: NOT AUTHORIZED
Docker/runtime/storage/model changes: NOT AUTHORIZED
Dashboard/video/realtime implementation: NOT AUTHORIZED
batch/custom-template report work: NOT AUTHORIZED
```

Planning does not equal implementation authorization. A separate Step 5 GO Decision must be created before any business code changes.

## 14. Step 5 Stable Tag State

```text
Step 5 stable tag: NOT CREATED
```

This planning task must not create a Step 5 stable tag.

## 15. Push State

```text
push: NOT DONE
```

This planning task must not push to any remote.

## 16. Current Decision

```text
Phase 2B Batch4 Step 5 Planning / Gate: OPENED
Recommended Step 5 direction: Word Report Export MVP
Reason: closest low-risk continuation of record-detail chain; single-record scope; additive; verifiable; reversible; no default DB schema/video/realtime/async/batch/template expansion.
Step 5 Implementation: NOT AUTHORIZED
Step 5 stable tag: NOT CREATED
push: NOT DONE
business code changes: NOT DONE
web-vue changes: NOT DONE
web-flask changes: NOT DONE
DB schema changes: NOT DONE
Docker changes: NOT DONE
runtime/storage changes: NOT DONE
model/weights/classes/training changes: NOT DONE
Dashboard implementation: NOT DONE
video / realtime implementation: NOT DONE
batch report / custom template implementation: NOT DONE
```

## 17. Post-Tag Archive Update

```text
Step 5 status: CLOSED / VERIFIED / TAGGED
Step 5 stable tag: phase2b-batch4-step5-word-report-stable
tag target: 645f2dccb7f32963123c8d16fac9f6a8044f906d
master HEAD before archive: 645f2dc
push: NOT DONE
Step 6: NOT AUTHORIZED
```

This post-tag archive update supersedes the original planning-time tag state. The original planning document did not create or authorize implementation by itself; later authorized implementation completed the Word Report Export MVP and the stable tag now points at the Step 5 evidence merge commit.

Tagged implementation summary:

- Backend Word report API: `GET /api/detection/records/<record_id>/report.docx`.
- JWT auth.
- Permission reuse via `get_record`.
- `resolve_object_path` path safety.
- `python-docx>=1.1`.
- `BytesIO` no persistent report file.
- Frontend `DetectionRecordDetail.vue` ??? Word ?????.
- `requestBlob()`.
- `exportDetectionRecordWordReport(id)`.
- `saveBlob()`.
- `Content-Disposition` filename parsing.

Tagged verification summary:

- backend compileall PASS.
- pytest PASS, 21 passed, 130 warnings.
- frontend npm build PASS.
- git diff --check PASS.
- working tree clean.

Confirmed NOT changed:

- DB schema.
- Dockerfile / `docker-compose.yml`.
- runtime/storage structure.
- model / weights / class / training.
- `detection_result.v1` semantics.
- image detection main flow semantics.
- auth/login semantics.
- Dashboard implementation.
- video detection implementation.
- realtime detection implementation.

Push remains NOT DONE. Step 6 remains NOT AUTHORIZED.
