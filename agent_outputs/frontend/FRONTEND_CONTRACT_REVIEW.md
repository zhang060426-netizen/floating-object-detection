# Frontend Contract Review

更新时间：2026-05-13
角色：Frontend Agent
阶段：Phase 2A：系统契约与重建基线
用途：从前端消费视角审查 API、检测结果、AI 输出、DB、文件存储契约需求。

## 1. 对 API_CONTRACT 的前端消费需求

当前未读取到 Backend 输出的正式 `API_CONTRACT.md`，以下为前端消费需求，不能视为后端实现事实。

| 需求 | 前端消费方式 | 必需性 | 证据等级 |
|---|---|---:|---|
| Base URL 与代理策略 | dev/build 环境请求地址、跨域或代理配置 | P0 | 待源码确认 |
| 统一响应格式 | 统一解析 `code`、`msg`、`data` 或实际字段 | P0 | 文档推断 |
| 错误响应格式 | 表单错误、业务错误、系统错误统一提示 | P0 | 待源码确认 |
| 鉴权 Header | `Authorization: Bearer <token>` 候选 | P0 | 文档推断 |
| 401 响应 | token 失效后清理登录态、跳转登录 | P0 | 待源码确认 |
| 403 响应 | 管理员权限不足提示和导航策略 | P0 | 待源码确认 |
| 分页格式 | 用户、检测记录、视频记录、评估记录列表分页 | P0 | 待源码确认 |
| 上传格式 | 图片、视频、ZIP、标签、权重、训练文件上传字段名 | P0 | 待源码确认 |
| 下载格式 | Word 报告、数据集 ZIP、模型权重下载响应 | P1 | 待源码确认 |
| 异步任务格式 | 视频任务 ID、状态、进度、失败原因 | P0 | 文档推断 |
| 轮询频率建议 | 视频检测进度接口的前端轮询间隔 | P1 | 待源码确认 |
| 请求取消/重复提交策略 | 防止上传和检测重复触发 | P1 | 待源码确认 |

前端请求 API_CONTRACT 明确以下分组：

| API 分组 | 前端页面 | 前端需要的最小接口 | 证据等级 |
|---|---|---|---|
| user | 登录、注册、个人中心、用户管理 | login、register、current、logout、password、page、status | 文档推断 |
| detection | 图片检测、图片记录 | models/published、detect、enhance-image、analyze-defects、generate-suggestions、save、export-word、records、crops | 文档推断 |
| video-detection | 视频检测、视频记录 | detect、progress、records、record detail、delete | 文档推断 |
| realtime-detection | 实时检测、实时记录 | detect、reset-tracker、sessions、records、delete | 文档推断 |
| dataset | 数据集管理 | upload、list、detail、update、delete、download | 文档推断 |
| model | 模型管理、检测模型选择 | create、list、published、datasets、base-models、classes、upload-weight、publish、unpublish、chart-data | 文档推断 |
| evaluation | 模型评估 | box-config、predict、save、evaluated-models、records、detail、delete | 文档推断 |
| file | 所有文件预览/下载 | URL 生成、静态访问或下载接口 | 待源码确认 |

## 2. 对 DETECTION_RESULT_SCHEMA 的展示需求

前端需要一个能同时支撑图片、视频关键帧、实时检测、评估预测结果的检测结果契约。

| 字段需求 | 展示用途 | 是否必需 | 证据等级 |
|---|---|---:|---|
| `schema_version` | 兼容不同版本检测结果 | P1 | 文档推断 |
| `model_id` | 展示使用模型、关联记录 | P0 | 文档推断 |
| `model_name` | 页面展示模型名称 | P0 | 文档推断 |
| `image_width` / `image_height` | 将 bbox 映射到图片显示坐标 | P0 | 待源码确认 |
| `detections[]` | 目标列表渲染 | P0 | 文档推断 |
| `detections[].class_id` | 类别颜色、统计、筛选 | P0 | 已资源确认 |
| `detections[].class_name` | 英文类别名展示/兼容 | P0 | 已资源确认 |
| `detections[].display_name` | 中文展示名，如“漂浮物” | P1 | 文档推断 |
| `detections[].confidence` | 置信度标签和排序 | P0 | 文档推断 |
| `detections[].bbox_xyxy` | 画框，像素坐标优先 | P0 | 文档推断 |
| `detections[].bbox_xywhn` | 归一化坐标，评估/兼容需要 | P1 | 已资源确认 |
| `detections[].track_id` | 实时/视频跟踪展示 | P1 | 文档推断 |
| `detections[].crop_url` 或文件 key | 裁剪图展示 | P1 | 文档推断 |
| `summary.total_count` | 统计卡片展示 | P0 | 文档推断 |
| `summary.by_class` | 类别统计 | P1 | 文档推断 |
| `artifacts.result_image_url` | 结果图展示 | P0 | 文档推断 |
| `artifacts.enhanced_image_url` | 增强图展示 | P1 | 文档推断 |
| `artifacts.result_video_url` | 视频检测结果播放 | P1 | 文档推断 |
| `artifacts.key_frame_urls` | 视频关键帧展示 | P1 | 文档推断 |
| `timing_ms` | 性能信息展示或调试 | P2 | 文档推断 |

前端无法接受的模糊点：

- bbox 坐标没有声明像素/归一化格式。
- 结果图 URL 和文件 key 混用但无转换规则。
- 图片、视频、实时检测各自返回完全不同字段且无版本标记。
- 置信度字段名在 `confidence`、`conf`、`score` 间不统一。

## 3. 对 AI_OUTPUT_SCHEMA 的展示需求

AI 输出包括 YOLO 输出和 Qwen-VL 多模态分析。前端主要消费 Qwen-VL 分析和治理建议。

| 字段需求 | 展示用途 | 是否必需 | 证据等级 |
|---|---|---:|---|
| `analysis_version` | 兼容 prompt/字段变化 | P1 | 文档推断 |
| `provider` | 展示或调试大模型来源，如阿里云百炼 | P2 | 文档推断 |
| `model` | 展示或调试模型名称 | P2 | 文档推断 |
| `pollution_description` | 图片检测结果页核心分析文本 | P0 | 文档推断 |
| `water_surface_status` | 水面状态维度展示 | P1 | 文档推断 |
| `pollution_level` 或 `risk_level` | 风险标签、颜色、筛选 | P0 | 文档推断 |
| `risk_reasons[]` | 风险原因列表 | P1 | 文档推断 |
| `pollution_source_analysis` | 污染来源分析 | P1 | 文档推断 |
| `ecological_impact` | 生态影响说明 | P1 | 文档推断 |
| `governance_suggestions[]` | 治理建议列表 | P0 | 文档推断 |
| `immediate_actions[]` | 立即清理建议 | P1 | 文档推断 |
| `long_term_plan[]` | 长期治理建议 | P1 | 文档推断 |
| `limitations[]` | 模型不确定性和限制提示 | P1 | 文档推断 |
| `raw_response` | 调试或报告备用，不默认展示 | P2 | 待源码确认 |
| `error` | AI 调用失败时降级展示 | P0 | 文档推断 |

前端展示要求：

- AI 分析失败时，图片检测结果仍应可展示。
- Qwen-VL 输出字段必须允许空值或错误对象。
- 治理建议应区分“分析文本”和“建议文本”，避免报告字段错位。
- 若返回 Markdown，需明确前端是否使用 `marked` 渲染以及 XSS 处理策略；当前只由依赖可见 `marked`，实现待源码确认。

## 4. 对 DB_CONTRACT 的前端可见字段需求

前端不直接访问数据库，但列表、详情、筛选、状态标签依赖 DB 字段经 API 返回。

| 表/领域 | 前端可见字段需求 | 使用页面 | 证据等级 |
|---|---|---|---|
| `user` | id、username、real_name、phone、email、avatar、role、status、create_time、update_time | 登录态、个人中心、用户管理 | 文档推断 |
| `datasets` | id、name、description、status、structure_info、zip file、create_time、update_time | 数据集管理、模型创建 | 文档推断 |
| `models` | id、name、description、dataset_id、base_model、status、model file、metrics、create_time、update_time | 模型管理、模型选择、评估 | 文档推断 |
| `detection_records` | id、title、model_id、model_name、origin_image、result_image、enhanced_image、detection_result、analysis_result、suggestion、create_time | 图片记录、报告 | 文档推断 |
| `detection_crops` | id、record_id、object_index、class_name、confidence、bbox、crop image | 图片检测详情 | 文档推断 |
| `video_detection_records` | id、title、model_id、status、progress、origin_video、result_video、error_message、create_time | 视频记录 | 文档推断 |
| `video_detection_frames` | id、record_id、frame_index、timestamp、image、detection_result | 视频详情关键帧 | 文档推断 |
| `evaluation_records` | id、model_id、origin_image、compare_image、label_content、detection_result、metrics、score、comment、create_time | 模型评估记录 | 文档推断 |
| `realtime_detection_sessions` | session_id、model_id、start_time、end_time、detection_count、status | 实时会话列表 | 文档推断 |
| `realtime_detection_detections` | id、session_id、track_id、class_name、confidence、bbox、image、create_time | 实时记录详情 | 文档推断 |

前端需要 DB_CONTRACT 明确的枚举：

| 枚举 | 候选值 | 使用场景 | 证据等级 |
|---|---|---|---|
| 用户角色 | `0` 普通用户，`1` 管理员 | 权限、菜单、管理页面 | 文档推断 |
| 用户状态 | 启用/禁用 | 登录限制、用户管理标签 | 文档推断 |
| 数据集状态 | 待验证、验证通过、验证失败 | 数据集管理状态标签 | 文档推断 |
| 模型状态 | 新建、训练中、训练完成、已发布 | 模型管理、模型选择 | 文档推断 |
| 视频任务状态 | pending、processing、completed、failed、cancelled | 进度条和操作按钮 | 文档推断 |
| 实时会话状态 | active、ended 或等价状态 | 会话展示 | 待源码确认 |

## 5. 对 FILE_STORAGE_CONTRACT 的文件访问需求

| 文件类型 | 前端使用位置 | 需要契约字段 | 证据等级 |
|---|---|---|---|
| 用户头像 | 个人中心、布局、用户管理 | bucket/object_key 或可访问 URL、默认头像策略 | 文档推断 |
| 原始图片 | 图片检测、图片记录、评估记录 | URL、文件名、尺寸、格式 | 文档推断 |
| 检测结果图 | 图片检测结果、记录详情 | URL、关联 record_id | 文档推断 |
| CLAHE 增强图 | 图片检测 AI 分析展示 | URL、是否必定存在 | 文档推断 |
| 目标裁剪图 | 图片检测详情 | URL、object_index、bbox | 文档推断 |
| Word 报告 | 图片检测记录 | 下载接口或 URL、文件名、权限 | 文档推断 |
| 原始视频 | 视频记录 | URL、格式、大小、时长 | 文档推断 |
| 结果视频 | 视频检测详情 | URL、编码格式、是否可在线播放 | 文档推断 |
| 视频关键帧 | 视频检测详情 | URL、frame_index、timestamp | 文档推断 |
| 实时检测截图 | 实时记录 | URL 或 Base64 存储策略 | 待源码确认 |
| 数据集 ZIP | 数据集管理 | 下载接口、权限、文件大小 | 文档推断 |
| 模型权重 | 模型管理 | 上传/下载接口、文件名、状态 | 文档推断 |
| 训练文件/图表 | 模型管理 | 文件类型、chart-data 接口、预览策略 | 文档推断 |

前端需要 FILE_STORAGE_CONTRACT 回答：

- API 返回的是完整 URL、相对路径、bucket/object_key，还是混合格式。
- 静态文件是否需要鉴权。
- Word、ZIP、权重下载是否走 blob 响应。
- 图片和视频是否存在清理生命周期，前端如何处理失效链接。
- 结果视频编码是否保证浏览器可播放。

## 6. 前端无法确认的字段

| 字段/问题 | 当前无法确认原因 | 影响 | 证据等级 |
|---|---|---|---|
| API 统一响应是否固定为 `{code,msg,data}` | 后端源码缺失 | request 封装无法冻结 | 待源码确认 |
| 分页字段名 | 后端源码缺失 | 列表页无法统一实现 | 待源码确认 |
| 文件 URL 字段名 | 文件存储实现缺失 | 图片/视频/报告无法访问 | 待源码确认 |
| JWT payload 完整字段 | 鉴权源码缺失 | 权限和登录态无法冻结 | 待源码确认 |
| `detection_result` 真实字段 | 推理封装和前端展示源码缺失 | 检测结果展示无法实现 | 待源码确认 |
| Qwen-VL 真实字段 | LLM 调用链缺失 | AI 分析展示和报告字段不稳定 | 待源码确认 |
| 视频进度字段 | 视频任务源码缺失 | 进度条和轮询逻辑无法冻结 | 待源码确认 |
| 实时检测返回字段 | 实时接口源码缺失 | 摄像头页面无法设计最终状态 | 待源码确认 |
| 模型状态枚举真实值 | DB 初始化/后端源码缺失 | 模型管理状态标签可能错误 | 待源码确认 |
| 数据集状态枚举真实值 | DB 初始化/后端源码缺失 | 数据集管理状态标签可能错误 | 待源码确认 |
| 评估 metrics JSON | 评估 API 源码缺失 | 图表和指标卡无法冻结 | 待源码确认 |
| `marked` 使用位置 | 只有依赖声明，无源码 | Markdown 渲染与安全策略无法确认 | 已资源确认/待源码确认 |

## 7. 需要 Backend / AI / Docs 回答的问题

### 7.1 需要 Backend 回答

| 问题 | 用途 | 优先级 | 证据等级 |
|---|---|---:|---|
| API 统一响应格式是否固定为 `{code,msg,data}`？ | request 封装 | P0 | 待源码确认 |
| 401、403、参数错误、业务错误的响应结构是什么？ | 错误提示和跳转 | P0 | 待源码确认 |
| JWT payload 是否只包含 `user_id`、`role`、`exp`？ | 登录态和权限 | P0 | 文档推断 |
| 用户、数据集、模型、记录列表分页字段是什么？ | 表格分页组件 | P0 | 待源码确认 |
| 文件返回完整 URL 还是 bucket/object_key？ | 图片/视频/报告展示 | P0 | 待源码确认 |
| 图片检测结果接口是否一次返回 AI 分析，还是分多步接口？ | 图片检测流程设计 | P0 | 文档推断 |
| 视频任务状态和进度字段是什么？ | 视频检测轮询 | P0 | 文档推断 |
| 模型“已发布”状态值是否为 `3`？ | 模型选择过滤 | P0 | 文档推断 |
| 管理员接口权限失败如何返回？ | 管理页面保护 | P1 | 待源码确认 |
| 下载接口是否需要 blob 处理？ | 报告、ZIP、权重下载 | P1 | 待源码确认 |

### 7.2 需要 AI 回答

| 问题 | 用途 | 优先级 | 证据等级 |
|---|---|---:|---|
| YOLO 输出推荐使用像素 `xyxy` 还是归一化 `xywhn` 作为前端主展示？ | 画框展示 | P0 | 已资源确认/文档推断 |
| 类别是否保持 `class_id=0`、`floating_object`？ | 类别颜色和统计 | P0 | 已资源确认 |
| confidence 推荐保留几位小数？ | UI 展示一致性 | P2 | 待源码确认 |
| Qwen-VL 分析字段是否能结构化返回？ | AI 分析展示 | P0 | 文档推断 |
| AI 分析失败时是否返回错误对象而非空字符串？ | 降级展示 | P0 | 待源码确认 |
| metrics 命名使用 `map50` 还是 `mAP50`？ | 评估图表字段统一 | P1 | 文档推断 |
| 历史 best.pt 缺失时，模型选择页面应如何提示？ | 模型状态展示 | P1 | 已资源确认 |

### 7.3 需要 Docs/Test 回答

| 问题 | 用途 | 优先级 | 证据等级 |
|---|---|---:|---|
| 证据等级是否统一写入 `EVIDENCE_LEVELS.md`？ | 所有前端交付物措辞统一 | P0 | 文档推断 |
| Phase 2B Gate 是否由 Leader 统一判定？ | 防止前端提前写代码 | P0 | 文档推断 |
| 图片检测最小冒烟图片是哪一张？ | 前端联调用例 | P1 | 已资源确认 |
| 视频检测最小冒烟视频是哪一个？ | 前端进度联调 | P1 | 已资源确认 |
| 评估测试图片和标签如何配对？ | 评估页面联调 | P1 | 已资源确认 |
| 实时检测无 USB 摄像头时是否允许跳过？ | 验收边界 | P1 | 文档推断 |
| 文档中的默认账号是否作为 Phase 2B 登录测试依据？ | 登录验收 | P1 | 文档推断 |

## 8. 前端结论

当前前端只能进行契约消费视角 review。进入 Phase 2B 前，必须至少获得：

- Backend 的 API、检测结果、DB、文件存储、JWT 契约草案。
- AI 的 YOLO 输出、Qwen-VL 分析、评估指标契约草案。
- Docs/Test 的证据等级、冒烟资源、Phase 2B Gate 总清单。
- Leader 对“恢复原源码”或“最小重建”的明确判定。

在这些条件满足前，Frontend 不应创建任何 Vue、TypeScript、CSS、路由、store 或 API 封装代码。
