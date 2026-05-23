# Phase 2B Batch4 Step 7 Planning / Gate

Status: PLANNING ONLY
Date: 2026-05-23
Phase: Phase 2B Batch4 Step 7
Working branch: `batch4-step7-planning`
Master HEAD baseline: `0d73cca` (`Archive Batch4 Step6 stable tag`)
Latest stable tag: `phase2b-batch4-step6-dashboard-stable` -> `708a61a`
Step 6 status: CLOSED / STABLE / ARCHIVED
Step 7 Implementation: **NOT AUTHORIZED**
Push: **NOT DONE**
Step 7 stable tag: **NOT CREATED**

## 1. Current Baseline

The controlling baseline for Step 7 planning is:

```text
master HEAD: 0d73cca
master HEAD message: Archive Batch4 Step6 stable tag
latest stable tag: phase2b-batch4-step6-dashboard-stable
latest stable tag target: 708a61a
working tree expected: clean
push: NOT DONE
Step 7 Implementation: NOT AUTHORIZED
```

Step 6 closed the Dashboard MVP continuation of the existing product chain:

```text
login -> image detection -> save record -> records list -> record detail -> Word report -> Dashboard
```

This Step 7 artifact opens a planning gate only. It does not authorize edits to frontend or backend business code, APIs, persistence, inference, runtime, or deployment configuration.

## 2. Step 7 Recommended Direction

Recommended direction:

```text
Detection Records Filter/Search Enhancement
检测记录筛选/搜索增强
```

Recommended objective:

```text
Evaluate a narrow, backward-compatible enhancement for the existing detection-records list so a user can find saved records by filename, model, status, and time range while preserving current pagination, detail navigation, Word report flow, and Dashboard behavior.
```

Planning does not equal implementation authorization. Any implementation requires a separate Step 7 Implementation GO Decision after all required read-only scans and checklist drafting are complete.

## 3. Why This Direction

Detection Records Filter/Search Enhancement is the recommended next step because it is:

- **小范围**: it stays on the existing records list/API boundary rather than opening a new product workflow;
- **风险低**: its default design is additive query/filter handling with no schema, model, storage, runtime, or permission-boundary change;
- **用户价值明显**: once records grow, users need to quickly locate historic detections by familiar fields and date;
- **延续现有闭环**: it strengthens the established `records -> detail -> Word report -> Dashboard` chain without replacing any part of it;
- **比 video/realtime 更适合当前阶段**: video and realtime would introduce upload/stream handling, performance, task-state, cancellation, and resource-control risks that are unnecessary for this incremental step.

The proposed direction is therefore a small, reversible usability improvement on top of the verified Step 6 stable baseline.

## 4. Candidate Scope

### 4.1 Backend Candidate Scope

Backend work is **read-only scan first**. The scan should:

- inspect the current `GET /api/detection/records` route, service/query flow, response shape, pagination semantics, and existing authentication/authorization behavior;
- evaluate additive query/filter support for:
  - keyword or filename search;
  - model filter;
  - status filter;
  - date/time range filter;
- determine whether the existing list response and pagination metadata can remain backward compatible when filters are absent or present;
- identify the smallest possible future backend file/test allowlist if a later GO Decision authorizes implementation;
- preserve existing permission boundaries exactly; no change in which records a user may access;
- default to **no DB schema change** and do not propose migrations unless a later read-only scan produces explicit evidence and a separate approval is granted.

Backend scan target:

```text
GET /api/detection/records
```

### 4.2 Frontend Candidate Scope

Frontend work is **read-only scan first**. The scan should:

- inspect `DetectionRecords.vue`, associated API helpers/types, routing, loading/empty/error behavior, and current paging interaction;
- evaluate a small filter/search UI for:
  - filename/keyword;
  - model;
  - status;
  - date range;
  - search/reset actions;
- retain current pagination semantics, including a clear decision for resetting to page 1 when search conditions change;
- keep detail-page navigation intact;
- keep existing record display fields, empty states, and error behavior intact;
- avoid Dashboard, report, detection-upload, layout-redesign, video, or realtime changes.

Frontend scan target:

```text
web-vue/**/DetectionRecords.vue
```

### 4.3 Docs/Test Candidate Scope

Docs/Test work is limited to preparing a verification checklist draft for later review. It should cover:

- baseline and scope guards;
- candidate filter input behavior and expected list results;
- pagination preservation;
- record-detail navigation preservation;
- Word report regression protection;
- Dashboard regression protection;
- permissions and backward-compatibility checks;
- empty-result and invalid-filter behavior;
- backend/frontend verification commands to run only after implementation is separately authorized;
- rollback expectations and explicit NO-GO confirmations.

## 5. Recommended Read-Only Scan Questions

### 5.1 Backend Agent Questions

Before an Implementation GO Decision, Backend Agent should provide file/line evidence for:

1. Where `GET /api/detection/records` is routed and how pagination parameters are currently parsed.
2. Which service/repository query builds the list, orders records, and computes total/page metadata.
3. Which stored fields already support filename, model, status, and created/detection-time filtering without schema changes.
4. Whether status values are normalized or derived, and what safe filter vocabulary a future implementation could accept.
5. How invalid page, page-size, date-range, or filter values currently map to API error behavior.
6. How admin versus normal-user record visibility is enforced and how that boundary must be reused unchanged.
7. Whether adding optional filters can remain backward compatible for existing callers and Dashboard behavior.
8. What focused backend tests would be required if filters are later authorized.

### 5.2 Frontend Agent Questions

Before an Implementation GO Decision, Frontend Agent should provide file/line evidence for:

1. The current location and structure of `DetectionRecords.vue`.
2. The API helper/type surface used to request paginated records.
3. The current pagination, loading, empty-state, error-state, and detail-navigation patterns.
4. The narrowest placement for a filter/search toolbar without changing existing record display.
5. Whether model and status filter options can come from known existing values without adding a new dependency or new management flow.
6. How date range values should be serialized for a later API contract proposal.
7. What frontend smoke/build checks prove detail navigation, Word report access, and Dashboard navigation remain intact.

### 5.3 Docs/Test Agent Questions

Before an Implementation GO Decision, Docs/Test Agent should define:

1. Acceptance cases for each proposed filter alone and for compatible filter combinations.
2. Pagination expectations when filters narrow results or are reset.
3. Permission-boundary cases for ordinary and admin users under filtered requests.
4. Regression cases for detail navigation, Word report export, and Dashboard.
5. Scope guards proving there are no DB schema, video, realtime, AI/LLM, model, Docker, runtime, or storage changes.
6. A narrow rollback strategy anchored to the Step 6 stable baseline.

## 6. Proposed Agent Tasks

| Agent | Step 7 planning responsibility | Authorization state |
|---|---|---|
| Backend Agent | Perform read-only scan of `GET /api/detection/records`; evaluate optional keyword/model/status/date filters, pagination compatibility, tests, and permission preservation. | READ-ONLY SCAN REQUIRED BEFORE GO |
| Frontend Agent | Perform read-only scan of `DetectionRecords.vue` and related API/type surfaces; evaluate compact filter/search UI while retaining pagination, navigation, and display. | READ-ONLY SCAN REQUIRED BEFORE GO |
| Docs/Test Agent | Prepare Step 7 verification checklist draft and scope/rollback checks. | PLANNING DRAFT REQUIRED BEFORE GO |
| AI Agent | No Step 7 responsibility; no inference, LLM, model, training, classes, weights, or evaluation changes are needed. | **NOT REQUIRED** |

No proposed Agent task in this document authorizes business-code implementation.

## 7. Explicit NO-GO

The following items are expressly prohibited during this planning gate:

- **no Step 7 implementation before a GO Decision**;
- no `web-vue/**` business-code implementation;
- no `web-flask/**` business-code implementation;
- no video detection implementation;
- no realtime detection implementation;
- no AI Agent / LLM feature;
- no model / weights / classes / training changes;
- no inference-output or `detection_result` semantic change;
- no DB schema change unless explicitly approved later after compelling read-only evidence; default decision is **NO-GO**;
- no permission-boundary or JWT-semantic change;
- no Docker/runtime/storage changes;
- no push;
- no tag.

This planning step also must not broaden scope into bulk operations, export redesign, new dashboards, new analytics storage, or record lifecycle changes.

## 8. Gate Requirements Before Implementation

Step 7 implementation may start only after all of the following conditions are met:

1. Backend read-only scan is completed with concrete route/service/query/test and permission-boundary evidence.
2. Frontend read-only scan is completed with concrete view/API/type/pagination/navigation evidence.
3. Docs/Test verification checklist draft is completed.
4. The Leader reviews the scan/checklist inputs and creates a separate **Step 7 Implementation GO Decision**.
5. That GO Decision explicitly defines the authorized backend/frontend/test/document file scope, expected API query contract, compatibility constraints, verification commands, rollback plan, and continuing NO-GO items.

Until all five requirements are satisfied:

```text
Step 7 Implementation: NOT AUTHORIZED
```

## 9. Draft Verification Checklist for a Future Authorized Implementation

The Docs/Test checklist draft should be prepared before any GO Decision and should at minimum propose checks for:

### Backend/API behavior

- unfiltered `GET /api/detection/records` remains backward compatible;
- filename/keyword filter behavior;
- model filter behavior;
- status filter behavior;
- date/time range filter behavior;
- permitted combinations of filters;
- invalid/empty query parameter behavior;
- filtered pagination totals/page transitions;
- existing user/admin permission boundary preservation;
- no DB schema or migration dependency.

### Frontend behavior

- filter bar is additive to the current records page;
- search and reset behavior are understandable;
- pagination remains functional under filtered and reset states;
- existing record table/card fields remain visible;
- detail navigation continues to work;
- empty filtered results display safely;
- loading/error states remain usable.

### Regression protection

- login remains unaffected;
- image detection and record-save flow remain unaffected;
- record detail remains reachable;
- Word report flow remains reachable from the existing detail surface;
- Dashboard remains reachable and does not rely on altered semantics;
- no video/realtime/AI/model/schema/Docker/runtime/storage entry occurs.

### Git/scope evidence

- `git status --short`;
- `git diff --stat`;
- `git diff --name-status`;
- `git diff --check`;
- allowed-file review against the later GO Decision;
- no push and no tag until separately instructed.

## 10. Compatibility, Risk, and Rollback Expectations

### Compatibility expectations

- Optional query/filter parameters, if later authorized, must preserve existing list behavior when omitted.
- Existing pagination, record-detail navigation, Word report flow, and Dashboard behavior must not be broken.
- Permission rules must be reused, not expanded.
- Existing persisted records must remain readable; no migration is expected.

### Main risks to evaluate during scans

- accidental mismatch between frontend filter serialization and backend parsing;
- incorrect filtered total/page metadata;
- ambiguous status or model values;
- date/timezone boundary behavior;
- unintended permission leakage when composing query filters;
- unintended regressions to existing records/detail/report/dashboard flows.

### Rollback baseline

```text
stable rollback tag: phase2b-batch4-step6-dashboard-stable
stable rollback commit: 708a61a
post-tag archive baseline: 0d73cca Archive Batch4 Step6 stable tag
```

Planning-only rollback is a narrow revert of this document commit. A future implementation rollback must be defined in its separate GO Decision and must remain additive/revertible without DB rollback by default.

## 11. Planning-Only Verification Requirements

For this Step 7 Planning / Gate document:

- only `agent_outputs/docs/PHASE2B_BATCH4_STEP7_PLANNING.md` is newly added or modified in the planning commit;
- no `web-vue/**` file is changed;
- no `web-flask/**` file is changed;
- no DB, Docker, runtime, storage, model, weight, class, training, inference, video, realtime, or AI/LLM file is changed;
- `git diff --check` passes before commit;
- no push occurs;
- no tag is created;
- Step 7 implementation remains **NOT AUTHORIZED**.

## 12. Current Gate Decision

```text
Phase 2B Batch4 Step 7 Planning / Gate: OPENED
Recommended Step 7 direction: Detection Records Filter/Search Enhancement / 检测记录筛选/搜索增强
Reason: small, low-risk, high-value continuation of the existing records/detail/report/dashboard chain; preferable to video or realtime expansion at this phase.
Backend Agent: READ-ONLY SCAN REQUIRED BEFORE GO
Frontend Agent: READ-ONLY SCAN REQUIRED BEFORE GO
Docs/Test Agent: VERIFICATION CHECKLIST DRAFT REQUIRED BEFORE GO
AI Agent: NOT REQUIRED
Step 7 Implementation: NOT AUTHORIZED
DB schema change: NO-GO BY DEFAULT
video detection implementation: NO-GO
realtime detection implementation: NO-GO
AI Agent / LLM feature: NO-GO
model / weights / classes / training changes: NO-GO
Docker/runtime/storage changes: NO-GO
push: NOT DONE
tag: NOT CREATED
```
