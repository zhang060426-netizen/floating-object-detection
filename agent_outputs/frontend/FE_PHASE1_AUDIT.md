# Frontend Phase 1 Audit

更新时间：2026-05-13
角色：Frontend Agent
阶段：Phase 1：源码结构确认与差异审计
范围：`1项目代码/floating-objects-detect-web/web-vue/`

## 1. 已确认事实

当前 `web-vue` 实际目录结构如下：

```text
1项目代码/floating-objects-detect-web/web-vue/
├─ package.json
└─ 2须知.txt
```

已确认：

- `web-vue/package.json` 存在。
- `web-vue/2须知.txt` 存在。
- `src/` 不存在。
- `src/router/` 不存在。
- `src/api/` 不存在。
- `src/views/` 不存在。
- `src/components/` 不存在。
- `src/stores/` 不存在。
- `src/types/` 不存在。
- `src/utils/` 不存在。
- 当前未发现 `index.html`、`vite.config.ts`、`src/main.ts` 等可运行前端入口文件。

`package.json` 已确认的技术栈/依赖包括：

- Vue 3.5.13
- Vue Router 4.5.0
- Pinia 2.3.1
- Axios 1.7.9
- Element Plus 2.9.4
- ECharts 5.6.0
- Vite 6.1.0
- TypeScript 5.7.2

## 2. 文档推断

以下内容来自根目录规划文档、`3项目文档/1系统介绍文档.md`、`web-vue/2须知.txt`，当前不是源码事实。

预期前端功能模块包括：

- 用户登录、注册、个人中心、用户管理。
- 图片检测：模型选择、图片上传、YOLO 检测、CLAHE 增强、Qwen-VL 分析、治理建议、Word 报告导出、检测记录管理。
- 视频检测：视频上传、异步任务创建、进度轮询、关键帧/结果视频展示、记录管理。
- 实时检测：本地 USB 摄像头帧检测、ByteTrack 跟踪、会话管理、实时记录管理。
- 数据集管理：ZIP 上传、数据集列表、详情、下载、删除。
- 模型管理：模型创建、权重上传、发布/取消发布、训练文件/曲线展示。
- 模型评估：上传图片与标签、预测、指标计算、评分、记录筛选。

文档预期的前端源码结构包括：

```text
src/
├─ api/
│  ├─ detection.ts
│  ├─ video_detection.ts
│  ├─ realtime_detection.ts
│  ├─ model.ts
│  ├─ dataset.ts
│  ├─ user.ts
│  ├─ file_request.ts
│  └─ request.ts
├─ components/
├─ views/
├─ stores/
├─ types/
├─ utils/
└─ router/
```

文档推断的页面-路由-API 关系：

| 页面/模块 | 推断前端路由 | 推断 API 模块 | 主要接口 |
|---|---|---|---|
| 登录 | `/login` | `user.ts` | `POST /api/user/login` |
| 注册 | `/register` | `user.ts` | `POST /api/user/register` |
| 个人中心 | `/profile` | `user.ts` | `GET /api/user/current`, `PUT /api/user`, `POST /api/user/password` |
| 用户管理 | `/admin/users` | `user.ts` | `GET /api/user/page`, `POST /api/user`, `GET /api/user/:id`, `DELETE /api/user/:id`, `PUT /api/user/:id/reset-password`, `PUT /api/user/:id/status` |
| 图片检测 | `/detection` | `detection.ts` | `GET /api/detection/models/published`, `POST /api/detection/detect`, `POST /api/detection/enhance-image`, `POST /api/detection/analyze-defects`, `POST /api/detection/generate-suggestions`, `POST /api/detection/save`, `POST /api/detection/export-word` |
| 图片检测记录 | `/detection/records` | `detection.ts` | `GET /api/detection/records`, `GET /api/detection/records/:id`, `GET /api/detection/records/:id/crops`, `PUT /api/detection/records/:id`, `DELETE /api/detection/records/:id` |
| 视频检测 | `/video-detection` | `video_detection.ts` | `POST /api/video-detection/detect`, `GET /api/video-detection/progress/:id` |
| 视频检测记录 | `/video-detection/records` | `video_detection.ts` | `GET /api/video-detection/records`, `GET /api/video-detection/records/:id`, `PUT /api/video-detection/records/:id`, `DELETE /api/video-detection/records/:id` |
| 实时检测 | `/realtime-detection` | `realtime_detection.ts` | `POST /api/realtime-detection/detect`, `POST /api/realtime-detection/reset-tracker` |
| 实时检测记录 | `/realtime-detection/records` | `realtime_detection.ts` | `GET /api/realtime-detection/sessions`, `GET /api/realtime-detection/records`, `DELETE /api/realtime-detection/sessions/:session_id`, `DELETE /api/realtime-detection/records/:id` |
| 数据集管理 | `/admin/datasets` | `dataset.ts` | `POST /api/dataset/upload`, `GET /api/dataset/list`, `GET /api/dataset/:id`, `PUT /api/dataset/:id`, `DELETE /api/dataset/:id`, `GET /api/dataset/:id/download` |
| 模型管理 | `/admin/models` | `model.ts` | `POST /api/model/create`, `GET /api/model/list`, `GET /api/model/datasets`, `GET /api/model/base-models`, `GET /api/model/classes`, `GET /api/model/:id`, `PUT /api/model/:id`, `DELETE /api/model/:id`, `POST /api/model/:id/upload-weight`, `POST /api/model/:id/publish`, `POST /api/model/:id/unpublish` |
| 模型评估 | `/evaluation` | `evaluation.ts` 或待确认 | `GET /api/evaluation/box-config`, `POST /api/evaluation/predict`, `POST /api/evaluation/save`, `GET /api/evaluation/evaluated-models`, `GET /api/evaluation/records`, `GET /api/evaluation/records/:id`, `DELETE /api/evaluation/records/:id` |

## 3. 待源码确认

以下内容必须等待完整 `web-vue/src/` 补齐后复核：

- 实际路由表、路由路径、路由名称、路由守卫。
- 实际页面文件列表、页面目录分层、页面与业务模块对应关系。
- 实际 API 封装文件、函数名、请求路径、入参、返回值解析方式。
- Axios 请求封装、baseURL、token 注入、401/403 处理、错误提示策略。
- Pinia store 结构，尤其是用户登录态、权限、菜单、token、用户信息。
- TypeScript 类型定义，包括 API response、检测结果、模型、数据集、评估记录等。
- 公共组件拆分，例如布局、分页、上传、检测结果展示、图表组件。
- UI 实际风格、Element Plus 主题、表格/表单/状态标签一致性。
- 图片/视频/实时检测结果展示是否复用同一数据模型。
- 模型评估页面是否存在 ECharts 可视化与评分筛选。

## 4. 缺失项

当前前端缺失项：

- 缺少完整 `src/` 源码目录。
- 缺少 `router` 路由配置。
- 缺少 `api` 请求封装。
- 缺少 `views` 页面源码。
- 缺少 `components` 公共组件。
- 缺少 `stores` 状态管理。
- 缺少 `types` 类型定义。
- 缺少 `utils` 工具函数。
- 缺少 `vite.config.ts`。
- 缺少 `index.html`。
- 缺少 `src/main.ts` 或等价入口。
- 缺少可运行前端基线。
- 缺少源码级页面-路由-API 调用矩阵。

## 5. 风险点

- 文档描述了完整前端系统，但当前可见目录没有源码，不能把文档预期当作源码事实。
- 当前无法运行、构建或截图验证前端。
- 当前无法确认 API 调用是否与后端接口文档一致。
- 当前无法确认权限控制、路由守卫、token 失效处理是否存在。
- 当前无法确认检测结果、`detection_result`、AI 分析字段、评估指标格式在前端的真实解析方式。
- 当前无法确认 UI 风格问题，因为没有页面源码或截图可审计。
- 若直接进入 Phase 2/Phase 3 功能优化，会造成基于假设开发，存在较高返工风险。

## 6. Phase 2 建议任务

建议在补齐完整 `web-vue` 源码后执行以下任务：

1. 重新执行 FE-1：生成真实前端目录地图。
2. 执行 FE-2：基于 `src/router`、`views`、`api` 生成源码确认版页面-路由-API 调用矩阵。
3. 建立前端 API 契约清单：请求路径、方法、入参、返回结构、错误格式、权限要求。
4. 对齐统一请求封装：Axios baseURL、token 注入、401/403 处理、统一错误提示、loading 策略。
5. 梳理权限与菜单：管理员/普通用户页面可见性、路由守卫、用户状态 store。
6. 设计统一检测结果展示模型：图片/视频/实时检测共用字段、目标框、置信度、裁剪图、AI 分析、报告下载。
7. 建立 UI 规范初稿：Element Plus 表格、表单、状态标签、上传控件、结果展示、ECharts 指标图。
8. 与 Backend/AI/Docs 对齐共享契约：API 响应结构、`detection_result` JSON、文件路径、JWT 字段、evaluation metrics、Qwen-VL 分析字段。

## 7. 本次审计边界

- 未修改业务代码。
- 未补写缺失源码。
- 未修改后端、数据库或 AI 模型逻辑。
- 未运行前端构建，因为当前缺少可运行前端入口。
