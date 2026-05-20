# web-vue Deployment: Phase 2B Batch3 Frontend Docker

## Scope

This deployment layer only packages the existing Vue frontend and nginx proxy configuration. It does not add pages, change backend business logic, change model weights, or alter the `detection_result.v1` consumer contract.

## Architecture

```text
browser -> frontend nginx :80 -> /api proxy -> backend:5000 on docker compose network
browser -> frontend nginx :80 -> Vue static assets / SPA fallback
```

Build-time frontend API base is `/api`, so browser requests stay same-origin. Runtime backend routing is controlled by nginx `BACKEND_UPSTREAM` and defaults to `http://backend:5000`.

## Commands

Run from repository root unless noted.

```powershell
cd web-vue
npm.cmd run build
cd ..

docker build -f Dockerfile.frontend -t floating-objects-frontend:phase2b-batch3 .
docker compose config
docker compose up -d frontend
```

If backend compose is managed in another worktree/file, combine compose files or copy the frontend service into the integrated compose file:

```powershell
docker compose -f docker-compose.backend.yml -f docker-compose.yml up -d backend frontend
```

## Environment variables

| Variable | Stage | Default | Purpose |
| --- | --- | --- | --- |
| `VITE_API_BASE_URL` | build | `/api` | Browser-facing API prefix compiled into the Vue bundle. |
| `VITE_DEV_PROXY_TARGET` | dev only | `http://localhost:5000` | Vite dev server `/api` proxy target. |
| `BACKEND_UPSTREAM` | runtime | `http://backend:5000` | nginx upstream inside compose network. |

See `.env.docker.example`.

## Verification checklist

1. `npm.cmd run build` succeeds in `web-vue`.
2. `docker compose config` renders a valid frontend service and `floating-net` network.
3. Docker daemon available: `docker build -f Dockerfile.frontend -t floating-objects-frontend:phase2b-batch3 .` succeeds.
4. Backend service is running on the same compose network as service name `backend`.
5. Open `http://localhost:8080`, log in, and verify image detection API requests are sent to `/api/...` and proxied to backend.

## Rollback

```powershell
git checkout -- Dockerfile.frontend docker-compose.yml .dockerignore deploy/nginx/default.conf.template web-vue/.env.docker.example web-vue/README.md web-vue/DEPLOYMENT.md
```

For untracked files, delete the Batch3 Docker files manually. Do not delete `node_modules`, `dist`, `.vite`, model weights, uploads, or backend files as part of this rollback.
