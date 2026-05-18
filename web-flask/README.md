# Phase 2B minimal Flask backend

Provides the Batch1 minimum backend for login, model listing, image detection boundary, file storage, and detection records.

## Start

```powershell
cd E:/MM/floating-worktrees/backend-worktree/web-flask
python app.py
```

Default API base: `http://localhost:5000/api`.

Default accounts:

- `admin` / `admin123` (also accepts legacy `123456`)
- `test` / `123456`

## Config

Environment variables:

- `APP_SECRET_KEY` / `JWT_SECRET`
- `APP_DB_PATH` (default `storage/app.sqlite3`)
- `APP_STORAGE_ROOT` (default `storage`)
- `APP_UPLOAD_MAX_MB` (default `16`)
- `AI_MODEL_ROOT` (optional, defaults to project AI weights directory when discoverable)


## Runtime diagnostics

Health checks:

- `GET /api/health` returns the minimal service liveness payload.
- `GET /api/health/db` verifies the SQLite connection with `SELECT 1`.

`GET /api/models/published` keeps the original model fields and adds `runtime_diagnostic` for Phase 2B Batch2 Stage1 readiness checks:

- `ultralytics_import_status` / `ultralytics_importable` / `ultralytics_version` / `ultralytics_error`
- `active_weight_path`
- `weight_exists`
- `weight_sha256` (`null` when the weight is missing)
- `is_dev_placeholder`

The top-level `weight_exists` and `is_dev_placeholder` fields remain available for backward compatibility.

## Image detection error contract

`POST /api/detection/image` does not fake inference success. Runtime failures return structured `data.reason` values:

- `dependency_unavailable` when `ultralytics` cannot be loaded.
- `weight_missing` when the selected model weight path is not readable.
- `invalid_image` when the uploaded file cannot be opened as an image.
- `unsupported_image_type` when the uploaded filename extension is outside `.jpg`, `.jpeg`, `.png`, `.webp`.

`confidence_threshold` must be numeric and between `0` and `1` for both image detection and manual record creation.

Successful requests return `detection_status` as either `detected` or `no_detection`. The same status is also present at `detection_result.summary.detection_status`; both outcomes may still save a detection record when `save_record=true`.

## Verification

```powershell
python -m compileall .
python -m pytest
```

Real YOLO inference requires `ultralytics` and a readable model weight. If unavailable, `/api/detection/image` returns a diagnostic error and does not create a fake successful record.
