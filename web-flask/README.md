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

## Verification

```powershell
python -m compileall .
python -m pytest
```

Real YOLO inference requires `ultralytics` and a readable model weight. If unavailable, `/api/detection/image` returns a diagnostic error and does not create a fake successful record.
