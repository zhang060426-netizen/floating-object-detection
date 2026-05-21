# Phase 2B Batch4 Step 3 Planning / Gate - Detection Records Management Enhancement

Status: PLANNING ARCHIVED / STEP 3 CLOSED / VERIFIED / TAGGED
Date: 2026-05-21
Phase: Phase 2B Batch4 Step 3
Step 3 name: Phase 2B Batch4 Step 3 - Detection Records Management Enhancement
Current master HEAD: `e85f8aa`
Latest stable baseline: `phase2b-batch4-step2-frontend-timing-stable`
Stable baseline target: `78b9896c133bfdf59b99a03a41348b3a372885b8`
Phase 2B Batch4 Step 2: CLOSED / VERIFIED / TAGGED / ARCHIVED
Push: NOT DONE
Step 3 Implementation: NOT AUTHORIZED

## 1. Planning Purpose

This document opens the Step 3 planning gate only. It defines the smallest safe future scope for improving detection-records management usability.

It does **not** authorize implementation.
It does **not** authorize business-code changes.
It does **not** authorize backend changes.
It does **not** authorize push or tag creation.

## 2. Step 3 Objective

Enhance the detection records list page usability and management experience while preserving existing list/detail behavior and legacy record compatibility.

Minimum user-facing goal for a future authorized implementation:

- records list remains readable and refreshable;
- records list supports backend pagination metadata when available;
- users can see total/current page/page size state;
- existing detail navigation remains available;
- old records with missing fields continue to render safely.

## 3. Current Evidence Snapshot (Read-Only)

Frontend read-only observations:

- `web-vue/src/views/DetectionRecords.vue:17` renders the records table.
- `web-vue/src/views/DetectionRecords.vue:19` displays record time via `recordTime(row)`.
- `web-vue/src/views/DetectionRecords.vue:21-28` displays file, model, and target count.
- `web-vue/src/views/DetectionRecords.vue:30-35` displays status.
- `web-vue/src/views/DetectionRecords.vue:39` keeps detail navigation to `/records/detection/{id}`.
- `web-vue/src/views/DetectionRecords.vue:63-64` already accepts either array responses or paged responses.
- `web-vue/src/views/DetectionRecords.vue:72-73` normalizes `items` / `records` / `list` arrays.
- `web-vue/src/api/detection.ts:24-26` currently fetches `/api/detection/records` without query params.
- `web-vue/src/types/detection.ts:120-126` already defines `PageResult<T>` with `items`, `records`, `list`, `total`, `page`, and `page_size`.
- `web-vue/src/utils/detectionDisplay.ts:13-28` provides count/status fallbacks for missing detection result shapes.
- `web-vue/src/utils/detectionDisplay.ts:85-96` consumes `detection_result.timing` and preserves `detection_result.timing_ms` legacy fallback.

Backend read-only observations:

- `web-flask/routes/detection.py:92-100` exposes `GET /detection/records` and parses `page` / `page_size` query parameters.
- `web-flask/services/detection_service.py:157-165` returns `items`, `total`, `page`, and `page_size`.
- `web-flask/routes/detection.py:103-109` exposes record detail lookup.

Planning inference: Step 3 can likely remain frontend-only if a later GO Decision is issued, because the existing backend list API already appears to support pagination metadata. Backend Agent should still perform a read-only contract check before implementation starts.

## 4. Recommended Allowed Scope for Future GO Decision

If and only if a separate Step 3 GO Decision is created later, the recommended implementation file surface is limited to:

- `web-vue/src/views/DetectionRecords.vue`
- `web-vue/src/api/detection.ts`
- `web-vue/src/types/detection.ts`
- `web-vue/src/utils/detectionDisplay.ts`

Expected direction for those files:

- add query-param support to the records API helper if needed;
- preserve current array-response fallback;
- preserve current `PageResult<T>` compatibility shape;
- add page/current page/page size/total state in the records view;
- keep refresh and detail navigation behavior;
- keep old record fallbacks for file/model/count/status fields.

This candidate list is planning-only and must not be treated as authorization.

## 5. Backend Agent Read-Only Scope

Backend Agent scope for Step 3 planning / pre-GO validation is read-only:

- check whether records list API already supports `page`;
- check whether records list API already supports `page_size`;
- check whether list response includes `total`;
- check whether list response echoes `page` and `page_size`;
- check whether record detail API remains unchanged;
- confirm no backend code change is needed by default.

Default backend decision:

```text
Backend implementation: NOT PLANNED BY DEFAULT
Backend changes: NOT AUTHORIZED
DB schema changes: NOT AUTHORIZED
```

## 6. Frontend Agent Planning

Future frontend planning should stay minimal and additive:

- add records-list pagination using existing backend metadata where present;
- display total/current page/page size state;
- keep the existing refresh button behavior;
- keep record-detail navigation behavior;
- display existing fields only:
  - detection time;
  - filename;
  - model name;
  - target count;
  - status;
- preserve compatibility for:
  - old records;
  - missing `detection_result`;
  - missing `detection_result.timing`;
  - legacy `detection_result.timing_ms`;
  - list responses that return arrays instead of paged objects;
  - paged objects using `items`, `records`, or `list`.

Suggested future UI behavior:

- default page: `1`;
- default page size: `20` unless existing backend/UI evidence says otherwise;
- page-size options should remain conservative, for example `10 / 20 / 50 / 100`;
- changing page or page size should reload records through the list API;
- refresh should reload the current page and preserve current page size;
- if the backend returns an array, show the array and derive total from array length without breaking.

## 7. Docs/Test Agent Planning

Future Step 3 evidence should include:

- `npm run build` from `web-vue/`;
- records list smoke:
  - page loads;
  - table renders;
  - pagination state is visible when metadata exists;
  - array fallback remains safe if applicable;
- record detail smoke:
  - detail navigation from the list still works;
  - detail page renders a selected record;
- legacy/no timing compatibility:
  - missing `detection_result` does not crash list rendering;
  - missing timing does not crash list/detail rendering;
  - legacy `detection_result.timing_ms` fallback remains preserved where timing display is used;
- scope guard:
  - no `web-flask/**` changes unless a separate backend GO Decision exists;
  - no Docker, DB, runtime/storage, model/weight/category/training changes;
  - no video/realtime/Word/Dashboard changes;
  - `detection_result.v1` semantics preserved.

Recommended future evidence archive names, if implementation is later authorized:

- `agent_outputs/docs/PHASE2B_BATCH4_STEP3_IMPLEMENTATION_GO_DECISION.md`
- `agent_outputs/docs/PHASE2B_BATCH4_STEP3_VERIFICATION_EVIDENCE.md`
- `agent_outputs/docs/PHASE2B_BATCH4_STEP3_DETECTION_RECORDS_CLOSEOUT.md`

These files are not required by this planning task.

## 8. Explicit Forbidden Scope

Step 3 planning does not authorize:

- deletion or batch deletion;
- Dashboard / large-screen work;
- Word report work;
- video detection work;
- realtime detection work;
- Dockerfile changes;
- `docker-compose.yml` changes;
- DB schema changes;
- `runtime/**` changes;
- `storage/**` changes;
- model weight changes;
- model class/category changes;
- model training changes;
- `detection_result.v1` semantic changes;
- backend implementation by default;
- Step 3 implementation;
- new tag creation;
- push.

## 9. Compatibility Rules

Future Step 3 must preserve:

```text
detection_result.v1: PRESERVED
detection_result.timing consumed: PRESERVED from Step 2
detection_result.timing_ms legacy fallback preserved: YES
timing optional: YES
missing timing / legacy no timing compatible: YES
missing detection_result compatible: YES
records list array response compatible: YES
records list paged response compatible: YES
record detail route behavior: PRESERVED
```

## 10. Acceptance Criteria for This Planning Gate

This planning gate is complete when:

- Step 3 name is recorded;
- objective is recorded;
- candidate frontend file scope is recorded;
- backend read-only scope is recorded;
- frontend planning items are recorded;
- Docs/Test verification plan is recorded;
- forbidden scope is recorded;
- Step 3 Implementation remains explicitly NOT AUTHORIZED;
- no business code is changed;
- no push is performed;
- no tag is created.

## 11. Future GO Decision Requirements

Before any Step 3 implementation begins, a separate GO Decision must be created and must restate:

- exact implementation file scope;
- whether backend remains read-only or receives a separate explicit authorization;
- test/smoke commands to run;
- rollback plan;
- forbidden scope guard;
- Step 3 implementation owner;
- Docs/Test evidence owner.

## 12. Current Decision

```text
Phase 2B Batch4 Step 3 Planning: OPENED
Phase 2B Batch4 Step 3 - Detection Records Management Enhancement: PLANNING ONLY
Step 3 Implementation: NOT AUTHORIZED
Backend implementation: NOT AUTHORIZED
Push: NOT DONE
Tag creation: NOT DONE
Business code changes: NOT DONE
```

## Phase 2B Batch4 Step 3 Post-Tag Archive

```text
latest stable baseline: phase2b-batch4-step3-detection-records-stable
stable commit: bfe3dc9298cdcb0cb405b4189b6db151d2fea1c6
Step 3 status: CLOSED / VERIFIED / TAGGED
Step 3 completed: Detection Records Management Enhancement
Step 3 implementation commit: cfe8d75
Step 3 frontend merge commit: e5a7b59
Step 3 checklist commit: 1c5d415
Step 3 stable tag commit: bfe3dc9
build: npm.cmd run build PASS
backend: read-only verification PASS
backend records API: supports page/page_size and returns items/total/page/page_size
backend detail API: exists
backend implementation required: NO
detection_result.v1: PRESERVED
forbidden scope:
  - no backend change
  - no Docker change
  - no DB schema change
  - no runtime/storage change
  - no model/weights/classes/training change
  - no Dashboard / Word / video / realtime
  - no delete / bulk delete / edit records
push: NOT DONE
Step 4: NOT AUTHORIZED
```

This is a documentation-only post-tag archive. It records the already-created Step 3 stable tag and does not create a new tag, push, or authorize Step 4 implementation.
