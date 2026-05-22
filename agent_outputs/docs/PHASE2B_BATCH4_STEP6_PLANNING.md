# Phase 2B Batch4 Step 6 Planning / Gate

Status: PLANNING ONLY
Date: 2026-05-22
Phase: Phase 2B Batch4 Step 6
Current branch: `master`
Current master HEAD: `b21caa8` (`Archive Batch4 Step5 stable tag`)
Current stable baseline: `phase2b-batch4-step5-word-report-stable`
Current stable baseline target: `645f2dccb7f32963123c8d16fac9f6a8044f906d`
Step 5 status: CLOSED / VERIFIED / TAGGED / ARCHIVED
Step 6 Implementation: NOT AUTHORIZED
Step 6 stable tag: NOT CREATED
Push: NOT DONE

## 1. Current Stable Baseline

The current restore baseline for any future Step 6 work is:

```text
master HEAD at planning time: b21caa8 Archive Batch4 Step5 stable tag
latest stable tag: phase2b-batch4-step5-word-report-stable
latest stable tag target: 645f2dccb7f32963123c8d16fac9f6a8044f906d
Step 5 scope: Word Report Export MVP
Step 5 status: CLOSED / VERIFIED / TAGGED / ARCHIVED
push: NOT DONE
Step 6 Implementation: NOT AUTHORIZED
Step 6 stable tag: NOT CREATED
```

Step 5 closed the single-record Word report export chain:

```text
login -> image detection -> save record -> records list -> record detail -> Word report export
```

Step 6 planning should continue from existing persisted detection-record data and should avoid opening video, realtime, model-training, storage-layout, or schema-changing work by default.

## 2. Step 5 Stable Tag Information

```text
Step 5 stable tag: phase2b-batch4-step5-word-report-stable
tag target: 645f2dccb7f32963123c8d16fac9f6a8044f906d
master HEAD before Step 6 planning: b21caa8
Step 5 status: CLOSED / VERIFIED / TAGGED / ARCHIVED
push: NOT DONE
```

Step 5 implementation summary retained as baseline context:

- Backend Word report API: `GET /api/detection/records/<record_id>/report.docx`.
- JWT auth.
- Permission reuse via `get_record`.
- `resolve_object_path` path safety.
- `python-docx>=1.1`.
- `BytesIO` no persistent report file.
- Frontend `DetectionRecordDetail.vue` export Word report button.
- `requestBlob()`.
- `exportDetectionRecordWordReport(id)`.
- `saveBlob()`.
- `Content-Disposition` filename parsing.

## 3. Step 6 Candidate Direction Comparison

| Candidate | Description | Fit with current baseline | Risk | Verification cost | Rollback safety | Default DB/schema need | Recommendation |
|---|---|---:|---:|---:|---:|---:|---|
| Dashboard 可视化增强 | Use existing detection records and `detection_result` data to show cards, trends, recent records, target counts, confidence metrics, and distribution summaries. | High | Low | Medium | High | Probably no | **Recommended first** |
| 视频检测 MVP | Upload a video, sample frames, run image detection/inference over frames, and expose processing/result state. | Medium | Medium-High | High | Medium-Low | Maybe | Defer until task-state and performance design are planned |
| 实时摄像头检测 MVP | Browser camera / stream flow with inference frequency control and live UI feedback. | Low-Medium | Highest | Highest | Low | Maybe | Defer; too much runtime/performance risk for Step 6 |
| 数据/模型管理增强 | Improve model list/switching, dataset management, and metadata lifecycle. | Medium | Medium | Medium | Medium | Maybe | Defer or split into separate model-management planning gate |

### Candidate assessment

1. **Dashboard 可视化增强** is the lowest-risk continuation because it can be derived from existing record list/detail data and `detection_result` fields. It provides visible system-completion value without opening inference, storage, or model-training changes.
2. **视频检测 MVP** is valuable but likely introduces large files, frame extraction, processing duration, job/task state, progress display, and error recovery. It should not be Step 6 unless a later planning gate explicitly accepts these risks.
3. **实时摄像头检测 MVP** has the highest uncertainty: browser permissions, live stream handling, inference cadence, CPU/GPU utilization, cancellation, throttling, and UX latency.
4. **数据/模型管理增强** is useful, but it touches model lifecycle and dataset boundaries. It should be scoped separately after read-only scans clarify current model/data surfaces.

## 4. Recommended Direction

Recommended Step 6 direction:

```text
Phase 2B Batch4 Step 6 - Dashboard 可视化增强 MVP
```

Recommended objective:

```text
Add a small, reversible dashboard/home overview based on existing detection records and persisted detection_result data, showing useful aggregate statistics and recent activity without changing inference, model, storage, or database semantics by default.
```

This document is only the Planning / Gate artifact. It does not authorize implementation.

## 5. Dashboard MVP Scope

The recommended MVP should be constrained to data that can be read from current APIs or from a narrow read-only backend aggregation if later authorized.

Suggested dashboard content:

- 首页/仪表盘统计卡片.
- 总检测记录数.
- 最近检测时间.
- 检测目标总数.
- Average confidence.
- 最近检测记录列表.
- 简单趋势或分布展示, such as daily record counts or class/status distribution, if feasible from current data.
- Empty-data state compatibility.
- Old-record compatibility, including missing `detection_result`, missing `summary`, empty detections, missing timing, and legacy records.

Recommended non-goals for the MVP:

- no live refresh requirement unless trivially safe;
- no multi-user admin analytics beyond existing permission behavior unless explicitly authorized;
- no new persistent analytics table by default;
- no expensive large-history processing in the request path without a scan-backed performance decision;
- no video/realtime/model-management implementation mixed into the dashboard step.

## 6. Explicitly Allowed Planning Scope

Allowed in this planning-only step:

- Create this planning document.
- Compare Step 6 candidate directions.
- Recommend Dashboard 可视化增强 MVP.
- Define future read-only scan questions for backend, frontend, and docs/test lanes.
- Define future validation and rollback expectations.
- Record that implementation, push, and tag creation are not authorized.

Allowed only in a later separately authorized Step 6 implementation:

- Frontend dashboard/home page UI changes within authorized files.
- Read-only API consumption of existing detection records.
- A narrow backend read-only aggregate endpoint only if scans prove the existing records API is insufficient and the GO Decision authorizes it.
- Lightweight chart/table/card UI based on existing dependencies.
- Tests/builds/docs for the authorized dashboard scope.

## 7. Explicitly Forbidden Scope

Strictly forbidden in this planning step:

- Step 6 implementation.
- Business code changes.
- Video detection implementation.
- Realtime detection implementation.
- Model / weights / class / training changes.
- DB schema changes.
- Dockerfile / `docker-compose.yml` changes.
- Runtime/storage structure changes.
- Push.
- Tag creation.

Forbidden by default for later Step 6 unless a separate GO Decision explicitly authorizes otherwise:

- new DB tables or migrations;
- background job/task framework;
- video upload/frame extraction/inference;
- browser camera/realtime inference;
- model upload/replacement/training;
- storage bucket/layout changes;
- auth/login semantic changes;
- changes to `detection_result.v1` semantics;
- changes to image detection main-flow semantics.

## 8. Backend Read-Only Scan Questions

A backend read-only scan should answer before any implementation GO Decision:

1. Which current endpoint(s) can provide detection record lists for dashboard cards and recent activity?
2. Does `list_records(get_db(), g.current_user, page, page_size)` already expose enough data for total records, recent detection time, target count, average confidence, status distribution, and recent records?
3. Are admin and normal-user permissions already suitable for dashboard aggregates, or would a new read-only endpoint need to reuse existing permission boundaries?
4. What is the shape and variability of `detection_result` in saved records, including missing `summary`, missing `detections`, empty detections, missing confidence fields, legacy `timing_ms`, and NULL/invalid JSON?
5. Can aggregate metrics be computed safely from paginated list data, or would a backend aggregate endpoint be needed to avoid incomplete totals?
6. If a backend endpoint is needed later, what minimal route/service file set would be authorized, and how can it avoid DB schema changes?
7. What tests already cover detection record listing and permission behavior that dashboard aggregation must not break?
8. What performance risks exist for aggregate scans over `detection_records`, and is the current expected dataset small enough for MVP aggregation?

## 9. Frontend Read-Only Scan Questions

A frontend read-only scan should answer before any implementation GO Decision:

1. What route currently acts as home/dashboard, and where should the Dashboard MVP live?
2. Which existing API helpers and types can be reused for detection records and `detection_result` display?
3. Does the project already include ECharts or any charting dependency, or should Step 6 avoid new chart dependencies and use cards/tables/simple CSS first?
4. Which UI patterns from record list/detail pages should be reused for loading, empty, error, and permission states?
5. How should old records with missing `detection_result`, missing `summary`, or empty detections affect totals and averages?
6. What frontend files would be the narrowest authorized implementation surface?
7. What build/typecheck risks exist around computed aggregate types and chart/table rendering?
8. How can the dashboard avoid breaking existing login, image detection, records list, record detail, and Word export flows?

## 10. Docs/Test Checklist Draft Task

A docs/test lane should create a Step 6 checklist draft before implementation authorization. It should include:

- expected dashboard metrics and formulas;
- permission expectations for admin and normal users;
- empty-data and old-record compatibility cases;
- missing `detection_result` behavior;
- missing/empty detections behavior;
- confidence average rules, including whether to ignore missing confidence values;
- recent detection list expectations;
- optional trend/distribution acceptance criteria;
- frontend build verification;
- backend compile/test verification if backend changes are later authorized;
- `git diff --check` and docs-only / code-scope guard checks;
- rollback baseline and rollback commands/strategy;
- explicit non-entry checks for video, realtime, DB schema, Docker/runtime/storage, model/weights/class/training, push, and tag creation.

Suggested future artifact:

```text
agent_outputs/docs/PHASE2B_BATCH4_STEP6_DASHBOARD_VERIFICATION_CHECKLIST_DRAFT.md
```

## 11. Verification Requirements

For this planning-only task:

- `git status --short` shows only the Step 6 planning document before commit.
- `git diff --stat` shows docs-only changes.
- `git diff --name-status` shows only `agent_outputs/docs/PHASE2B_BATCH4_STEP6_PLANNING.md`.
- `git diff --check` passes.
- No business code is changed.
- No tag is created.
- No push is performed.

For a later Step 6 implementation, if separately authorized:

- frontend build must pass, e.g. `cd web-vue && npm.cmd run build`;
- backend compile/tests must pass if backend code changes are authorized, e.g. `cd web-flask && python -m compileall .` and `cd web-flask && python -m pytest`;
- dashboard smoke checks must verify cards, recent records, empty-data state, old-record compatibility, and permission boundaries;
- `git diff --check` must pass;
- changed files must match the future GO Decision allowlist;
- video/realtime/model/training/DB/Docker/runtime/storage non-entry must be confirmed.

## 12. Rollback Baseline

Rollback baseline for future Step 6 work:

```text
stable rollback tag: phase2b-batch4-step5-word-report-stable
stable rollback commit: 645f2dccb7f32963123c8d16fac9f6a8044f906d
post-tag archive commit before Step 6 planning: b21caa8
```

Rollback expectation:

- This planning commit can be reverted independently if the Step 6 direction changes.
- Future Step 6 implementation must remain revertible without DB migrations by default.
- If later implementation introduces frontend-only dashboard files, rollback should be a narrow revert of the Step 6 implementation merge.
- If a backend aggregate endpoint is later authorized, rollback must include backend route/service/test files but still avoid schema rollback unless a later gate explicitly changes this rule.

## 13. Implementation State

```text
Step 6 Implementation: NOT AUTHORIZED
```

No implementation work is authorized by this document. A separate Step 6 GO Decision is required before editing frontend/backend business code.

## 14. Stable Tag State

```text
Step 6 stable tag: NOT CREATED
```

This planning task must not create a Step 6 stable tag.

## 15. Push State

```text
push: NOT DONE
```

This planning task must not push commits or tags.

## 16. Planning Decision

```text
Phase 2B Batch4 Step 6 Planning / Gate: OPENED
Recommended Step 6 direction: Dashboard 可视化增强 MVP
Reason: lowest-risk visible continuation using existing detection records and detection_result data; no model, video, realtime, DB schema, Docker, runtime/storage, or training changes required by default; clear acceptance criteria; simple rollback.
Step 6 Implementation: NOT AUTHORIZED
Step 6 stable tag: NOT CREATED
push: NOT DONE
```
