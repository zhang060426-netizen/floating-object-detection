# Phase 2B Batch2 Stage2 AI Readiness Notes

Date: 2026-05-18
Scope: AI runtime readiness implementation only. No training, no full dataset validation, no weight mutation, no class definition changes, no backend/frontend business-code edits.

## Implemented Runtime Surface

Added a small read-only runtime adapter under:

```text
other/model_train/detect/runtime/
  __init__.py
  yolo_runtime.py
other/model_train/detect/tests/
  test_yolo_runtime_contract.py
```

Primary import surface:

```python
from other.model_train.detect.runtime import (
    check_weight_readiness,
    get_dev_model_manifest,
    infer_image,
    normalize_ultralytics_result,
)
```

## Frozen Batch2 Runtime Defaults

| Field | Value |
|---|---|
| Model ID | `m_yolo26n_dev` |
| Model name | `YOLO26n Dev Baseline` |
| Weight | `other/model_train/detect/weights/yolo26n.pt` |
| Expected size | `5,544,453 bytes` |
| Expected SHA256 | `9b09cc8bf347f0fc8a5f7657480587f25db09b34bf33b0652110fb03a8ad4fef` |
| Default confidence | `0.5` |
| Default imgsz | `640` |
| Class ID | `0` |
| Class name | `floating_object` |
| Output schema | `detection_result.v1` |

## Behavior Guarantees

- Module import does **not** require `ultralytics`; the dependency is imported only inside `infer_image()`.
- `check_weight_readiness()` is read-only and can optionally verify SHA256.
- `get_dev_model_manifest()` returns the backend-consumable dev model record and readiness status.
- `normalize_ultralytics_result()` converts a YOLO result-like object into the frozen Stage2 detection payload:
  - `model`
  - `image`
  - `detections`
  - `summary`
  - `timing`
- Empty detections are successful payloads (`detections=[]`, `has_detections=false`).
- No files are written by the runtime adapter during manifest checks or normalization.
- `infer_image()` performs no save/render operation; result image persistence remains backend responsibility.

## Explicit Non-goals / Prohibitions

- Did not run training.
- Did not run validation.
- Did not run real image inference as part of verification.
- Did not modify `weights/`, `output/`, or `dataset/` contents.
- Did not add `.pt`, `.pth`, `.onnx`, training outputs, or dataset cache files.
- Did not change class definitions.
- Did not modify `web-flask` or `web-vue` business logic.

## Backend Handoff Notes

Backend can use this adapter for Phase 2B model-load and image-detection smoke integration:

1. Call `get_dev_model_manifest()` for model list/readiness.
2. Call `check_weight_readiness(verify_hash=True)` in explicit smoke or diagnostics only.
3. Call `infer_image(image_path, confidence_threshold=0.5, imgsz=640)` only when `ultralytics` and the dev weight are available.
4. Preserve the returned `detection_result.v1` shape when saving detection records.

If the weight file is absent in a worktree, readiness returns `ready=false`; this is a blocked runtime asset state, not a code failure.

## Verification Commands

```powershell
python -m py_compile other/model_train/detect/runtime/yolo_runtime.py other/model_train/detect/tests/test_yolo_runtime_contract.py
python -m unittest other.model_train.detect.tests.test_yolo_runtime_contract
python other/model_train/detect/runtime/yolo_runtime.py --manifest
```

## Verification Result

Executed on 2026-05-18 from `E:\MM\floating-worktrees\ai-worktree`:

| Command | Result |
|---|---|
| `python -m py_compile other/model_train/detect/runtime/yolo_runtime.py other/model_train/detect/tests/test_yolo_runtime_contract.py` | PASS |
| `python -m unittest other.model_train.detect.tests.test_yolo_runtime_contract` | PASS: 3 tests |
| `python other/model_train/detect/runtime/yolo_runtime.py --manifest` | PASS: manifest generated; `readiness.ready=false` because `weights/yolo26n.pt` binary is not present in this worktree |

PowerShell profile loading emitted execution-policy warnings before command output; they did not affect Python command results.
