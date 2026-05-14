# Backend Source Recovery Tasks

阶段：Phase 2A：系统契约与重建基线  
角色：Backend Agent  
边界：本文档只列后端源码恢复任务，不补写源码、不创建 Flask 文件、不修改数据库。

## 1. 当前后端源码缺失清单

当前实际目录：

```text
1项目代码/floating-objects-detect-web/web-flask/
├─ requirements.txt
└─ 1须知.txt
```

缺失清单：

| 缺失项 | 文档期望 | 当前状态 | 证据等级 |
|---|---|---|---|
| Flask 启动入口 | `app.py` | 未发现 | 冲突/差异 |
| 配置文件 | `config.py` | 未发现 | 冲突/差异 |
| routes | `routes/` | 未发现 | 冲突/差异 |
| services | `services/` | 未发现 | 冲突/差异 |
| DB 工具 | `utils/db.py` 或等价 | 未发现 | 冲突/差异 |
| 数据模型 | `utils/models.py` 或等价 | 未发现 | 冲突/差异 |
| JWT 工具 | `utils/jwt_util.py` | 未发现 | 冲突/差异 |
| 响应工具 | `utils/response.py` | 未发现 | 冲突/差异 |
| 安全工具 | `utils/security_utils.py` | 未发现 | 冲突/差异 |
| LLM 配置 | `algo/llm/config.py` | 未发现 | 冲突/差异 |
| 文件客户端 | `clients/file_client.py` | 未发现 | 冲突/差异 |
| 文件存储目录 | `file_store/` | 未发现 | 冲突/差异 |
| 临时目录 | `temp/` | 未发现 | 冲突/差异 |
| SQLite DB | `yyxz_sqlite.db` | 未发现 | 冲突/差异 |
| 权重目录 | `web-flask/weights/` | 未发现；AI 训练目录有基础权重 | 冲突/差异 / 已资源确认 |

已确认资源：

| 资源 | 状态 | 证据等级 |
|---|---|---|
| `requirements.txt` | 存在，含 Flask-CORS、PyJWT、ultralytics、openai、python-docx、lap | 已资源确认 |
| AI 训练目录基础权重 | `yolov8n.pt`、`yolo11n.pt`、`yolo12n.pt`、`yolo26n.pt` 存在 | 已资源确认 |
| 测试包 | 图片、视频、评估图片/标签、small_dataset.zip 存在 | 已资源确认 |

## 2. 必须恢复的启动入口

恢复目标不是本阶段实现，而是 Phase 2B 前必须找到或恢复真实源码。

| 任务 | 最小证据 | 证据等级目标 |
|---|---|---|
| 定位 Flask 启动入口 | 找到真实 `app.py` 或等价启动模块路径 | 已源码确认 |
| 确认应用创建方式 | 能说明 Flask app、CORS、Blueprint 注册位置 | 已源码确认 |
| 确认运行端口与配置 | 能说明是否使用 `5000`、debug、环境变量 | 已源码确认 |
| 确认依赖安装方式 | `requirements.txt` 可对应源码 import | 已源码确认 / 已资源确认 |
| 确认健康检查或最小启动验证方式 | 存在 health route 或启动日志 | 已源码确认 |

当前状态：全部待源码确认。

## 3. 必须恢复的 routes

| route 文件候选 | API 前缀候选 | 必须确认内容 | 证据等级目标 |
|---|---|---|---|
| `routes/health.py` | `/api/health` 候选 | 健康检查路径、返回结构 | 已源码确认 |
| `routes/user.py` | `/api/user` | 登录、注册、当前用户、用户管理、权限 | 已源码确认 |
| `routes/detection.py` | `/api/detection` | 图片检测、增强、分析、建议、保存、报告、记录 | 已源码确认 |
| `routes/video_detection.py` | `/api/video-detection` | 视频任务、进度、记录、删除 | 已源码确认 |
| `routes/realtime_detection.py` | `/api/realtime-detection` | 实时检测、tracker、会话、记录 | 已源码确认 |
| `routes/dataset.py` | `/api/dataset` | 数据集上传、验证、列表、下载、删除 | 已源码确认 |
| `routes/model.py` | `/api/model` | 模型创建、权重、发布、训练产物、类别 | 已源码确认 |
| `routes/evaluation.py` | `/api/evaluation` | 预测、指标、保存、查询、删除 | 已源码确认 |
| `routes/file.py` | `/api/file` 候选 | 文件访问、上传下载、鉴权 | 已源码确认 |

恢复后重新审计：

- 实际路径是否与 `API_CONTRACT.md` 一致。
- 请求字段是否与候选契约冲突。
- 返回结构是否统一。
- 权限控制是否与文档一致。

## 4. 必须恢复的 services

| 服务候选 | 业务职责 | 必须确认内容 | 证据等级目标 |
|---|---|---|---|
| 用户服务 | 用户查询、创建、密码、状态 | 数据隔离、密码处理、角色判断 | 已源码确认 |
| 图片检测服务 | 图片保存、YOLO 推理、裁剪、增强、记录 | `detection_result` 真实结构 | 已源码确认 |
| 视频检测服务 | 异步任务、抽帧、推理、进度、结果视频 | 状态机与失败处理 | 已源码确认 |
| 实时检测服务 | 帧处理、ByteTrack、会话、去重入库 | tracker 生命周期、资源释放 | 已源码确认 |
| 数据集服务 | ZIP 上传、结构验证、状态更新 | 验证规则、失败原因 | 已源码确认 |
| 模型服务 | 模型状态、权重、发布、训练产物 | 发布门禁、权重路径 | 已源码确认 |
| 评估服务 | 标签解析、预测、IoU、指标、对比图 | metrics 真实结构 | 已源码确认 |
| 文件服务 | bucket/object_key、URL、删除 | 路径规则、权限、清理 | 已源码确认 |
| 报告服务 | Word 报告生成 | 模板字段、返回方式 | 已源码确认 |

当前状态：所有服务层均未发现，证据等级为冲突/差异。

## 5. 必须恢复的 DB 初始化 / DAO

| 任务 | 必须确认内容 | 证据等级目标 |
|---|---|---|
| DB 连接管理 | SQLite 文件路径、连接生命周期、外键开关 | 已源码确认 |
| 建表初始化 | 10 张表是否与 `DB_CONTRACT.md` 一致 | 已源码确认 |
| 默认数据初始化 | `admin/test`、默认数据集、默认模型是否创建 | 已源码确认 |
| DAO 或查询封装 | SQL 位置、参数化、防注入策略 | 已源码确认 |
| 索引创建 | 文档索引是否真实创建 | 已源码确认 |
| JSON 字段处理 | `detection_result`、`metrics`、`structure_info` 编解码 | 已源码确认 |
| 删除策略 | DB 删除与文件删除是否一致 | 已源码确认 |

禁止事项：Phase 2A 不创建 DB、不写迁移脚本、不修改表结构。

## 6. 必须恢复的鉴权与 JWT 实现

| 任务 | 必须确认内容 | 证据等级目标 |
|---|---|---|
| JWT 签发 | payload 字段、过期时间、密钥来源 | 已源码确认 |
| JWT 校验 | Header 格式、异常处理、过期处理 | 已源码确认 |
| 权限装饰器 | 登录必需、管理员必需、错误返回 | 已源码确认 |
| 用户状态校验 | 禁用用户是否拒绝登录/访问 | 已源码确认 |
| 数据隔离 | 普通用户是否只能查询自己的记录 | 已源码确认 |
| 密码处理 | MD5 是否真实使用，是否有 salt 或迁移 | 已源码确认 |

候选字段 `user_id`、`role`、`exp` 当前仅为文档推断；`role/status` 来自数据库文档确认。

## 7. 必须恢复的 YOLO 推理封装

| 任务 | 必须确认内容 | 证据等级目标 |
|---|---|---|
| 模型加载入口 | 后端如何加载模型权重 | 已源码确认 |
| 模型缓存 | 是否懒加载、是否按 `model_id` 缓存 | 已源码确认 |
| 图片推理 | 输入预处理、阈值、输出字段 | 已源码确认 |
| 视频逐帧推理 | 抽帧策略、处理帧率、结果写入 | 已源码确认 |
| 实时 track | ByteTrack 参数、persist、track_id 生成 | 已源码确认 |
| 类别映射 | `0 -> floating_object / 漂浮物` 映射位置 | 已源码确认 / 已资源确认 |
| bbox 格式 | `xyxy`、`xywhn`、像素/归一化 | 已源码确认 |
| 异常处理 | 模型文件缺失、推理失败、空结果 | 已源码确认 |

AI 资源确认：类别 `floating_object` 与基础权重存在，但业务推理封装待源码确认。

## 8. 必须恢复的 Qwen-VL 调用链

| 任务 | 必须确认内容 | 证据等级目标 |
|---|---|---|
| 配置位置 | 是否为 `web-flask/algo/llm/config.py` | 已源码确认 |
| API provider | 阿里云百炼 / Qwen-VL 配置 | 已源码确认 |
| 密钥加载 | 环境变量、配置文件、脱敏策略 | 已源码确认 |
| 图片分析 prompt | 污染描述、风险、生态影响、清理建议维度 | 已源码确认 |
| 治理建议 prompt | 立即清理、工艺优化、预防、长期规划等维度 | 已源码确认 |
| 超时和重试 | 超时、限流、失败降级 | 已源码确认 |
| 返回字段 | 文本、结构化字段、raw response | 已源码确认 |
| 日志 | 是否避免记录 API key 和敏感内容 | 已源码确认 |

约束：不得替换大模型 API。证据等级：Phase 2A 边界 / 文档推断。

## 9. 源码恢复后重新审计任务

恢复或定位完整 `web-flask` 源码后，Backend Agent 必须重新执行：

| ID | 任务 | 输出 | 目标证据等级 |
|---|---|---|---|
| BE-R1 | 真实后端目录地图 | 更新 `BE_PHASE1_AUDIT.md` 或新审计文件 | 已源码确认 |
| BE-R2 | API-服务-DB 映射 | 更新 `API_CONTRACT.md`，标注冲突 | 已源码确认 |
| BE-R3 | DB 初始化差异核对 | 更新 `DB_CONTRACT.md` 差异表 | 已源码确认 |
| BE-R4 | `detection_result` 真实结构核对 | 更新 `DETECTION_RESULT_SCHEMA.md` | 已源码确认 |
| BE-R5 | 文件存储路径核对 | 更新 `FILE_STORAGE_CONTRACT.md` | 已源码确认 |
| BE-R6 | JWT 和权限核对 | 更新 `API_CONTRACT.md` 鉴权章节 | 已源码确认 |
| BE-R7 | 视频状态机核对 | 更新 API/DB/任务状态章节 | 已源码确认 |
| BE-R8 | Qwen-VL 调用链核对 | 与 AI Agent 的 AI 输出契约对齐 | 已源码确认 |
| BE-R9 | Phase 2B gate 判定资料 | 提供启动、API、DB、文件、AI 推理证据 | 已源码确认 |

若恢复源码与当前候选契约不一致，不得直接改业务代码；应先标注“冲突/差异”，由 Leader 判断契约修订或源码适配方向。

