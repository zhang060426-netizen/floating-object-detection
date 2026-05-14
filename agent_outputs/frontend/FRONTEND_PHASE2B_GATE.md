# Frontend Phase 2B Gate

更新时间：2026-05-13
角色：Frontend Agent
阶段：Phase 2A：系统契约与重建基线
用途：定义前端进入 Phase 2B 最小代码重建/可运行基线前的门禁。

## 1. Phase 2B 前端进入条件

| 条件 | 判定标准 | 当前状态 | 证据等级 |
|---|---|---|---|
| 前端源码恢复策略明确 | 已确认是恢复原源码还是最小重建 | 未明确 | 待源码确认 |
| 独立 worktree 策略明确 | 若进入代码重建，必须使用独立前端工作线 | 规划文档已要求，当前未执行 | 文档推断 |
| API_CONTRACT 可用 | Backend 输出请求/响应/错误/权限契约 | 当前待输出 | 待源码确认 |
| DETECTION_RESULT_SCHEMA 可用 | Backend+AI 输出检测结果契约 | 当前待输出 | 待源码确认 |
| AI_OUTPUT_SCHEMA 可用 | AI 输出 YOLO/Qwen-VL/metrics 契约 | 当前待输出 | 待源码确认 |
| FILE_STORAGE_CONTRACT 可用 | Backend 输出文件访问契约 | 当前待输出 | 待源码确认 |
| 页面优先级明确 | 登录 -> 图片检测 -> 检测记录 -> 模型选择 -> 基础布局 | 已由 Phase 2A 计划提出 | 文档推断 |
| 禁止项未违反 | 未创建 `src/`、未写页面、未写 API 封装 | 当前未违反 | 已资源确认 |

## 2. 最小可运行前端门禁

以下门禁必须在 Phase 2B 执行前由 Leader 判定；当前不创建文件。

| 门禁项 | 最小要求 | 当前状态 | 证据等级 |
|---|---|---|---|
| `index.html` | 存在并能挂载前端应用 | 当前不存在 | 冲突/差异 |
| `vite.config.*` | 存在并明确 dev/build/proxy 策略 | 当前不存在 | 冲突/差异 |
| `src/main.*` | 注册 Vue、Router、Pinia、Element Plus | 当前不存在 | 冲突/差异 |
| `src/App.vue` | 存在根组件或布局入口 | 当前不存在 | 冲突/差异 |
| 依赖安装 | `package.json` 可作为依赖依据 | 当前只有依赖声明，未验证安装 | 已资源确认 |
| 构建脚本 | `dev`、`build`、`preview` 脚本存在 | `package.json` 已声明 | 已资源确认 |
| 开发服务 | 能启动 Vite dev server | 当前无法验证 | 待源码确认 |
| 生产构建 | 能执行前端 build | 当前无法验证 | 待源码确认 |

## 3. 最小页面门禁

| 页面 | 最小可验收行为 | 权限候选 | 当前状态 | 证据等级 |
|---|---|---|---|---|
| 登录 | 输入账号密码、提交、保存 token、跳转 | 公开 | 页面源码缺失 | 待源码确认 |
| 基础布局 | 展示菜单、用户信息、退出入口 | 登录 | 页面源码缺失 | 待源码确认 |
| 图片检测 | 选择已发布模型、上传图片、展示检测结果 | 登录 | 页面源码缺失 | 待源码确认 |
| 图片检测记录 | 列表、详情、裁剪图、报告入口 | 登录 | 页面源码缺失 | 待源码确认 |
| 模型选择 | 只展示已发布模型 | 登录 | 页面源码缺失 | 待源码确认 |
| 个人中心 | 当前用户信息展示和退出 | 登录 | 页面源码缺失 | 待源码确认 |
| 管理员入口 | 管理员页面对普通用户不可见 | 管理员 | 页面源码缺失 | 待源码确认 |

Phase 2B P1 后续页面：

| 页面 | 前置依赖 | 证据等级 |
|---|---|---|
| 视频检测 | 视频任务状态机、文件存储契约 | 待源码确认 |
| 实时检测 | 摄像头环境、实时接口、tracker 契约 | 待源码确认 |
| 数据集管理 | 数据集 API、文件上传契约、管理员权限 | 待源码确认 |
| 模型管理 | 模型状态、权重文件契约、管理员权限 | 待源码确认 |
| 模型评估 | evaluation metrics、评估文件上传契约 | 待源码确认 |

## 4. 最小 API 接入门禁

| API 接入项 | 最小要求 | 依赖契约 | 当前状态 | 证据等级 |
|---|---|---|---|---|
| 请求 baseURL | 明确后端地址和代理策略 | API_CONTRACT | 未确认 | 待源码确认 |
| 统一响应解析 | 明确 `code`、`msg`、`data` 或实际格式 | API_CONTRACT | 文档候选为 `{code,msg,data}` | 文档推断 |
| 错误响应解析 | 明确参数错误、鉴权失败、权限不足、服务异常 | API_CONTRACT | 未确认 | 待源码确认 |
| token 注入 | 明确 Header 格式 `Authorization: Bearer <token>` | API_CONTRACT/JWT | 文档推断 | 文档推断 |
| 登录接口 | `POST /api/user/login` | API_CONTRACT | 文档推断 | 文档推断 |
| 当前用户接口 | `GET /api/user/current` | API_CONTRACT | 文档推断 | 文档推断 |
| 已发布模型接口 | `GET /api/detection/models/published` 或模型契约替代接口 | API_CONTRACT | 文档推断 | 文档推断 |
| 图片检测接口 | `POST /api/detection/detect` | API_CONTRACT/DETECTION_RESULT_SCHEMA | 文档推断 | 文档推断 |
| 检测记录接口 | `GET /api/detection/records`、`GET /records/:id` | API_CONTRACT/DB_CONTRACT | 文档推断 | 文档推断 |
| 文件访问 | 图片、视频、裁剪图、报告 URL 规则 | FILE_STORAGE_CONTRACT | 未确认 | 待源码确认 |

## 5. 权限与登录态门禁

| 门禁项 | 最小要求 | 当前状态 | 证据等级 |
|---|---|---|---|
| token 存储策略 | 明确 localStorage/sessionStorage/store 使用边界 | 未确认 | 待源码确认 |
| JWT 字段 | 至少明确 `user_id`、`role`、`exp` | 文档推断 | 文档推断 |
| 当前用户状态 | 可获取 username、role、status、头像等展示字段 | 待契约确认 | 待源码确认 |
| 管理员判断 | `role=1` 管理员，`role=0` 普通用户 | 文档推断 | 文档推断 |
| 管理页面保护 | 普通用户不能访问用户/数据集/模型/评估管理 | 文档推断 | 文档推断 |
| 401 处理 | token 失效后清理登录态并回登录页 | 未确认 | 待源码确认 |
| 403 处理 | 权限不足有统一提示和导航策略 | 未确认 | 待源码确认 |
| 多用户限制 | 同时登录多个用户需不同浏览器 | 文档明确 | 文档推断 |
| 默认账号 | `admin / 123456`、`test / 123456` | 使用注意事项明确 | 文档推断 |

## 6. 阻塞条件

出现以下任一情况，应阻塞 Phase 2B 前端代码重建：

| 阻塞条件 | 原因 | 证据等级 |
|---|---|---|
| 未确认源码恢复还是最小重建 | 范围不清会导致重复实现或覆盖真实源码 | 待源码确认 |
| 未使用独立 worktree 进入代码修改 | 多 Agent 可能互相覆盖 | 文档推断 |
| `API_CONTRACT` 缺失 | 前端无法稳定请求/响应解析 | 待源码确认 |
| `DETECTION_RESULT_SCHEMA` 缺失 | 图片/视频/实时结果展示字段无法冻结 | 待源码确认 |
| `AI_OUTPUT_SCHEMA` 缺失 | AI 分析展示字段无法冻结 | 待源码确认 |
| `FILE_STORAGE_CONTRACT` 缺失 | 文件预览、下载、报告导出 URL 无法确定 | 待源码确认 |
| `DB_CONTRACT` 关键枚举缺失 | 模型/数据集/视频状态和权限字段可能错误 | 待源码确认 |
| 后端最小启动路径不明 | 前端无法做真实 API 联调 | 待源码确认 |
| 任何 Agent 在 Phase 2A 创建前端源码 | 违反阶段边界 | 冲突/差异 |

## 7. Leader 判定所需证据

Leader 判定 Frontend Phase 2B Gate 时，至少需要以下证据：

| 证据 | 提供方 | PASS 标准 | 证据等级目标 |
|---|---|---|---|
| 前端源码恢复/最小重建决策 | Leader + Frontend | 明确恢复原源码或最小重建范围 | 文档推断 |
| 前端最小入口清单 | Frontend | `index.html`、`vite.config.*`、`src/main.*`、`App.vue` 范围明确 | 待源码确认 |
| API_CONTRACT | Backend | 覆盖 user、detection、file 基础接口和错误格式 | 文档推断/待源码确认 |
| DETECTION_RESULT_SCHEMA | Backend + AI | 至少覆盖 bbox、class、confidence、artifacts | 文档推断/待源码确认 |
| AI_OUTPUT_SCHEMA | AI | 覆盖 YOLO 输出、Qwen-VL 分析、metrics 候选字段 | 已资源确认/文档推断 |
| FILE_STORAGE_CONTRACT | Backend | 明确图片/视频/裁剪图/报告 URL 访问方式 | 文档推断/待源码确认 |
| 权限/JWT 契约 | Backend | 明确 role、token header、401/403 响应 | 文档推断/待源码确认 |
| 测试资源映射 | Docs/Test | 明确图片检测最小冒烟资源 | 已资源确认 |
| 禁止项检查 | Leader | 未修改业务代码、未创建源码目录 | 已资源确认 |

当前建议判定：

```text
Frontend Phase 2B Gate: BLOCKED

原因：
- web-vue/src 缺失；
- API_CONTRACT / DETECTION_RESULT_SCHEMA / AI_OUTPUT_SCHEMA / FILE_STORAGE_CONTRACT 尚未最终输出；
- 前端恢复原源码还是最小重建范围尚未由 Leader 判定；
- 当前只能继续 Phase 2A 文档契约工作。
```
