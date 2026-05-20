# TASK_PHASE2B_BATCH4_PLANNING — Backend Agent

Status: PLANNING ONLY
Owner: Backend Agent
Phase: Phase 2B Batch4
Baseline tag: `phase2b-batch3-docker-compose-stable`
Baseline code point: `fddb0c8`
Archive commit: `ff731de`

## 1. Context

Phase 2B Batch3 proved the Docker Compose runtime and image detection API chain. Batch4 is planning only and must not modify backend implementation.

Backend planning focuses on future image-inference performance measurement, observability, and additive `detection_result.v1` compatibility strategy.

## 2. Allowed Scope

- Plan future image API performance measurement.
- Plan future timing fields such as upload/save/model-load/inference/draw/record-save/total latency.
- Plan how to preserve `detection_result.v1` while adding optional metadata in the future.
- Plan future diagnostics around model readiness and runtime weight identity.
- Plan rollback and verification criteria for any later implementation.

## 3. Forbidden Scope

- Do not change Flask routes, services, DB schema, or repositories.
- Do not change API response envelope.
- Do not change `detection_result.v1` fields or semantics.
- Do not modify Dockerfile or docker-compose.yml.
- Do not change model loading behavior.
- Do not modify model weights, classes, or training logic.
- Do not implement performance endpoints.
- Do not enter video, realtime, Word, dashboard, or large-screen scope.
- Do not start Batch4 implementation.

## 4. Planning Deliverables

Recommended Backend planning outputs:

- `agent_outputs/backend/PHASE2B_BATCH4_INFERENCE_PERFORMANCE_PLAN.md`
- `agent_outputs/backend/PHASE2B_BATCH4_DETECTION_RESULT_EXTENSION_PLAN.md`

These deliverables should remain planning artifacts only.

## 5. Required Questions to Answer

1. Which performance measurements are needed for current image detection API?
2. Which future metrics can be collected without breaking current consumers?
3. What optional metadata could be appended to `detection_result.v1` safely?
4. What should remain outside `detection_result.v1` and belong in logs or diagnostics?
5. What future implementation gate would be required before backend code changes?
6. How should Docker-path-specific environment issues be documented in future smoke plans?

## 6. Acceptance Criteria

- Future performance metric list is defined.
- Additive-only schema extension rules are defined.
- No API, DB, Flask, Docker, or detection service code is modified.
- No model/category/weight/training changes are proposed as implementation.
- Video/realtime/Word/dashboard remain excluded.

## 7. Handoff Notes

AI provides model-quality constraints. Frontend consumes future display requirements. Docs/Test aggregates the final planning gate and verifies implementation remains blocked.
