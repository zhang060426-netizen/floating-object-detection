# Phase 2B Batch4 Step 2 Implementation GO Decision

Status: GO
Date: 2026-05-20
Baseline tag: `phase2b-batch4-step1-backend-timing-stable`
Baseline code point: `2f94ddc`
Archive commit: `4bdc1f1`
Step 2 name: Frontend display backend timing metadata

## 1. Decision

```text
Phase 2B Batch4 Step 2 Implementation GO Decision: GO
```

This decision authorizes the Frontend Agent to enter Step 2 implementation in an independent frontend worktree.

## 2. Authorized Step 2 Scope

Step 2 is limited to frontend display of backend timing metadata in image detection result views.

### 2.1 Authorized goals

- Display timing metadata in the immediate image detection result page
- Display timing metadata in the detection record detail page
- Show a performance information block when timing exists
- Render normally when timing is missing
- Keep legacy records without timing compatible
- Preserve existing detection result display behavior

### 2.2 Timing fields authorized for display

- `total_api_ms`
- `inference_ms`
- `model_load_ms`
- `preprocess_ms`
- `postprocess_ms`
- `result_image_save_ms`
- `record_save_ms`

## 3. Authorized Frontend Files

Default allowed files are limited to:

- `web-vue/src/components/DetectionResultPanel.vue`
- `web-vue/src/views/DetectionRecordDetail.vue`
- `web-vue/src/types/detection.ts`
- `web-vue/src/utils/detectionDisplay.ts`

## 4. Conditionally Allowed Files

The following files are **not** part of the default target surface, but may be modified only if implementation proves they are strictly necessary and the change stays within the same frontend-only Step 2 scope:

- `web-vue/src/views/ImageDetect.vue`
- `web-vue/src/api/detection.ts`

Any use of these files must remain frontend-only and must not widen scope beyond Step 2.

## 5. Hard Constraints

Step 2 must preserve these constraints:

- `detection_result.v1` remains preserved
- no field deletion
- no field renaming
- no change to existing field semantics
- timing remains optional metadata only
- old records without timing remain readable
- no regression in existing detection-result presentation

## 6. Forbidden Scope

Step 2 must not modify:

- `web-flask/**`
- `Dockerfile`
- `docker-compose.yml`
- `web-flask/db/schema.sql`
- `runtime/**`
- `storage/**`
- `*.pt`
- `*.pth`
- `*.onnx`
- model weights
- model categories
- training logic
- video detection
- realtime detection
- Word report
- Dashboard / large-screen work
- AI Agent implementation
- Backend Agent implementation
- push
- tag creation

## 7. Required Verification

A future Step 2 implementation must be verified with:

- `cd web-vue && npm run build`
- timing-present rendering path
- timing-missing rendering path
- legacy no-timing record rendering
- immediate result page rendering
- detection record detail page rendering
- existing image/result-image/detection-box/class/confidence/summary display non-regression
- login / routing / API call non-regression
- `git diff --check`
- `git status` / `git diff` proving only authorized files changed

## 8. Worktree Requirement

Frontend Agent must use an independent frontend worktree for Step 2 implementation.

## 9. Rollback Strategy

If Step 2 later needs rollback:

- revert only the frontend incremental code
- no backend rollback expected
- no DB migration rollback expected
- no Docker rollback expected
- no model / weight / category rollback expected
- no frontend data migration rollback expected

## 10. Relationship to Planning

This GO decision supersedes the planning-only Step 2 checklist for the purpose of implementation start.
The checklist itself remains documentation and must not be treated as implementation authorization.

## 11. Change Control Notes

- Frontend Agent is the primary implementation owner.
- Docs/Test Agent will own verification evidence and closeout.
- Backend Agent and AI Agent are not required for this Step 2 implementation lane.
- A separate closeout/review cycle is still required after implementation.
