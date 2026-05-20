# Phase 2B Batch4 Step 1 GO Decision

Status: GO
Date: 2026-05-20
Baseline tag: `phase2b-batch3-docker-compose-stable`
Baseline code point: `fddb0c8`
Archive commit: `ff731de`
Step 1 name: Backend single-image detection timing metadata additive implementation
Decision scope: Backend single-image detection timing metadata additive implementation only

## 1. Decision

```text
Phase 2B Batch4 Step 1 GO Decision: GO
```

This decision authorizes Backend Agent to enter Step 1 implementation in an independent backend worktree.

## 2. Authorized Step 1 Scope

Allowed scope is limited to:

- backend single-image detection only;
- additive timing metadata only;
- optional `detection_result.v1.timing` fields only;
- no frontend implementation required;
- no AI Agent implementation required.

### 2.1 Authorized future timing fields

- `total_api_ms`
- `model_load_ms` or `model_ready_ms`
- `preprocess_ms`
- `inference_ms`
- `postprocess_ms`
- `result_image_save_ms`
- `record_save_ms`

## 3. Authorized Backend Files

Backend Agent may modify only:

- `web-flask/ai/yolo_infer.py`
- `web-flask/services/detection_service.py`
- `web-flask/routes/detection.py`
- `web-flask/tests/test_smoke.py`
- `web-flask/tests/test_stage2_api_hardening.py`
- `web-flask/tests/test_runtime_diagnostics.py`

## 4. Hard Constraints

Step 1 must preserve these constraints:

- `schema_version` remains `detection_result.v1`
- no field deletion
- no field renaming
- no change to existing field semantics
- `timing` only gains optional additive keys
- old records without timing remain readable
- old frontend consumers can ignore unknown fields
- records save/read round-trip remains intact

## 5. Forbidden Scope

Step 1 must not modify:

- `web-vue/**`
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
- Frontend Agent implementation

## 6. Required Tests

A future Step 1 implementation must keep these tests passing:

- `/api/health` PASS
- login PASS
- `/api/detection/image` success branch PASS
- `unsupported_image_type` / `invalid_image` / bad confidence behavior unchanged
- timing fields readable when present
- missing timing fields do not error
- records save/read PASS
- `detection_result.v1` structure not broken

## 7. Worktree Requirement

Backend Agent must use an independent backend worktree for Step 1 implementation.

## 8. Rollback Strategy

If Step 1 needs rollback:

- revert only backend incremental code
- no DB migration rollback expected
- no Docker rollback expected
- no model / weight / category rollback expected
- no frontend rollback expected

## 9. Relationship to Existing Documents

This GO decision supersedes the earlier preparatory-only Step 1 authorization status for the purpose of implementation start.
The master planning gate remains unchanged and still describes Batch4 planning context.
