# Phase 2B Batch4 Backend Performance Plan

Role: Backend Agent  
Project: 水面漂浮物垃圾检测系统  
Phase: Phase 2B Batch4  
Mode: Planning only; no implementation  
Date: 2026-05-20

## 0. Context restored

User-provided latest state:

- Phase 2B Batch3: CLOSED / ARCHIVED.
- Stable tag: `phase2b-batch3-docker-compose-stable`.
- Stable code point: `fddb0c8`.
- Archive commit: `ff731de`.
- Final Smoke Verification: PASS.
- Docker Compose deployment: PASS.
- `detection_result.v1`: PRESERVED.
- Runtime model mount: PASS.
- Batch4 is planning only.

Local context notes from this worktree:

- The current worktree contains the minimal Flask backend rebuilt in Phase 2B, including image detection route and service files.
- The requested `tasks/backend/TASK_PHASE2B_BATCH4_PLANNING.md` and `agent_outputs/docs/PHASE2B_BATCH4_MASTER_PLANNING_GATE.md` were not present in the current worktree at planning time; this plan therefore relies on the user-supplied Batch4 boundary plus existing backend docs/code artifacts.
- Existing uncommitted `.omx` runtime-state modifications were present before this planning output; this Batch4 plan does not depend on or modify those runtime files.

## 1. Hard boundary for Batch4 Backend Planning

This document is the only allowed Batch4 backend output in this turn:

- Allowed output: `agent_outputs/backend/PHASE2B_BATCH4_BACKEND_PERFORMANCE_PLAN.md`.
- No Flask route/service/DB/API/Docker/model edits.
- No benchmark code, no scripts, no pytest changes, no production timing instrumentation.
- No changes to current `detection_result.v1` implementation.
- No model training, model replacement, class-map change, video/realtime/Word/dashboard work.
- No commit.

Implementation ideas below are explicitly future work and must pass a later implementation gate before code changes.

## 2. Existing backend facts relevant to performance planning

| Fact | Evidence |
|---|---|
| Image detection API entrypoint exists at `POST /api/detection/image`. | `web-flask/routes/detection.py:34` |
| `detect_image(...)` currently performs upload persistence, image metadata validation, YOLO inference, result image copy/draw, result assembly, and optional record save. | `web-flask/services/detection_service.py:61` |
| YOLO model is loaded inside `run_yolo_image(...)` on each call through `_load_yolo(...)`, then inference is executed. | `web-flask/ai/yolo_infer.py:76` |
| Current inference timing measures around model load + model call, because the timer starts before `_load_yolo(...)`. | `web-flask/ai/yolo_infer.py:77-80` |
| `detection_result.v1` currently contains a top-level `timing` object. | `web-flask/ai/yolo_infer.py:126`, `web-flask/ai/yolo_infer.py:153` |
| Current `detect_image(...)` passes `timings={"inference_ms": ..., "device": None, "model_cached": False}` into `build_detection_result(...)`. | `web-flask/services/detection_service.py:99` |
| Detection records persist `detection_result` as JSON text in `detection_records.detection_result`. | `web-flask/db/schema.sql:33` |
| Runtime diagnostics already expose model-weight/dependency information on published models. | `web-flask/README.md:49`, `web-flask/services/model_service.py` |
| Batch3 Docker runtime keeps DB/uploads/results/models outside the image. | `web-flask/DEPLOYMENT.md:5` |

Planning consequence: Batch4 should treat the existing `timing` object as an additive extension point, not as a schema to rename or replace.

## 3. Performance goals for the image detection API

### 3.1 Measurement objective

Create a future, repeatable way to answer four questions without changing user-facing detection semantics:

1. How long does the complete image detection API request take?
2. How much of that time is upload/file handling versus YOLO model load versus YOLO inference versus result rendering/record save?
3. What is the cold-start penalty when the model is not yet loaded or the process is newly started?
4. What is the warm inference latency after the model is already available in process memory?

### 3.2 Metric categories

| Category | Metric name | Unit | Definition | Planned source | Notes |
|---|---:|---|---|---|---|
| API total | `api_total_ms` | ms | Wall-clock duration from entering `image_detection()` route after Flask dispatch to response payload completion. | Future route/service wrapper. | Includes validation, upload save, model lookup, inference, result rendering, optional DB save. |
| Request validation | `request_parse_ms` | ms | Time to validate multipart fields and parse confidence/save flags. | Future route-level timer. | Keep optional; useful only for regressions. |
| Upload persistence | `upload_save_ms` | ms | Time to save uploaded image into storage and return bucket/object key/path. | Future `save_upload` boundary. | Separate from image metadata decode. |
| Image metadata | `image_metadata_ms` | ms | Time to open image and read width/height/format. | Future `image_metadata` boundary. | Also helps identify invalid/large-image overhead. |
| Model lookup | `model_lookup_ms` | ms | Time to fetch/validate model record from SQLite. | Future `get_model` boundary. | Expected small; track for DB regressions. |
| Model load | `model_load_ms` | ms | Time to instantiate/load YOLO model object from weight path when not cached. | Future `_load_yolo` or cache wrapper. | Critical for cold latency. |
| Warm inference | `inference_ms` | ms | Time for model forward/prediction only, excluding model load when cache exists. | Future `run_yolo_image` split timer. | Current `inference_ms` includes load; future plan must preserve old key semantics carefully. |
| Current-compatible inference | `legacy_inference_ms` | ms | Optional explicit alias for current behavior if future split changes `inference_ms`. | Future additive key. | Use only if needed to avoid ambiguity. |
| Result rendering | `result_render_ms` | ms | Time to copy and draw annotated result image. | Future `copy_result_image` + `draw_result_image` boundary. | Can be high for large images. |
| Record save | `record_save_ms` | ms | Time to persist `detection_records` when `save_record=true`. | Future `save_record` boundary. | Optional when `save_record=false`. |
| Response assembly | `response_assembly_ms` | ms | Time to build response dict after all processing. | Future service timer. | Usually small. |
| Cold/warm state | `model_cache_state` | enum | `cold_loaded`, `warm_cached`, `not_cached_legacy`, `unavailable`. | Future model loader/cache metadata. | Do not expose as required field. |
| Model identity | `model_weight_sha256` | string/null | SHA256 of loaded weight for reproducibility. | Existing runtime diagnostic helper can be reused later. | Avoid recomputing per request unless cached. |
| Runtime device | `device` | string/null | CPU/GPU device reported by backend or YOLO runtime. | Future inference wrapper. | Current value is `None`; keep compatible. |

### 3.3 Recommended benchmark dimensions for future implementation

| Dimension | Values to plan for | Reason |
|---|---|---|
| Process state | cold process, first request after process start, repeated warm requests | Separates Docker/process startup from in-process model reuse. |
| Cache state | no model cache, cache miss, cache hit | Determines whether model caching actually improves API latency. |
| Image size | small smoke image, representative test image, large uploaded image | Result rendering and upload overhead scale with image size. |
| Save mode | `save_record=false`, `save_record=true` | DB persistence and storage artifact costs differ. |
| Model availability | missing dependency, missing weight, valid mounted weight | Must preserve diagnostic error contract and avoid fake success. |
| Deployment mode | local Flask, Docker Compose backend | Batch3 stable deployment must remain reproducible. |

## 4. Cold and warm latency definitions

### 4.1 Cold inference latency

`cold_inference_latency_ms` should mean the first successful image detection request in a fresh backend process where the model object has not been loaded in memory yet.

Recommended future breakdown:

```text
cold_api_total_ms
  = request_parse_ms
  + upload_save_ms
  + image_metadata_ms
  + model_lookup_ms
  + model_load_ms
  + inference_ms
  + result_render_ms
  + optional record_save_ms
  + response_assembly_ms
```

Rules:

- Cold timing must be measured after backend process is ready to accept HTTP requests; it should not include container build, compose startup, or Flask import time.
- If `ultralytics` or the weight is unavailable, record a failure diagnostic in benchmark output only; do not create a detection success result.
- Cold measurement must state whether it includes a model cache warm-up request or is the first real user-style request.

### 4.2 Warm inference latency

`warm_inference_latency_ms` should mean a successful image detection request where the same `model_id` / weight path is already loaded in process memory.

Recommended future rules:

- Run one explicit warm-up request, discard its timing, then measure N repeated requests.
- Report `p50`, `p90`, `p95`, `p99`, `min`, `max`, and `mean` for both `api_total_ms` and inference-only timing.
- Record `model_cache_state=warm_cached` only when the implementation can prove the model object was reused.
- If no cache has been implemented yet, classify as `not_cached_legacy` rather than pretending warm cache exists.

### 4.3 Model load time

`model_load_ms` should measure only model-object construction/loading from a readable weight path, excluding upload save, image decode, inference, and result drawing.

Recommended future constraints:

- Key by immutable model identity: at minimum `(model_id, weight_path, weight_sha256)`.
- If using a cache, invalidate when weight path or SHA256 changes.
- Do not store full weight paths in public responses if later security review decides path disclosure is sensitive; for Batch4 planning, only mark this as a future review item.

### 4.4 API total latency

`api_total_ms` should be the primary user-facing SLA metric because it reflects the end-to-end cost perceived by frontend callers.

Planned future reporting buckets:

- `api_total_ms.p50`: normal user experience.
- `api_total_ms.p95`: slow-path user experience.
- `api_total_ms.p99`: regression guard for outliers.
- `api_total_ms.max`: diagnostic, not SLA by itself.

## 5. Proposed performance targets for future gates

These are planning targets, not current measured results. They must be validated with actual benchmark implementation later.

| Gate | Environment | Proposed target | Status now |
|---|---|---|---|
| Planning gate | Current Batch4 | Metrics and schema strategy documented. | This document. |
| Benchmark implementation gate | Future Batch4/Batch5 implementation | Script can measure cold/warm/API total on Docker Compose without changing API contract. | Not implemented now. |
| Baseline measurement gate | Future | Establish measured baseline with current no-cache behavior; no pass/fail optimization target yet. | Not measured now. |
| Optimization gate | Future after baseline | Improve warm `api_total_ms` and split model-load from inference while preserving `detection_result.v1`. | Not implemented now. |

Suggested initial non-binding thresholds after benchmark exists:

- Cold request: report-only until real hardware/model baseline is known.
- Warm request: report-only until model cache exists and hardware is fixed.
- Regression guard: after two stable baselines, fail only on large relative regressions, e.g. +25% p95 on same machine/container/model/image set.

Rationale: hard millisecond targets before measuring the mounted model and hardware would be misleading.

## 6. Additive-only `detection_result.v1` extension strategy

### 6.1 Compatibility principles

1. Keep `schema_version` exactly `detection_result.v1` unless a separate version migration is explicitly approved later.
2. Do not rename, delete, or change meaning of existing keys: `model`, `image`, `detections`, `summary`, `artifacts`, `timing`.
3. Treat all new timing metadata as optional.
4. Add nested fields only; do not require frontend/DB/API callers to send or read them.
5. Existing records with sparse or empty `timing` must remain valid.
6. Manual record creation must continue accepting older `detection_result.v1` payloads without timing details.

### 6.2 Current timing shape to preserve

Current generated payload includes:

```json
"timing": {
  "inference_ms": 123.4,
  "device": null,
  "model_cached": false
}
```

Current constraints:

- `inference_ms` currently measures the timed region inside `run_yolo_image(...)`; because the timer starts before `_load_yolo(...)`, it may include model-load time in the current implementation.
- `model_cached` is currently always passed as `false` by `detect_image(...)`.
- `device` is currently `null`.

Future work must not silently redefine these fields without documenting the transition.

### 6.3 Planned additive timing metadata

Recommended future optional shape:

```json
"timing": {
  "inference_ms": 123.4,
  "device": null,
  "model_cached": false,
  "api_total_ms": 180.2,
  "model_load_ms": 52.1,
  "request_parse_ms": 1.0,
  "upload_save_ms": 3.2,
  "image_metadata_ms": 4.8,
  "model_lookup_ms": 0.7,
  "result_render_ms": 12.0,
  "record_save_ms": 6.5,
  "response_assembly_ms": 0.4,
  "model_cache_state": "not_cached_legacy",
  "measurement_version": "timing.v1",
  "measurement_source": "backend.image_detection",
  "measured_at": "2026-05-20T00:00:00Z"
}
```

Rules:

- `measurement_version` is versioning for timing metadata only; it does not change `detection_result.v1`.
- `measurement_source` identifies the instrumentation owner without adding a new API contract.
- `measured_at` should use UTC ISO-8601 if implemented later.
- Keep `api_total_ms` optional; old clients must tolerate absence.
- If future split makes `inference_ms` exclude model load, add a migration note and, if needed, a `legacy_inference_ms` additive key for one release window.

### 6.4 Forbidden schema changes for future implementation unless separately approved

- Changing `schema_version` to `detection_result.v2` for timing-only additions.
- Moving `timing` outside `detection_result` in the existing API response.
- Requiring frontend to display timing metadata for successful detection.
- Requiring DB schema migration just to store request timing.
- Removing current `summary.detection_status`, `summary.total_detections`, or detection bbox fields.
- Changing model class map or class ID semantics.

## 7. Non-destructive timing metadata storage strategy

### 7.1 Phase 1 future implementation: embedded optional timing only

Preferred first implementation path:

- Add optional timing keys under `detection_result.timing` before saving the JSON.
- No DB column changes.
- No response envelope change.
- No frontend contract requirement.
- No separate analytics table.

Why: `detection_records.detection_result` already stores JSON text, and optional nested timing keys are backward-compatible.

### 7.2 Phase 2 future implementation: benchmark artifact file

For repeatable performance testing, write benchmark outputs to a non-production artifact path such as:

```text
agent_outputs/backend/performance/phase2b-batch4-image-detection-baseline.json
```

This is future work only. The artifact should contain aggregate metrics, environment fingerprint, model identity, image set, and git commit. It should not require database changes.

### 7.3 Phase 3 future implementation: optional normalized table only after need is proven

A future DB table, if needed, should be additive and not required by the API. Candidate name:

```text
detection_timing_metrics
```

Candidate fields:

- `id`
- `record_id` nullable for unsaved benchmark requests
- `request_id`
- `model_id`
- `weight_sha256`
- `image_width`, `image_height`
- `save_record`
- `api_total_ms`, `model_load_ms`, `inference_ms`, `result_render_ms`, `record_save_ms`
- `cache_state`
- `created_at`

This is not approved for Batch4 implementation and must go through DB/documentation gate before any migration.

## 8. Future benchmark implementation plan (not executed now)

### 8.1 Future prerequisites

- Stable runtime from `phase2b-batch3-docker-compose-stable` or a later approved tag.
- Readable mounted model at the expected runtime path.
- Fixed benchmark image set from `4测试包/` or a documented small representative fixture.
- Clear command to start backend locally or via Docker Compose.
- Explicit statement of CPU/GPU availability.

### 8.2 Future implementation steps

1. Add internal timing helper using `time.perf_counter()` at route/service boundaries.
2. Split YOLO model-load timing from prediction timing.
3. Add optional in-process model cache keyed by model identity only if approved after baseline.
4. Add benchmark runner that can:
   - login,
   - discover published model,
   - run one cold request,
   - run warm-up request,
   - run N warm requests,
   - export aggregate JSON.
5. Add tests that assert schema compatibility, not exact latency values.
6. Update docs with measured baseline and rollback notes.

### 8.3 Future verification steps

- `python -m compileall web-flask`
- `python -m pytest web-flask/tests`
- Docker Compose health checks.
- Image detection success with real mounted model.
- Benchmark artifact review confirming cold/warm separation.
- Regression test confirming old manual `detection_result.v1` payloads still save and read back.

None of these are executed in this planning-only Batch4 turn.

## 9. Acceptance criteria for this planning output

- [x] Defines image detection API performance metric categories.
- [x] Defines cold/warm inference latency, model load time, and API total latency.
- [x] Preserves `detection_result.v1` and uses additive-only timing metadata.
- [x] Plans non-destructive timing metadata storage without DB/API/Docker changes now.
- [x] Separates future implementation work from current planning scope.
- [x] Does not modify Flask routes/services/DB/API/Docker/model files.

## 10. Rollback plan

Because this Batch4 output is documentation only, rollback is limited to removing this file:

```powershell
Remove-Item agent_outputs/backend/PHASE2B_BATCH4_BACKEND_PERFORMANCE_PLAN.md
```

No runtime, database, Docker, model, or API rollback is required because none were modified.
