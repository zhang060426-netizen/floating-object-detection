# Phase 2B Batch3 Backend Docker Deployment

This deployment keeps application runtime state outside the image. The integrated root-level compose file runs both backend and frontend on the shared `floating-net` network.

## Runtime volumes

- SQLite host bind: `./runtime/db:/app/runtime/db`
- Models host bind: `./runtime/models:/app/runtime/models:ro`
- Uploads host bind: `./runtime/uploads:/app/runtime/uploads`
- Detection results host bind: `./runtime/results:/app/runtime/results`

The backend default weight path inside the container is:

```text
/app/runtime/models/yolo26n.pt
```

Do not bake model weights, uploads, results, or SQLite files into the image.

## Build

From repository root:

```powershell
New-Item -ItemType Directory -Force -Path runtime/db,runtime/models,runtime/uploads,runtime/results | Out-Null
docker build -f Dockerfile.backend -t floating-backend:phase2b-batch3 .
```

## Run with Docker

```powershell
New-Item -ItemType Directory -Force -Path runtime/db,runtime/models,runtime/uploads,runtime/results | Out-Null

docker run --rm --name floating-backend `
  -p 5000:5000 `
  -e APP_SECRET_KEY=change-me `
  -e JWT_SECRET=change-me `
  -e APP_DB_PATH=/app/runtime/db/app.sqlite3 `
  -e APP_STORAGE_ROOT=/app/runtime `
  -e AI_MODEL_ROOT=/app/runtime/models `
  -v ${PWD}/runtime/db:/app/runtime/db `
  -v ${PWD}/runtime/models:/app/runtime/models:ro `
  -v ${PWD}/runtime/uploads:/app/runtime/uploads `
  -v ${PWD}/runtime/results:/app/runtime/results `
  floating-backend:phase2b-batch3
```

## Run with Compose

```powershell
New-Item -ItemType Directory -Force -Path runtime/db,runtime/models,runtime/uploads,runtime/results | Out-Null
docker compose config
docker compose up --build -d backend frontend
docker compose ps
```

When validating from a backend-only worktree before frontend files are merged into the same repository root, point Compose at the frontend worktree without changing the final root-level defaults:

```powershell
$env:FRONTEND_BUILD_CONTEXT="E:/MM/floating-worktrees/frontend-worktree"
docker compose build backend frontend
docker compose up -d backend frontend
```

## Smoke checks

```powershell
curl http://localhost:5000/api/health
curl http://localhost:5000/api/health/db
```

Expected: both endpoints return `code=0`; `/api/health/db` confirms SQLite access.

## Model weights

Copy `yolo26n.pt` into `runtime/models/yolo26n.pt` when real inference is required. Expected Phase 2B Batch3 smoke SHA256:

```text
9B09CC8BF347F0FC8A5F7657480587F25DB09B34BF33B0652110FB03A8AD4FEF
```

If the weight or `ultralytics` runtime is unavailable, image detection must return the existing diagnostic error contract instead of fake success.

## Rollback

```powershell
docker compose down
git checkout phase2b-batch2-image-detection-stable -- web-flask/README.md
Remove-Item Dockerfile.backend,Dockerfile.frontend,.dockerignore,docker-compose.yml,web-flask/DEPLOYMENT.md,web-flask/.env.example -Force
Remove-Item deploy/nginx/default.conf.template -Force
```

If you also need to remove Batch3 runtime bind-mount state, remove only generated DB/uploads/results. Do not delete model weights unless explicitly intended:

```powershell
Remove-Item runtime/db,runtime/uploads,runtime/results -Recurse -Force
```
