# Phase 2B Batch3 AI Docker Runtime Readiness

Date: 2026-05-18
Agent: AI
Scope: Docker deployment/runtime readiness documentation only. No training, no weight mutation, no class-definition change, and no `detection_result.v1` schema change.
Baseline tag: `phase2b-batch2-image-detection-stable`
Gate input: Batch3 Implementation Gate Review = PASS

## 1. Batch3 Decision

Batch3 keeps AI runtime readiness **read-only** and deployment-oriented. The AI side does not introduce a new model, does not train, does not validate accuracy, and does not change the normalized detection payload. Docker readiness is limited to proving that the container can see the expected `yolo26n.pt` file and import/load the Ultralytics runtime when the approved weight is mounted.

## 2. Runtime Weight Placement Contract

The Batch3 Docker contract for the dev runtime baseline is fixed as:

| Location | Path |
|---|---|
| Host path | `runtime/models/yolo26n.pt` |
| Container path | `/app/runtime/models/yolo26n.pt` |
| Weight name | `yolo26n.pt` |
| Expected size | `5,544,453 bytes` |
| Expected SHA256 | `9b09cc8bf347f0fc8a5f7657480587f25db09b34bf33b0652110fb03a8ad4fef` |
| Model ID | `m_yolo26n_dev` |
| Model name | `YOLO26n Dev Baseline` |
| Class ID/name | `0` / `floating_object` |
| Output schema | `detection_result.v1` |

Required Docker mount intent:

```yaml
# Compose-side intent; service name may differ in Backend worktree.
volumes:
  - ./runtime/models:/app/runtime/models:ro
```

The mount must be read-only (`:ro`) for Batch3. If the file is absent, readiness should fail closed with model-not-ready/model-not-found behavior rather than downloading or generating a replacement.

## 3. CPU-only Baseline

Batch3 acceptance is CPU-only:

- The container must be able to run readiness checks without NVIDIA runtime, CUDA, or GPU device mappings.
- `ultralytics`/`torch` may report CPU device availability only; this is acceptable for Batch3.
- No throughput, latency, or production precision claim is made from this baseline.
- Real inference smoke is optional and should remain separate from this read-only readiness check.

GPU can be added later as an optional deployment profile, but it is explicitly **not** part of Batch3 acceptance.

## 4. Host-side Weight Hash and Size Checks

Run from the repository/deployment root that contains `runtime/models/yolo26n.pt`:

```powershell
# PowerShell: size + SHA256
$weight = "runtime\models\yolo26n.pt"
$item = Get-Item $weight
"size=$($item.Length)"
Get-FileHash -Algorithm SHA256 $weight
```

Expected:

```text
size=5544453
SHA256=9B09CC8BF347F0FC8A5F7657480587F25DB09B34BF33B0652110FB03A8AD4FEF
```

Cross-platform/Python equivalent:

```bash
python -c "import hashlib,pathlib; p=pathlib.Path('runtime/models/yolo26n.pt'); h=hashlib.sha256(); f=p.open('rb'); [h.update(c) for c in iter(lambda:f.read(1024*1024), b'')]; f.close(); print('path='+str(p.resolve())); print('size='+str(p.stat().st_size)); print('sha256='+h.hexdigest())"
```

## 5. Docker Container Readiness Checks

Replace `<backend-service>` with the actual Backend service name used by the Batch3 Docker implementation.

### 5.1 Mounted file presence and read-only visibility

```bash
docker compose exec <backend-service> python -c "from pathlib import Path; p=Path('/app/runtime/models/yolo26n.pt'); print('exists='+str(p.exists())); print('is_file='+str(p.is_file())); print('size='+str(p.stat().st_size if p.exists() else 0)); print('path='+str(p))"
```

Expected minimum:

```text
exists=True
is_file=True
size=5544453
path=/app/runtime/models/yolo26n.pt
```

### 5.2 Container-side hash check

```bash
docker compose exec <backend-service> python -c "import hashlib; from pathlib import Path; p=Path('/app/runtime/models/yolo26n.pt'); h=hashlib.sha256(); f=p.open('rb'); [h.update(c) for c in iter(lambda:f.read(1024*1024), b'')]; f.close(); print('size='+str(p.stat().st_size)); print('sha256='+h.hexdigest())"
```

Expected:

```text
size=5544453
sha256=9b09cc8bf347f0fc8a5f7657480587f25db09b34bf33b0652110fb03a8ad4fef
```

### 5.3 Ultralytics import/readiness check

This checks dependency availability without training and without running prediction:

```bash
docker compose exec <backend-service> python -c "import ultralytics, torch; from pathlib import Path; p=Path('/app/runtime/models/yolo26n.pt'); print('ultralytics='+str(getattr(ultralytics, '__version__', 'unknown'))); print('torch='+str(torch.__version__)); print('cuda_available='+str(torch.cuda.is_available())); print('weight_exists='+str(p.is_file()))"
```

Expected for Batch3 CPU-only baseline:

```text
cuda_available=False
weight_exists=True
```

`cuda_available=True` is also acceptable on a GPU-enabled host, but it is not required and must not be used as a Batch3 pass/fail gate.

### 5.4 Ultralytics model-load readiness check

This performs model construction/load only. It must not train, mutate weights, save outputs, or run full dataset validation:

```bash
docker compose exec <backend-service> python -c "from pathlib import Path; from ultralytics import YOLO; p=Path('/app/runtime/models/yolo26n.pt'); m=YOLO(str(p)); print('loaded=True'); print('model_path='+str(p)); print('task='+str(getattr(m, 'task', 'unknown')))"
```

Expected minimum:

```text
loaded=True
model_path=/app/runtime/models/yolo26n.pt
```

If this fails with `ModuleNotFoundError: ultralytics`, the container image is missing runtime dependencies. If it fails with file-not-found or bad zip/checkpoint errors, the mount or weight asset is invalid. Do not repair by downloading or replacing the file inside the container during Batch3.

## 6. Contract Preservation

Batch3 does **not** change:

- `detection_result.v1`
- class ID `0`
- class name `floating_object`
- `m_yolo26n_dev` identity
- expected `yolo26n.pt` hash/size metadata
- any `.pt`, `.pth`, or `.onnx` binary
- training scripts, datasets, validation outputs, video/realtime/Word/dashboard scopes

## 7. Backend/Deployment Handoff

Backend Docker implementation should:

1. Mount `./runtime/models` to `/app/runtime/models:ro`.
2. Configure the AI runtime/model loader to use `/app/runtime/models/yolo26n.pt` in containerized deployment.
3. Return not-ready/model-not-found style diagnostics if the file is absent or hash/size checks fail.
4. Avoid any first-run download behavior for Batch3 readiness.
5. Keep image detection persistence compatible with existing `detection_result.v1` records.

## 8. Risks

- The AI worktree currently does not include the binary weight; readiness is a deployment contract, not proof that this local worktree has the asset.
- Backend service naming and compose file location are owned by Backend/DevOps; commands above use `<backend-service>` placeholder.
- `ultralytics` and `torch` versions are runtime-image concerns; this document only defines checks, not dependency pin changes.
- CPU-only readiness does not prove production latency or GPU behavior.

## 9. Rollback

Rollback is documentation-only:

1. Remove `agent_outputs/ai/AI_BATCH3_DOCKER_RUNTIME_READINESS.md`.
2. Remove `other/model_train/detect/BATCH3_DOCKER_RUNTIME_READINESS.md`.
3. Revert any downstream Docker mount/readiness changes to the Batch2 stable tag `phase2b-batch2-image-detection-stable`.

No weight, class, schema, dataset, training, backend business-code, or frontend business-code changes are required to roll back this AI Batch3 handoff.

## 10. Verification Performed in AI Worktree

Planned verification for this documentation change:

```powershell
git status --short
git diff -- -- agent_outputs/ai/AI_BATCH3_DOCKER_RUNTIME_READINESS.md other/model_train/detect/BATCH3_DOCKER_RUNTIME_READINESS.md
Get-ChildItem -Recurse -File -Include *.pt,*.pth,*.onnx | Select-Object FullName,Length
```

Expected result: only the two Batch3 Markdown files are new/changed by this task, and no model binary appears in the diff.
