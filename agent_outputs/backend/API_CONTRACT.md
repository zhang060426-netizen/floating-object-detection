# API Contract Candidate

阶段：Phase 2A：系统契约与重建基线  
角色：Backend Agent  
边界：本文档是 API 候选契约，不是已实现事实；当前 `web-flask` 业务源码缺失，所有接口实现均待源码确认。

## 1. 范围与边界

本文档覆盖后端候选 API 契约：

- user
- detection
- video-detection
- realtime-detection
- dataset
- model
- evaluation
- file / health

证据等级统一使用：

| 证据等级 | 含义 |
|---|---|
| 已源码确认 | 有明确 Flask / Python / SQL 源码证据。当前 API 实现无此等级。 |
| 已资源确认 | 有 `requirements.txt`、训练资源、测试包等文件证据。 |
| 数据库文档确认 | 来自 `3项目文档/5数据库开发文档.md`。 |
| 文档推断 | 来自系统介绍、架构、规划文档。 |
| 待源码确认 | 必须等 `web-flask` 业务源码补齐后确认。 |
| 冲突/差异 | 文档与当前可见文件存在明确不一致。 |

当前边界：

| 项 | 结论 | 证据等级 |
|---|---|---|
| `web-flask/requirements.txt` 存在，包含 Flask-CORS、PyJWT、ultralytics、openai、python-docx、lap | 可确认后端依赖意图 | 已资源确认 |
| `web-flask/app.py`、`routes/`、`services/`、`utils/`、`dao/`、`models/` 当前未发现 | 文档期望结构与当前文件不一致 | 冲突/差异 |
| API 路径、权限、业务说明 | 只来自系统介绍文档 | 文档推断 |
| 真实请求参数、响应字段、错误码、鉴权装饰器 | 当前无法确认 | 待源码确认 |

## 2. 统一响应格式候选

候选成功响应：

| 字段 | 类型候选 | 必填候选 | 含义 | 证据等级 |
|---|---|---:|---|---|
| `code` | integer | 是 | 业务状态码，成功候选为 `200` | 文档推断 |
| `msg` | string | 是 | 响应消息，成功候选为 `success` | 文档推断 |
| `data` | object / array / null | 是 | 业务数据载荷 | 文档推断 |
| `request_id` | string | 否 | 排障追踪 ID，文档未明确 | 待源码确认 |
| `timestamp` | string | 否 | 服务端响应时间，文档未明确 | 待源码确认 |

统一响应格式候选来源：`3项目文档/1系统介绍文档.md` 明确描述 `{ "code": 200, "msg": "success", "data": { ... } }`。

## 3. 错误响应格式候选

候选错误响应：

| 字段 | 类型候选 | 必填候选 | 含义 | 证据等级 |
|---|---|---:|---|---|
| `code` | integer | 是 | 业务错误码或 HTTP 映射码 | 文档推断 |
| `msg` | string | 是 | 用户可读错误消息 | 文档推断 |
| `data` | null / object | 是 | 错误时通常为空或附带最小上下文 | 文档推断 |
| `error` | object | 否 | 结构化错误详情 | 待源码确认 |
| `error.field` | string | 否 | 参数错误字段 | 待源码确认 |
| `error.reason` | string | 否 | 机器可读失败原因 | 待源码确认 |

候选错误码：

| code 候选 | 场景 | 证据等级 |
|---:|---|---|
| `400` | 参数错误、文件格式不支持、缺少必填字段 | 文档推断 |
| `401` | 未登录、token 缺失、token 失效 | 文档推断 |
| `403` | 权限不足，例如普通用户访问管理员接口 | 文档推断 |
| `404` | 记录、模型、数据集、文件不存在 | 文档推断 |
| `409` | 状态冲突，例如模型未训练完成但尝试发布 | 文档推断 |
| `500` | 服务端异常、推理失败、文件处理失败 | 文档推断 |

真实错误码、HTTP 状态码与业务 `code` 是否一致：待源码确认。

## 4. 鉴权与 JWT 候选契约

认证方式候选：

| 项 | 候选值 | 证据等级 |
|---|---|---|
| Header | `Authorization` | 文档推断 |
| Scheme | `Bearer <token>` | 文档推断 |
| 公开接口 | 登录、注册 | 文档推断 |
| 登录接口 | 除登录/注册外大部分接口 | 文档推断 |
| 管理员接口 | 用户管理、数据集管理、模型管理、模型评估等部分接口 | 文档推断 |

JWT payload 候选：

| 字段 | 类型候选 | 必填候选 | 含义 | 证据等级 |
|---|---|---:|---|---|
| `user_id` | integer | 是 | 当前用户 ID | 文档推断 |
| `role` | integer | 是 | 用户角色，`0` 普通用户，`1` 管理员 | 数据库文档确认 / 文档推断 |
| `exp` | integer | 是 | 过期时间 | 文档推断 |
| `username` | string | 否 | 用户名 | 待源码确认 |
| `status` | integer | 否 | 用户启用状态 | 待源码确认 |
| `iat` | integer | 否 | 签发时间 | 待源码确认 |

默认账号：

| 用户名 | 密码 | 角色 | 证据等级 |
|---|---|---|---|
| `admin` | `123456` | 管理员 | 数据库文档确认 |
| `test` | `123456` | 普通用户 | 数据库文档确认 |

密码存储候选：MD5，默认密码哈希为 `e10adc3949ba59abbe56e057f20f883e`。证据等级：数据库文档确认。真实实现待源码确认。

## 5. API 模块总览

| 模块 | 前缀候选 | 主要职责 | 权限候选 | 证据等级 |
|---|---|---|---|---|
| user | `/api/user` | 登录、注册、用户信息、用户管理 | 公开 / 登录 / 管理员 | 文档推断 |
| detection | `/api/detection` | 图片检测、增强、AI 分析、建议、报告、记录 | 登录 | 文档推断 |
| video-detection | `/api/video-detection` | 视频检测任务、进度、记录 | 登录 | 文档推断 |
| realtime-detection | `/api/realtime-detection` | 实时帧检测、tracker、会话、记录 | 登录 | 文档推断 |
| dataset | `/api/dataset` | 数据集上传、验证、查询、下载、删除 | 登录 / 管理员 | 文档推断 |
| model | `/api/model` | 模型创建、上传、发布、查询、导出 | 登录 / 管理员 | 文档推断 |
| evaluation | `/api/evaluation` | 模型评估、指标、记录 | 登录 / 管理员候选 | 文档推断 |
| file | `/api/file` 候选 | 文件访问或上传下载封装 | 登录候选 | 文档推断 / 待源码确认 |
| health | `/api/health` 候选 | 健康检查 | 公开候选 | 文档推断 / 待源码确认 |

当前未发现任何 Flask route 源码。证据等级：冲突/差异。

## 6. user API 候选

前缀候选：`/api/user`。证据等级：文档推断。

| 方法 | 路径候选 | 权限候选 | 功能 | 主要请求字段候选 | 主要响应字段候选 | 证据等级 |
|---|---|---|---|---|---|---|
| POST | `/login` | 公开 | 登录 | `username`, `password` | `token`, `user` | 文档推断 |
| POST | `/register` | 公开 | 注册 | `username`, `password`, `real_name`, `phone`, `email` | 用户摘要 | 文档推断 |
| POST | `/password` | 登录 | 修改当前用户密码 | `old_password`, `new_password` | 操作结果 | 文档推断 |
| PUT | `` | 登录 | 更新当前用户信息 | `real_name`, `phone`, `email`, `avatar_*` | 当前用户 | 文档推断 |
| GET | `/current` | 登录 | 获取当前用户信息 | 无 | `id`, `username`, `role`, `status` 等 | 文档推断 |
| POST | `/logout` | 登录 | 登出 | 无 | 操作结果 | 文档推断 |
| GET | `/page` | 管理员 | 分页查询用户 | `page`, `page_size`, filters | 分页结果 | 文档推断 |
| POST | `` | 管理员 | 新建用户 | 用户字段 | 用户摘要 | 文档推断 |
| GET | `/:id` | 管理员 | 用户详情 | path `id` | 用户详情 | 文档推断 |
| DELETE | `/:id` | 管理员 | 删除用户 | path `id` | 操作结果 | 文档推断 |
| PUT | `/:id/reset-password` | 管理员 | 重置密码 | path `id`, password 候选 | 操作结果 | 文档推断 |
| PUT | `/:id/status` | 管理员 | 启用/禁用 | path `id`, `status` | 操作结果 | 文档推断 |

关联表候选：`user`。证据等级：数据库文档确认。  
真实路径、请求字段、是否允许空路径映射：待源码确认。

## 7. detection API 候选

前缀候选：`/api/detection`。证据等级：文档推断。

| 方法 | 路径候选 | 权限候选 | 功能 | 主要请求字段候选 | 主要响应字段候选 | 证据等级 |
|---|---|---|---|---|---|---|
| GET | `/models/published` | 登录 | 获取已发布模型 | 无 | 模型列表 | 文档推断 |
| POST | `/detect` | 登录 | 上传图片执行 YOLO 检测 | image file, `model_id`, `confidence_threshold` | result image, `detection_result` | 文档推断 |
| POST | `/enhance-image` | 登录 | CLAHE 增强 | image / image key | enhanced image | 文档推断 |
| POST | `/analyze-defects` | 登录 | Qwen-VL 多模态分析 | image, detection context | `analysis_result` | 文档推断 |
| POST | `/generate-suggestions` | 登录 | 生成治理建议 | `analysis_result` | `suggestions` | 文档推断 |
| POST | `/save` | 登录 | 保存检测记录 | record fields, artifacts, results | record id | 文档推断 |
| POST | `/export-word` | 登录 | 导出 Word 报告 | record id / record payload | docx attachment 或 file info | 文档推断 |
| GET | `/records` | 登录 | 分页查询检测记录 | page, page_size, filters | 分页记录 | 文档推断 |
| GET | `/records/:id` | 登录 | 检测记录详情 | path `id` | record detail | 文档推断 |
| GET | `/records/:id/crops` | 登录 | 目标裁剪图列表 | path `id` | crop list | 文档推断 |
| PUT | `/records/:id` | 登录 | 更新标题/描述 | `title`, `description` | 操作结果 | 文档推断 |
| DELETE | `/records/:id` | 登录 | 删除记录和关联文件 | path `id` | 操作结果 | 文档推断 |

关联表候选：`detection_records`、`detection_crops`、`models`、`user`。证据等级：数据库文档确认。  
与 AI 依赖：YOLO 输出、CLAHE、Qwen-VL 分析字段。证据等级：文档推断 / 已资源确认 / 待源码确认。

## 8. video-detection API 候选

前缀候选：`/api/video-detection`。证据等级：文档推断。

| 方法 | 路径候选 | 权限候选 | 功能 | 主要请求字段候选 | 主要响应字段候选 | 证据等级 |
|---|---|---|---|---|---|---|
| POST | `/detect` | 登录 | 上传视频并创建异步检测任务 | video file, `model_id`, `confidence_threshold`, `frame_rate` | `record_id`, `status` | 文档推断 |
| GET | `/progress/:id` | 登录 | 查询处理进度 | path `id` | `progress`, `status`, frame counters | 文档推断 |
| GET | `/records` | 登录 | 分页查询视频记录 | page, page_size, filters | 分页记录 | 文档推断 |
| GET | `/records/:id` | 登录 | 视频记录详情 | path `id` | record detail, frames, artifacts | 文档推断 |
| PUT | `/records/:id` | 登录 | 更新标题/描述 | `title`, `description` | 操作结果 | 文档推断 |
| DELETE | `/records/:id` | 登录 | 删除记录和关联视频文件 | path `id` | 操作结果 | 文档推断 |

关联表候选：`video_detection_records`、`video_detection_frames`、`models`、`user`。证据等级：数据库文档确认。  
视频任务实现方式：文档描述多进程异步，当前无源码证据。证据等级：文档推断 / 待源码确认。

## 9. realtime-detection API 候选

前缀候选：`/api/realtime-detection`。证据等级：文档推断。

| 方法 | 路径候选 | 权限候选 | 功能 | 主要请求字段候选 | 主要响应字段候选 | 证据等级 |
|---|---|---|---|---|---|---|
| POST | `/detect` | 登录 | 发送 Base64 帧并执行 ByteTrack 检测 | `image_data`, `session_id`, `model_id`, `confidence_threshold` | `result_image`, `new_detections` | 文档推断 |
| POST | `/reset-tracker` | 登录 | 重置 tracker | `session_id` 候选 | 操作结果 | 文档推断 |
| GET | `/sessions` | 登录 | 会话列表 | filters | session list, detection counts | 文档推断 |
| GET | `/records` | 登录 | 实时检测记录 | `session_id` filter | record list | 文档推断 |
| DELETE | `/sessions/:session_id` | 登录 | 删除会话及记录 | path `session_id` | 操作结果 | 文档推断 |
| DELETE | `/records/:id` | 登录 | 删除单条记录 | path `id` | 操作结果 | 文档推断 |

关联表候选：`realtime_detection_sessions`、`realtime_detection_detections`、`models`、`user`。证据等级：数据库文档确认。  
限制：仅支持本地 USB 摄像头，不支持网络摄像头。证据等级：文档推断。

## 10. dataset API 候选

前缀候选：`/api/dataset`。证据等级：文档推断。

| 方法 | 路径候选 | 权限候选 | 功能 | 主要请求字段候选 | 主要响应字段候选 | 证据等级 |
|---|---|---|---|---|---|---|
| POST | `/upload` | 管理员 | 上传 ZIP 数据集并验证 | zip file, `name`, `description` | dataset id, status | 文档推断 |
| GET | `/list` | 登录 | 获取数据集列表 | filters | dataset list | 文档推断 |
| GET | `/:id` | 登录 | 数据集详情 | path `id` | dataset detail, `structure_info` | 文档推断 |
| PUT | `/:id` | 管理员 | 更新数据集 | `name`, `description` | 操作结果 | 文档推断 |
| DELETE | `/:id` | 管理员 | 删除数据集及 ZIP | path `id` | 操作结果 | 文档推断 |
| GET | `/:id/download` | 管理员 | 下载数据集 ZIP | path `id` | file download | 文档推断 |

关联表候选：`datasets`。证据等级：数据库文档确认。  
数据集 ZIP 测试资源：`4测试包/数据集/small_dataset.zip`。证据等级：已资源确认。

## 11. model API 候选

前缀候选：`/api/model`。证据等级：文档推断。

| 方法 | 路径候选 | 权限候选 | 功能 | 主要请求字段候选 | 主要响应字段候选 | 证据等级 |
|---|---|---|---|---|---|---|
| POST | `/create` | 管理员 | 创建模型记录 | `name`, `dataset_id`, `base_model`, `description` | model id | 文档推断 |
| GET | `/list` | 登录 | 模型列表 | filters | model list | 文档推断 |
| GET | `/datasets` | 登录 | 已使用数据集列表 | filters | dataset list | 文档推断 |
| GET | `/base-models` | 登录 | 基础权重列表 | 无 | base model list | 文档推断 / 已资源确认 |
| GET | `/classes` | 登录 | 类别配置 | 无 | class list | 文档推断 / 已资源确认 |
| GET | `/:id` | 登录 | 模型详情 | path `id` | model detail | 文档推断 |
| PUT | `/:id` | 管理员 | 更新模型 | model fields | 操作结果 | 文档推断 |
| DELETE | `/:id` | 管理员 | 删除模型 | path `id` | 操作结果 | 文档推断 |
| POST | `/:id/upload-weight` | 管理员 | 上传训练权重 | weight file | model file info | 文档推断 |
| GET | `/:id/export` | 管理员 | 下载权重 | path `id` | file download | 文档推断 |
| POST | `/:id/publish` | 管理员 | 发布模型 | path `id` | status | 文档推断 |
| POST | `/:id/unpublish` | 管理员 | 取消发布 | path `id` | status | 文档推断 |
| POST | `/:id/train-images` | 管理员 | 上传训练样例图 | files | artifact info | 文档推断 |
| POST | `/:id/train-files` | 管理员 | 上传训练结果文件 | files | artifact info | 文档推断 |
| GET | `/:id/train-files/:index/chart-data` | 登录 | 训练曲线数据 | path params | chart data | 文档推断 |

关联表候选：`models`、`datasets`。证据等级：数据库文档确认。  
可见基础权重：`yolov8n.pt`、`yolo11n.pt`、`yolo12n.pt`、`yolo26n.pt`。证据等级：已资源确认。

## 12. evaluation API 候选

前缀候选：`/api/evaluation`。证据等级：文档推断。

| 方法 | 路径候选 | 权限候选 | 功能 | 主要请求字段候选 | 主要响应字段候选 | 证据等级 |
|---|---|---|---|---|---|---|
| GET | `/box-config` | 登录 | 获取框颜色配置 | 无 | color config | 文档推断 |
| POST | `/predict` | 登录 / 管理员候选 | 上传图片与标签并计算指标 | image file, label file, `model_id`, thresholds | predictions, metrics, compare image | 文档推断 |
| POST | `/save` | 登录 | 保存评估记录 | evaluation payload | record id | 文档推断 |
| GET | `/evaluated-models` | 登录 | 获取已评估模型 | filters | model list | 文档推断 |
| GET | `/records` | 登录 | 评估记录列表 | `model_id`, `score_min`, `score_max`, page | record list | 文档推断 |
| GET | `/records/:id` | 登录 | 评估记录详情 | path `id` | record detail | 文档推断 |
| DELETE | `/records/:id` | 登录 | 删除评估记录 | path `id` | 操作结果 | 文档推断 |

关联表候选：`evaluation_records`、`models`、`user`。证据等级：数据库文档确认。  
评估测试资源：40 张图片、40 个标签，类别 ID 仅 `0`。证据等级：已资源确认。

## 13. file / health API 候选

### file API

文档目录结构提到 `routes/file.py`、`clients/file_client.py`、`file_store/`，但未给出完整接口表。

| 方法 | 路径候选 | 权限候选 | 功能 | 证据等级 |
|---|---|---|---|---|
| GET | `/api/file/:bucket/:object_key` | 登录候选 | 读取文件或生成文件响应 | 文档推断 / 待源码确认 |
| POST | `/api/file/upload` | 登录候选 | 通用上传 | 文档推断 / 待源码确认 |
| DELETE | `/api/file/:bucket/:object_key` | 登录候选 | 删除文件 | 文档推断 / 待源码确认 |

以上路径只是候选，不得作为已实现接口。

### health API

文档目录结构提到 `routes/health.py`，但未给出接口表。

| 方法 | 路径候选 | 权限候选 | 功能 | 证据等级 |
|---|---|---|---|---|
| GET | `/api/health` | 公开候选 | 服务健康检查 | 文档推断 / 待源码确认 |
| GET | `/api/health/db` | 公开或管理员候选 | DB 连通性检查 | 待源码确认 |

## 14. 待源码确认项

- Flask app 启动入口与 Blueprint 注册。
- 所有 API 的真实路径、方法、权限、请求字段、响应字段。
- 统一响应工具是否存在，以及 `code/msg/data` 是否全局一致。
- 错误响应格式、HTTP 状态码与业务 `code` 映射。
- JWT 签发、校验、过期时间、密钥来源、Header 解析。
- 普通用户数据隔离是否在 SQL 查询层落实。
- 文件访问 API、静态文件暴露方式、URL 生成规则。
- 图片检测、视频检测、实时检测、模型评估的真实字段。
- Qwen-VL 调用接口、超时、重试、降级与脱敏日志。
- Word 报告导出接口是直接附件还是返回文件引用。

## 15. 与 Frontend / AI / Docs 的依赖

| 依赖方 | 后端契约依赖点 | 当前状态 |
|---|---|---|
| Frontend | API 路径、统一响应、错误码、JWT、分页结构、文件 URL、`detection_result` | 文档推断 / 待源码确认 |
| AI | YOLO 输出字段、类别定义、bbox 格式、Qwen-VL 输入上下文、评估指标 | 已资源确认 + 文档推断 / 待源码确认 |
| Docs/Test | DB 字段、接口清单、文件存储、状态枚举、冒烟测试入口 | 数据库文档确认 + 文档推断 / 待源码确认 |

协作原则：Phase 2A 只冻结候选契约；Phase 2B 补齐源码后必须重新审计并将字段升级为“已源码确认”或标记“冲突/差异”。

