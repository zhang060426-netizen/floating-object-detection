# TASK_PHASE2B_BATCH4_STEP2_PLANNING — Frontend Agent

Status: PLANNING ONLY
Owner: Frontend Agent
Phase: Phase 2B Batch4 Step 2
Baseline tag: `phase2b-batch4-step1-backend-timing-stable`
Baseline code point: `2f94ddc`
Archive commit: `4bdc1f1`

## 1. Context

Phase 2B Batch4 Step 1 has been closed, verified, tagged, and archived. Step 2 is a separate future phase and remains planning only.

Step 2 focuses on frontend display of backend timing metadata from image detection results while preserving legacy compatibility.

## 2. Allowed Scope

- Plan how to display timing metadata in image detection result views.
- Plan how to show timing metadata in record detail views.
- Plan behavior when timing metadata is present.
- Plan behavior when timing metadata is absent.
- Plan legacy record compatibility.
- Plan minimal frontend-only display updates.

## 3. Forbidden Scope

- Do not modify `web-flask/**`.
- Do not modify backend `detection_result.v1`.
- Do not modify backend schema.
- Do not modify Dockerfile or `docker-compose.yml`.
- Do not modify model weights, classes, or training logic.
- Do not add video, realtime, Word, or Dashboard scope.
- Do not start Step 2 implementation.

## 4. Planning Deliverables

Recommended Frontend planning output:

- `agent_outputs/docs/PHASE2B_BATCH4_STEP2_FRONTEND_TIMING_PLANNING.md`

This deliverable is planning-only and does not authorize implementation.

## 5. Required Questions to Answer

1. Where should timing metadata appear in the existing detection result UI?
2. How should the UI behave when timing is missing?
3. Which timing fields are worth surfacing to users?
4. How should old records without timing remain readable?
5. What minimal frontend file surface would be needed later if implementation is authorized?

## 6. Acceptance Criteria

- Future timing display plan is documented.
- No Vue/frontend source files are modified.
- Timing missing remains a non-error state.
- Legacy record compatibility is preserved.
- Dashboard/video/realtime/Word remain excluded.

## 7. Handoff Notes

Backend owns the additive timing contract from Step 1. Docs/Test owns evidence and closeout. Frontend planning must not become implementation authorization.
