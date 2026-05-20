# Phase 2B Batch4 Step 1 Implementation Authorization

Status: PREPARED FOR STEP 1 GO REVIEW ONLY
Date: 2026-05-20
Baseline tag: `phase2b-batch3-docker-compose-stable`
Baseline code point: `fddb0c8`
Archive commit: `ff731de`
Step 1 name: Backend single-image detection timing metadata additive implementation
Current Step 1 gate: GO Decision recorded; implementation may begin in an independent backend worktree

## 1. Authorization Intent

This document records the Step 1 authorization boundary that is now paired with the GO Decision document.

It does **not** authorize implementation in this turn.
It does **not** authorize any code, schema, model, Docker, or frontend change.
It exists only to define the narrow authorization boundary for a future backend-only timing metadata change.

## 2. Step 1 Allowed Scope

Step 1 is limited to:

- backend single-image detection only;
- additive timing metadata only;
- optional `detection_result.v1.timing` fields only;
- no frontend synchronization required for initial implementation;
- no AI Agent participation required for initial implementation.

### 2.1 Future timing fields allowed by this authorization

- `total_api_ms`
- `model_load_ms` or `model_ready_ms`
- `preprocess_ms`
- `inference_ms`
- `postprocess_ms`
- `result_image_save_ms`
- `record_save_ms`

## 3. Files Allowed for Future Step 1 Implementation

If and only if a later GO review passes, Step 1 may modify:

- `web-flask/ai/yolo_infer.py`
- `web-flask/services/detection_service.py`
- `web-flask/routes/detection.py`
- `web-flask/tests/test_smoke.py`
- `web-flask/tests/test_stage2_api_hardening.py`
- `web-flask/tests/test_runtime_diagnostics.py`

## 4. Files and Areas Explicitly Forbidden

Step 1 must not modify:

- `web-vue/**`
- `other/model_train/detect/**`
- `web-flask/db/schema.sql`
- `Dockerfile`
- `docker-compose.yml`
- `runtime/**`
- `storage/**`
- `*.pt`
- `*.pth`
- `*.onnx`
- model categories
- model weights
- training logic
- video detection
- realtime detection
- Word report
- Dashboard / large-screen work

## 5. `detection_result.v1` Hard Constraints

Step 1 must preserve the current detection result contract:

- `schema_version` must remain `detection_result.v1`
- no field deletion
- no field renaming
- no change to existing field semantics
- `timing` may only gain optional keys
- old records without `timing` must remain readable
- old frontend consumers must be able to ignore unknown fields
- records save/read round-trip must remain intact

## 6. Smoke Test Hard Constraints

A future Step 1 implementation must keep these smoke conditions true:

- `/api/health` PASS
- login PASS
- `/api/detection/image` success branch PASS
- `unsupported_image_type` / `invalid_image` / bad confidence behavior unchanged
- new timing fields readable when present
- missing timing fields do not error
- records save/read PASS
- `detection_result.v1` structure not broken

## 7. Agent Responsibilities

- Backend Agent: future implementation owner
- Docs/Test Agent: future gate, smoke, and evidence owner
- Frontend Agent: not required for Step 1
- AI Agent: not required for Step 1

## 8. Rollback Strategy

If Step 1 is later authorized and needs rollback:

- revert only backend incremental code
- no DB migration rollback expected
- no Docker rollback expected
- no model / weight / category rollback expected
- no frontend rollback expected

## 9. Authorization Status

This document authorizes **preparation for Step 1 only**.

This document now serves as the implementation authorization boundary for the GO decision. Backend Agent may enter implementation for this one narrow scope only, in an independent backend worktree, while preserving the hard constraints above.

