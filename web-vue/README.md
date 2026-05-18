# web-vue Phase 2B Batch2 Stage2

## Scope

Stage2 is limited to the image-detection minimum loop:

- login through the Flask smoke backend
- load published model list
- upload one image and run detection
- display model name, detection count, `detected` / `no_detection`, dev-placeholder warning, and backend reason
- load original/result images through `AuthImage` with JWT header support
- inspect detection record detail with JSON, model, confidence threshold, and detections summary

Out of scope: video, realtime, Word reports, dashboard/big-screen, backend changes, model weights, and Batch3 features.

## Start

```powershell
cd E:/MM/floating-worktrees/frontend-worktree/web-vue
npm.cmd install
npm.cmd run dev
```

Build:

```powershell
npm.cmd run build
```

## Environment

- `VITE_API_BASE_URL`: optional absolute API base. Leave empty when using the Vite dev proxy.
- `VITE_DEV_PROXY_TARGET`: Vite `/api` proxy target, default `http://localhost:5000`.

## Stage2 API contract used by frontend

- `POST /api/auth/login`
- `GET /api/auth/me`
- `GET /api/models/published`
- `POST /api/detection/image`
- `GET /api/detection/records`
- `GET /api/detection/records/:id`
- Authenticated image files under `/api/files/{bucket}/{object_key}` or direct `url` fields.

Responses may be wrapped as `{ code, message/msg, data }`; `code === 0` and `code === 200` are treated as success.

## Reproducible smoke checklist

1. Start backend smoke service at `http://127.0.0.1:5000`.
2. Start frontend dev server at `http://127.0.0.1:5173`.
3. Login with the Stage2 smoke account: `admin / admin123`.
4. Open `/detect/image`.
5. Confirm model list loads and model name is visible.
6. Upload one image and run detection.
7. Confirm the result panel shows:
   - model name
   - detection status (`detected` or `no_detection`)
   - detection count
   - confidence threshold
   - dev-placeholder warning when returned by backend
   - backend reason when returned by backend
8. Confirm original/result images load through `AuthImage` with the JWT `Authorization` header.
9. Open `/records/detection` and then `/records/detection/:id`.
10. Confirm record detail shows original/result image, model, confidence, detections summary, and `detection_result JSON`.
11. Error branch smoke: upload a non-image file or use an unavailable backend/model and confirm the error alert is readable.

## Notes

- Stage2 preserves `detection_result.v1` compatibility and only adds tolerant fallback fields for known backend variants.
- `AuthImage` creates blob URLs for authenticated images and revokes the previous object URL on source change/unmount.
- Build may show non-blocking Vite chunk-size warnings because Element Plus is bundled in the minimal app.
