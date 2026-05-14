# Frontend Source Recovery Tasks

更新时间：2026-05-13
角色：Frontend Agent
阶段：Phase 2A：系统契约与重建基线
范围：前端源码恢复/重建任务清单；不执行源码恢复或重建。

## 1. 当前缺失源码清单

| 缺失项 | 当前状态 | 影响 | 证据等级 |
|---|---|---|---|
| `web-vue/src/` | 不存在 | 无法确认页面、路由、API、store、类型 | 冲突/差异 |
| `web-vue/index.html` | 不存在 | 无法确认 Vite 前端入口 | 冲突/差异 |
| `web-vue/vite.config.*` | 不存在 | 无法确认构建配置、代理、插件配置 | 冲突/差异 |
| `src/main.*` | 不存在 | 无法确认 Vue 应用挂载、Pinia、Router、Element Plus 初始化 | 冲突/差异 |
| `src/App.vue` | 不存在 | 无法确认根组件和布局入口 | 冲突/差异 |
| `src/router/` | 不存在 | 无法确认真实路由表、路由守卫、权限 meta | 冲突/差异 |
| `src/api/` | 不存在 | 无法确认 API 封装、request 拦截器、函数命名 | 冲突/差异 |
| `src/views/` | 不存在 | 无法确认页面列表、页面结构、业务流程 | 冲突/差异 |
| `src/components/` | 不存在 | 无法确认公共组件、布局、分页、上传、结果展示组件 | 冲突/差异 |
| `src/stores/` | 不存在 | 无法确认 Pinia store、登录态、权限、业务缓存 | 冲突/差异 |
| `src/types/` | 不存在 | 无法确认 API response、检测结果、模型、数据集、评估类型 | 冲突/差异 |
| `src/utils/` | 不存在 | 无法确认文件 URL、日期格式、权限判断等工具 | 冲突/差异 |
| 静态资源目录 | 未确认 | 无法确认 logo、默认头像、图标、样式资产 | 待源码确认 |
| 样式入口 | 未确认 | 无法确认 Element Plus 主题、全局样式、响应式布局 | 待源码确认 |

## 2. 必须恢复或重建的前端入口

以下内容是 Phase 2B 最小可运行前端的入口条件。当前只列任务，不创建文件。

| 入口 | 恢复/重建目的 | 最小判定标准 | 证据等级 |
|---|---|---|---|
| `index.html` | Vite HTML 入口 | 能挂载前端应用 | 待源码确认 |
| `vite.config.*` | 构建、开发服务、插件、代理配置 | 能运行 Vite，代理后端 API 策略明确 | 待源码确认 |
| `src/main.*` | Vue 应用启动入口 | 注册 Router、Pinia、Element Plus、全局样式 | 待源码确认 |
| `src/App.vue` | 根组件 | 能承载路由出口或基础布局 | 待源码确认 |
| `src/router/index.*` | 路由入口 | 登录、主布局、核心页面路由可枚举 | 待源码确认 |
| `src/api/request.*` | API 请求入口 | baseURL、token 注入、错误处理策略明确 | 待源码确认 |
| `src/stores/user.*` | 登录态入口 | token、role、当前用户、退出流程明确 | 待源码确认 |

## 3. 必须恢复或重建的目录

| 目录 | 最小内容候选 | 依赖契约 | 证据等级 |
|---|---|---|---|
| `src/router/` | 路由表、路由守卫、权限 meta | JWT 字段、页面权限矩阵 | 待源码确认 |
| `src/api/` | `request`、用户、检测、视频、实时、数据集、模型、评估 API 封装 | API_CONTRACT、FILE_STORAGE_CONTRACT | 待源码确认 |
| `src/views/user/` | 登录、注册、个人中心、用户首页 | API_CONTRACT、JWT、DB user 字段 | 文档推断 |
| `src/views/admin/` | 管理控制台、用户管理、数据集管理、模型管理 | API_CONTRACT、权限契约、DB_CONTRACT | 文档推断 |
| `src/views/detection/` | 图片检测、图片检测记录、详情 | API_CONTRACT、DETECTION_RESULT_SCHEMA、AI_OUTPUT_SCHEMA | 文档推断 |
| `src/views/video-detection/` | 视频检测、视频记录、详情 | API_CONTRACT、视频状态机、FILE_STORAGE_CONTRACT | 文档推断 |
| `src/views/realtime-detection/` | 实时检测、实时记录、会话详情 | API_CONTRACT、DETECTION_RESULT_SCHEMA | 文档推断 |
| `src/views/evaluation/` | 模型评估、评估记录 | API_CONTRACT、evaluation metrics、FILE_STORAGE_CONTRACT | 文档推断 |
| `src/components/` | Layout、Pagination、上传、结果展示、图表组件 | 页面地图、UI 规范 | 文档推断 |
| `src/stores/` | user、permission、model、detection、video、realtime、evaluation | API_CONTRACT、JWT、业务状态 | 文档推断 |
| `src/types/` | API response、用户、模型、数据集、检测结果、AI 输出、评估指标类型 | API_CONTRACT、DB_CONTRACT、AI_OUTPUT_SCHEMA | 文档推断 |
| `src/utils/` | 文件 URL、日期格式、权限判断、下载、错误格式化 | FILE_STORAGE_CONTRACT、API_CONTRACT | 文档推断 |

## 4. 源码恢复后需要重新审计的内容

源码补齐后必须重新执行以下审计：

| 审计项 | 需要证据 | 输出 | 证据等级目标 |
|---|---|---|---|
| 真实目录结构 | `web-vue/src` 文件树 | 更新前端目录地图 | 已源码确认 |
| 路由表 | `src/router` 源码 | 源码确认版路由清单 | 已源码确认 |
| 页面清单 | `src/views` 源码 | 页面-路由矩阵 | 已源码确认 |
| API 封装 | `src/api` 源码 | 页面-API 调用矩阵 | 已源码确认 |
| Request 拦截器 | `request` 封装源码 | token、错误、loading 策略说明 | 已源码确认 |
| Store | `src/stores` 源码 | 页面-store 状态依赖矩阵 | 已源码确认 |
| TypeScript 类型 | `src/types` 或页面内类型 | 类型与契约字段对照表 | 已源码确认 |
| 文件访问 | 文件 URL 生成和预览逻辑 | 文件访问契约消费清单 | 已源码确认 |
| 检测结果展示 | 图片/视频/实时页面源码 | detection_result 字段消费清单 | 已源码确认 |
| AI 分析展示 | 图片检测页面源码 | AI_OUTPUT_SCHEMA 字段消费清单 | 已源码确认 |
| 评估展示 | 评估页面源码 | metrics 字段消费清单 | 已源码确认 |
| UI 一致性 | 页面源码和截图 | UI 问题清单 | 已源码确认 |

## 5. 不允许凭文档直接实现的内容

以下内容只能作为候选任务或契约需求，不允许在 Phase 2A 直接实现：

| 内容 | 禁止原因 | 证据等级 |
|---|---|---|
| 新建 `src/` | 当前阶段禁止补齐 web-vue 源码 | 冲突/差异 |
| 新建页面组件 | 页面结构仅文档推断，未通过 Phase 2B Gate | 文档推断 |
| 新建路由表 | 实际路径、权限 meta、菜单规则未确认 | 待源码确认 |
| 新建 API 封装 | API_CONTRACT 尚待 Backend 输出和复核 | 待源码确认 |
| 新建 Pinia store | 状态结构、token 策略、缓存策略未确认 | 待源码确认 |
| 新建 TypeScript 类型 | API、DB、AI 字段尚未冻结 | 待源码确认 |
| 新建检测结果组件 | DETECTION_RESULT_SCHEMA 未最终确认 | 待源码确认 |
| 新建 AI 分析组件 | AI_OUTPUT_SCHEMA 未最终确认 | 待源码确认 |
| 新建视频轮询逻辑 | 视频任务状态机和失败策略未源码确认 | 待源码确认 |
| 新建实时检测逻辑 | 本地摄像头、Base64 协议、tracker 生命周期未源码确认 | 待源码确认 |
| 新建 UI 主题 | 真实页面和现有样式缺失，无法判断兼容性 | 待源码确认 |

## 6. 与 Backend / AI / Docs 的依赖关系

| 依赖方 | 前端需要的交付物 | 用途 | 证据等级 |
|---|---|---|---|
| Backend | `API_CONTRACT.md` | 请求路径、方法、入参、响应、错误格式、权限 | 待源码确认 |
| Backend | `DETECTION_RESULT_SCHEMA.md` | 图片/视频/实时检测结果展示字段 | 待源码确认 |
| Backend | `DB_CONTRACT.md` | 列表字段、详情字段、枚举、筛选条件 | 待源码确认 |
| Backend | `FILE_STORAGE_CONTRACT.md` | 图片、视频、裁剪图、报告、权重、数据集文件访问 | 待源码确认 |
| Backend | JWT/权限契约 | 登录态、路由守卫、管理员页面控制 | 文档推断 |
| AI | `AI_OUTPUT_SCHEMA.md` | YOLO 输出字段、类别、置信度、bbox 展示 | 待源码确认 |
| AI | `QWEN_VL_ANALYSIS_SCHEMA.md` | 污染描述、风险、治理建议、限制说明展示 | 待源码确认 |
| AI | `EVALUATION_METRICS_SCHEMA.md` | Precision、Recall、mAP50、mAP50-95、IoU、匹配数量展示 | 待源码确认 |
| Docs/Test | `EVIDENCE_LEVELS.md` | 统一证据等级和验收措辞 | 文档推断 |
| Docs/Test | `SMOKE_TEST_RESOURCE_MAP.md` | 图片、视频、评估、实时冒烟资源选择 | 已资源确认 |
| Docs/Test | `PHASE2B_GATE_CHECKLIST.md` | 判定是否进入前端代码重建 | 文档推断 |

协作约束：

- Backend/AI 契约未冻结前，Frontend 只能记录消费需求。
- Docs/Test 统一证据等级前，Frontend 输出仍需自带证据等级标注。
- Leader 判定 Phase 2B Gate 通过前，Frontend 不得创建源码目录。
