# Backend Phase 1 Audit

## 1. 已确认事实

本次审计范围为：

- 根目录协作文档与规划文档
- `3项目文档/1系统介绍文档.md`
- `3项目文档/5数据库开发文档.md`
- `1项目代码/floating-objects-detect-web/web-flask/`

已由当前工作区源码确认的事实：

| 项目 | 结论 | 依据 |
|---|---|---|
| 后端目录位置 | `1项目代码/floating-objects-detect-web/web-flask/` 存在 | 文件系统 |
| 后端目录内容 | 当前仅发现 `requirements.txt` 与 `1须知.txt` | 文件系统 |
| Flask 应用入口 | 未发现 `app.py` | `rg --files` / 目录枚举 |
| 配置文件 | 未发现 `config.py` 或配置目录 | `rg --files` / 目录枚举 |
| 路由目录 | 未发现 `routes/` | 目录枚举 |
| 服务层目录 | 未发现 `services/` | 目录枚举 |
| 模型/实体目录 | 未发现 `models/` | 目录枚举 |
| DAO/Repository 目录 | 未发现 `dao/` | 目录枚举 |
| 算法封装目录 | 未发现 `algo/` | 目录枚举 |
| 工具目录 | 未发现 `utils/` | 目录枚举 |
| SQLite 数据库文件 | 未发现 `.db` / `.sqlite` / `.sqlite3` | `rg --files` |
| 后端 Python 源码 | `web-flask` 内未发现 `.py` 文件 | `rg --files -g "*.py"` |
| 后端依赖意图 | 存在 Flask-CORS、PyJWT、ultralytics、openai、python-docx、lap 等依赖 | `requirements.txt` |

当前工作区可见 Python 源码只出现在 AI 训练目录：

- `1项目代码/floating-objects-detect-web/other/model_train/detect/code/train.py`
- `1项目代码/floating-objects-detect-web/other/model_train/detect/code/val.py`
- `1项目代码/floating-objects-detect-web/other/model_train/detect/code/predict.py`

因此，本阶段无法从 Flask 源码确认 API 实现、服务层、数据库初始化、JWT 实现、视频任务实现、实时检测实现或模型调用封装。

## 2. 文档推断

以下内容来自项目文档、数据库开发文档、架构文档和规划文档，尚未由 `web-flask` 源码确认。

### 2.1 期望后端结构

文档描述的后端结构候选为：

```text
web-flask/
├── algo/
│   └── llm/
├── routes/
│   ├── health.py
│   ├── user.py
│   ├── detection.py
│   ├── video_detection.py
│   ├── realtime_detection.py
│   ├── dataset.py
│   ├── model.py
│   └── file.py
├── services/
├── utils/
├── clients/
├── weights/
├── file_store/
├── temp/
├── app.py
├── config.py
└── yyxz_sqlite.db
```

当前实际源码未提供上述目录和文件。

### 2.2 API 模块候选

| 模块 | API 前缀 | 主要职责 | 状态 |
|---|---|---|---|
| user | `/api/user` | 登录、注册、JWT、用户管理、权限控制 | 文档推断 |
| detection | `/api/detection` | 图片检测、CLAHE、Qwen-VL 分析、治理建议、报告导出、检测记录 | 文档推断 |
| video-detection | `/api/video-detection` | 视频上传、异步检测任务、进度查询、视频记录 | 文档推断 |
| realtime-detection | `/api/realtime-detection` | Base64 帧检测、ByteTrack、会话和实时检测记录 | 文档推断 |
| dataset | `/api/dataset` | ZIP 数据集上传、结构验证、数据集管理 | 文档推断 |
| model | `/api/model` | 模型创建、权重上传、发布、训练产物文件管理 | 文档推断 |
| evaluation | `/api/evaluation` | GT 标签对比、模型预测、指标计算、评估记录 | 文档推断 |

### 2.3 API-服务-数据库映射候选

| API 模块 | 服务候选 | 关联数据库表 | 状态 |
|---|---|---|---|
| user | `user_service`, `jwt_util`, `security_utils` | `user` | 文档推断 |
| detection | 图片上传、YOLO 推理、CLAHE、Qwen-VL、Word 导出服务 | `detection_records`, `detection_crops`, `models`, `user` | 文档推断 |
| video-detection | 视频任务、帧采样、关键帧、进度更新服务 | `video_detection_records`, `video_detection_frames`, `models`, `user` | 文档推断 |
| realtime-detection | 实时帧检测、ByteTrack、会话管理服务 | `realtime_detection_sessions`, `realtime_detection_detections`, `models`, `user` | 文档推断 |
| dataset | ZIP 上传、YOLO 数据集结构验证服务 | `datasets` | 文档推断 |
| model | 模型生命周期、权重文件、发布状态服务 | `models`, `datasets` | 文档推断 |
| evaluation | 标签解析、IoU 匹配、指标计算、对比图生成服务 | `evaluation_records`, `models`, `user` | 文档推断 |

### 2.4 数据库表关系候选

数据库开发文档定义 10 张核心表：

- `user`
- `datasets`
- `models`
- `detection_records`
- `detection_crops`
- `video_detection_records`
- `video_detection_frames`
- `evaluation_records`
- `realtime_detection_sessions`
- `realtime_detection_detections`

关系候选：

| 关系 | 含义 | 状态 |
|---|---|---|
| `user` -> `detection_records` | 一个用户有多条图片检测记录 | 数据库文档确认，源码待确认 |
| `user` -> `video_detection_records` | 一个用户有多条视频检测记录 | 数据库文档确认，源码待确认 |
| `user` -> `realtime_detection_sessions` | 一个用户有多个实时检测会话 | 数据库文档确认，源码待确认 |
| `user` -> `evaluation_records` | 一个用户有多条评估记录 | 数据库文档确认，源码待确认 |
| `datasets` -> `models` | 一个数据集可用于多个模型 | 数据库文档确认，源码待确认 |
| `models` -> 检测/视频/实时/评估记录 | 模型被各业务模块引用 | 数据库文档确认，源码待确认 |
| `detection_records` -> `detection_crops` | 一条图片检测记录包含多个裁剪目标 | 数据库文档确认，源码待确认 |
| `video_detection_records` -> `video_detection_frames` | 一条视频记录包含多个关键帧 | 数据库文档确认，源码待确认 |
| `realtime_detection_sessions` -> `realtime_detection_detections` | 一个实时会话包含多条检测记录 | 数据库文档确认，源码待确认 |

### 2.5 共享契约候选

#### detection_result 候选

```json
{
  "objects": [
    {
      "object_index": 0,
      "class_id": 0,
      "class_name": "floating_object",
      "chinese_name": "漂浮物",
      "confidence": 0.89,
      "bbox": [0, 0, 100, 100],
      "bbox_format": "xyxy_pixel"
    }
  ],
  "summary": {
    "total_objects": 1,
    "confidence_threshold": 0.5
  }
}
```

说明：候选结构由图片检测、裁剪图、视频帧和实时检测文档综合推断。真实字段名、是否为数组根结构、是否包含图片尺寸/模型名/裁剪图引用，待源码确认。

#### JWT 字段候选

```json
{
  "user_id": 1,
  "role": 1,
  "exp": 1234567890
}
```

说明：文档明确提到 JWT payload 包含 `user_id`、`role`、`exp`。是否包含 `username`、`status`、`iat`、token 类型、刷新机制，待源码确认。

#### evaluation metrics 候选

```json
{
  "precision": 0.889,
  "recall": 0.827,
  "mAP50": 0.915,
  "avg_iou": 0.76,
  "iou_threshold": 0.5,
  "gt_count": 10,
  "pred_count": 9,
  "match_count": 8
}
```

说明：数据库文档和系统介绍文档确认 `precision`、`recall`、`mAP50`、`avg_iou` 是强候选字段。`mAP50-95` 出现在模型总体指标中，但未明确为每条评估记录字段，建议作为可选扩展字段。

#### 视频任务状态机候选

| 状态 | DB 数值候选 | 含义 | 状态 |
|---|---:|---|---|
| `pending` | 0 | 已创建，待处理 | 数据库文档确认 |
| `processing` | 1 | 正在处理 | 数据库文档确认 |
| `completed` | 2 | 已完成 | 数据库文档确认 |
| `failed` | 3 | 失败 | 数据库文档确认 |
| `cancelled` | 4 | 用户取消 | 架构/AI 文档建议，数据库文档未定义 |

进度计算候选：

- `processed_frames / total_frames * 100`
- `actual_processed_frames / target_frames * 100`

真实进度字段使用方式、失败原因字段、取消清理策略、后台执行模型待源码确认。

## 3. 待源码确认

### 3.1 后端工程结构

- Flask app 创建方式与启动入口
- Blueprint 注册方式和 URL prefix
- CORS 配置
- 环境变量和配置加载方式
- 文件存储根目录、URL 生成方式、临时目录清理策略
- 是否存在统一响应封装、错误码和异常处理

### 3.2 用户与权限

- JWT 签发字段、过期时间、密钥来源
- `Authorization` Header 解析规则
- `token_required` 或等价鉴权装饰器实现
- 管理员权限判断方式
- 普通用户数据隔离是否在 SQL 层实现
- 密码是否仍使用 MD5，以及是否有 salt 或迁移策略

### 3.3 图片检测

- `/api/detection` 实际路由与请求/响应字段
- YOLO 模型加载与缓存策略
- `detection_result` 真实 JSON 结构
- 原图、结果图、增强图、裁剪图的 bucket/object_key 规则
- Qwen-VL prompt、超时、重试、降级策略
- Word 报告字段和模板

### 3.4 视频检测

- 视频任务使用进程、线程、队列还是同步阻塞
- 任务状态更新位置
- 进度计算真实逻辑
- 关键帧保存策略
- 结果视频编码器和失败回退策略
- 失败原因是否持久化
- 是否支持取消任务

### 3.5 实时检测

- 前端帧上传协议是否为 Base64
- ByteTrack tracker 生命周期
- track_id 去重逻辑
- 模型缓存策略
- 会话开始/停止接口边界
- 摄像头资源释放策略
- 实时检测记录截图和裁剪图存储规则

### 3.6 数据集、模型、评估

- ZIP 数据集验证代码位置和校验规则
- 模型状态变更实现
- 权重上传、导出和发布权限控制
- 评估标签解析逻辑
- IoU 匹配算法和 mAP50 计算方式
- `metrics` 字段真实 JSON 结构

## 4. API/数据库缺失项

### 4.1 API 缺失项

当前 `web-flask` 未提供任何可源码确认的 Flask API 文件。缺失项包括：

- `routes/user.py`
- `routes/detection.py`
- `routes/video_detection.py`
- `routes/realtime_detection.py`
- `routes/dataset.py`
- `routes/model.py`
- `routes/evaluation.py`
- `routes/file.py`
- `routes/health.py`
- 统一响应工具
- 鉴权装饰器
- API 错误码定义
- 请求参数校验
- 文件上传接口实现

### 4.2 服务层缺失项

当前未发现服务层实现。缺失项包括：

- 用户服务
- 图片检测服务
- 视频任务服务
- 实时检测服务
- 数据集验证服务
- 模型生命周期服务
- 模型评估服务
- 文件存储服务
- Qwen-VL 客户端或适配器
- YOLO 推理封装

### 4.3 数据库缺失项

当前未发现 DB 初始化代码或 SQLite 文件。缺失项包括：

- 建表 SQL 执行入口
- 初始化默认用户、默认数据集、默认模型的脚本
- 连接管理工具
- 查询封装或 DAO
- 外键启用策略
- 索引创建脚本
- 数据迁移策略
- 测试数据库或种子数据

### 4.4 契约缺失项

当前缺少源码级契约证据：

- API 统一响应格式是否固定为 `{ code, msg, data }`
- 错误响应格式
- `detection_result` JSON schema
- `metrics` JSON schema
- JWT payload schema
- 文件 bucket/object_key 枚举和值域
- 状态码枚举集中定义

## 5. 风险点

| 风险 | 等级 | 影响 | 建议 |
|---|---:|---|---|
| `web-flask` 源码缺失 | 高 | 无法源码级确认 API、DB、任务状态机和 AI 调用链 | Phase 2 前先补齐或定位真实后端源码 |
| 文档结构与实际目录不一致 | 高 | 多 Agent 可能基于文档误判实现状态 | 所有结论继续标注“源码确认/文档推断” |
| 共享契约未固化 | 高 | 前端、后端、AI、报告可能解析不一致 | 先落地 schema 文档，再实现或对齐代码 |
| 数据库初始化缺失 | 高 | 无法验证字段、索引、外键和默认数据 | 补齐 DB 初始化脚本或提供现有 DB |
| `detection_result` 未确认 | 高 | 影响图片展示、视频关键帧、实时记录、Word 报告和评估 | 由 Backend + AI 共同定义兼容 schema |
| 视频状态机不完整 | 中 | 长任务失败、进度异常、无法取消或恢复 | 明确状态枚举、失败原因、进度公式 |
| JWT 字段未确认 | 中 | 前端权限、接口鉴权、用户隔离可能不一致 | 固化 JWT payload 和鉴权错误格式 |
| Qwen-VL 调用链未确认 | 中 | 分析失败、超时、费用和密钥泄漏风险 | 明确配置、超时、重试、降级和脱敏日志 |
| 实时检测资源管理未确认 | 中 | 摄像头占用、重复入库、性能不可控 | 建立会话生命周期和资源释放验证 |

## 6. Phase 2 建议任务

### 6.1 源码补齐与定位

1. 确认真实 Flask 源码是否遗漏、压缩包未解压或位于其他目录。
2. 补齐或定位 `app.py`、`routes/`、`services/`、`utils/`、数据库初始化代码。
3. 在补齐后重新执行 Backend Phase 1 源码确认，升级本报告中的“文档推断”为“源码确认”。

### 6.2 后端契约固化

1. 输出 API 统一响应契约：成功、失败、鉴权失败、权限不足、参数错误。
2. 输出 JWT payload 契约：字段、类型、过期策略、Header 格式。
3. 输出 `detection_result` schema：图片、视频帧、实时检测是否共用或分版本。
4. 输出 `evaluation metrics` schema：指标字段、类型、取值范围、可选字段。
5. 输出视频任务状态机：状态枚举、DB 值、合法迁移、失败原因、取消策略。

### 6.3 数据库对齐

1. 将 `5数据库开发文档.md` 与实际建表代码逐字段比对。
2. 明确默认数据初始化方式。
3. 明确 bucket/object_key 文件存储约定。
4. 为共享字段建立枚举说明：模型状态、数据集状态、视频任务状态、实时会话状态、用户角色和状态。

### 6.4 可运行基线准备

1. 建立后端启动 checklist。
2. 建立图片检测冒烟测试路径。
3. 建立视频检测任务创建和进度查询冒烟测试路径。
4. 建立实时检测最小会话测试路径。
5. 建立模型评估上传图片和标签的冒烟测试路径。

### 6.5 协作建议

1. Backend 与 AI Agent 先对齐 YOLO 输出字段和 Qwen-VL 分析字段。
2. Backend 与 Frontend Agent 对齐 API 响应格式、状态码和权限错误格式。
3. Backend 与 Docs/Test Agent 对齐数据库字段字典、ER 关系和测试 checklist。
4. 当前阶段不修改数据库结构、不重构业务代码、不替换模型或大模型 API。

