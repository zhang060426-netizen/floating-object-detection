# Phase 2B Batch4 Frontend Display Plan

Status: Planning only  
Role: Frontend Agent  
Project: 水面漂浮物垃圾检测系统  
Date: 2026-05-20  
Scope: Future UI/UX planning for model quality and inference-performance display. No implementation in this batch.

## 1. Context Recovery

### 1.1 Current Phase State

- Phase 2B Batch3: CLOSED / ARCHIVED.
- Stable tag: `phase2b-batch3-docker-compose-stable`.
- Stable code point: `fddb0c8`.
- Archive commit: `ff731de`.
- Final Smoke Verification: PASS.
- Docker Compose deployment: PASS.
- `detection_result.v1`: PRESERVED.
- Runtime model mount: PASS.
- Batch4 is explicitly **planning only**.

### 1.2 Frontend Boundary for This Document

Allowed:

- Plan future frontend display of model quality and inference-performance signals.
- Evaluate whether to expose model baseline type, detection count, inference time, no-detection state, and dev-placeholder/baseline warnings.
- Produce this planning document only.

Forbidden in Batch4:

- No Vue page changes.
- No API client changes.
- No Dockerfile or `docker-compose.yml` changes.
- No business-code changes.
- No `detection_result.v1` implementation changes.
- No model/category/weight changes.
- No video/realtime/Word/Dashboard/big-screen work.
- No commit.

### 1.3 Inputs Reviewed

Read or inspected:

- `AGENTS.md`
- `PROJECT_CONTEXT.md`
- `README.md`
- `PHASE2B_PRE_DEV_FREEZE.md`
- `agent_outputs/frontend/`
- `agent_outputs/backend/DETECTION_RESULT_SCHEMA.md`
- `agent_outputs/ai/MODEL_ASSET_BASELINE.md`
- `.omx/specs/`
- `.omx/plans/`

Expected but not present in this worktree at planning time:

- `tasks/frontend/TASK_PHASE2B_BATCH4_PLANNING.md`
- `agent_outputs/docs/PHASE2B_BATCH4_MASTER_PLANNING_GATE.md`

Because those two Batch4-specific gate files are absent locally, this document treats the user-provided Batch4 boundary as authoritative and does not widen scope.

## 2. Planning Goal

Future frontend should make the following clear to users without overstating model capability:

1. Which model/baseline was used.
2. Whether the model is a development placeholder or a trained production-quality asset.
3. How many objects were detected.
4. Whether the image has no detected target.
5. How long inference took, when backend provides stable timing.
6. What quality evidence exists for the model, and whether that evidence is historical, verified, or placeholder-only.

This is UI/UX planning only. No page, route, store, type, request, or component is created in Batch4.

## 3. Display Decisions

| Item | Future Display Decision | Rationale | Evidence / Dependency | Batch4 Action |
|---|---|---|---|---|
| Model baseline type | Should display | Users must distinguish `yolo26n`, `yolov8n`, etc.; also prevents confusing base weights with trained weights. | `base_model` exists in model API and `detection_result.model`. | Planning only |
| Detection count | Should display | It is the primary quick outcome of image detection and supports no-detection state. | `summary.total_detections`; `detections.length` fallback if contract allows. | Planning only |
| Inference time | Should display when stable | Useful for performance transparency, but must not become a hard UI dependency until field naming is stable. | `timing.inference_ms` appears in pre-dev freeze; schema also mentions `timing_ms`. | Planning only |
| No-detection status | Should display | Empty detections need explicit safe wording; otherwise users may misread blank results as UI/API failure. | `summary.has_detections=false` and `summary.total_detections=0`. | Planning only |
| Dev placeholder / baseline warning | Must display when applicable | Current dev baseline may not represent historical precision/production effect; warning is required for user trust and AI-safety boundary. | `is_dev_placeholder=true`; model baseline docs warn that base weights are not trained business weights. | Planning only |
| Model quality metrics | Should display as contextual evidence, not as a guarantee | Historical P/R/mAP can help but must be labeled by source and verification level. | `MODEL_ASSET_BASELINE.md` records historical precision/recall/mAP, while `best.pt` is missing. | Planning only |

## 4. Recommended Future UI Placement

### 4.1 Image Detection Page: Model Selector Area

Future display near model selection:

- Model name: `YOLO26n Dev Baseline` or actual published model name.
- Baseline type: `base_model`, e.g. `yolo26n`.
- Status badge: `Published` / unavailable if contract provides it.
- Warning badge when `is_dev_placeholder=true`: `开发占位模型`.
- Tooltip/callout text for placeholder models:
  - “当前模型仅用于开发联调，不代表历史精度或生产效果。”

Do not block image detection solely because a warning exists; warning is informational unless future backend gate marks the model unusable.

### 4.2 Image Detection Result Summary

Future result summary should display after a successful image detection request:

- Detection count: `summary.total_detections`.
- No-detection state:
  - If `summary.has_detections=false` or `total_detections=0`, show “未检测到水面漂浮物目标”.
  - Keep original/result image visible if available.
  - Do not render empty target rows as an error.
- Confidence summary, if already provided:
  - `max_confidence`
  - `avg_confidence`
- Inference time, if provided:
  - Preferred future label: “推理耗时”
  - Preferred unit: `ms`
  - Field compatibility note: support should be planned around a stable backend contract before implementation because current docs mention both `timing.inference_ms` and `timing_ms`.

### 4.3 Detection Detail / Record Detail

Future record detail should preserve the same semantics as the immediate result page:

- Model used for the saved result.
- Baseline type.
- Dev-placeholder warning if applicable at detection time.
- Detection count and no-detection status.
- Inference time if persisted in `detection_result.v1`.

Important: saved records should display the model metadata captured at detection time, not silently replace it with current model registry values.

### 4.4 Model Quality Evidence Display

Recommended future display style:

- Use a compact “模型质量参考” panel, not a Dashboard/big-screen chart in this phase.
- Show only metrics that have a clear source and verification level:
  - Precision
  - Recall
  - mAP50
  - mAP50-95
  - Dataset split/source if available
- Label historical metrics as historical evidence, e.g. “历史测试集指标（不可等同于当前占位权重效果）”.
- If the current model is a base/dev placeholder, visually separate historical trained-model metrics from the active placeholder model.

Do not claim that the active dev placeholder reaches historical metrics unless a future verified trained weight is mounted and validated.

## 5. Field-Level Planning Notes

### 5.1 Model Baseline Type

Future frontend can consume:

- Model list: `data[].base_model`.
- Detection result: `detection_result.model.base_model`.

Display rule:

- Prefer the model value embedded in `detection_result` for completed detections.
- Use model-list value only before detection or when choosing a model.

### 5.2 Dev Placeholder / Baseline Warning

Future frontend can consume:

- Model list: `data[].is_dev_placeholder`.
- Detection result currently does not consistently include `is_dev_placeholder`; future contract may add it or frontend may map by `model_id` from the model registry.

Planning recommendation:

- Prefer adding `is_dev_placeholder` to the detection-time model snapshot in a future contract revision only if Backend/Docs approve it.
- Until then, warning display can be planned as model-selector-only, and record warning can be best-effort if registry data is available.

No Batch4 implementation is performed.

### 5.3 Detection Count

Future frontend should prioritize:

1. `detection_result.summary.total_detections`
2. Fallback only if contract permits: `detection_result.detections.length`

No-detection state should not depend only on array length if `summary.has_detections` exists.

### 5.4 Inference Time

Current planning conflict:

- `PHASE2B_PRE_DEV_FREEZE.md` example uses `timing.inference_ms`.
- `DETECTION_RESULT_SCHEMA.md` mentions `timing_ms` as an object.

Future frontend should wait for Backend/Docs to freeze exact `detection_result.v1` timing field before implementation. Planned display can be approved, but code should not be written until the field name is contract-stable.

### 5.5 No-Detection Status

Future frontend should treat no-detection as a valid result, not an error.

Recommended UI copy:

- Title: “未检测到水面漂浮物目标”
- Detail: “本次检测未返回目标框，可调整图片、模型或置信度阈值后重试。”

Avoid wording that implies the water is definitely clean; object detection can miss targets.

## 6. UX Risk Controls

| Risk | UI/UX Control |
|---|---|
| Users confuse base model with trained model | Always label `base_model` as “基础模型类型”, not “精度模型”. |
| Users assume dev placeholder has production quality | Show explicit dev-placeholder warning. |
| No-detection result is misread as failure | Use a dedicated empty-success state. |
| Inference time becomes a misleading benchmark | Show as single-run reference only; avoid ranking or SLA claims. |
| Historical metrics are overclaimed | Label source/evidence and separate from active placeholder model. |
| Future contract drift breaks UI | Do not implement until Backend/Docs freeze fields for Batch4 implementation or later. |

## 7. Future Acceptance Criteria for Implementation Phase

These criteria are for a later implementation batch, not Batch4 planning:

1. Model selector displays model name, `base_model`, and dev-placeholder warning where applicable.
2. Image detection result displays detection count and no-detection success state.
3. Inference time displays only when stable timing field exists; absent timing does not break result rendering.
4. Record detail displays detection-time model metadata from `detection_result.v1`.
5. Model quality metrics are labeled with source and verification level.
6. Dev placeholder warning clearly states that the model does not represent historical precision or production effect.
7. Existing `detection_result.v1` parsing remains backward compatible.

## 8. Current Batch4 Conclusion

Frontend planning recommendation:

- Display model baseline type: **Yes**.
- Display detection count: **Yes**.
- Display inference time: **Yes, after field name is frozen and only when present**.
- Display no-detection status: **Yes**.
- Display dev-placeholder / baseline warning: **Yes, mandatory when `is_dev_placeholder=true` or equivalent evidence exists**.
- Display model quality metrics: **Yes, but only as source-labeled reference evidence, never as a guarantee for dev placeholder models**.

This document does not modify Vue pages, API clients, Docker files, business code, model assets, categories, weights, or `detection_result.v1` implementation.