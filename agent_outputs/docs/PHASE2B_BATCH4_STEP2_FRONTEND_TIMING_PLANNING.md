# Phase 2B Batch4 Step 2 Planning / Authorization Checklist

Status: PLANNING ONLY
Date: 2026-05-20
Phase: Phase 2B Batch4 Step 2
Step 2 name: Frontend display backend timing metadata
Current Step 2 implementation status: NOT AUTHORIZED

## 1. Purpose

This document defines the planning boundary and authorization checklist for a future frontend-only Step 2.

It does **not** authorize implementation.
It does **not** authorize code changes.
It does **not** authorize backend changes.
It exists only to specify what would be required before a separate GO Decision can be issued later.

## 2. Step 2 Planning Scope

Future Step 2 is limited to frontend display of backend timing metadata in detection-result views.

### 2.1 Minimum intended display scope

- Immediate image detection result page timing display
- Detection record detail page timing display
- Timing block visible only when timing exists
- Timing-missing state renders normally without error
- Legacy records without timing remain compatible
- Existing detection result rendering remains intact
- Login, routing, and base API flows remain unchanged

### 2.2 Timing fields that may be displayed later

- `total_api_ms`
- `inference_ms`
- `model_load_ms`
- `preprocess_ms`
- `postprocess_ms`
- `result_image_save_ms`
- `record_save_ms`

## 3. Explicit Forbidden Scope

Step 2 planning does not authorize:

- `web-flask/**` changes
- backend `detection_result.v1` changes
- backend schema changes
- Dockerfile changes
- `docker-compose.yml` changes
- `runtime/**` changes
- `storage/**` changes
- `.pt` / `.pth` / `.onnx` submission or mutation
- model weights changes
- model class changes
- training logic changes
- video detection
- realtime detection
- Word report work
- Dashboard / large-screen work
- AI Agent implementation
- Backend Agent implementation unless separately authorized later
- push
- tag creation

## 4. Required Compatibility Rules

Future Step 2 must preserve:

- `detection_result.v1` exactly as a preserved backend contract
- timing as optional additive metadata only
- frontend compatibility when timing is absent
- old records without timing must not error
- existing result rendering must continue to function

## 5. Candidate Frontend Files for Future Implementation Only

If and only if a later GO Decision is issued, Step 2 implementation may be limited to frontend files such as:

- `web-vue/src/views/ImageDetect.vue`
- `web-vue/src/views/DetectionRecordDetail.vue`
- `web-vue/src/components/DetectionResultPanel.vue`
- `web-vue/src/types/detection.ts`
- `web-vue/src/utils/detectionDisplay.ts`
- `web-vue/src/api/detection.ts`

This is a planning-only candidate list, not an implementation authorization.

## 6. Agent Responsibilities

- Frontend Agent: prospective primary implementation owner
- Docs/Test Agent: prospective evidence and closeout owner
- Backend Agent: not needed for Step 2 planning unless a contract clarification is separately requested
- AI Agent: not needed for Step 2 planning

## 7. Smoke / Test Expectations for a Future Authorized Step 2

Future implementation should be verified against:

- frontend build / typecheck / lint as applicable
- timing-present result rendering
- timing-missing result rendering
- old record compatibility
- no regression in login, routing, or base API usage
- no regression in existing detection-result presentation

## 8. Rollback Strategy

If Step 2 is later authorized and needs rollback:

- revert only the frontend incremental code
- no backend rollback expected
- no DB migration rollback expected
- no Docker rollback expected
- no model / weight / category rollback expected
- no frontend data migration rollback expected

## 9. Authorization Rule

This checklist is **not** a GO Decision.

A separate Step 2 GO Decision document must be created later before any frontend implementation begins.
This checklist must never be treated as implementation authorization.

## 10. Current Decision

```text
Phase 2B Batch4 Step 2 Planning: GO
Phase 2B Batch4 Step 2 Implementation: NOT AUTHORIZED
```
