# TASK_PHASE2B_BATCH4_PLANNING — Frontend Agent

Status: PLANNING ONLY
Owner: Frontend Agent
Phase: Phase 2B Batch4
Baseline tag: `phase2b-batch3-docker-compose-stable`
Baseline code point: `fddb0c8`
Archive commit: `ff731de`

## 1. Context

Batch3 confirmed the Docker Compose frontend can serve the app and same-origin API routing works. Batch4 is planning only and must not modify frontend implementation.

Frontend planning focuses on how future model-quality and inference-performance information should be displayed without changing current UI code.

## 2. Allowed Scope

- Plan future UI copy and placement for current YOLO26n dev-baseline notice.
- Plan how to display `no_detection`, detection count, result image, record state, and performance metadata.
- Plan model-quality warnings without changing API or Vue code.
- Plan how future additive metadata could be consumed safely.
- Preserve compatibility with existing `detection_result.v1` consumers.

## 3. Forbidden Scope

- Do not edit Vue components, routes, stores, API clients, styles, or build config.
- Do not add dashboard / large-screen features.
- Do not add video, realtime, or Word report UI.
- Do not request breaking API/schema changes.
- Do not modify Dockerfile or docker-compose.yml.
- Do not modify model weights, classes, or training logic.
- Do not start Batch4 implementation.

## 4. Planning Deliverables

Recommended Frontend planning output:

- `agent_outputs/frontend/PHASE2B_BATCH4_MODEL_EVAL_UI_PLAN.md`

This deliverable should remain a planning artifact only.

## 5. Required Questions to Answer

1. Where should the UI eventually disclose that YOLO26n is a dev baseline?
2. How should no-detection results be displayed without implying failure?
3. Which performance metrics are useful to users vs. developer diagnostics?
4. How can the frontend remain compatible if optional metadata is absent?
5. What UI changes must be deferred until implementation is explicitly authorized?

## 6. Acceptance Criteria

- Future UI display needs are documented.
- No Vue/frontend source files are modified.
- No new feature scope is introduced.
- Dashboard/video/realtime/Word remain excluded.
- `detection_result.v1` compatibility is preserved.

## 7. Handoff Notes

Backend defines future metadata shape. AI defines model-quality warnings. Docs/Test validates that frontend planning does not become UI implementation.
