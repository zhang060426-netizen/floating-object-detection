# Phase 2B Batch2 Stage1 AI Runtime Notes

Date: 2026-05-17
Scope: AI documentation only. No training, no full dataset validation, no weight mutation, no class definition changes.

## yolo26n.pt Batch2 Usage

`yolo26n.pt` is allowed for Phase 2B Batch2 as a **dev runtime baseline** / backend smoke-test placeholder only.

It must be treated as a runtime-readiness asset, not as a production-quality model:

- Purpose: verify backend can locate and read a YOLO weight file during smoke tests.
- Production accuracy: **not certified** by this Batch2 Stage1 task.
- Dataset validation: full dataset validation was **not** executed in this task.
- Training: **not executed** in this task.
- Weight mutation: **not allowed** and **not performed**.

## Fixed Weight Record

| Field | Value |
|---|---|
| Weight file | `yolo26n.pt` |
| Expected project-relative location | `other/model_train/detect/weights/yolo26n.pt` |
| Observed source path from Batch1 readiness check | `E:\MM\?????????(YOLO_?????)\1????\floating-objects-detect-web\other\model_train\detect\weights\yolo26n.pt` |
| Size | `5,544,453 bytes` |
| SHA256 | `9b09cc8bf347f0fc8a5f7657480587f25db09b34bf33b0652110fb03a8ad4fef` |
| Batch2 role | dev runtime baseline / backend smoke placeholder |
| Backend smoke allowed | Yes, read-only load only |
| Production precision claim allowed | No |

## Read-only Weight Verification Commands

PowerShell hash check:

```powershell
Get-FileHash -Algorithm SHA256 "other\model_train\detect\weights\yolo26n.pt"
```

PowerShell size/readability check:

```powershell
$item = Get-Item "other\model_train\detect\weights\yolo26n.pt"
[PSCustomObject]@{
  Path = $item.FullName
  SizeBytes = $item.Length
  Readable = $item.Exists
}
```

Python read-only check:

```powershell
python -c "import hashlib, pathlib; p=pathlib.Path('other/model_train/detect/weights/yolo26n.pt'); h=hashlib.sha256(); f=p.open('rb'); [h.update(c) for c in iter(lambda:f.read(1024*1024), b'')]; f.close(); print(p.resolve()); print(p.stat().st_size); print(h.hexdigest())"
```

Expected SHA256:

```text
9b09cc8bf347f0fc8a5f7657480587f25db09b34bf33b0652110fb03a8ad4fef
```

## Non-changing Contracts

These values are frozen for Phase 2B Batch2 Stage1 and must remain compatible with backend/frontend contracts:

| Contract | Required value / rule | Status |
|---|---|---|
| Class ID | `class_id=0` | unchanged |
| Class name | `class_name=floating_object` | unchanged |
| Detection result schema | `detection_result.v1` | unchanged |
| bbox output compatibility | keep existing bbox fields and formats compatible with backend smoke usage | unchanged |

## Explicit Prohibitions for This Stage

- Do not train a model.
- Do not validate the full dataset.
- Do not modify `yolo26n.pt` or any other weight file.
- Do not change class definitions, class IDs, or class names.
- Do not use this placeholder as evidence of production precision.
