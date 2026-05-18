# web-vue Phase 2B Batch1

## 范围

本前端仅覆盖 Phase 2B Batch1 最小可运行链路：

- Vue3 + Vite + Element Plus + Pinia + Vue Router 工程骨架
- 登录、JWT 本地保存、路由鉴权守卫
- 图片检测：选择已发布模型、上传单张图片、展示结果图与目标列表
- 检测记录：列表、详情、原始 JSON 折叠展示

暂不实现视频检测、实时检测、Word 报告、大屏可视化、训练/数据集/模型评估完整 UI；相关入口必须标注“Phase 2B 暂不开放”。

## 启动

```powershell
cd E:/MM/floating-worktrees/frontend-worktree/web-vue
npm install
npm run dev
```

构建验证：

```powershell
npm run build
```

## 环境变量

- `VITE_API_BASE_URL`：前端请求 API 的基础地址；为空时使用同源 `/api`。
- `VITE_DEV_PROXY_TARGET`：Vite dev server `/api` 代理目标，默认 `http://localhost:5000`。

## Batch1 对接接口

- `POST /api/user/login`
- `GET /api/user/current`
- `GET /api/detection/models/published`
- `POST /api/detection/detect`
- `GET /api/detection/records`
- `GET /api/detection/records/:id`
- 文件访问：优先使用响应中的 `url`；若仅返回 `bucket/object_key`，前端生成 `/api/file/:bucket/*object_key`。

响应兼容 `{ code, msg/message, data }` 包装；`code === 0` 或 `code === 200` 视为成功。

## 已知限制

- 必须有后端最小 API 服务与已发布模型，图片检测才可完成端到端 smoke。
- 构建可能出现 Element Plus/Vite chunk size 警告，不影响 Batch1 功能。
- 若后端契约继续调整，仅在 `src/api/` 与 `src/types/` 小范围同步，不进入 Batch2。
