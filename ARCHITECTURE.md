# ARCHITECTURE.md

## 1. 架构结论

系统采用前后端分离 + 后端业务/算法一体化 + 本地文件存储 + SQLite 数据库的单体平台架构。当前阶段不建议微服务化或云原生拆分，应优先完成模块边界、工程结构、接口契约、AI 链路和测试文档治理。

## 2. 分层架构

| 层级 | 职责 | 技术/依据 | 待确认项 |
|---|---|---|---|
| 表现层 | 检测、管理、评估、可视化页面 | Vue3、Element Plus、Pinia、ECharts、Axios | 完整 `src/` 页面、路由和状态管理源码缺失 |
| API/业务层 | 用户、检测、视频、实时、模型、数据集、评估、报告 | Flask、JWT、CORS、SQLite | 完整 Flask routes/services/models 源码缺失 |
| AI/算法层 | YOLO 推理、训练脚本、CLAHE、ByteTrack、多模态分析 | Ultralytics、OpenCV、Qwen-VL、训练目录 | 应用内推理封装源码待确认 |
| 数据层 | 用户/模型/数据集/检测/评估/实时记录 | `5数据库开发文档.md` | 实际 DB 初始化、迁移、索引代码待确认 |
| 文件层 | 图片、视频、裁剪图、关键帧、模型权重、报告 | bucket/object_key 模式 | 实际存储目录、命名规则、清理策略待确认 |
| 测试资源层 | 测试图片/视频/评估标签/小数据集 | `4测试包/`、训练目录 | 自动化测试脚本待补 |

## 3. 核心数据流

### 3.1 图片检测流

1. 前端上传图片并选择已发布模型。
2. 后端保存原图，调用 YOLO 推理。
3. YOLO 返回目标框、类别、置信度。
4. 后端保存标注图、目标裁剪图，执行 CLAHE 增强。
5. 后端将原图/增强图 + 检测结果传给 Qwen-VL。
6. Qwen-VL 返回污染描述、风险分析、治理建议。
7. 后端写入 `detection_records`、`detection_crops`。
8. 前端展示结果，并支持 Word 报告导出。

关键共享契约：`detection_result` JSON、目标框坐标格式、类别 ID/类别名、文件存储路径、Word 报告字段。

### 3.2 视频检测流

视频上传 → 创建检测任务 → 后台/子进程异步处理 → 按帧率采样 → YOLO 逐帧检测 → 保存关键帧/结果视频 → 更新进度和状态 → 前端轮询展示。

优化重点：任务状态机、失败恢复、帧采样策略、长视频资源释放、关键帧去重、结果文件生命周期。

### 3.3 实时检测流

本地 USB 摄像头 → 帧读取 → YOLO 实时推理 → ByteTrack 目标跟踪 → 目标去重/会话统计 → 保存实时检测记录 → 前端展示。

已知限制：仅支持本地物理摄像头，不支持网络摄像头；性能受 CPU/GPU、模型大小、帧率和分辨率影响。

## 4. 数据库架构

数据库文档定义 10 张核心表：

| 表 | 作用 |
|---|---|
| `user` | 用户、角色、状态、头像 |
| `datasets` | 数据集上传、验证、状态 |
| `models` | 模型元信息、权重、发布状态 |
| `detection_records` | 图片检测记录 |
| `detection_crops` | 图片检测目标裁剪图 |
| `video_detection_records` | 视频检测任务/记录 |
| `video_detection_frames` | 视频关键帧记录 |
| `evaluation_records` | 模型评估记录和指标 |
| `realtime_detection_sessions` | 实时检测会话 |
| `realtime_detection_detections` | 实时检测目标记录 |

当前阶段保持 SQLite，不做数据库重构；优先补齐 ER 图、字段字典、索引说明、数据生命周期和备份/清理策略。

## 5. 模型与数据集架构

- 数据源：ModelScope `Echo0174/Trash_floater`
- 类别：`0: floating_object`
- 数据规模：总样本 5544，train 4032，valid 907，test 605
- 当前指标：Precision 0.889，Recall 0.827，mAP50 0.915，mAP50-95 0.659
- 训练目录：`other/model_train/detect/`
- 权重：`yolov8n.pt`、`yolo11n.pt`、`yolo12n.pt`、`yolo26n.pt`

## 6. 待源码确认

| 领域 | 当前依据 | 待确认 |
|---|---|---|
| 前端路由/页面 | 系统介绍文档、package.json | `src/router`、views、api 封装、状态管理实现 |
| 后端 API | 系统介绍/API 文档、requirements | Flask routes、鉴权装饰器、服务层、错误码 |
| 推理封装 | 训练脚本、系统文档 | 应用内模型加载、缓存、并发、异常处理 |
| LLM 集成 | 使用注意事项、PROJECT_CONTEXT | `algo/llm/config.py`、prompt 模板、超时/降级策略 |
| 文件存储 | 数据库文档 bucket/object_key | 实际目录、文件清理、URL 生成方式 |
| 测试 | 测试包资源 | 自动化测试入口、评估脚本、CI 方案 |
