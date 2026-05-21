# Phase 2B Batch4 Step 3 Verification Checklist

Status: PREPARED / CHECKLIST ONLY
Date: 2026-05-21
Owner: Docs/Test Agent
Branch: `batch4-step3-docs-test`
Base: `master 0015ce1`
Phase: Phase 2B Batch4 Step 3
Step 3 theme: Detection Records Management Enhancement
Step 3 Frontend implementation: IN PROGRESS IN ANOTHER WORKTREE
Step 3 stable tag: NOT CREATED
Push: NOT DONE
Task scope: Documentation/test checklist preparation only; no business-code implementation.

## 0. Purpose

This document prepares the verification checklist that Docs/Test Agent should use after the separate Frontend Agent finishes the authorized Step 3 implementation.

This checklist does not implement Step 3. It does not authorize additional scope. It exists to make later verification repeatable and to keep the boundary between documentation/test preparation and business-code implementation explicit.

## 1. Scope Guard Checklist

Before accepting Step 3 implementation evidence, verify all of the following:

- [ ] Implementation changes are limited to the separately authorized frontend Step 3 files.
- [ ] No `web-flask/**` file changed unless a later, separate backend authorization exists.
- [ ] No Dockerfile, compose, or container runtime file changed.
- [ ] No database schema, migration, SQL initialization, or DB contract file changed as an implementation side effect.
- [ ] No `runtime/**` or `storage/**` file changed.
- [ ] No model weights, model classes/categories, training scripts, inference model assets, `.pt`, `.pth`, or `.onnx` files changed.
- [ ] No Dashboard / large-screen feature entered.
- [ ] No Word report feature entered.
- [ ] No video detection feature entered.
- [ ] No realtime detection feature entered.
- [ ] No delete, bulk delete, or edit-record behavior added.
- [ ] `detection_result.v1` semantic meaning remains unchanged.
- [ ] Existing record-detail navigation remains available.
- [ ] Existing image detection main flow, upload flow, and login/auth behavior are not semantically changed.
- [ ] Step 3 stable tag is still not created during checklist preparation.
- [ ] No push is performed during checklist preparation.

Recommended command evidence after implementation is available:

```powershell
git status --short --branch
git diff --name-status master...HEAD
git diff --stat master...HEAD
git diff --check
```

## 2. Frontend Build Checklist

Run from `web-vue/` in the implementation worktree after Step 3 frontend changes are present:

```powershell
npm run build
```

Pass criteria:

- [ ] Build exits with code `0`.
- [ ] TypeScript / Vue build reports no blocking errors.
- [ ] No new dependency installation is required unless separately authorized and documented.
- [ ] Build output does not require backend, Docker, DB, runtime/storage, or model changes.
- [ ] Any warnings are recorded with risk assessment; warnings must not indicate broken records-list behavior.

Evidence to record later:

```text
command: cd web-vue && npm run build
result: PASS / FAIL
log location or pasted summary:
```

## 3. Records List Smoke Test

Verify the detection records list page after the frontend implementation is available.

Smoke steps:

1. Start the frontend/backend using the normal local smoke-test method for this project.
2. Log in only if required by the existing app flow.
3. Navigate to the detection records list page.
4. Confirm the records table/list renders without console-breaking errors.
5. Confirm existing columns/fields remain readable:
   - detection time;
   - original filename or safe fallback;
   - model name or safe fallback;
   - target count or safe fallback;
   - status or safe fallback;
   - detail action/jump affordance.

Pass criteria:

- [ ] Records page loads.
- [ ] Records table/list renders.
- [ ] Existing field display remains compatible.
- [ ] No crash when records are returned.
- [ ] No unauthorized features appear, especially delete / bulk delete / edit records.

## 4. Pagination Smoke Test

Verify the Step 3 pagination behavior using existing backend pagination metadata when present.

Smoke steps:

1. Open the detection records list.
2. Confirm current page, page size, and total state are visible when backend metadata exists.
3. Change page.
4. Change page size if a page-size selector is present.
5. Confirm the list reloads and remains readable.
6. Confirm fallback behavior remains safe if the API returns an array rather than a paged object.

Pass criteria:

- [ ] Default page is safe, expected to be page `1` unless implementation evidence documents otherwise.
- [ ] Default page size is conservative, expected to be `20` unless implementation evidence documents otherwise.
- [ ] Page-size options are conservative, for example `10 / 20 / 50 / 100`.
- [ ] Backend metadata variants remain compatible: `items`, `records`, or `list`.
- [ ] `total`, `page`, and `page_size` are consumed when present.
- [ ] Array response fallback derives safe total/list state without crashing.

## 5. Refresh Button Smoke Test

Verify refresh remains additive and does not reset unrelated state unexpectedly.

Smoke steps:

1. Open the detection records list.
2. Move to a non-default page if enough records exist.
3. Click the refresh button.
4. Confirm the list reloads successfully.
5. Confirm current page/page size are preserved when feasible.

Pass criteria:

- [ ] Refresh button remains visible and usable.
- [ ] Refresh triggers records reload.
- [ ] Refresh does not crash on empty, paged, or array responses.
- [ ] Refresh does not introduce delete/edit/bulk actions.
- [ ] Refresh does not modify backend data.

## 6. Record Detail Jump Smoke Test

Verify list-to-detail navigation remains intact.

Smoke steps:

1. Open a populated detection records list.
2. Click the existing detail action for one record.
3. Confirm navigation reaches the expected record detail route/page.
4. Confirm the selected record detail renders.
5. Return to the records list and confirm list remains usable.

Pass criteria:

- [ ] Detail jump/action is still present.
- [ ] Route target remains compatible with existing record-detail behavior.
- [ ] Detail page renders the selected record.
- [ ] Pagination/list changes do not break detail navigation.
- [ ] No record edit/delete behavior is introduced on the list or detail path.

## 7. Empty List Compatibility

Verify records-list behavior when the backend returns no records.

Acceptable response shapes to test or simulate when feasible:

```json
[]
```

```json
{ "items": [], "total": 0, "page": 1, "page_size": 20 }
```

```json
{ "records": [], "total": 0, "page": 1, "page_size": 20 }
```

```json
{ "list": [], "total": 0, "page": 1, "page_size": 20 }
```

Pass criteria:

- [ ] Empty records state renders without crash.
- [ ] Pagination state is safe when total is `0`.
- [ ] Refresh remains usable on an empty list.
- [ ] Detail action is not shown for nonexistent rows.
- [ ] No backend, DB, or storage mutation is needed to support empty state.

## 8. Legacy Record Compatibility

Verify older records with partial fields remain safe.

Legacy record conditions to cover by fixture, mock, existing local data, or code-path review:

- missing or null original filename;
- missing or null model name;
- missing or null target count field;
- missing or unknown status;
- older field names already supported by existing frontend compatibility helpers.

Pass criteria:

- [ ] Legacy records render safe placeholders/fallbacks.
- [ ] Target count fallback remains compatible.
- [ ] Status fallback remains compatible.
- [ ] Record time fallback remains compatible.
- [ ] No `detection_result.v1` semantic changes are made to force compatibility.

## 9. Missing `detection_result` Compatibility

Verify records without `detection_result` do not crash the list or detail entry path.

Smoke conditions:

- `detection_result` absent;
- `detection_result: null`;
- `detection_result` present but missing expected nested sections.

Pass criteria:

- [ ] Records list renders without runtime crash.
- [ ] Count/status/timing display uses safe fallbacks.
- [ ] Detail jump remains controlled by record identity, not by requiring `detection_result`.
- [ ] No backend data rewrite is required.
- [ ] `detection_result.v1` semantics remain preserved.

## 10. Missing Timing Compatibility

Verify Step 2 timing-display compatibility is preserved while Step 3 list management is added.

Timing cases to cover by fixture, mock, existing local data, or code-path review:

- `detection_result.timing` present;
- `detection_result.timing` missing;
- `detection_result.timing: null`;
- legacy `detection_result.timing_ms` present;
- no timing fields at all.

Pass criteria:

- [ ] Missing timing does not crash records list.
- [ ] Missing timing does not crash record detail.
- [ ] Legacy `detection_result.timing_ms` fallback remains preserved where timing helpers are used.
- [ ] Optional timing remains display-only.
- [ ] No backend schema or detection-result semantic change is required.

## 11. Forbidden Path Checklist

The following paths/features are explicitly forbidden for this Step 3 checklist-preparation task and remain forbidden for Step 3 implementation unless later separately authorized:

| Area | Rule |
|---|---|
| Backend | No `web-flask/**` changes unless a later standalone backend authorization is issued. |
| Docker | No Dockerfile, compose, image, container, or deployment changes. |
| DB schema | No migrations, schema edits, SQL initialization edits, or DB contract semantic changes. |
| Runtime/storage | No `runtime/**`, `storage/**`, upload storage, generated-result storage, or file-layout changes. |
| Model/AI | No model weights, model classes/categories, model training, inference chain, `.pt`, `.pth`, or `.onnx` changes. |
| Dashboard | No Dashboard / large-screen changes. |
| Word | No Word report/export changes. |
| Video | No video detection changes. |
| Realtime | No realtime detection changes. |
| Records mutation | No delete records, bulk delete, or edit-record features. |
| Detection result contract | No `detection_result.v1` semantic changes. |
| Release operations | No commit, push, or tag from this checklist-preparation task. |

Forbidden-path command checks to record later:

```powershell
git diff --name-status master...HEAD
```

Expected result for this docs/test checklist-preparation task:

```text
A\tagent_outputs/docs/PHASE2B_BATCH4_STEP3_VERIFICATION_CHECKLIST.md
```

## 12. Docs/Test Checklist Preparation Completion Assertion

For this current task only:

```text
Checklist file prepared: YES
Business code changed: NO
Backend changed: NO
Docker changed: NO
DB schema changed: NO
Runtime/storage changed: NO
Model/weights/classes/training changed: NO
Dashboard / Word / video / realtime entered: NO
Delete / bulk delete / edit records implemented: NO
detection_result.v1 semantic changes: NO
Step 3 stable tag created: NO
Push performed: NO
Commit performed: NO
```
