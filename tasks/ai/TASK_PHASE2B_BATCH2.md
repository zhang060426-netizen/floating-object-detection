# Task: Phase 2B Batch2 AI Planning

Status: PLANNING ARTIFACT ONLY
Owner: AI Agent
Phase: Phase 2B Batch2
Date: 2026-05-17

## 1. Boundary

Batch2 planning is allowed. Batch2 implementation is not started by this file.

Allowed scope:
- Preserve the Batch1 YOLO image inference success path.
- Plan runtime readiness checks and reproducibility notes.
- Keep model output compatible with `detection_result.v1`.
- Plan low-threshold and default-threshold smoke coverage.

Forbidden scope:
- Do not train, replace, move, delete, or rename weights from this planning artifact.
- Do not change model class definitions.
- Do not change the detection result JSON shape in a breaking way.
- Do not expand to video, realtime, Word report, dashboard, or large-screen features.

## 2. Frozen Inputs

Latest smoke facts:
- `ultralytics=8.4.51` is available.
- `yolo26n.pt` exists and is readable.
- `yolo26n.pt` size: `5,544,453 bytes`.
- `yolo26n.pt` SHA256: `9b09cc8bf347f0fc8a5f7657480587f25db09b34bf33b0652110fb03a8ad4fef`.
- `/api/detection/image` returns HTTP 200 and `code=0`.
- Low threshold `0.10` record `dr_227020535354488a99b3703c07b62449` has detection count `1`.
- `detection_result.schema_version=detection_result.v1`.
- Result image generated: `131182 bytes`.
- pytest: `4 passed, 25 warnings`.

## 3. AI Batch2 Planning Objectives

1. Preserve dependency and weight readiness evidence.
2. Plan regression smoke for default threshold and low threshold.
3. Confirm output classes remain compatible with `0/floating_object` expectation.
4. Keep bbox and confidence fields stable for frontend/backend consumers.
5. Record warning triage if pytest warnings indicate future runtime risk.

## 4. Acceptance Targets

| Target | Required result | Evidence |
|---|---|---|
| Runtime dependency | `ultralytics` import/version works | command output |
| Weight identity | size and SHA256 match frozen value or approved update is documented | hash output |
| Inference | image detection success path works | backend/API smoke output |
| Non-empty detection | low-threshold smoke can produce count >= 1 | record/detail evidence |
| Schema | `detection_result.v1` preserved | JSON snippet |
| Result image | generated image exists and is readable | file metadata |
| Tests | pytest passes | pytest output |

## 5. Handoff Notes

- AI Agent must not start implementation until Leader explicitly authorizes Batch2 implementation.
- Any weight or class-definition change requires Leader approval plus frontend/backend contract notice.
- Any schema extension must be additive and backward compatible with `detection_result.v1` consumers.
