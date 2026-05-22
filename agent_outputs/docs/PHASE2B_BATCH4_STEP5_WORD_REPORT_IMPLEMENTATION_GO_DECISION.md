# Phase 2B Batch4 Step 5 Word Report Implementation GO Decision

Status: GO DECISION / IMPLEMENTATION AUTHORIZATION
Date: 2026-05-22
Phase: Phase 2B Batch4 Step 5
Step 5 name: Phase 2B Batch4 Step 5 - Word Report Export MVP
Current master HEAD: `cb1c4a9`
Planning commit: `fe214a8`
Planning merge commit: `cb1c4a9`
Planning file: `agent_outputs/docs/PHASE2B_BATCH4_STEP5_WORD_REPORT_PLANNING.md`
Rollback baseline: `phase2b-batch4-step4-detail-readability-stable`
Rollback baseline commit: `66349abc9ba3f8ad4a31afe85d5430a52b0a4393`
Step 4 status: CLOSED / VERIFIED / TAGGED / ARCHIVED
Step 5 stable tag: NOT CREATED
Push: NOT DONE
Step 6: NOT AUTHORIZED

## 1. GO / NO-GO Conclusion

```text
Backend Agent implementation: GO
Frontend Agent implementation: GO
Docs/Test checklist/evidence: GO
AI Agent: NOT REQUIRED
Dashboard implementation: NO-GO
video detection implementation: NO-GO
realtime detection implementation: NO-GO
DB schema change: NO-GO
Docker/runtime/model changes: NO-GO
Step 5 stable tag: NOT CREATED
push: NOT DONE
Step 6: NOT AUTHORIZED
```

This GO Decision authorizes only the Step 5 Word Report Export MVP. It does not authorize any implementation beyond a single-record Word report export/download flow based on existing detection-record data.

This document creation task is documentation-only. Business-code edits are authorized for the later Step 5 implementation lane, but no business code is changed by this GO Decision document itself.

## 2. Read-only Scan Evidence

Backend read-only scan conclusion:

```text
Backend Agent read-only scan: PASS
recommended new API: GET /api/detection/records/<record_id>/report.docx
DB schema change required: NO
Docker volume change required: NO
runtime/storage structure change required: NO
new dependency required: python-docx>=1.1
permission model: reuse get_record authorization behavior
path safety: reuse resolve_object_path safety logic
result_image missing: degrade gracefully
detection_result missing: show unavailable state, do not return 500
```

Frontend read-only scan conclusion:

```text
Frontend Agent read-only scan: PASS
recommended request helper: requestBlob()
recommended API helper: exportDetectionRecordWordReport(id)
recommended UI: DetectionRecordDetail.vue top action button "?? Word ??"
recommended state: exportLoading
recommended UX: success / failure prompts
recommended type change: do not modify web-vue/src/types/detection.ts by default
```

Docs/Test scan conclusion:

```text
Docs/Test checklist draft exists as a draft only:
agent_outputs/docs/PHASE2B_BATCH4_STEP5_WORD_REPORT_VERIFICATION_CHECKLIST_DRAFT.md
Draft checklist is not submitted by this GO Decision task.
Formal evidence should be prepared after implementation is complete.
```

## 3. Authorized Agents

| Agent | Decision | Authorized responsibility |
|---|---|---|
| Backend Agent | GO | Implement the single-record Word report export endpoint, service, dependency, and backend tests inside the authorized backend file scope only. |
| Frontend Agent | GO | Implement the record-detail export button, blob download helper, API helper, loading state, and error handling inside the authorized frontend file scope only. |
| Docs/Test Agent | GO | Prepare formal checklist/evidence after implementation, verify scope, and archive closeout evidence. |
| AI Agent | NOT REQUIRED | No model, training, class/category, weight, inference-chain, video, or realtime work. |

## 4. Authorized Backend File Scope

Backend Agent may modify only these files:

- `web-flask/routes/detection.py`
- `web-flask/services/report_service.py`
- `web-flask/requirements.txt`
- `web-flask/tests/test_report_export.py`
- `web-flask/README.md` optional

No other `web-flask/**` files are authorized by this GO Decision unless a blocker is escalated and a separate authorization is created.

`web-flask/requirements.txt` may be changed only to add the minimal Word-generation dependency:

```text
python-docx>=1.1
```

## 5. Authorized Frontend File Scope

Frontend Agent may modify only these files:

- `web-vue/src/api/request.ts`
- `web-vue/src/api/detection.ts`
- `web-vue/src/views/DetectionRecordDetail.vue`
- `web-vue/src/utils/download.ts` only if needed

Not recommended and not authorized by default:

- `web-vue/src/types/detection.ts`

No other `web-vue/**` files are authorized by this GO Decision unless a blocker is escalated and a separate authorization is created.

## 6. Backend Required Implementation

Backend implementation must satisfy all of the following:

1. Add a single-record Word report download API:
   - `GET /api/detection/records/<record_id>/report.docx`
2. The API must require JWT authentication.
3. Authorization must match the existing detection-record detail API.
4. A normal user must not export another user's record.
5. An administrator may export all records.
6. The report must be generated from existing detection record data.
7. Use `python-docx` to generate `.docx` content.
8. Return the generated report directly from `BytesIO`; do not persist report files.
9. Do not add or change DB schema.
10. Do not add a reports bucket.
11. Do not modify runtime/storage directory structure.
12. Path resolution for original/result images must reuse existing safe path resolution logic, including `resolve_object_path` or the current equivalent; do not hand-write absolute path concatenation.
13. If `result_image` is missing or unreadable, the report must degrade gracefully and still generate when the record exists.
14. If `detection_result` is missing, the report must show `???????` or an equivalent explicit placeholder and must not return 500.
15. Old records must remain compatible.

Backend implementation must preserve existing detection APIs, record detail semantics, image detection main-flow semantics, auth/login semantics, and `detection_result.v1` semantics.

## 7. Frontend Required Implementation

Frontend implementation must satisfy all of the following:

1. Add a top-level `?? Word ??` button on the detection record detail page.
2. Add a blob download wrapper that reuses token authentication.
3. 401 handling must remain consistent with existing `request()` behavior.
4. Both non-JSON error responses and JSON error responses must produce a user-facing error message.
5. Extract the download filename from `Content-Disposition` when available.
6. A successful response must trigger browser file saving.
7. The export button must show loading state while downloading.
8. Failed export must call `ElMessage.error` or the existing equivalent error-message pattern.
9. If the record does not exist or is not loaded, the export action must be hidden or disabled.
10. Existing detail-page display must not be broken, including images, metadata, detection result rendering, empty/missing states, and JSON collapse.

Frontend implementation must preserve existing route behavior, list-to-detail navigation, image rendering, API call semantics, auth/login semantics, and `detection_result.v1` semantics.

## 8. Word Report MVP Content

The generated Word report must include the following MVP content where data is available:

- report title;
- record ID;
- file name;
- detection time;
- model information;
- detection status;
- target count;
- confidence threshold;
- highest confidence and average confidence, if available;
- elapsed/timing information, if available;
- detection target table;
- original image, if it can be safely resolved and read;
- result image, if it exists and can be safely resolved and read;
- explicit missing-field explanations;
- `detection_result.v1` summary.

Missing optional fields must render safe placeholders such as `N/A`, `???`, or `???????`. Missing optional images must not fail the whole report when the record itself is available.

## 9. Explicit Forbidden Scope

This GO Decision does not authorize:

- DB schema changes;
- migration scripts;
- Dockerfile changes;
- `docker-compose.yml` changes;
- runtime/storage directory structure changes;
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
- report history management;
- persistent report artifacts;
- reports bucket creation;
- asynchronous report task queue;
- scheduled report jobs;
- user-configurable report designer;
- external report service integration;
- broad UI redesign;
- unlisted backend files;
- unlisted frontend files;
- AI/model/training changes;
- push;
- tag creation;
- Step 6 planning or implementation.

If implementation needs any forbidden item, stop and request a separate explicit authorization gate.

## 10. Verification Requirements

Step 5 implementation is not complete until evidence records all required verification below.

### Backend verification

Run from `web-flask/`:

```text
python -m compileall .
python -m pytest
```

Backend evidence must also cover:

- successful `.docx` export for an existing record;
- JWT required;
- normal users cannot export other users' records;
- administrators can export all records;
- missing optional fields do not crash;
- missing/unreadable result image degrades gracefully;
- missing `detection_result` displays unavailable text and does not return 500;
- response headers support Word `.docx` download;
- generated report is returned from `BytesIO` and not persisted;
- path traversal is prevented by reused safe path resolution logic;
- old records remain compatible.

### Frontend verification

Run from `web-vue/`:

```text
npm.cmd run build
```

Frontend evidence must also cover:

- detail page still loads an existing record;
- `?? Word ??` button appears only when a record is available or is disabled when no record is available;
- export button uses loading state during download;
- successful export triggers browser file saving;
- filename is taken from `Content-Disposition` when available;
- JSON and non-JSON error responses show user-facing error prompts;
- 401 behavior remains consistent with existing request handling;
- detail page display, image rendering, empty states, and JSON collapse remain intact.

### General verification

Run from repository root:

```text
git diff --check
```

General evidence must confirm:

- only authorized files are modified;
- no DB schema changes;
- no Dockerfile or `docker-compose.yml` changes;
- no runtime/storage structure changes;
- no model/weight/category/training changes;
- no Dashboard, video, realtime, batch report, custom template, or report history implementation;
- `detection_result.v1` semantics preserved;
- Step 5 stable tag: NOT CREATED;
- push: NOT DONE;
- Step 6: NOT AUTHORIZED.

## 11. Rollback Baseline

Rollback baseline for Step 5 implementation:

```text
rollback baseline: phase2b-batch4-step4-detail-readability-stable
rollback baseline commit: 66349abc9ba3f8ad4a31afe85d5430a52b0a4393
rollback baseline meaning: Step 4 closed, verified, tagged, and archived; Step 5 implementation not started
```

If Step 5 implementation must be reverted later:

1. Revert only Step 5 implementation commits and Step 5 verification/closeout docs.
2. Preserve the Step 4 stable tag unless separately authorized.
3. No DB rollback should be required because DB schema changes are not authorized.
4. No Docker/runtime/storage/model rollback should be required because those changes are not authorized.
5. If `python-docx>=1.1` is added under this GO Decision, remove it by reverting the authorized Step 5 implementation commit that added it.

## 12. Release / Tag / Push State

```text
Step 5 stable tag: NOT CREATED
push: NOT DONE
Step 6: NOT AUTHORIZED
```

This GO Decision does not create a tag, does not push, and does not authorize Step 6. A future Step 5 stable tag requires completed implementation, verification evidence, closeout, and a separate tag/archive instruction.

## 13. Implementation Handoff Summary

```text
Step 5 Implementation: AUTHORIZED FOR WORD REPORT EXPORT MVP ONLY
Recommended direction: Word Report Export MVP
Backend Agent implementation: GO
Frontend Agent implementation: GO
Docs/Test checklist/evidence: GO
AI Agent: NOT REQUIRED
New backend API: GET /api/detection/records/<record_id>/report.docx
Backend dependency authorization: python-docx>=1.1 only
DB schema change: NO-GO
Docker/runtime/storage/model changes: NO-GO
Dashboard/video/realtime implementation: NO-GO
batch/custom-template/history report work: NO-GO
Step 5 stable tag: NOT CREATED
push: NOT DONE
Step 6: NOT AUTHORIZED
```

## 14. Current Decision

```text
Phase 2B Batch4 Step 5 Implementation GO Decision: GO
Backend Agent implementation: GO
Frontend Agent implementation: GO
Docs/Test checklist/evidence: GO
AI Agent: NOT REQUIRED
Business code changes in this GO Decision document task: NOT DONE
Step 5 stable tag: NOT CREATED
push: NOT DONE
Step 6: NOT AUTHORIZED
```
