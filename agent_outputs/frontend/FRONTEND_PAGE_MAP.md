# Frontend Page Map

更新时间：2026-05-13
角色：Frontend Agent
阶段：Phase 2A：系统契约与重建基线
范围：仅基于文档与当前可见资源建立前端页面、路由、API、状态和共享契约候选地图；不写业务代码。

## 1. 范围与边界

本文件只写入 `agent_outputs/frontend/` 下的文档交付物。

禁止事项：

- 不创建 `web-vue/src/`。
- 不创建 `views/`、`router/`、`api/`、`stores/`、`types/`、`utils/` 等源码目录。
- 不实现 Vue 页面、组件、路由、状态管理或 API 封装。
- 不修改后端、数据库、AI 模型逻辑或模型权重。
- 不将文档推断声明为源码事实。

证据等级说明：

| 证据等级 | 含义 |
|---|---|
| 已源码确认 | 有明确源码文件证据。当前前端业务源码缺失，因此本文件没有页面/路由/API/store/type 属于此等级。 |
| 已资源确认 | 有 `package.json`、说明文件、测试资源、配置文件等非业务源码证据。 |
| 文档推断 | 来自 README、系统文档、规划文档，但当前没有源码证据。 |
| 待源码确认 | 必须等 `web-vue/src` 补齐后才能确认。 |
| 冲突/差异 | 文档与当前可见文件存在明确不一致。 |

## 2. 已确认事实

| 项目 | 结论 | 证据等级 |
|---|---|---|
| 前端实际路径 | `1项目代码/floating-objects-detect-web/web-vue/` 存在 | 已资源确认 |
| 当前可见文件 | 仅发现 `package.json`、`2须知.txt` | 已资源确认 |
| 前端依赖意图 | Vue、Vue Router、Pinia、Axios、Element Plus、ECharts、Vite、TypeScript | 已资源确认 |
| `src/` | 当前不存在 | 冲突/差异 |
| `src/router/` | 当前不存在 | 冲突/差异 |
| `src/api/` | 当前不存在 | 冲突/差异 |
| `src/views/` | 当前不存在 | 冲突/差异 |
| `src/components/` | 当前不存在 | 冲突/差异 |
| `src/stores/` | 当前不存在 | 冲突/差异 |
| `src/types/` | 当前不存在 | 冲突/差异 |
| `src/utils/` | 当前不存在 | 冲突/差异 |
| `index.html` | 当前不存在 | 冲突/差异 |
| `vite.config.ts` | 当前不存在 | 冲突/差异 |
| `src/main.ts` | 当前不存在 | 冲突/差异 |
| 可运行前端基线 | 当前无法确认 | 待源码确认 |

## 3. 文档推断的页面清单

| 页面/模块 | 候选页面 | 功能说明 | 证据等级 |
|---|---|---|---|
| 登录 | Login | 用户登录，获取 JWT token | 文档推断 |
| 注册 | Register | 新用户注册 | 文档推断 |
| 个人中心 | Profile | 当前用户信息、头像、密码修改 | 文档推断 |
| 用户首页 | User Dashboard | 普通用户首页或检测入口 | 文档推断 |
| 管理控制台 | Admin Dashboard | 管理端入口与概览 | 文档推断 |
| 用户管理 | User Management | 用户分页、启用/禁用、重置密码、删除 | 文档推断 |
| 图片检测 | Image Detection | 图片上传、模型选择、检测、增强、AI 分析、治理建议、报告导出 | 文档推断 |
| 图片检测记录 | Image Detection Records | 图片检测历史、详情、裁剪图、编辑、删除 | 文档推断 |
| 视频检测 | Video Detection | 视频上传、异步任务创建、进度轮询 | 文档推断 |
| 视频检测记录 | Video Detection Records | 视频记录列表、详情、结果视频、关键帧、删除 | 文档推断 |
| 实时检测 | Realtime Detection | 本地 USB 摄像头检测、Base64 帧上传、实时结果展示 | 文档推断 |
| 实时检测记录 | Realtime Detection Records | 实时会话列表、实时检测记录、会话删除 | 文档推断 |
| 数据集管理 | Dataset Management | ZIP 上传、验证状态、列表、详情、下载、删除 | 文档推断 |
| 模型管理 | Model Management | 模型创建、权重上传、训练文件、发布/取消发布、导出 | 文档推断 |
| 模型评估 | Evaluation | 上传图片与标签、预测、指标、对比图、评分、记录筛选 | 文档推断 |
| 文件访问/预览 | File Preview | 图片、视频、报告、模型训练文件访问 | 文档推断 |

## 4. 文档推断的路由清单

当前未发现 `src/router`，以下路由均为候选。

| 候选路由 | 页面/模块 | 权限候选 | 证据等级 |
|---|---|---|---|
| `/login` | 登录 | 公开 | 文档推断 |
| `/register` | 注册 | 公开 | 文档推断 |
| `/profile` | 个人中心 | 登录 | 文档推断 |
| `/dashboard` | 用户首页 | 登录 | 文档推断 |
| `/admin` 或 `/admin/dashboard` | 管理控制台 | 管理员 | 文档推断 |
| `/admin/users` | 用户管理 | 管理员 | 文档推断 |
| `/detection` | 图片检测 | 登录 | 文档推断 |
| `/detection/records` | 图片检测记录 | 登录 | 文档推断 |
| `/detection/records/:id` | 图片检测详情 | 登录 | 文档推断 |
| `/video-detection` | 视频检测 | 登录 | 文档推断 |
| `/video-detection/records` | 视频检测记录 | 登录 | 文档推断 |
| `/video-detection/records/:id` | 视频检测详情 | 登录 | 文档推断 |
| `/realtime-detection` | 实时检测 | 登录 | 文档推断 |
| `/realtime-detection/records` | 实时检测记录 | 登录 | 文档推断 |
| `/admin/datasets` | 数据集管理 | 管理员 | 文档推断 |
| `/admin/models` | 模型管理 | 管理员 | 文档推断 |
| `/evaluation` | 模型评估 | 管理员 | 文档推断 |
| `/evaluation/records` | 评估记录 | 管理员 | 文档推断 |

待源码确认：

- 实际路径命名、嵌套路由、默认重定向、404 页面、路由 meta 字段、权限守卫实现。

## 5. 页面-API 依赖候选矩阵

当前未发现 `src/api`，以下 API 均为候选消费关系。

| 页面/模块 | API 组 | 候选接口 | 前端消费目的 | 证据等级 |
|---|---|---|---|---|
| 登录 | `/api/user` | `POST /login` | 获取 token、初始化登录态 | 文档推断 |
| 注册 | `/api/user` | `POST /register` | 创建普通用户 | 文档推断 |
| 个人中心 | `/api/user` | `GET /current`, `PUT /`, `POST /password`, `POST /logout` | 用户信息展示、修改资料、改密、退出 | 文档推断 |
| 用户管理 | `/api/user` | `GET /page`, `POST /`, `GET /:id`, `DELETE /:id`, `PUT /:id/reset-password`, `PUT /:id/status` | 管理员用户维护 | 文档推断 |
| 图片检测 | `/api/detection` | `GET /models/published`, `POST /detect`, `POST /enhance-image`, `POST /analyze-defects`, `POST /generate-suggestions`, `POST /save`, `POST /export-word` | 检测主流程和报告导出 | 文档推断 |
| 图片检测记录 | `/api/detection` | `GET /records`, `GET /records/:id`, `GET /records/:id/crops`, `PUT /records/:id`, `DELETE /records/:id` | 历史记录和裁剪图展示 | 文档推断 |
| 视频检测 | `/api/video-detection` | `POST /detect`, `GET /progress/:id` | 创建视频任务、轮询进度 | 文档推断 |
| 视频检测记录 | `/api/video-detection` | `GET /records`, `GET /records/:id`, `PUT /records/:id`, `DELETE /records/:id` | 视频任务历史和详情 | 文档推断 |
| 实时检测 | `/api/realtime-detection` | `POST /detect`, `POST /reset-tracker` | 上传 Base64 帧、重置 tracker | 文档推断 |
| 实时检测记录 | `/api/realtime-detection` | `GET /sessions`, `GET /records`, `DELETE /sessions/:session_id`, `DELETE /records/:id` | 会话和记录管理 | 文档推断 |
| 数据集管理 | `/api/dataset` | `POST /upload`, `GET /list`, `GET /:id`, `PUT /:id`, `DELETE /:id`, `GET /:id/download` | 数据集上传、状态、下载、删除 | 文档推断 |
| 模型管理 | `/api/model` | `POST /create`, `GET /list`, `GET /datasets`, `GET /base-models`, `GET /classes`, `GET /:id`, `PUT /:id`, `DELETE /:id`, `POST /:id/upload-weight`, `GET /:id/export`, `POST /:id/publish`, `POST /:id/unpublish`, `POST /:id/train-images`, `POST /:id/train-files`, `GET /:id/train-files/:index/chart-data` | 模型生命周期、训练产物、发布状态 | 文档推断 |
| 模型评估 | `/api/evaluation` | `GET /box-config`, `POST /predict`, `POST /save`, `GET /evaluated-models`, `GET /records`, `GET /records/:id`, `DELETE /records/:id` | 评估预测、指标展示、记录管理 | 文档推断 |
| 文件预览/下载 | 待确认 | 静态文件 URL 或文件接口 | 展示图片、视频、裁剪图、报告下载 | 待源码确认 |

## 6. 页面-状态管理候选关系

当前未发现 `src/stores`。以下 store 均为候选，不得视作已实现。

| Store 候选 | 关联页面 | 候选状态/动作 | 证据等级 |
|---|---|---|---|
| `user` | 登录、注册、个人中心、所有鉴权页面 | token、user_id、role、用户信息、登录、退出、刷新当前用户 | 文档推断 |
| `permission` 或路由 meta | 管理页面、普通用户页面 | 角色判断、管理员菜单、路由守卫 | 文档推断 |
| `model` | 图片检测、视频检测、实时检测、模型管理、评估 | 已发布模型列表、模型状态、基础模型、类别配置 | 文档推断 |
| `detection` | 图片检测、检测记录 | 当前检测结果、结果图、裁剪图、AI 分析、治理建议、导出状态 | 文档推断 |
| `videoDetection` | 视频检测、视频记录 | task_id、progress、status、轮询状态、结果视频、关键帧 | 文档推断 |
| `realtimeDetection` | 实时检测、实时记录 | 摄像头状态、会话 ID、检测统计、tracker reset 状态 | 文档推断 |
| `dataset` | 数据集管理 | 数据集列表、验证状态、结构统计 | 文档推断 |
| `evaluation` | 模型评估、评估记录 | GT/预测结果、metrics、评分、筛选条件 | 文档推断 |
| `ui` | 全局布局、请求交互 | loading、错误提示、菜单折叠、主题 | 文档推断 |

## 7. 页面-共享契约依赖

| 页面/模块 | 依赖共享契约 | 前端关注点 | 证据等级 |
|---|---|---|---|
| 登录/注册/个人中心 | API_CONTRACT、JWT 字段、DB user 字段 | token、role、status、当前用户资料、错误格式 | 文档推断 |
| 用户管理 | API_CONTRACT、DB user 字段 | 分页结构、角色/状态枚举、头像文件访问 | 文档推断 |
| 图片检测 | API_CONTRACT、DETECTION_RESULT_SCHEMA、AI_OUTPUT_SCHEMA、FILE_STORAGE_CONTRACT | 检测框、置信度、结果图、增强图、裁剪图、AI 分析、报告下载 | 文档推断 |
| 图片检测记录 | DB_CONTRACT、DETECTION_RESULT_SCHEMA、FILE_STORAGE_CONTRACT | 记录字段、裁剪图列表、文件 URL、编辑/删除权限 | 文档推断 |
| 视频检测 | API_CONTRACT、DETECTION_RESULT_SCHEMA、FILE_STORAGE_CONTRACT、视频状态机 | task_id、progress、status、结果视频、关键帧 | 文档推断 |
| 实时检测 | API_CONTRACT、DETECTION_RESULT_SCHEMA、FILE_STORAGE_CONTRACT | Base64 帧、结果图、新目标、会话统计 | 文档推断 |
| 数据集管理 | API_CONTRACT、DB datasets 字段、FILE_STORAGE_CONTRACT | ZIP 上传、验证状态、结构统计、下载权限 | 文档推断 |
| 模型管理 | API_CONTRACT、DB models 字段、FILE_STORAGE_CONTRACT、AI_OUTPUT_SCHEMA | 模型状态、发布状态、权重文件、训练图表、类别配置 | 文档推断 |
| 模型评估 | API_CONTRACT、DETECTION_RESULT_SCHEMA、evaluation metrics、FILE_STORAGE_CONTRACT | GT/预测框对比、指标、评分、对比图 | 文档推断 |

## 8. 待源码确认项

| 待确认项 | 当前阻塞原因 | 证据等级 |
|---|---|---|
| 实际页面文件名和目录结构 | `src/views` 缺失 | 待源码确认 |
| 实际路由表 | `src/router` 缺失 | 待源码确认 |
| 实际 API 封装文件和函数名 | `src/api` 缺失 | 待源码确认 |
| 实际 request 封装 | `src/api/request.ts` 缺失 | 待源码确认 |
| token 保存位置 | store/localStorage/sessionStorage 源码缺失 | 待源码确认 |
| 401/403 处理 | request 拦截器源码缺失 | 待源码确认 |
| 管理员菜单/权限控制 | route meta 和 store 缺失 | 待源码确认 |
| 检测结果渲染模型 | 页面和类型定义缺失 | 待源码确认 |
| 图片/视频/实时结果是否共用组件 | components 缺失 | 待源码确认 |
| 文件 URL 生成方式 | 前端与后端文件访问实现均缺失 | 待源码确认 |
| ECharts 使用位置 | 页面源码缺失 | 待源码确认 |
| UI 风格和组件复用 | 页面源码和截图缺失 | 待源码确认 |

## 9. Phase 2B 前端重建优先级

以下为进入代码重建阶段后的优先级建议；当前 Phase 2A 不执行。

| 优先级 | 任务 | 说明 | 证据等级 |
|---:|---|---|---|
| P0 | 恢复/确认最小前端入口 | `index.html`、`vite.config.*`、`src/main.*` | 待源码确认 |
| P0 | 恢复/确认路由和请求封装 | `src/router`、`src/api/request.*` | 待源码确认 |
| P0 | 恢复/确认用户登录链路 | 登录、token、当前用户、权限守卫 | 待源码确认 |
| P0 | 建立源码确认版页面-API 矩阵 | 用真实 router/views/api 复核本文档 | 待源码确认 |
| P1 | 图片检测最小页面 | 模型选择、上传、检测结果、报告导出 | 待源码确认 |
| P1 | 图片检测记录页面 | 列表、详情、裁剪图、删除 | 待源码确认 |
| P1 | 模型选择与模型状态展示 | 仅使用已发布模型 | 文档推断 |
| P1 | 管理员数据集/模型/评估页面 | 管理权限、上传、状态展示、指标 | 文档推断 |
| P2 | 视频检测与实时检测页面 | 依赖后端任务状态机和实时接口确认 | 待源码确认 |
| P2 | UI 统一与组件化 | 基于真实页面截图和源码执行 | 待源码确认 |

## 10. 风险与影响

| 风险 | 影响 | 证据等级 |
|---|---|---|
| 文档描述完整前端，但当前没有 `src/` | 任何页面/路由/API/store/type 都不能声明为已实现 | 冲突/差异 |
| 直接按文档实现页面 | 可能重复造轮子，且与真实后端契约不兼容 | 文档推断 |
| API_CONTRACT 尚未由 Backend 最终输出 | 前端无法冻结请求/响应解析 | 待源码确认 |
| DETECTION_RESULT_SCHEMA 尚未由 Backend+AI 最终输出 | 检测结果组件不能进入实现 | 待源码确认 |
| AI_OUTPUT_SCHEMA 尚未由 AI+Backend 最终输出 | AI 分析展示字段不能冻结 | 待源码确认 |
| FILE_STORAGE_CONTRACT 尚未确认 | 图片、视频、裁剪图、报告 URL 无法确定 | 待源码确认 |
| DB_CONTRACT 尚未源码核对 | 前端列表字段、筛选字段、枚举值可能变化 | 待源码确认 |
| 实时检测依赖本地 USB 摄像头 | Phase 2B 测试需环境条件，不能仅靠文件系统验证 | 文档推断 |
