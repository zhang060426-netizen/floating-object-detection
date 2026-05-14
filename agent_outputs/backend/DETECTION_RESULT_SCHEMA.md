# Detection Result Schema Candidate

阶段：Phase 2A：系统契约与重建基线  
角色：Backend Agent  
边界：本文档定义 `detection_result` 候选契约，不代表当前后端已实现；当前 `web-flask` 推理封装源码缺失。

## 1. 设计目标

`detection_result` 候选契约目标：

| 目标 | 说明 | 证据等级 |
|---|---|---|
| 跨图片、视频、实时检测复用核心目标字段 | 降低前端展示、报告、评估解析差异 | 文档推断 |
| 保留 YOLO 原始检测语义 | 类别、置信度、bbox、模型信息可追溯 | 已资源确认 / 文档推断 |
| 支持文件产物关联 | 原图、结果图、增强图、裁剪图、关键帧、结果视频、报告 | 数据库文档确认 / 文档推断 |
| 支持向后兼容 | 新字段追加，避免破坏历史记录 | 文档推断 |
| 清晰标注证据等级 | 防止候选字段被误认为已实现 | Phase 2A 约束 |

当前不能确认真实 `detection_result` JSON 结构。证据等级：待源码确认。

## 2. 适用范围：图片 / 视频 / 实时检测

| 场景 | 存储位置候选 | 用途 | 证据等级 |
|---|---|---|---|
| 图片检测 | `detection_records.detection_result` | 保存一次图片检测的完整检测结果 | 数据库文档确认 |
| 图片裁剪目标 | `detection_crops.bbox` 等字段 | 保存单个目标裁剪信息 | 数据库文档确认 |
| 视频检测总体 | `video_detection_records.detection_result` | 保存视频任务总体检测摘要 | 数据库文档确认 |
| 视频关键帧 | `video_detection_frames.detections` | 保存某一关键帧目标列表 | 数据库文档确认 |
| 实时检测目标 | `realtime_detection_detections.detection_result` | 保存实时目标完整上下文 | 数据库文档确认 |
| 模型评估 | `evaluation_records.detection_result` | 保存预测框结果，用于与 GT 对比 | 数据库文档确认 |

## 3. detection_result 顶层结构候选

| 字段 | 类型候选 | 必填候选 | 说明 | 证据等级 |
|---|---|---:|---|---|
| `schema_version` | string | 是 | 契约版本，例如 `1.0` | 文档推断 |
| `source_type` | string enum | 是 | `image` / `video_frame` / `video_summary` / `realtime_frame` / `evaluation` | 文档推断 |
| `model` | object | 是 | 本次检测使用的模型信息 | 文档推断 |
| `image` | object | 否 | 图片或帧尺寸、格式等输入信息 | 文档推断 |
| `detections` | array | 是 | 目标检测列表 | 文档推断 |
| `summary` | object | 是 | 聚合统计 | 文档推断 |
| `artifacts` | object | 否 | 文件产物引用 | 数据库文档确认 / 文档推断 |
| `timing_ms` | object | 否 | 推理、后处理耗时 | 文档推断 |
| `tracker` | object | 否 | 实时检测 / 视频跟踪信息 | 文档推断 |
| `raw` | object | 否 | 保留原始模型输出摘要，不建议前端依赖 | 待源码确认 |

`model` 字段候选：

| 字段 | 类型候选 | 说明 | 证据等级 |
|---|---|---|---|
| `model_id` | string | 业务模型 ID | 数据库文档确认 |
| `model_name` | string | 模型名称 | 数据库文档确认 |
| `base_model` | string | 基础模型类型，如 `yolov8n`、`yolo11n`、`yolo12n`、`yolo26n` | 数据库文档确认 / 已资源确认 |
| `weight_ref` | object | bucket/object_key 或本地权重引用 | 数据库文档确认 / 待源码确认 |
| `confidence_threshold` | number | 置信度阈值 | 数据库文档确认 |

## 4. detection object 字段候选

| 字段 | 类型候选 | 必填候选 | 说明 | 证据等级 |
|---|---|---:|---|---|
| `object_index` | integer | 是 | 目标序号，从 0 开始候选 | 数据库文档确认 |
| `class_id` | integer | 是 | YOLO 类别 ID，当前资源确认 `0` | 已资源确认 |
| `class_name` | string | 是 | 当前资源确认 `floating_object` | 已资源确认 |
| `chinese_name` | string | 是 | 中文名候选：`漂浮物` | 数据库文档确认 / 文档推断 |
| `confidence` | number | 是 | 置信度分数，范围候选 `0..1` | 数据库文档确认 / 文档推断 |
| `bbox` | object | 是 | 坐标框结构 | 数据库文档确认 / 文档推断 |
| `track_id` | integer | 否 | ByteTrack 跟踪 ID，实时检测使用 | 数据库文档确认 |
| `frame_number` | integer | 否 | 实时检测帧号 | 数据库文档确认 |
| `frame_index` | integer | 否 | 视频帧索引 | 数据库文档确认 |
| `timestamp_ms` | integer | 否 | 视频时间戳毫秒候选 | 文档推断 |
| `crop_artifact` | object | 否 | 目标裁剪图引用 | 数据库文档确认 |
| `attributes` | object | 否 | 后续扩展属性 | 文档推断 |

当前类别契约：

| class_id | class_name | chinese_name 候选 | 证据等级 |
|---:|---|---|---|
| 0 | `floating_object` | `漂浮物` | class_id/class_name 已资源确认；中文名数据库文档确认 / 文档推断 |

## 5. bbox 坐标格式候选

主格式候选：

| 字段 | 类型候选 | 必填候选 | 说明 | 证据等级 |
|---|---|---:|---|---|
| `format` | string | 是 | 候选固定为 `xyxy_pixel` | 数据库文档确认 / 文档推断 |
| `x1` | number | 是 | 左上角 x，像素坐标 | 文档推断 |
| `y1` | number | 是 | 左上角 y，像素坐标 | 文档推断 |
| `x2` | number | 是 | 右下角 x，像素坐标 | 文档推断 |
| `y2` | number | 是 | 右下角 y，像素坐标 | 文档推断 |
| `xyxy` | number[4] | 否 | 兼容数据库文档中的 `[x1, y1, x2, y2]` | 数据库文档确认 |
| `xywhn` | number[4] | 否 | YOLO 归一化中心点格式，评估标签兼容候选 | 已资源确认 / 文档推断 |

坐标规则候选：

| 规则 | 说明 | 证据等级 |
|---|---|---|
| 数据库 `bbox` 可保存 `[x1, y1, x2, y2]` | `detection_crops` 与实时检测表均描述 bbox 为 JSON 坐标 | 数据库文档确认 |
| 图片/视频/实时展示优先使用像素坐标 | 前端画框通常需要像素坐标 | 文档推断 |
| 评估标签输入为 YOLO 归一化格式 | 评估文档描述 `x_center, y_center, width, height` 转像素框 | 文档推断 / 已资源确认 |
| 是否同时返回 `xyxy` 与 `xywhn` | 当前后端实现未知 | 待源码确认 |

## 6. summary 字段候选

| 字段 | 类型候选 | 必填候选 | 说明 | 证据等级 |
|---|---|---:|---|---|
| `total_detections` | integer | 是 | 检测目标总数 | 文档推断 |
| `by_class` | object | 是 | 按 `class_name` 聚合数量 | 文档推断 |
| `max_confidence` | number | 否 | 最高置信度 | 文档推断 |
| `avg_confidence` | number | 否 | 平均置信度 | 文档推断 |
| `confidence_threshold` | number | 是 | 本次阈值 | 数据库文档确认 |
| `has_detections` | boolean | 否 | 是否检测到目标 | 文档推断 |

视频汇总扩展候选：

| 字段 | 类型候选 | 说明 | 证据等级 |
|---|---|---|---|
| `total_frames` | integer | 视频总帧数 | 数据库文档确认 |
| `processed_frames` | integer | 已读取帧数 | 数据库文档确认 |
| `target_frames` | integer | 需处理帧数 | 数据库文档确认 |
| `actual_processed_frames` | integer | 实际 AI 处理帧数 | 数据库文档确认 |
| `key_frame_count` | integer | 关键帧数量 | 文档推断 |

实时汇总扩展候选：

| 字段 | 类型候选 | 说明 | 证据等级 |
|---|---|---|---|
| `session_id` | string | 实时检测会话 ID | 数据库文档确认 |
| `new_detection_count` | integer | 当前帧新增入库目标数 | 文档推断 |
| `tracked_count` | integer | 当前帧跟踪目标数 | 文档推断 |

## 7. artifacts 字段候选

`artifacts` 用于承载文件引用，不直接承载二进制内容。

| 字段 | 类型候选 | 适用场景 | 说明 | 证据等级 |
|---|---|---|---|---|
| `original_image` | file_ref | 图片 / 评估 | 原图引用 | 数据库文档确认 |
| `result_image` | file_ref | 图片 | 标注结果图引用 | 数据库文档确认 |
| `enhanced_image` | file_ref | 图片 | CLAHE 增强图引用 | 数据库文档确认 |
| `crops` | file_ref[] | 图片 / 实时 | 裁剪图列表 | 数据库文档确认 |
| `original_video` | file_ref | 视频 | 原始视频引用 | 数据库文档确认 |
| `result_video` | file_ref | 视频 | 结果视频引用 | 数据库文档确认 |
| `key_frames` | file_ref[] | 视频 | 关键帧图片列表 | 数据库文档确认 |
| `compare_image` | file_ref | 评估 | GT / 预测框对比图 | 数据库文档确认 |
| `word_report` | file_ref | 图片报告 | Word 报告引用 | 文档推断 / 待源码确认 |

`file_ref` 候选字段：

| 字段 | 类型候选 | 说明 | 证据等级 |
|---|---|---|---|
| `bucket` | string | 文件存储桶 | 数据库文档确认 |
| `object_key` | string | 文件对象键 | 数据库文档确认 |
| `url` | string | 前端访问 URL | 文档推断 / 待源码确认 |
| `mime_type` | string | 文件 MIME 类型 | 待源码确认 |
| `size_bytes` | integer | 文件大小 | 数据库文档确认 / 待源码确认 |

## 8. 与 AI_OUTPUT_SCHEMA 的关系

| 关系点 | 契约说明 | 证据等级 |
|---|---|---|
| YOLO 原始输出 | AI 输出负责描述模型层字段；`detection_result` 负责业务存储和前端消费字段 | 文档推断 |
| 类别定义 | `class_id=0`、`class_name=floating_object` 来自训练资源 | 已资源确认 |
| bbox | AI 输出可提供模型原始坐标；后端契约建议标准化为 `xyxy_pixel` 并可附带 `xywhn` | 文档推断 |
| Qwen-VL | AI 分析输出不应混入每个 detection object，建议存放于 `analysis_result` / AI 输出契约 | 数据库文档确认 / 文档推断 |
| metrics | 模型评估指标应由 evaluation metrics 契约承载，`detection_result` 只保存预测框 | 数据库文档确认 / 文档推断 |

## 9. 与前端展示的关系

前端消费候选：

| 前端需求 | 后端字段候选 | 证据等级 |
|---|---|---|
| 画检测框 | `detections[].bbox` | 文档推断 |
| 显示目标列表 | `detections[].class_name`, `chinese_name`, `confidence` | 数据库文档确认 / 文档推断 |
| 显示裁剪图 | `artifacts.crops` 或 crop API | 数据库文档确认 / 文档推断 |
| 展示图片检测结果 | `artifacts.result_image`, `summary` | 文档推断 |
| 展示视频进度 | 视频记录字段与 summary frame counters | 数据库文档确认 / 文档推断 |
| 展示实时新增目标 | `track_id`, `new_detection_count`, frame result | 数据库文档确认 / 文档推断 |
| 展示评估对比 | `evaluation_records.metrics`, `compare_image` | 数据库文档确认 |

前端实际解析方式当前无法确认。证据等级：待源码确认。

## 10. 向后兼容策略

| 策略 | 说明 | 证据等级 |
|---|---|---|
| 增加 `schema_version` | 允许后续 schema 演进 | 文档推断 |
| 保留数据库文档中的 `bbox` 数组语义 | 避免破坏历史记录或表字段说明 | 数据库文档确认 / 文档推断 |
| 新字段只追加不重命名 | 例如追加 `bbox.xyxy`、`bbox.xywhn`，不删除旧 `bbox` | 文档推断 |
| 类别定义不变 | 当前阶段不改变 `0: floating_object` | 已资源确认 |
| 文件引用继续使用 bucket/object_key | 与数据库字段保持一致 | 数据库文档确认 |
| 前端不依赖 `raw` 字段 | 原始模型输出仅用于排障 | 文档推断 |

## 11. 待源码确认项

- 后端真实 `detection_result` 顶层是否为对象、数组或字符串。
- 图片检测 `/api/detection/detect` 的真实返回字段。
- `detection_records.detection_result` 保存的是检测列表、完整上下文还是模型原始输出。
- 视频 `video_detection_records.detection_result` 与 `video_detection_frames.detections` 是否共用结构。
- 实时检测 `realtime_detection_detections.detection_result` 是否保存整帧结果或单目标结果。
- 评估 `evaluation_records.detection_result` 是否只保存预测框。
- bbox 坐标是否为像素 `xyxy`、归一化 `xywh`，或两者都有。
- 中文类别名是否由后端写入，还是前端映射。
- 文件产物是否直接在 `detection_result` 中返回，还是只通过独立表字段返回。
- Qwen-VL 分析结果是否与 `detection_result` 同时返回，还是作为 `analysis_result` 独立字段。

