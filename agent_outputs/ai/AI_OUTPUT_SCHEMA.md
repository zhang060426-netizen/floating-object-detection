# AI Output Schema

阶段：Phase 2A 系统契约与重建基线  
角色：AI Agent  
边界：本文档仅定义 YOLO 推理输出候选契约，不训练模型、不验证模型、不预测图片、不修改权重、不修改类别定义、不修改 `train.py` / `val.py` / `predict.py`、不修改后端推理代码。

证据等级统一使用：

- 已源码确认：有 `train.py` / `val.py` / `predict.py` 等源码证据。
- 已资源确认：有 `data.yaml`、weights、output、测试包等资源证据。
- 历史输出确认：来自 `output/` 中历史结果、指标文件。
- 文档推断：来自训练文档、系统文档、规划文档。
- 待后端源码确认：必须等 `web-flask` 推理调用链补齐后确认。
- 冲突/差异：脚本、历史输出、文档之间存在不一致。

## 1. 范围与边界

| 项目 | 内容 | 证据等级 |
|---|---|---|
| 覆盖范围 | 图片、视频帧、实时帧中 YOLO 检测结果的 AI 输出候选字段 | 文档推断 |
| 训练目录 | `1项目代码/floating-objects-detect-web/other/model_train/detect/` | 已资源确认 |
| 离线脚本 | `code/train.py`、`code/val.py`、`code/predict.py` | 已源码确认 |
| 类别边界 | 当前仅允许 `class_id=0`、`class_name=floating_object` | 已资源确认 |
| 实现状态 | 当前不是后端真实返回结构，只是 AI 输出候选契约 | 待后端源码确认 |
| 禁止事项 | 不训练、不验证、不预测、不改权重、不改类别、不改 Python 源码 | 文档推断 |

## 2. YOLO 输出来源说明

| 来源 | 当前事实 | 契约影响 | 证据等级 |
|---|---|---|---|
| `train.py` | 加载 `weights/yolo26n.pt`，使用 `dataset/small_dataset/data.yaml`，`epochs=50`，`imgsz=640` | 说明当前脚本可提供模型、数据、imgsz 参考，但不代表业务推理实现 | 已源码确认 |
| `val.py` | 加载 `output/train/weights/best.pt`，使用 `split="test"`，打印 mAP 指标 | 说明验证指标字段可包含 `map50_95`、`map50`、`map75`、`per_class_maps` | 已源码确认 |
| `predict.py` | 加载历史路径 `output/已经训练好的模型和测试结果/train/weights/best.pt`，预测示例图片 | 说明预测输出来自 Ultralytics Results 对象，但当前未执行 | 已源码确认 |
| `data.yaml` | `nc: 1`，`names: ['floating_object']` | class 字段必须兼容单类别配置 | 已资源确认 |
| 历史输出目录 | 存在训练/验证曲线、混淆矩阵、历史指标文本 | artifacts 可引用曲线图、混淆矩阵、批次预测图 | 历史输出确认 |
| `best.pt` 状态 | 历史权重目录下没有真实 `best.pt`，只有占位文件 | 不得声明当前已训练权重存在 | 已资源确认 |
| 脚本与历史输出 | 当前 `train.py` 使用 `small_dataset`/50 epochs，历史 `args.yaml` 使用 `all_dataset`/100 epochs | 不得把当前脚本参数等同于历史训练参数 | 冲突/差异 |

## 3. 模型信息字段候选

| 字段 | 类型候选 | 含义 | 必填候选 | 证据等级 |
|---|---|---|---|---|
| `schema_version` | string | AI 输出 schema 版本，例如 `ai_output.v1` | 是 | 文档推断 |
| `model_id` | string/integer/null | 后端模型记录 ID | 是，业务返回时 | 待后端源码确认 |
| `model_name` | string/null | 后端展示模型名 | 是，业务返回时 | 待后端源码确认 |
| `weight_path` | string/null | 实际加载权重路径 | 是，调试/审计字段 | 待后端源码确认 |
| `weight_name` | string | 权重文件名，如 `yolo26n.pt` 或 `best.pt` | 是 | 已源码确认 + 待后端源码确认 |
| `base_model` | string/null | 基础模型类型，如 `yolov8n`、`yolo11n`、`yolo12n`、`yolo26n` | 可选 | 已资源确认 |
| `class_map` | object | 类别映射，例如 `{ "0": "floating_object" }` | 是 | 已资源确认 |
| `imgsz` | integer | 推理图像尺寸，脚本使用 640 | 是 | 已源码确认 |
| `conf_threshold` | number/null | 置信度阈值 | 是，业务推理时 | 待后端源码确认 |
| `iou_threshold` | number/null | NMS 或评估 IoU 阈值；历史训练参数中有 `iou: 0.7` | 可选 | 历史输出确认 |
| `device` | string/null | 推理设备，如 `cpu`、`cuda:0` | 可选 | 待后端源码确认 |
| `runtime` | string/null | 推理库/版本，例如 `ultralytics` | 可选 | 已源码确认 |
| `is_published` | boolean/null | 模型是否已发布可用于检测 | 可选 | 文档推断 + 待后端源码确认 |

## 4. 输入 image / frame 信息候选

| 字段 | 类型候选 | 含义 | 必填候选 | 证据等级 |
|---|---|---|---|---|
| `source_type` | enum | `image`、`video_frame`、`realtime_frame` | 是 | 文档推断 |
| `source_id` | string/integer/null | 图片记录、视频任务、实时会话或帧 ID | 可选 | 待后端源码确认 |
| `file_key` | string/null | 原始图片或视频帧文件对象 key | 可选 | 待后端源码确认 |
| `filename` | string/null | 上传文件名 | 可选 | 文档推断 |
| `width` | integer/null | 输入图像宽度 | 是，若坐标为像素 | 待后端源码确认 |
| `height` | integer/null | 输入图像高度 | 是，若坐标为像素 | 待后端源码确认 |
| `frame_index` | integer/null | 视频/实时帧序号 | 视频/实时必填 | 文档推断 |
| `timestamp_ms` | integer/null | 视频帧时间戳 | 视频推荐必填 | 文档推断 |
| `session_id` | string/null | 实时检测会话 ID | 实时推荐必填 | 文档推断 |
| `input_format` | string/null | `jpg`、`png`、`base64` 等 | 可选 | 文档推断 |

## 5. detections 数组字段候选

| 字段 | 类型候选 | 含义 | 必填候选 | 证据等级 |
|---|---|---|---|---|
| `detection_id` | string/null | 单个检测目标 ID | 可选 | 待后端源码确认 |
| `object_index` | integer | 当前结果中的目标序号 | 是 | 文档推断 |
| `class_id` | integer | YOLO 类别 ID；当前仅确认 `0` | 是 | 已资源确认 |
| `class_name` | string | 当前仅确认 `floating_object` | 是 | 已资源确认 |
| `chinese_name` | string/null | 中文显示名，例如 `漂浮物` | 可选 | 文档推断 |
| `confidence` | number | 目标置信度，范围建议 0-1 | 是 | 文档推断 |
| `bbox_xyxy` | number[4] | 像素坐标 `[x1,y1,x2,y2]` | 推荐必填 | 文档推断 |
| `bbox_xywhn` | number[4] | YOLO 归一化 `[x_center,y_center,w,h]` | 推荐保留 | 已资源确认 |
| `bbox_format` | string | 当前主坐标格式，例如 `xyxy_pixel` | 是 | 文档推断 |
| `area_px` | number/null | 检测框面积 | 可选 | 文档推断 |
| `track_id` | integer/string/null | ByteTrack 目标 ID | 实时/视频可选 | 文档推断 + 待后端源码确认 |
| `crop_key` | string/null | 目标裁剪图对象 key | 图片检测可选 | 文档推断 + 待后端源码确认 |
| `frame_index` | integer/null | 目标所在帧序号 | 视频/实时可选 | 文档推断 |

## 6. bbox 坐标格式候选

| 格式字段 | 类型候选 | 坐标定义 | 使用建议 | 证据等级 |
|---|---|---|---|---|
| `bbox_xyxy` | number[4] | `[x1,y1,x2,y2]`，像素坐标 | 后端绘图、前端框选、裁剪推荐主格式 | 文档推断 |
| `bbox_xywhn` | number[4] | `[x_center,y_center,width,height]`，归一化坐标 | 与 YOLO label 兼容，用于评估和复现 | 已资源确认 |
| `bbox_xywh` | number[4] | `[x,y,width,height]`，像素坐标 | 可选兼容字段 | 文档推断 |
| `bbox_format` | string | 标记主坐标格式 | 避免前后端歧义 | 文档推断 |
| `image_size` | object | `{ "width": n, "height": n }` | 所有像素 bbox 必须配套图像尺寸 | 待后端源码确认 |

## 7. confidence / class 字段候选

| 字段 | 类型候选 | 取值候选 | 说明 | 证据等级 |
|---|---|---|---|---|
| `class_id` | integer | `0` | 当前唯一类别 ID | 已资源确认 |
| `class_name` | string | `floating_object` | 当前唯一类别名 | 已资源确认 |
| `class_display_name` | string | `漂浮物` | 前端/报告中文显示候选 | 文档推断 |
| `confidence` | number | `0.0-1.0` | 单框置信度 | 文档推断 |
| `confidence_percent` | number/null | `0-100` | 前端展示可选，不建议作为主存储字段 | 文档推断 |
| `conf_threshold` | number/null | 例如 `0.25`、`0.5` | 阈值由后端实际接口确认 | 待后端源码确认 |
| `class_map_version` | string/null | 例如 `trash_floater.v1` | 若后续多类别扩展，需版本化 | 文档推断 |

## 8. summary 字段候选

| 字段 | 类型候选 | 含义 | 必填候选 | 证据等级 |
|---|---|---|---|---|
| `object_count` | integer | 检测目标总数 | 是 | 文档推断 |
| `class_counts` | object | 按类别统计，例如 `{ "floating_object": 3 }` | 是 | 文档推断 |
| `max_confidence` | number/null | 最高置信度 | 可选 | 文档推断 |
| `mean_confidence` | number/null | 平均置信度 | 可选 | 文档推断 |
| `has_detection` | boolean | 是否检测到目标 | 是 | 文档推断 |
| `frame_count` | integer/null | 视频处理帧数或当前批次帧数 | 视频可选 | 待后端源码确认 |
| `new_track_count` | integer/null | 实时/视频中新目标数量 | 实时可选 | 文档推断 + 待后端源码确认 |

## 9. artifacts 字段候选

| 字段 | 类型候选 | 含义 | 必填候选 | 证据等级 |
|---|---|---|---|---|
| `original_image_key` | string/null | 原图文件 key | 图片检测推荐 | 待后端源码确认 |
| `annotated_image_key` | string/null | 标注图文件 key | 图片检测推荐 | 文档推断 + 待后端源码确认 |
| `enhanced_image_key` | string/null | CLAHE 增强图 key | 图片检测可选 | 文档推断 + 待后端源码确认 |
| `crop_keys` | array | 目标裁剪图 key 列表 | 可选 | 文档推断 + 待后端源码确认 |
| `result_video_key` | string/null | 结果视频 key | 视频检测可选 | 文档推断 + 待后端源码确认 |
| `keyframe_keys` | array | 关键帧 key 列表 | 视频检测可选 | 文档推断 + 待后端源码确认 |
| `preview_image_key` | string/null | 前端列表预览图 key | 可选 | 文档推断 |
| `report_key` | string/null | Word 报告 key | 可选 | 文档推断 + 待后端源码确认 |

## 10. timing / performance 字段候选

| 字段 | 类型候选 | 含义 | 场景 | 证据等级 |
|---|---|---|---|---|
| `preprocess_ms` | number/null | 预处理耗时 | 图片/视频/实时 | 文档推断 |
| `inference_ms` | number/null | YOLO 推理耗时 | 图片/视频/实时 | 文档推断 |
| `postprocess_ms` | number/null | NMS、绘图、裁剪等耗时 | 图片/视频/实时 | 文档推断 |
| `total_ms` | number/null | 单帧或单图总耗时 | 图片/视频/实时 | 文档推断 |
| `fps` | number/null | 实际处理 FPS | 视频/实时 | 文档推断 |
| `frame_stride` | integer/null | 跳帧间隔 | 视频/实时 | 文档推断 |
| `device` | string/null | 推理设备 | 全部 | 待后端源码确认 |
| `model_cached` | boolean/null | 是否命中模型缓存 | 全部 | 待后端源码确认 |

## 11. 与 DETECTION_RESULT_SCHEMA 的关系

| 关系点 | AI 输出建议 | 与后端 `DETECTION_RESULT_SCHEMA` 的关系 | 证据等级 |
|---|---|---|---|
| 职责边界 | `AI_OUTPUT_SCHEMA` 描述 YOLO/AI 原始候选输出 | 后端 schema 应定义最终 API/DB/报告可消费格式 | 文档推断 |
| 字段复用 | `detections`、`summary`、`artifacts` 可直接进入 `detection_result` | 最终字段名、嵌套层级和落库形式由后端确认 | 待后端源码确认 |
| bbox | 建议同时保留 `bbox_xyxy` 和 `bbox_xywhn` | 后端需确认前端、报告、裁剪实际使用哪个格式 | 待后端源码确认 |
| 类别 | AI 侧只确认 `0/floating_object` | 后端不得在无通知情况下改类别定义 | 已资源确认 |
| 版本 | 建议加入 `schema_version` | 后端 schema 需同步版本 | 文档推断 |
| 兼容性 | 新字段应追加，不删除已消费字段 | 需与 Frontend/Backend/Docs 共同确认 | 文档推断 |

## 12. 待后端源码确认项

| 编号 | 确认项 | 当前状态 | 证据等级 |
|---|---|---|---|
| AI-BE-001 | 应用内 YOLO 推理封装位置 | `web-flask` 当前缺少可审计推理代码 | 待后端源码确认 |
| AI-BE-002 | 实际加载的权重路径和模型发布逻辑 | 文档说明需发布模型，源码未确认 | 待后端源码确认 |
| AI-BE-003 | `detection_result` 真实 JSON 结构 | 当前只有候选 | 待后端源码确认 |
| AI-BE-004 | 坐标格式与前端/报告字段 | 当前只有建议格式 | 待后端源码确认 |
| AI-BE-005 | 模型缓存/懒加载策略 | 文档建议，源码未确认 | 待后端源码确认 |
| AI-BE-006 | CLAHE 是否参与模型输入或仅展示/分析 | 文档描述存在，源码未确认 | 待后端源码确认 |
| AI-BE-007 | 视频关键帧和实时 `track_id` 字段 | 文档描述存在，源码未确认 | 待后端源码确认 |
| AI-BE-008 | 文件 key、URL、bucket/object_key 规则 | 文档推断，源码未确认 | 待后端源码确认 |

