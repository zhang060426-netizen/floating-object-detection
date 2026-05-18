# Task: Phase 2B Batch2 Frontend Planning

Status: PLANNING ARTIFACT ONLY
Owner: Frontend Agent
Phase: Phase 2B Batch2
Date: 2026-05-17

## 1. Boundary

Batch2 planning is allowed. Batch2 implementation is not started by this file.

Allowed scope:
- Preserve Batch1 login and image detection page behavior.
- Keep compatibility with `detection_result.v1` and existing backend response envelope.
- Plan UI resilience for loading, empty detections, one-or-more detections, and backend error display.
- Plan regression checks for build and core page display.

Forbidden scope:
- Do not implement from this planning artifact.
- Do not modify backend, AI inference, weights, database, video, realtime, Word report, dashboard, or large-screen features.
- Do not require `detection_result.v2` or new API fields.
- Do not redesign the full UI system in Batch2.

## 2. Frozen Inputs

Batch1 smoke reached FULL PASS CANDIDATE. Frontend build passed and display compatibility was completed for current Batch1 output.

Current critical runtime facts to preserve:
- `/api/detection/image` success returns HTTP 200 and `code=0`.
- `detection_result.schema_version=detection_result.v1`.
- Runtime can produce a result image and auto-saved records.
- Low threshold smoke produced one persisted detection.

## 3. Frontend Batch2 Planning Objectives

1. Preserve login flow and token handling.
2. Preserve image detection upload/display flow.
3. Plan display handling for:
   - no detections;
   - one detection;
   - multiple detections;
   - backend error responses;
   - missing or delayed result image URL.
4. Plan record list/detail compatibility with auto-generated detection records.
5. Keep build gate as a mandatory smoke step.

## 4. Acceptance Targets

| Target | Required result | Evidence |
|---|---|---|
| Build | Frontend build passes | build log / exit code |
| Login | Existing login still works | screenshot or network summary |
| Image page | Page loads and can submit image | screenshot or browser log |
| Detection display | `detection_result.v1` renders without crash | screenshot / DOM note |
| Result image | Generated image displays or fallback is clear | screenshot |
| Records | Auto-saved record can be shown if linked in UI | screenshot / network summary |

## 5. Handoff Notes

- Frontend Agent must not start implementation until Leader explicitly authorizes Batch2 implementation.
- If frontend needs new backend fields, stop and request API contract review first.
- Frontend must remain backward compatible with Batch1 records already saved under `detection_result.v1`.
