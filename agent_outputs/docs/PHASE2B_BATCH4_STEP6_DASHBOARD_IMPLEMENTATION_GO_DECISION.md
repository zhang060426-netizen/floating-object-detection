# Phase 2B Batch4 Step 6 Dashboard Implementation GO Decision

Status: GO DECISION / IMPLEMENTATION AUTHORIZATION
Date: 2026-05-22
Phase: Phase 2B Batch4 Step 6
Step 6 name: Dashboard ????? MVP
Current master HEAD: `e4a3820` (`Add Batch4 Step6 planning`)
Step 5 stable tag: `phase2b-batch4-step5-word-report-stable`
Step 5 stable tag target: `645f2dccb7f32963123c8d16fac9f6a8044f906d`
Step 5 status: CLOSED / VERIFIED / TAGGED / ARCHIVED
Step 6 Planning: `e4a3820 Add Batch4 Step6 planning`
Step 6 Implementation before this document: NOT AUTHORIZED
Step 6 stable tag: NOT CREATED
Push: NOT DONE
Step 7: NOT AUTHORIZED

## 1. Decision Summary

```text
Step 6 Implementation: AUTHORIZED FOR DASHBOARD ????? MVP ONLY
Recommended direction: Dashboard ????? MVP
Backend Agent implementation: GO
Frontend Agent implementation: GO
Docs/Test checklist/evidence: GO
AI Agent: NOT REQUIRED
video detection implementation: NO-GO
realtime detection implementation: NO-GO
model / weights / class / training changes: NO-GO
DB schema change: NO-GO
Docker/runtime/storage changes: NO-GO
Step 7: NOT AUTHORIZED
push: NOT DONE
Step 6 stable tag: NOT CREATED
```

This GO Decision authorizes only a narrow Dashboard ????? MVP. It does not authorize video detection, realtime detection, model/training work, DB schema changes, Docker/runtime/storage changes, push, tag creation, or Step 7.

## 2. Read-Only Scan Inputs

### 2.1 Frontend read-only scan: PASS

Recommended frontend direction:

- Add `web-vue/src/views/Dashboard.vue`.
- Add `/dashboard` route.
- Add a top menu entry in `AppLayout.vue`: Dashboard / ????.
- Use Element Plus cards, tables, tags, alerts, skeleton/loading, and empty state for the MVP.
- Reuse `detectionDisplay.ts` and `format.ts` helpers where useful.
- Do not add a chart dependency.
- Do not add shared types unless needed for stable API consumption.
- Do not implement video or realtime UI.

### 2.2 Backend read-only scan: PASS

Recommended backend direction:

```text
GET /api/detection/dashboard/summary
```

Reasons:

- supports accurate full totals;
- avoids frontend pagination loops over every record;
- centralizes compatibility logic for old records, missing `detection_result`, empty detections, and missing confidence;
- reuses backend permission boundaries: admins aggregate all records, normal users aggregate only their records;
- does not require a DB schema change.

Recommended backend file range:

- `web-flask/routes/detection.py`
- `web-flask/services/detection_service.py`
- `web-flask/tests/test_dashboard_summary.py`

### 2.3 Docs/Test draft: GO

Draft checklist already exists locally for later evidence organization:

```text
agent_outputs/docs/PHASE2B_BATCH4_STEP6_DASHBOARD_VERIFICATION_CHECKLIST_DRAFT.md
```

This GO Decision does not require committing that draft now. After implementation, Docs/Test should consolidate formal verification evidence and closeout docs.

## 3. GO / NO-GO Matrix

| Lane / Scope | Decision | Notes |
|---|---|---|
| Backend Agent implementation | GO | Implement the narrow authenticated dashboard summary API and tests within the authorized backend file set only. |
| Frontend Agent implementation | GO | Implement Dashboard page, route, menu entry, and optional API/types helpers within the authorized frontend file set only. |
| Docs/Test checklist/evidence | GO | Prepare verification checklist/evidence after implementation; no business code ownership. |
| AI Agent | NOT REQUIRED | Dashboard MVP uses structured detection-record statistics; it does not need natural-language generation, multimodal interpretation, Qwen-VL, or external LLM calls. |
| Video detection implementation | NO-GO | Deferred; higher runtime, file-size, task-state, and progress complexity. |
| Realtime detection implementation | NO-GO | Deferred; highest streaming/camera/performance risk. |
| Model / weights / class / training changes | NO-GO | No model semantics or training work is needed for dashboard statistics. |
| DB schema change | NO-GO | Dashboard MVP should compute from existing `detection_records` and `detection_result`. |
| Docker/runtime/storage changes | NO-GO | No deployment/runtime/storage changes are needed. |
| Step 7 | NOT AUTHORIZED | Step 7 requires separate planning/authorization. |
| Push | NOT DONE / NO-GO in implementation | Push remains outside this local implementation gate. |
| Tag | NOT CREATED / NO-GO in implementation | Stable tag can only be created after implementation, verification, evidence, and explicit tag instruction. |

## 4. Authorized Backend File Scope

Backend Agent may modify only:

- `web-flask/routes/detection.py`
- `web-flask/services/detection_service.py`
- `web-flask/tests/test_dashboard_summary.py`

Backend Agent must not modify:

- DB schema files;
- Dockerfile / `docker-compose.yml`;
- runtime/storage structure;
- model/weights/class/training files;
- auth/login semantics;
- file storage layout;
- video/realtime code paths;
- unrelated backend routes/services/tests.

## 5. Authorized Frontend File Scope

Frontend Agent may modify only:

- `web-vue/src/views/Dashboard.vue`
- `web-vue/src/router/index.ts`
- `web-vue/src/components/AppLayout.vue`
- `web-vue/src/api/detection.ts` only if needed
- `web-vue/src/types/detection.ts` only if needed

Frontend Agent should avoid new dependencies. In particular, do not add a chart library for this MVP.

Frontend Agent must not modify:

- video detection UI;
- realtime detection UI;
- login/401 semantics except through existing request behavior;
- Word report download behavior;
- model training or model-weight surfaces;
- unrelated pages/components.

## 6. Backend MVP Requirements

Backend must implement:

1. New API:

   ```text
   GET /api/detection/dashboard/summary
   ```

2. API must require JWT via the existing auth decorator.
3. Permission boundaries must match records list behavior:
   - admin users aggregate all records;
   - normal users aggregate only their own records.
4. No DB schema changes.
5. No `detection_result.v1` semantic changes.
6. Summary logic must tolerate:
   - missing `detection_result`;
   - invalid / non-dict / legacy detection result values;
   - empty detections;
   - missing confidence;
   - old records missing `summary`;
   - missing `result_image`.
7. Recommended stable response fields:
   - `total_records`
   - `total_targets`
   - `average_confidence`
   - `detected_records`
   - `no_detection_records`
   - `unknown_records`
   - `latest_detection_time`
   - `recent_records`
8. `recent_records` should be limited to 5 or 10 records.
9. JSON shape must be stable and directly consumable by the frontend.
10. MVP may scan all matching records, but implementation/evidence must record future optimization direction for large datasets.

Recommended response shape:

```json
{
  "total_records": 0,
  "total_targets": 0,
  "average_confidence": null,
  "detected_records": 0,
  "no_detection_records": 0,
  "unknown_records": 0,
  "latest_detection_time": null,
  "recent_records": []
}
```

Recommended `recent_records` item fields:

```json
{
  "id": "dr_xxx",
  "record_id": "dr_xxx",
  "create_time": "...",
  "filename": "...",
  "model_id": "...",
  "model_name": "...",
  "target_count": 0,
  "status": "unknown",
  "average_confidence": null
}
```

The exact item shape may reuse existing record/detail display conventions, but it must remain stable and documented in evidence.

## 7. Frontend MVP Requirements

Frontend must implement:

1. New Dashboard page:

   ```text
   web-vue/src/views/Dashboard.vue
   ```

2. New route:

   ```text
   /dashboard
   ```

3. Add top menu entry in `AppLayout.vue`:

   ```text
   Dashboard / ????
   ```

4. Optional root route redirect to `/dashboard` if it does not break existing flows.
5. Page must display:
   - total detection records;
   - total detected targets;
   - average confidence;
   - latest detection time;
   - detected / no_detection / unknown record counts;
   - recent detection record list.
6. Recent records list must include:
   - time;
   - filename;
   - model;
   - target count;
   - status;
   - detail entry/link.
7. Must support:
   - loading;
   - error;
   - empty state;
   - missing `detection_result`;
   - old records.
8. Do not introduce a chart library.
9. Do not implement video detection UI.
10. Do not implement realtime detection UI.
11. Must not break:
    - `/detect/image`;
    - `/records/detection`;
    - `/records/detection/:id`;
    - login / 401 behavior;
    - Word report download.

## 8. Dashboard MVP Content

Dashboard MVP should prioritize simple, verifiable visual summaries:

- statistics cards for total records, total targets, average confidence, and latest detection time;
- status cards or compact distribution for detected / no_detection / unknown;
- recent records table with a clear detail entry;
- empty state when no records exist;
- friendly error state if the summary API fails;
- loading state while fetching;
- old-record safe labels for missing fields.

A simple trend/distribution display is optional only if it can be implemented without new dependencies or broad scope. Element Plus cards/tables/tags are sufficient for MVP acceptance.

## 9. Strictly Forbidden Scope

Strictly forbidden in Step 6 implementation:

- video detection implementation;
- realtime detection implementation;
- model training;
- model / weights / class changes;
- DB schema changes;
- Dockerfile / `docker-compose.yml` changes;
- runtime/storage changes;
- complex asynchronous task system;
- caching system;
- permission-system refactor;
- Step 7;
- push;
- tag creation.

Also forbidden unless a separate future GO Decision authorizes it:

- new charting dependency;
- data warehouse / analytics table;
- batch/report-history system;
- changes to `detection_result.v1` semantics;
- changes to image detection main-flow semantics;
- auth/login semantic changes.

## 10. Verification Requirements

Backend verification after implementation:

```powershell
cd web-flask
python -m compileall .
python -m pytest
```

Frontend verification after implementation:

```powershell
cd web-vue
npm.cmd run build
```

General verification:

```powershell
git diff --check
git status --short
```

Required verification confirmations:

- dashboard summary API requires JWT;
- admin sees aggregate over all records;
- normal user sees only own records;
- missing `detection_result` does not 500;
- empty detections are handled;
- missing confidence is ignored or safely represented;
- old records missing summary are handled;
- missing `result_image` does not affect dashboard summary;
- frontend loading/error/empty states work;
- recent record detail links work;
- `/detect/image`, `/records/detection`, `/records/detection/:id`, login/401, and Word report download remain intact;
- no DB schema changes;
- no Docker/runtime/storage changes;
- no model/weights/class/training changes;
- Step 6 stable tag remains NOT CREATED during implementation;
- push remains NOT DONE.

## 11. Docs/Test Evidence Requirements

Docs/Test should convert the draft checklist into formal evidence after implementation. Evidence should record:

- implementation commit(s);
- backend file scope;
- frontend file scope;
- API response shape;
- permission verification;
- old-record/missing-field compatibility;
- backend compile/test results;
- frontend build result;
- diff/status checks;
- no-entry checks for DB, Docker, runtime/storage, model/weights/class/training, video, realtime, push, tag, and Step 7.

The existing draft checklist path is:

```text
agent_outputs/docs/PHASE2B_BATCH4_STEP6_DASHBOARD_VERIFICATION_CHECKLIST_DRAFT.md
```

It should remain docs/test material and not expand implementation scope.

## 12. Rollback Baseline

Rollback baseline:

```text
phase2b-batch4-step5-word-report-stable -> 645f2dccb7f32963123c8d16fac9f6a8044f906d
```

Rollback plan:

1. Revert any Step 6 implementation merge commit(s) if dashboard implementation must be backed out.
2. Revert backend dashboard summary API changes if backend work causes regressions.
3. Revert frontend dashboard page/route/menu/API helper changes if frontend work causes regressions.
4. No DB migration rollback should be required because DB schema changes are NO-GO.
5. No Docker/runtime/storage/model/training rollback should be required because those scopes are NO-GO.

## 13. Implementation Handoff Boundaries

Backend Agent handoff:

```text
Implement only GET /api/detection/dashboard/summary, summary aggregation helpers, and backend tests inside the authorized backend files.
```

Frontend Agent handoff:

```text
Implement only Dashboard.vue, /dashboard routing, AppLayout menu entry, and any needed detection API/types helpers inside the authorized frontend files.
```

Docs/Test handoff:

```text
Maintain checklist/evidence/closeout only. Do not modify business code.
```

AI Agent handoff:

```text
NOT REQUIRED. Dashboard MVP is based on structured statistics from persisted detection records and does not need natural-language generation, multimodal explanation, Qwen-VL integration, or external LLM calls.
```

## 14. Final GO Decision

```text
Phase 2B Batch4 Step 6 Dashboard Implementation: GO FOR DASHBOARD ????? MVP ONLY
Backend Agent implementation: GO
Frontend Agent implementation: GO
Docs/Test checklist/evidence: GO
AI Agent: NOT REQUIRED
video detection implementation: NO-GO
realtime detection implementation: NO-GO
model / weights / class / training changes: NO-GO
DB schema change: NO-GO
Docker/runtime/storage changes: NO-GO
complex async task system: NO-GO
cache system: NO-GO
permission-system refactor: NO-GO
Step 6 stable tag: NOT CREATED
push: NOT DONE
Step 7: NOT AUTHORIZED
```

This document authorizes implementation only within the file scopes and MVP requirements above. It does not itself implement code, push, tag, or authorize Step 7.

## 15. Post-Tag Archive Update

```text
Step 6 stable tag: phase2b-batch4-step6-dashboard-stable
tag target: 708a61a
tag target commit message: Merge Phase 2B Batch4 Step6 dashboard verification evidence
Step 6 status: CLOSED / STABLE / ARCHIVED
push: NOT DONE
Step 7: NOT AUTHORIZED
```

This post-tag archive update records the completed Step 6 outcome after the earlier GO Decision. It does not change the original GO Decision constraints; it records that the authorized Dashboard MVP was implemented, verified, merged, and tagged.

Tagged implementation summary:

- Backend Dashboard summary API.
- `GET /api/detection/dashboard/summary`.
- JWT auth.
- admin all / normal user own records.
- `recent_records` default 5 max 10.
- Frontend `Dashboard.vue`.
- `/dashboard` route.
- `/` redirect to `/dashboard`.
- `AppLayout` Dashboard / ????.
- API field mapping fix.
- unified verification PASS.

Tagged verification summary:

- compileall PASS.
- pytest PASS, 26 passed, 152 warnings.
- `npm.cmd run build` PASS.
- git diff --check PASS.
- git status clean.

Confirmed NOT changed:

- DB schema.
- Docker/runtime/storage.
- model/weights/class/training.
- `detection_result.v1` semantics.
- video/realtime implementation.
- AI Agent / LLM feature.

Push remains NOT DONE. Step 7 remains NOT AUTHORIZED.
