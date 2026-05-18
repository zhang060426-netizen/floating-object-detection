# Task: Phase 2B Batch2 Backend Planning

Status: PLANNING ARTIFACT ONLY
Owner: Backend Agent
Phase: Phase 2B Batch2
Date: 2026-05-17

## 1. Boundary

Batch2 planning is allowed. Batch2 implementation is not started by this file.

Allowed scope:
- Harden the existing Batch1 backend path after FULL PASS CANDIDATE.
- Preserve login, model listing, image detection, file access, and detection record APIs.
- Add backend-side observability and defensive checks only when implementation is later authorized.
- Keep `detection_result.v1` backward compatible.

Forbidden scope:
- Do not implement from this planning artifact.
- Do not modify frontend UI, AI weights, model classes, video, realtime, Word report, dashboard, or large-screen features.
- Do not change the API response envelope without contract coordination.
- Do not break existing Batch1 record IDs, file object keys, JWT fields, or `detection_result.v1` consumers.

## 2. Frozen Inputs

Batch1 smoke reached FULL PASS CANDIDATE based on:
- `ultralytics=8.4.51` runtime available.
- `yolo26n.pt` exists and is readable.
- `/api/models/published` returns `weight_exists=true`.
- `/api/detection/image` returns HTTP 200 and `code=0`.
- Result image generation works.
- Records auto-save works.
- `detection_result.schema_version=detection_result.v1`.
- Backend/AI pytest: `4 passed, 25 warnings`.
- Frontend build/display compatibility complete.

## 3. Backend Batch2 Planning Objectives

1. Stabilize backend runtime startup checks for model/dependency readiness.
2. Improve error classification for image detection failures without changing successful response shape.
3. Confirm detection record persistence remains idempotent enough for user retries.
4. Keep file access security checks intact for original/result images.
5. Keep `/api/models/published` compatible while retaining `weight_exists` visibility.
6. Add or document regression tests for Batch1 success path when implementation is authorized.

## 4. Acceptance Targets

| Target | Required result | Evidence |
|---|---|---|
| Health/auth/model | Existing Batch1 behavior unchanged | HTTP smoke output |
| Image detection | Existing success response still HTTP 200 `code=0` | Sanitized response JSON |
| Record auto-save | Successful detection creates readable record | `record_id` list/detail evidence |
| File URLs | Original/result images are retrievable with auth | HTTP status and content metadata |
| Schema compatibility | `detection_result.v1` preserved | JSON snippet |
| Tests | Backend tests pass | pytest output |

## 5. Handoff Notes

- Backend Agent must not start implementation until Leader explicitly authorizes Batch2 implementation.
- Any API response, DB field, JWT, file path, or detection result change requires cross-agent contract notice.
- Any discovery of schema drift must be reported to Docs/Test before code changes.
