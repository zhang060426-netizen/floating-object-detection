# Phase 2B Batch1 Frontend Task Record

## 必读输入读取记录

- [x] `AGENTS.md`
- [x] `PROJECT_CONTEXT.md`
- [x] `PHASE2B_PRE_DEV_FREEZE.md`
- [x] `PHASE2A_MASTER_SUMMARY.md`
- [x] `agent_outputs/frontend/FRONTEND_PAGE_MAP.md`
- [x] `agent_outputs/frontend/FRONTEND_CONTRACT_REVIEW.md`
- [x] `agent_outputs/frontend/FRONTEND_PHASE2B_GATE.md`
- [x] `agent_outputs/backend/API_CONTRACT.md`
- [x] `agent_outputs/backend/DETECTION_RESULT_SCHEMA.md`
- [x] `agent_outputs/backend/FILE_STORAGE_CONTRACT.md`
- [x] `agent_outputs/ai/AI_OUTPUT_SCHEMA.md`
- [x] `agent_outputs/docs/SMOKE_TEST_RESOURCE_MAP.md`

## 执行边界

- 仅写入 `web-vue/`。
- 未修改 `web-flask/`、`other/model_train/detect/`、`agent_outputs/backend/`、`agent_outputs/ai/`、数据库文件、模型权重或训练脚本。
- 视频检测、实时检测、Word 报告入口只提示“Phase 2B 暂不开放”。

## 验证记录

```powershell
cd E:/MM/floating-worktrees/frontend-worktree/web-vue
npm.cmd install
npm.cmd run build
```

结果：构建通过。Vite 输出大 chunk 警告，属于 Element Plus 全量引入下的体积提示，不影响本批次最小可运行验收。

## Local Integration Continuation - 2026-05-17

Scope kept to Phase 2B Batch1 local integration and image detection display smoke.

Changes:
- Aligned Batch1 endpoints with frozen contract:
  - `POST /api/user/login`
  - `GET /api/user/current`
  - `GET /api/detection/models/published`
  - `POST /api/detection/detect`
- Fixed file URL generation to `/api/file/{bucket}/{object_key}`.
- Added result image fallback from `detection_result.artifacts.result_image` / `result_image_url` for image detection display.
- Added detection record detail fallback for artifact image refs and paged record list variants.
- Refreshed `web-vue/README.md` with current Batch1 startup and endpoint notes.

Verification:
```powershell
cd E:/MM/floating-worktrees/frontend-worktree/web-vue
npm.cmd run build
```
Result: pass. Vite reports non-blocking Rollup pure-comment and chunk-size warnings from dependencies.

Local preview smoke:
```powershell
npm.cmd run preview -- --host 127.0.0.1 --port 4173
Invoke-WebRequest http://127.0.0.1:4173/
```
Result: HTTP 200 and root `#app` present.

Image detection display smoke checks:
- `/api/detection/detect` present in API client.
- `/api/detection/models/published` present in model API client.
- result panel consumes `artifacts.result_image` / `artifacts.result_image_url`.
- file refs resolve to `/api/file/`.

Full PASS still depends on live backend/API smoke with an actual published model and sample image.
