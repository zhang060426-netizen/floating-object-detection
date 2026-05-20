# Phase 2B Batch4 AI Model Evaluation Plan

Date: 2026-05-20
Agent: AI Agent
Project: 水面漂浮物垃圾检测系统
Phase: Phase 2B Batch4
Mode: Planning only

## 0. Batch4 Scope Boundary

This document is the only AI Batch4 deliverable. It is a planning artifact, not an implementation change.

### Allowed in this batch

- Clarify the current runtime model identity for `yolo26n.pt`.
- Separate runtime/link availability from model-quality availability.
- Plan future model evaluation methodology.
- Plan future higher-precision model introduction gates.
- Plan ONNX / TensorRT feasibility checks without exporting or building anything.
- Preserve the current `detection_result.v1` contract and single-class model contract.

### Explicitly not executed in this batch

- No model training.
- No model replacement, deletion, move, or binary mutation.
- No class definition change.
- No ONNX export.
- No TensorRT engine generation.
- No full dataset evaluation.
- No image/video/realtime/Word/dashboard implementation.
- No Flask, Vue, YOLO logic, Dockerfile, or `docker-compose.yml` edits.
- No `detection_result.v1` implementation change.
- No commit.

## 1. Context Recovery Summary

Current state supplied by Leader:

| Item | Current value |
|---|---|
| Previous phase | Phase 2B Batch3 CLOSED / ARCHIVED |
| Stable tag | `phase2b-batch3-docker-compose-stable` |
| Stable code point | `fddb0c8` |
| Archive commit | `ff731de` |
| Final smoke verification | PASS |
| Docker Compose deployment | PASS |
| Runtime model mount | PASS |
| Current batch | Batch4 planning only |
| Preserved schema | `detection_result.v1` |

Read or checked locally:

- `AGENTS.md`, `PROJECT_CONTEXT.md`, `README.md`
- `agent_outputs/ai/AI_BATCH3_DOCKER_RUNTIME_READINESS.md`
- `agent_outputs/ai/AI_RUNTIME_READINESS_BATCH2_STAGE1.md`
- `agent_outputs/ai/AI_RUNTIME_READINESS_BATCH2_STAGE2.md`
- `agent_outputs/ai/MODEL_ASSET_BASELINE.md`
- `agent_outputs/ai/AI_OUTPUT_SCHEMA.md`
- `agent_outputs/ai/AI_PHASE2B_GATE.md`
- `.omx/specs/deep-interview-floating-yolo-architecture-upgrade.md`
- `.omx/plans/phase2a-system-contract-rebuild-plan-20260513.md`
- `.omx/plans/replan-floating-yolo-engineering-20260513T025133Z.md`
- Runtime adapter constants in `other/model_train/detect/runtime/yolo_runtime.py`
- Historical training script references under `1项目代码/floating-objects-detect-web/other/model_train/detect/code/`

Requested files `tasks/ai/TASK_PHASE2B_BATCH4_PLANNING.md` and `agent_outputs/docs/PHASE2B_BATCH4_MASTER_PLANNING_GATE.md` are not present in this worktree and were also not found at `phase2b-batch3-docker-compose-stable` or `ff731de`. This plan therefore treats the user-provided Batch4 instruction as the authoritative Batch4 gate.

## 2. Current Runtime Model Identity: `yolo26n.pt`

### 2.1 Frozen Batch3 runtime identity

The current runtime baseline is identified as:

| Field | Value |
|---|---|
| Runtime weight name | `yolo26n.pt` |
| Host runtime path | `runtime/models/yolo26n.pt` |
| Container runtime path | `/app/runtime/models/yolo26n.pt` |
| Expected size | `5,544,453 bytes` |
| Expected SHA256 | `9b09cc8bf347f0fc8a5f7657480587f25db09b34bf33b0652110fb03a8ad4fef` |
| Model ID | `m_yolo26n_dev` |
| Model name | `YOLO26n Dev Baseline` |
| Base model | `yolo26n` |
| Class map | `{ "0": "floating_object" }` |
| Output schema | `detection_result.v1` |
| Role | dev runtime baseline / backend smoke placeholder |
| Production precision certified | No |

This identity is supported by Batch2/Batch3 AI notes and the runtime adapter constants:

- `DEV_MODEL_ID = "m_yolo26n_dev"`
- `DEV_MODEL_NAME = "YOLO26n Dev Baseline"`
- `DEV_WEIGHT_NAME = "yolo26n.pt"`
- `EXPECTED_DEV_WEIGHT_SIZE_BYTES = 5_544_453`
- `EXPECTED_DEV_WEIGHT_SHA256 = "9b09cc8bf347f0fc8a5f7657480587f25db09b34bf33b0652110fb03a8ad4fef"`
- `CLASS_ID = 0`, `CLASS_NAME = "floating_object"`

### 2.2 What `yolo26n.pt` is

For Phase 2B Batch4 planning, `yolo26n.pt` must be described as:

> The approved dev runtime baseline weight used to prove that the Docker/Backend runtime can locate, read, hash-check, and load a YOLO-compatible `.pt` model while preserving `detection_result.v1`.

It is valid for:

- Docker mount/readiness checks.
- Import/load smoke checks.
- Backend model-not-ready and model-ready behavior.
- Minimal image-detection chain smoke after gate approval.
- JSON normalization compatibility checks.

It is not valid for:

- Claiming historical precision/recall/mAP.
- Claiming production model quality.
- Replacing a trained business `best.pt` baseline.
- Justifying UI/marketing statements about detection accuracy.
- Proving real-world water-surface trash detection robustness.

## 3. Runtime Chain Availability vs Model Effect Availability

Batch4 must keep two kinds of readiness separate.

### 3.1 Runtime/link availability

Runtime/link availability means the system path works technically:

| Check | Meaning | Quality implication |
|---|---|---|
| File exists at mounted path | The container can see `yolo26n.pt` | No precision claim |
| Size/hash match expected metadata | The mounted file is the approved dev asset | No precision claim |
| Ultralytics/Torch import works | Runtime dependencies are present | No precision claim |
| `YOLO(path)` loads | Weight can be deserialized by runtime | No precision claim |
| One controlled smoke inference returns `detection_result.v1` | Backend normalization path is wired | Only chain smoke, not model quality |
| Detection record can be saved | DB/API persistence contract works | Only data-flow readiness |

Batch3 final smoke PASS and Docker Compose PASS belong to this category.

### 3.2 Model effect/quality availability

Model effect availability requires dataset-grounded evaluation:

| Requirement | Meaning |
|---|---|
| Frozen evaluation dataset | Images and labels are versioned and match the declared class map. |
| Exact model binary identity | Weight hash is recorded and tied to the evaluated artifact. |
| Reproducible evaluation command | Runtime version, image size, confidence/IoU thresholds, device, and split are recorded. |
| Metrics artifacts | Precision, recall, mAP50, mAP50-95, per-class metrics, confusion matrix, and prediction samples are saved. |
| Error analysis | False positives/false negatives and scenario limitations are reviewed. |
| Cross-agent signoff | AI owns metrics, Backend owns integration safety, Frontend/Docs own presentation wording. |

Current `yolo26n.pt` has runtime/link availability evidence, but it does not have Batch4-approved model-effect evidence.

## 4. Historical `best.pt` Metrics Attribution Rule

Historical metrics recorded in earlier AI baseline documents include values such as:

| Split/source type | Precision | Recall | mAP50 | mAP50-95 | Attribution status |
|---|---:|---:|---:|---:|---|
| Historical validation output | 0.904 | 0.845 | 0.927 | 0.675 | Historical output only |
| Historical test output | 0.889 | 0.827 | 0.915 | 0.659 | Historical output only |

These metrics must not be attributed to the current runtime `yolo26n.pt` baseline because:

1. The historical `best.pt` binary is not confirmed as the current runtime-mounted file.
2. The current runtime identity is `m_yolo26n_dev` / `yolo26n.pt`, not a verified trained `best.pt` release.
3. Historical scripts refer to `output/train/weights/best.pt` or historical paths, while Batch3 runtime uses `runtime/models/yolo26n.pt`.
4. Historical training/evaluation context and current Docker runtime context are different evidence classes.
5. Batch2/Batch3 explicitly disallowed production precision claims from `yolo26n.pt`.

Required wording for future docs/UI until a formal evaluation is completed:

> Current runtime model is a dev baseline for chain verification. Historical best.pt metrics are retained as historical records only and are not certified metrics for the mounted `yolo26n.pt` runtime baseline.

## 5. Future Model Quality Evaluation Plan

### 5.1 Evaluation gates

Future evaluation may start only when all gates are satisfied:

| Gate | Required condition |
|---|---|
| Dataset gate | Evaluation image/label set exists, is versioned, and uses `nc=1`, `names=['floating_object']`. |
| Weight gate | Evaluated `.pt` file hash/size is recorded before evaluation. |
| Contract gate | Output remains compatible with `detection_result.v1`; no class-map change. |
| Environment gate | Ultralytics/Torch versions, Python version, device, image size, thresholds are recorded. |
| Scope gate | Leader approves evaluation scope; full evaluation is not part of Batch4. |
| Artifact gate | Evaluation outputs go to a new timestamped folder, never overwrite existing weights or historical outputs. |

### 5.2 Evaluation tiers

| Tier | Purpose | Dataset size | Allowed future use |
|---|---|---:|---|
| Smoke evaluation | Prove evaluation script can run and produce schema | 1-5 labeled images | Tooling check only |
| Mini regression | Catch obvious regressions | 20-100 labeled images | Pre-merge sanity |
| Candidate acceptance | Compare candidate vs current approved baseline | Fixed validation/test split | Release decision input |
| Full evaluation | Certify model quality for production wording | Full held-out split | Production-quality claim input |

Batch4 executes none of these tiers; it only defines them.

### 5.3 Metrics to record

Future evaluation artifacts should include:

| Metric/artifact | Reason |
|---|---|
| Precision, Recall | Core detection correctness. |
| mAP50, mAP50-95 | Standard YOLO evaluation summary. |
| Per-class metrics | Still required even for one class to preserve future compatibility. |
| Confusion matrix | Helps explain false positives/negatives. |
| PR/F1 curves | Helps choose confidence threshold. |
| Prediction sample sheet | Human review of representative successes/failures. |
| Runtime latency summary | Separate from quality; record CPU/GPU and batch size. |
| Model hash manifest | Prevents metric-to-weight attribution drift. |

### 5.4 Required evaluation manifest

Every future evaluation run should write a manifest similar to:

```json
{
  "schema_version": "model_evaluation.v1",
  "model": {
    "model_id": "candidate-or-baseline-id",
    "weight_name": "model.pt",
    "sha256": "...",
    "size_bytes": 0,
    "class_map": { "0": "floating_object" }
  },
  "dataset": {
    "dataset_id": "trash_floater_eval_v1",
    "split": "test",
    "image_count": 0,
    "label_count": 0,
    "source": "..."
  },
  "runtime": {
    "ultralytics_version": "...",
    "torch_version": "...",
    "python_version": "...",
    "device": "cpu-or-cuda",
    "imgsz": 640,
    "conf": 0.25,
    "iou": 0.7
  },
  "metrics": {
    "precision": null,
    "recall": null,
    "map50": null,
    "map50_95": null
  },
  "attribution": {
    "claim_allowed": false,
    "notes": "Metrics are tied only to the exact hash above."
  }
}
```

## 6. Future Higher-Precision Model Introduction Conditions

A future higher-precision model may be introduced only through an explicit release gate.

### 6.1 Candidate requirements

| Requirement | Rule |
|---|---|
| Binary provenance | Source, training run, dataset version, and creator are documented. |
| Hash identity | SHA256 and size are recorded before any deployment. |
| Class compatibility | Must keep `class_id=0`, `class_name=floating_object` unless a separate multi-class migration is approved. |
| Schema compatibility | Must preserve `detection_result.v1` or introduce a versioned backward-compatible extension. |
| Evaluation improvement | Must beat or intentionally trade off against the approved baseline on fixed evaluation data. |
| Runtime compatibility | Must load in the target Docker runtime without first-run downloads. |
| Rollback path | Previous runtime model remains restorable by path/hash. |

### 6.2 Decision thresholds to define before implementation

The project should define release thresholds before accepting a candidate. Suggested planning values:

| Dimension | Suggested gate |
|---|---|
| mAP50 | Candidate must be >= current certified baseline, or exception documented. |
| Recall | Must not regress materially for floating-object detection unless precision tradeoff is approved. |
| False positives | Must be reviewed on clean-water/background images. |
| Latency | Must remain within Backend image-detection timeout budget. |
| Model size | Must fit Docker/runtime deployment constraints. |
| CPU fallback | Must still load and return clear errors or acceptable latency on CPU-only environments. |

No threshold is activated in Batch4; these are future planning inputs.

### 6.3 Release sequence for a future model

1. Register candidate as a separate model ID; do not overwrite `m_yolo26n_dev`.
2. Store binary in a staging location; record hash and size.
3. Run smoke evaluation.
4. Run fixed candidate acceptance evaluation.
5. Compare against the current certified baseline.
6. Review failure cases and latency.
7. Backend verifies model selection and rollback.
8. Frontend/Docs update wording only after certification.
9. Promote by configuration/manifest, not by silent file replacement.
10. Archive evaluation manifest and artifacts.

## 7. ONNX / TensorRT Feasibility Plan Only

### 7.1 ONNX feasibility questions

Future ONNX work should answer:

| Question | Planning note |
|---|---|
| Export compatibility | Does the chosen Ultralytics version export this exact model architecture to ONNX? |
| Dynamic vs static shape | Decide whether fixed `imgsz=640` is enough or dynamic axes are required. |
| NMS behavior | Decide whether NMS is embedded or remains in application postprocess. |
| Numeric parity | Compare PyTorch vs ONNX predictions on a fixed mini set. |
| Runtime target | Choose ONNX Runtime CPU/GPU provider before implementation. |
| Contract preservation | Output must still normalize to `detection_result.v1`. |

Batch4 does not run `model.export(format='onnx')` and does not create `.onnx` files.

### 7.2 TensorRT feasibility questions

Future TensorRT work should answer:

| Question | Planning note |
|---|---|
| Hardware target | TensorRT requires NVIDIA GPU/runtime; Batch3 CPU-only acceptance does not prove this. |
| Precision mode | FP32/FP16/INT8 must be selected with accuracy and calibration implications. |
| Engine portability | TensorRT engines are hardware/runtime specific and should not be treated like portable weights. |
| Calibration data | INT8 requires representative calibration images and separate quality checks. |
| Parity test | PyTorch vs TensorRT outputs must be compared on fixed images. |
| Deployment profile | TensorRT should be an optional profile, not the default CPU baseline. |

Batch4 does not generate `.engine` files and does not require NVIDIA runtime.

### 7.3 Future conversion gate

Before any ONNX/TensorRT implementation, require:

- Leader-approved conversion task.
- Exact source `.pt` hash.
- Export tool/version manifest.
- Output artifact naming and storage policy.
- Parity test plan.
- Rollback plan to PyTorch `.pt` runtime.
- Confirmation that `detection_result.v1` remains unchanged.

## 8. Future Implementation Items Not Executed Now

The following items are explicitly deferred:

| Deferred item | Future owner | Why deferred |
|---|---|---|
| Full dataset validation of `yolo26n.pt` | AI | Batch4 is planning only. |
| Training a higher-precision model | AI | Requires dataset/training plan and gate approval. |
| Replacing runtime model | AI + Backend | Would mutate deployment behavior and requires release gate. |
| Adding model registry fields | Backend | Business-code change, out of scope. |
| Adding evaluation API/UI | Backend + Frontend | Out of Batch4; also touches contracts. |
| ONNX export script | AI | Implementation artifact, not planning. |
| TensorRT engine build | AI/DevOps | Requires GPU/runtime target and parity tests. |
| Video/realtime performance benchmark | AI + Backend | Explicitly out of Batch4. |
| Word/report/dashboard updates | Frontend/Backend/Docs | Explicitly out of Batch4. |

## 9. Risks and Controls

| Risk | Control |
|---|---|
| Runtime readiness is mistaken for model quality | Always label `yolo26n.pt` as dev runtime baseline until certified evaluation exists. |
| Historical metrics are attributed to wrong binary | Tie every metric to exact weight hash and dataset manifest. |
| Higher-precision model silently changes class map | Block release unless `0/floating_object` remains unchanged or formal migration is approved. |
| ONNX/TensorRT changes break output shape | Require parity tests and `detection_result.v1` normalization before deployment. |
| Evaluation artifacts overwrite historical outputs | Use timestamped output directories and never write into existing weight folders. |
| UI exposes uncertified precision | Frontend/Docs wording must distinguish chain smoke from quality certification. |

## 10. Batch4 Acceptance Checklist

- [x] Runtime `yolo26n.pt` identity clarified as `m_yolo26n_dev` / dev baseline.
- [x] Chain availability and model-effect availability separated.
- [x] Future model quality evaluation method planned.
- [x] Future higher-precision model introduction conditions planned.
- [x] ONNX / TensorRT feasibility planned without implementation.
- [x] Historical `best.pt` metrics marked as non-attributable to current runtime baseline.
- [x] Future implementation items explicitly deferred.
- [x] No business code, Docker config, model binary, class definition, or `detection_result.v1` change performed.

## 11. Rollback

This Batch4 change is documentation-only. Rollback is to remove:

```text
agent_outputs/ai/PHASE2B_BATCH4_AI_MODEL_EVALUATION_PLAN.md
```

No model weights, source code, Docker files, schema implementation, dataset files, or generated evaluation artifacts are affected.
