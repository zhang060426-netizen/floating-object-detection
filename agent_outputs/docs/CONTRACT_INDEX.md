# Contract Index

更新时间：2026-05-13  
阶段：Phase 2A：系统契约与重建基线  
边界：本文件只索引契约责任、状态和证据等级；不创建业务代码、不修改数据库。

## 1. 契约文件总览

| 契约文件 | 目标位置 | 主责 | 当前状态 | 证据等级 |
|---|---|---|---|---|
| API_CONTRACT | `agent_outputs/backend/API_CONTRACT.md` | Backend Agent | 待 Backend 输出 | 待源码确认 |
| DETECTION_RESULT_SCHEMA | `agent_outputs/backend/DETECTION_RESULT_SCHEMA.md` | Backend Agent + AI Agent | 待 Backend 输出 | 待源码确认 |
| AI_OUTPUT_SCHEMA | `agent_outputs/ai/AI_OUTPUT_SCHEMA.md` | AI Agent | 待 AI 输出 | 已资源确认 |
| DB_CONTRACT | `agent_outputs/backend/DB_CONTRACT.md` | Backend Agent + Docs/Test | 待 Backend 输出 | 数据库文档确认 |
| FRONTEND_PAGE_MAP | `agent_outputs/frontend/FRONTEND_PAGE_MAP.md` | Frontend Agent | 待 Frontend 输出 | 待源码确认 |
| FILE_STORAGE_CONTRACT | `agent_outputs/backend/FILE_STORAGE_CONTRACT.md` | Backend Agent | 待 Backend 输出 | 数据库文档确认 |
| QWEN_VL_ANALYSIS_SCHEMA | `agent_outputs/ai/QWEN_VL_ANALYSIS_SCHEMA.md` | AI Agent | 待 AI 输出 | 待源码确认 |
| EVALUATION_METRICS_SCHEMA | `agent_outputs/ai/EVALUATION_METRICS_SCHEMA.md` | AI Agent | 待 AI 输出 | 历史输出确认 |

## 2. API_CONTRACT 索引

| 子项 | 覆盖范围 | 来源 | 当前状态 | 证据等级 |
|---|---|---|---|---|
| 用户 API | `/api/user` 登录、注册、当前用户、用户管理 | `3项目文档/1系统介绍文档.md` | 文档候选，待 routes 确认 | 文档推断 |
| 图片检测 API | `/api/detection` 检测、增强、分析、建议、保存、导出、记录 | 系统介绍文档 | 文档候选，待 routes 确认 | 文档推断 |
| 视频检测 API | `/api/video-detection` 创建任务、进度、记录 | 系统介绍文档 | 文档候选，待 routes 确认 | 文档推断 |
| 实时检测 API | `/api/realtime-detection` 帧检测、tracker、会话、记录 | 系统介绍文档 | 文档候选，待 routes 确认 | 文档推断 |
| 数据集/模型/评估 API | dataset、model、evaluation 模块 | 系统介绍文档 | 文档候选，待 routes 确认 | 文档推断 |

## 3. DETECTION_RESULT_SCHEMA 索引

| 子项 | 覆盖范围 | 来源 | 当前状态 | 证据等级 |
|---|---|---|---|---|
| 图片检测结果 | 类别、置信度、bbox、裁剪图、标注图 | 系统介绍、DB 文档 | 字段候选，待推理源码确认 | 待源码确认 |
| 视频帧检测结果 | frame_index、timestamp、detections、关键帧 | DB 文档、AI_PIPELINE_ANALYSIS | 字段候选，待视频源码确认 | 待源码确认 |
| 实时检测结果 | track_id、frame_number、bbox、截图、裁剪图 | DB 文档、系统介绍 | 字段候选，待实时源码确认 | 待源码确认 |

## 4. AI_OUTPUT_SCHEMA 索引

| 子项 | 覆盖范围 | 来源 | 当前状态 | 证据等级 |
|---|---|---|---|---|
| YOLO 类别 | `class_id=0`、`floating_object` | `data.yaml` | 已可资源确认 | 已资源确认 |
| YOLO bbox | `xyxy`、`xywhn`、confidence 候选 | AI 审计、Ultralytics 脚本使用 | 待应用源码确认 | 已资源确认 |
| 模型信息 | model_name、weight_path、imgsz、threshold、device | AI 审计 | 候选字段 | 已资源确认 |

## 5. DB_CONTRACT 索引

| 子项 | 覆盖范围 | 来源 | 当前状态 | 证据等级 |
|---|---|---|---|---|
| 10 张核心表 | user、datasets、models、detection_records 等 | `3项目文档/5数据库开发文档.md` | 文档定义完整 | 数据库文档确认 |
| 字段/索引/外键 | 表结构、索引、外键关系 | DB 文档 | 待实际 DB 初始化确认 | 数据库文档确认 |
| 初始化数据 | admin/test、默认数据集、默认模型 | DB 文档、使用注意事项 | 待实际 DB 确认 | 数据库文档确认 |

## 6. FRONTEND_PAGE_MAP 索引

| 子项 | 覆盖范围 | 来源 | 当前状态 | 证据等级 |
|---|---|---|---|---|
| 登录/注册/个人中心 | 用户入口与账户功能 | 系统介绍、Frontend Phase 1 | 文档候选 | 文档推断 |
| 图片/视频/实时检测 | 核心检测页面 | 系统介绍、架构文档 | 文档候选 | 文档推断 |
| 管理页面 | 用户、模型、数据集、评估管理 | 系统介绍 | 文档候选 | 文档推断 |
| 前端源码入口 | `index.html`、`vite.config.*`、`src/main.*` | Frontend Phase 1 | 当前缺失 | 冲突/差异 |

## 7. FILE_STORAGE_CONTRACT 索引

| 子项 | 覆盖范围 | 来源 | 当前状态 | 证据等级 |
|---|---|---|---|---|
| 图片对象 | 原图、结果图、增强图、裁剪图 | DB 文档字段 | 待存储实现确认 | 数据库文档确认 |
| 视频对象 | 原视频、结果视频、关键帧 | DB 文档字段 | 待存储实现确认 | 数据库文档确认 |
| 报告对象 | Word 报告导出 | 系统介绍文档 | 待后端源码确认 | 文档推断 |
| 模型/数据集对象 | 权重、训练文件、数据集 zip | DB 文档、测试资源 | 待后端源码确认 | 数据库文档确认 |

## 8. QWEN_VL_ANALYSIS_SCHEMA 索引

| 子项 | 覆盖范围 | 来源 | 当前状态 | 证据等级 |
|---|---|---|---|---|
| 分析输入 | 原图/增强图、YOLO 检测结果、prompt | 系统介绍、AI_PIPELINE_ANALYSIS | 文档候选 | 文档推断 |
| 分析输出 | 污染描述、风险分析、治理建议 | 系统介绍、PROJECT_CONTEXT | 文档候选 | 文档推断 |
| 配置位置 | `web-flask/algo/llm/config.py` | 使用注意事项 | 当前文件缺失 | 冲突/差异 |

## 9. EVALUATION_METRICS_SCHEMA 索引

| 子项 | 覆盖范围 | 来源 | 当前状态 | 证据等级 |
|---|---|---|---|---|
| 核心指标 | precision、recall、mAP50、avg_iou | DB 文档、系统介绍 | 字段候选 | 数据库文档确认 |
| 历史模型指标 | precision 0.889、recall 0.827、mAP50 0.915、mAP50-95 0.659 | AI 历史 output | 历史结果确认 | 历史输出确认 |
| 评估资源 | 40 张评估图片、40 个标签 | `4测试包/` | 资源确认 | 已资源确认 |

## 10. 每份契约责任人

| 契约 | 主责 | 协作 | Leader 关注点 | 证据等级 |
|---|---|---|---|---|
| API_CONTRACT | Backend | Frontend、Docs/Test | 不得声明 routes 已实现 | 待源码确认 |
| DETECTION_RESULT_SCHEMA | Backend | AI、Frontend、Docs/Test | 必须兼容图片/视频/实时 | 待源码确认 |
| AI_OUTPUT_SCHEMA | AI | Backend、Docs/Test | 不改变类别和权重 | 已资源确认 |
| DB_CONTRACT | Backend | Docs/Test | 不修改 DB，只做契约草案 | 数据库文档确认 |
| FRONTEND_PAGE_MAP | Frontend | Backend、Docs/Test | 不创建页面源码 | 文档推断 |
| FILE_STORAGE_CONTRACT | Backend | Docs/Test | 不移动资源文件 | 数据库文档确认 |
| QWEN_VL_ANALYSIS_SCHEMA | AI | Backend、Docs/Test | 标注配置缺失 | 待源码确认 |
| EVALUATION_METRICS_SCHEMA | AI | Backend、Frontend、Docs/Test | 区分历史指标与新测试结果 | 历史输出确认 |

## 11. 每份契约当前状态

| 契约 | 当前状态 | 阻塞项 | Phase 2B 前要求 | 证据等级 |
|---|---|---|---|---|
| API_CONTRACT | 待输出 | 后端 routes 缺失 | 草案完成并通过 Frontend review | 待源码确认 |
| DETECTION_RESULT_SCHEMA | 待输出 | 推理封装缺失 | 草案完成并通过 AI/Frontend review | 待源码确认 |
| AI_OUTPUT_SCHEMA | 待输出 | 应用封装缺失 | 明确离线输出与应用输出边界 | 已资源确认 |
| DB_CONTRACT | 待输出 | DB 初始化缺失 | 文档字段完整索引 | 数据库文档确认 |
| FRONTEND_PAGE_MAP | 待输出 | `src/` 缺失 | 页面/API 候选矩阵 | 文档推断 |
| FILE_STORAGE_CONTRACT | 待输出 | 存储实现缺失 | bucket/object_key 候选规范 | 数据库文档确认 |
| QWEN_VL_ANALYSIS_SCHEMA | 待输出 | LLM 配置源码缺失 | 字段草案与错误降级草案 | 待源码确认 |
| EVALUATION_METRICS_SCHEMA | 待输出 | 评估 API 缺失 | metrics 字段草案 | 历史输出确认 |

## 12. 每份契约证据等级

| 契约 | 最高可用证据等级 | 不可声明内容 | 证据等级 |
|---|---|---|---|
| API_CONTRACT | 文档推断 | 不可声明接口已实现 | 文档推断 |
| DETECTION_RESULT_SCHEMA | 文档推断 + 已资源确认 | 不可声明真实 JSON 字段已确认 | 待源码确认 |
| AI_OUTPUT_SCHEMA | 已资源确认 | 不可声明后端应用输出一致 | 已资源确认 |
| DB_CONTRACT | 数据库文档确认 | 不可声明实际 DB 已创建 | 数据库文档确认 |
| FRONTEND_PAGE_MAP | 文档推断 | 不可声明页面源码存在 | 文档推断 |
| FILE_STORAGE_CONTRACT | 数据库文档确认 | 不可声明真实目录/URL 规则 | 数据库文档确认 |
| QWEN_VL_ANALYSIS_SCHEMA | 文档推断 | 不可声明配置文件存在 | 待源码确认 |
| EVALUATION_METRICS_SCHEMA | 历史输出确认 | 不可声明本轮评估已执行 | 历史输出确认 |
