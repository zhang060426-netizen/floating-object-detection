# Phase 2B Batch4 Step 7 Record Filter Implementation GO Decision

Status: GO DECISION / IMPLEMENTATION AUTHORIZATION
Date: 2026-05-23
Phase: Phase 2B Batch4 Step 7
Step 7 name: Detection Records Filter/Search Enhancement / 检测记录筛选/搜索增强
Working branch: `batch4-step7-record-filter-go`
Current master HEAD baseline: `1d81d33` (`Merge Phase 2B Batch4 Step7 planning`)
Step 7 Planning commit: `c40e016` (`Add Batch4 Step7 planning`)
Step 7 Planning merge commit: `1d81d33` (`Merge Phase 2B Batch4 Step7 planning`)
Latest stable baseline: `phase2b-batch4-step6-dashboard-stable` -> `708a61a`
Step 7 implementation before this document: NOT AUTHORIZED
Step 7 stable tag: NOT CREATED
Push: NOT DONE
Step 8: NOT AUTHORIZED

## 1. Decision Summary

```text
Step 7 Implementation: AUTHORIZED FOR DETECTION RECORDS FILTER/SEARCH ENHANCEMENT ONLY
Backend Agent implementation: GO
Frontend Agent implementation: GO
Docs/Test checklist/evidence: GO
AI Agent: NOT REQUIRED
Step 7 stable tag: NOT CREATED
push: NOT DONE
Step 8: NOT AUTHORIZED
```

This GO Decision authorizes a narrow additive enhancement to the existing detection-records list flow only. It authorizes server-side filtering and the matching frontend filter controls within the file allowlists and behavior constraints defined below.

This document is a docs-only authorization artifact. Creating or committing this document does **not** itself implement Step 7 functionality and must not modify business code.

## 2. Baseline and Prerequisite Inputs

### 2.1 Current Baseline

```text
master HEAD at GO Decision baseline: 1d81d33
master HEAD message: Merge Phase 2B Batch4 Step7 planning
Step 7 Planning commit: c40e016 Add Batch4 Step7 planning
latest stable tag: phase2b-batch4-step6-dashboard-stable
latest stable tag target: 708a61a
push: NOT DONE
Step 7 stable tag: NOT CREATED
Step 8: NOT AUTHORIZED
```

The stable product chain entering this implementation gate is:

```text
login -> image detection -> save record -> records list -> record detail -> Word report -> Dashboard
```

Step 7 may improve finding records in the existing records list. It must not change the semantics of the surrounding product chain.

### 2.2 Backend Read-Only Scan Input: COMPLETE

Backend read-only scan conclusions accepted for this GO Decision:

- `GET /api/detection/records` currently supports `page` and `page_size` only.
- The current list API does not yet support `keyword`, `model_id`, `detection_status`, `date_start`, or `date_end`.
- Existing permission behavior is:
  - admin users see all records;
  - normal users see only their own records.
- DB schema change for this MVP is not recommended.
- New DB index for this MVP is not recommended.
- Recommended backend implementation files are:
  - `web-flask/routes/detection.py`;
  - `web-flask/services/detection_service.py`;
  - `web-flask/tests/test_detection_records_filters.py`.

### 2.3 Frontend Read-Only Scan Input: COMPLETE

Frontend read-only scan conclusions accepted for this GO Decision:

- `DetectionRecords.vue` already supports records display, refresh, pagination, and detail navigation.
- It currently has no search/filter UI.
- `fetchDetectionRecords` currently supports `page` and `page_size` only.
- Filters must use a server-side paginated filter contract; filtering the currently visible frontend page is prohibited.
- Recommended frontend implementation files are:
  - `web-vue/src/views/DetectionRecords.vue`;
  - `web-vue/src/api/detection.ts`;
  - `web-vue/src/types/detection.ts`.
- `Dashboard`, detail, report, router, and menu changes are not recommended and are not authorized by this decision.

### 2.4 Docs/Test Checklist Input: COMPLETE FOR GO

The verification checklist draft has been prepared as a prerequisite input:

```text
agent_outputs/docs/PHASE2B_BATCH4_STEP7_RECORD_FILTER_VERIFICATION_CHECKLIST_DRAFT.md
```

The draft is currently not required to be committed as part of this GO Decision. Docs/Test is authorized to consolidate and commit the defined checklist/evidence/closeout documentation in the subsequent implementation verification and evidence phase.

## 3. GO / NO-GO Matrix

| Lane / Scope | Decision | Authorized purpose |
|---|---|---|
| Backend Agent implementation | **GO** | Implement optional server-side detection-record filtering within the backend allowlist and compatibility constraints. |
| Frontend Agent implementation | **GO** | Implement the records-page filter bar and pass applied filters to the server-side paginated API within the frontend allowlist. |
| Docs/Test checklist/evidence | **GO** | Organize verification checklist, evidence, closeout, and authorized planning/context documentation. |
| AI Agent | **NOT REQUIRED** | No AI/LLM, model, inference-chain, training, weight, or class work is needed. |
| Step 8 | **NOT AUTHORIZED** | Separate future gate required. |
| Push | **NOT DONE / NO-GO** | No remote push is authorized by this decision. |
| Tag | **NOT CREATED / NO-GO** | No Step 7 stable tag may be created until later verification and explicit instruction. |

## 4. Authorized Step 7 Implementation Scope

Authorized feature:

```text
Detection Records Filter/Search Enhancement
检测记录筛选/搜索增强
```

The implementation may add optional filters to the existing detection-record list endpoint and an additive search/filter bar to the existing records list page. It must preserve:

- existing JWT authentication;
- existing record visibility permissions;
- existing list response structure;
- existing unfiltered pagination behavior;
- existing record-detail navigation;
- existing Word report behavior;
- existing Dashboard behavior and summary API;
- existing `detection_result.v1` semantics.

## 5. Backend Agent Implementation Authorization: GO

### 5.1 Authorized Backend Files

Backend Agent may modify only:

```text
web-flask/routes/detection.py
web-flask/services/detection_service.py
web-flask/tests/test_detection_records_filters.py
```

Any additional backend file need requires a separate scope amendment before editing.

### 5.2 Required Backend Behavior

Backend Agent must implement all of the following:

1. Preserve JWT protection on:

   ```text
   GET /api/detection/records
   ```

2. Preserve the existing response shape:

   ```text
   items
   total
   page
   page_size
   ```

3. Preserve existing `page` / `page_size` compatibility:

   - `page` default is `1`;
   - `page_size` default is `20`;
   - `page_size` maximum is `100`;
   - non-integer `page` or `page_size` returns HTTP `400`.

4. Add only these optional filter query parameters:

   ```text
   keyword
   model_id
   detection_status
   date_start
   date_end
   ```

5. Preserve existing permission boundaries unchanged:

   - admin users see all permitted records;
   - normal users see only their own records;
   - filters narrow the already-authorized result set and must never broaden visibility.

6. Authorize only these canonical `detection_status` filter values:

   ```text
   detected
   no_detection
   unknown
   ```

   Any other `detection_status` value must return HTTP `400`.

7. Implement `detection_status` compatibility handling consistently with existing stored records and existing service/dashboard compatibility behavior, including:

   - missing `detection_result` maps to `unknown`;
   - malformed `detection_result` maps to `unknown`;
   - `summary.detection_status` when present;
   - legacy compatible status representations such as `success` / `empty` when already handled by service logic;
   - old records with detections but missing `summary`.

8. Apply `date_start` and `date_end` to:

   ```text
   create_time
   ```

9. Reject an inverted date range:

   ```text
   date_start > date_end -> HTTP 400
   ```

10. Reject invalid date formats with HTTP `400`.

11. Keep `detection_result.v1` semantics unchanged.

12. Make no DB schema change.

13. Add no new index for this MVP.

14. Make no change to the Dashboard summary API.

15. Make no change to detail or Word report APIs.

### 5.3 Backend Compatibility and Test Expectations

Backend implementation must remain additive:

- requests without optional filters must retain current records-list behavior;
- filtered results must retain server-side pagination and correct `total` metadata;
- query composition must retain the current permission scope;
- tests must cover successful filtering, invalid status, invalid/inverted dates, pagination compatibility, and user/admin visibility preservation as feasible within the authorized backend test file.

## 6. Frontend Agent Implementation Authorization: GO

### 6.1 Authorized Frontend Files

Frontend Agent may modify only:

```text
web-vue/src/views/DetectionRecords.vue
web-vue/src/api/detection.ts
web-vue/src/types/detection.ts
```

Any additional frontend file need requires a separate scope amendment before editing.

### 6.2 Required Frontend Behavior

Frontend Agent must implement all of the following:

1. Add an additive filter/search bar to `DetectionRecords.vue`.

2. Provide the following controls:

   - `keyword` input;
   - `model_id` input or simple text input;
   - `detection_status` select;
   - date range picker;
   - 查询 button;
   - 重置 button.

3. Extend `fetchDetectionRecords` to pass the newly authorized query parameters to the backend list endpoint.

4. Extend `DetectionRecordQuery` with:

   ```ts
   keyword?: string
   model_id?: string
   detection_status?: string
   date_start?: string
   date_end?: string
   ```

5. On a new query action, set:

   ```text
   currentPage = 1
   ```

6. When paging, preserve currently applied filters.

7. When `page_size` changes, preserve currently applied filters and reset:

   ```text
   currentPage = 1
   ```

8. When refreshing the list, preserve currently applied filters.

9. When resetting filters, clear all filter inputs/applied filters and reset:

   ```text
   currentPage = 1
   ```

10. Do not implement frontend current-page/local-only filtering. All filtering must be supplied to the server-side paginated records API.

11. Do not modify Dashboard.

12. Do not modify `DetectionRecordDetail`.

13. Do not modify Word report behavior.

14. Do not modify router or menu.

15. Do not add a chart or other new UI dependency.

### 6.3 Frontend Compatibility Expectations

Frontend implementation must preserve:

- existing list rendering;
- refresh behavior, with applied-filter preservation added only as authorized;
- existing pagination user experience;
- existing loading, error, and empty-result handling unless narrowly adjusted within `DetectionRecords.vue` for filtered states;
- existing detail navigation;
- existing Dashboard, report, route, and menu behavior.

## 7. Docs/Test Authorization: GO

Docs/Test may later organize, amend, or add only the following documentation/evidence surfaces for this Step 7 scope:

```text
agent_outputs/docs/PHASE2B_BATCH4_STEP7_RECORD_FILTER_VERIFICATION_CHECKLIST_DRAFT.md
agent_outputs/docs/PHASE2B_BATCH4_STEP7_RECORD_FILTER_VERIFICATION_EVIDENCE.md
agent_outputs/docs/PHASE2B_BATCH4_STEP7_RECORD_FILTER_CLOSEOUT.md
PROJECT_CONTEXT.md
README.md
agent_outputs/docs/PHASE2B_BATCH4_MASTER_PLANNING_GATE.md
```

Docs/Test responsibility includes:

- validation checklist maintenance;
- backend/frontend evidence consolidation;
- scope-guard confirmation;
- rollback recording;
- closeout documentation after implementation passes verification.

Docs/Test authorization does not allow business-code changes.

## 8. AI Agent Decision: NOT REQUIRED

```text
AI Agent: NOT REQUIRED
```

Step 7 concerns detection-record retrieval and filter UI only. No work is authorized or needed for:

- AI Agent / LLM features;
- multimodal analysis;
- model inference behavior;
- model weights;
- detection classes;
- model training or evaluation;
- model replacement;
- `detection_result.v1` semantic changes.

## 9. Explicit NO-GO

The following remain prohibited:

- no Step 8;
- no video detection implementation;
- no realtime detection implementation;
- no AI Agent / LLM feature;
- no model / weights / classes / training changes;
- no DB schema change;
- no DB migration;
- no new index for the MVP;
- no Docker/runtime/storage changes;
- no auth/login semantic change;
- no permission-boundary change;
- no `detection_result.v1` semantic change;
- no Dashboard summary API change;
- no Dashboard frontend change;
- no detection-detail API or UI change;
- no Word report behavior change;
- no router/menu change;
- no new chart dependency;
- no push;
- no tag.

## 10. Verification Requirements After Implementation

Implementation is not complete until all authorized implementation branches and evidence are verified against this allowlist and all checks below pass.

### 10.1 Backend Verification

From `web-flask/`:

```powershell
python -m compileall .
python -m pytest
```

Backend evidence must also demonstrate:

- optional filter behavior;
- backward-compatible unfiltered behavior;
- pagination response-shape preservation;
- invalid `detection_status` returns `400`;
- invalid/inverted date range returns `400`;
- user/admin permission boundary preservation;
- no DB schema/index/API-boundary expansion.

### 10.2 Frontend Verification

From `web-vue/`:

```powershell
npm.cmd run build
```

Frontend evidence must also demonstrate:

- filter bar presence and query/reset behavior;
- paging/page-size/refresh with applied filters retained as specified;
- no local-only filtering;
- existing record display and detail navigation retained;
- Dashboard, report, router, and menu unchanged.

### 10.3 General Verification

Before Step 7 closeout:

```powershell
git diff --check
git status
```

Evidence must confirm:

- the relevant working trees are clean after committed implementation/evidence work;
- only files explicitly authorized by this GO Decision were changed;
- no model, DB, Docker, runtime, storage, video, realtime, AI/LLM, Dashboard summary API, report, auth, push, or tag entry occurred.

## 11. Rollback Baseline and Scope Control

Rollback baseline:

```text
latest stable rollback tag: phase2b-batch4-step6-dashboard-stable
latest stable rollback commit: 708a61a
pre-implementation Step 7 planning merge baseline: 1d81d33
```

Rollback expectations:

- This docs-only GO Decision commit can be reverted independently if authorization is withdrawn before implementation.
- Future Step 7 implementation must remain revertible through narrow backend/frontend implementation reverts and should not require DB rollback because schema changes and migrations are prohibited.
- No stable tag may be created until implementation and evidence have separately passed review and explicit tag instruction is given.
- No push may occur under this decision.

## 12. Authorization State

```text
Phase 2B Batch4 Step 7 Planning: COMPLETED / MERGED
Step 7 authorized implementation: Detection Records Filter/Search Enhancement ONLY
Backend Agent implementation: GO
Frontend Agent implementation: GO
Docs/Test checklist/evidence: GO
AI Agent: NOT REQUIRED
Step 7 stable tag: NOT CREATED
push: NOT DONE
Step 8: NOT AUTHORIZED

NO-GO remains in force for:
- video detection implementation
- realtime detection implementation
- AI Agent / LLM features
- model / weights / classes / training changes
- DB schema / migration / new MVP index
- Docker/runtime/storage changes
- auth/login or permission-boundary semantic changes
- detection_result.v1 semantic changes
- Dashboard summary API / Dashboard frontend changes
- detail / Word report / router / menu changes
- push
- tag
```
