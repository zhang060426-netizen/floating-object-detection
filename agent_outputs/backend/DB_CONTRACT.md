# Database Contract Candidate

阶段：Phase 2A：系统契约与重建基线  
角色：Backend Agent  
边界：本文档是数据库候选契约汇总，不创建 SQL、不修改数据库、不代表实际 DB 初始化已存在。

## 1. 数据库契约来源

| 来源 | 用途 | 证据等级 |
|---|---|---|
| `3项目文档/5数据库开发文档.md` | 10 张核心表、字段、关系、索引、初始化数据 | 数据库文档确认 |
| `ARCHITECTURE.md` | 数据层职责、文件层 bucket/object_key 模式 | 文档推断 |
| `BE_PHASE1_AUDIT.md` | 当前未发现 DB 初始化代码或 SQLite 文件 | 冲突/差异 |
| `3项目文档/1系统介绍文档.md` | 业务模块与 API 对 DB 的使用描述 | 文档推断 |

当前状态：

| 项 | 结论 | 证据等级 |
|---|---|---|
| `yyxz_sqlite.db` 文档描述存在 | 预期 SQLite 数据库文件名 | 数据库文档确认 |
| 当前 `web-flask/` 未发现 SQLite 文件 | 实际可见文件与文档描述不一致 | 冲突/差异 |
| 当前未发现建表或初始化源码 | 无法确认真实表结构 | 待源码确认 |

## 2. 10 张核心表总览

| 表名 | 主职责 | 主键候选 | 证据等级 |
|---|---|---|---|
| `user` | 用户、角色、状态、头像 | `id` integer autoincrement | 数据库文档确认 |
| `datasets` | 数据集上传、结构信息、验证状态 | `id` text UUID | 数据库文档确认 |
| `models` | 模型元信息、训练/发布状态、权重引用 | `id` text UUID | 数据库文档确认 |
| `detection_records` | 图片检测记录、AI 分析、建议、图片引用 | `id` text UUID | 数据库文档确认 |
| `detection_crops` | 图片检测目标裁剪图 | `id` text UUID | 数据库文档确认 |
| `video_detection_records` | 视频检测任务、状态、进度、视频引用 | `id` text UUID | 数据库文档确认 |
| `video_detection_frames` | 视频关键帧与帧级检测结果 | `id` text UUID | 数据库文档确认 |
| `evaluation_records` | 模型评估记录、指标、评分 | `id` text UUID | 数据库文档确认 |
| `realtime_detection_sessions` | 实时检测会话 | `id` text UUID | 数据库文档确认 |
| `realtime_detection_detections` | 实时检测目标记录 | `id` text UUID | 数据库文档确认 |

## 3. user 表候选契约

| 字段 | 类型候选 | 必填 | 默认值候选 | 含义 | 证据等级 |
|---|---|---:|---|---|---|
| `id` | INTEGER | 是 | autoincrement | 用户 ID | 数据库文档确认 |
| `username` | VARCHAR(50) | 是 | 无 | 登录账号，唯一 | 数据库文档确认 |
| `password` | VARCHAR(100) | 是 | 无 | 密码，文档候选 MD5 | 数据库文档确认 |
| `real_name` | VARCHAR(50) | 否 | NULL | 真实姓名 | 数据库文档确认 |
| `phone` | VARCHAR(20) | 否 | NULL | 联系电话 | 数据库文档确认 |
| `email` | VARCHAR(100) | 否 | NULL | 邮箱 | 数据库文档确认 |
| `avatar_bucket` | VARCHAR(50) | 否 | NULL | 头像 bucket | 数据库文档确认 |
| `avatar_object_key` | VARCHAR(255) | 否 | NULL | 头像 object key | 数据库文档确认 |
| `role` | INTEGER | 是 | 0 | `0` 普通用户，`1` 管理员 | 数据库文档确认 |
| `status` | INTEGER | 是 | 1 | `0` 禁用，`1` 启用 | 数据库文档确认 |
| `create_time` | TIMESTAMP | 是 | CURRENT_TIMESTAMP | 创建时间 | 数据库文档确认 |
| `update_time` | TIMESTAMP | 是 | CURRENT_TIMESTAMP | 更新时间 | 数据库文档确认 |

待确认：真实密码哈希实现、更新时间触发方式、是否存在软删除。证据等级：待源码确认。

## 4. datasets 表候选契约

| 字段 | 类型候选 | 必填 | 默认值候选 | 含义 | 证据等级 |
|---|---|---:|---|---|---|
| `id` | TEXT | 是 | 无 | 数据集 UUID | 数据库文档确认 |
| `name` | TEXT | 是 | 无 | 数据集名称 | 数据库文档确认 |
| `description` | TEXT | 否 | NULL | 描述 | 数据库文档确认 |
| `zip_bucket` | TEXT | 是 | 无 | ZIP 文件 bucket | 数据库文档确认 |
| `zip_object_key` | TEXT | 是 | 无 | ZIP 文件 object key | 数据库文档确认 |
| `structure_info` | TEXT | 否 | NULL | 数据集结构 JSON | 数据库文档确认 |
| `upload_time` | TEXT | 是 | 无 | 上传时间 | 数据库文档确认 |
| `file_size` | INTEGER | 否 | NULL | 文件大小 | 数据库文档确认 |
| `status` | INTEGER | 否 | 0 | `0` 待验证，`1` 通过，`2` 失败 | 数据库文档确认 |

`structure_info` 候选字段：`total_files`、`train_images`、`train_labels`、`valid_images`、`valid_labels`、`test_images`、`test_labels`。证据等级：数据库文档确认。

## 5. models 表候选契约

| 字段 | 类型候选 | 必填 | 默认值候选 | 含义 | 证据等级 |
|---|---|---:|---|---|---|
| `id` | TEXT | 是 | 无 | 模型 UUID | 数据库文档确认 |
| `name` | TEXT | 是 | 无 | 模型名称 | 数据库文档确认 |
| `description` | TEXT | 否 | NULL | 模型描述 | 数据库文档确认 |
| `dataset_id` | TEXT | 否 | NULL | 关联数据集 | 数据库文档确认 |
| `base_model` | TEXT | 否 | NULL | 基础模型类型 | 数据库文档确认 |
| `status` | SMALLINT | 否 | 0 | 模型状态 | 数据库文档确认 |
| `model_bucket` | TEXT | 否 | NULL | 权重 bucket | 数据库文档确认 |
| `model_object_key` | TEXT | 否 | NULL | 权重 object key | 数据库文档确认 |
| `train_images` | TEXT | 否 | NULL | 训练过程图片 JSON 数组 | 数据库文档确认 |
| `train_files` | TEXT | 否 | NULL | 训练过程文件 JSON 数组 | 数据库文档确认 |
| `create_time` | TEXT | 是 | 无 | 创建时间 | 数据库文档确认 |

基础权重资源候选：

| base_model 候选 | 资源状态 | 证据等级 |
|---|---|---|
| `yolov8n` | 基础权重文件存在 | 已资源确认 |
| `yolo11n` | 基础权重文件存在 | 已资源确认 |
| `yolo12n` | 基础权重文件存在 | 已资源确认 |
| `yolo26n` | 基础权重文件存在 | 已资源确认 |

## 6. detection_records 表候选契约

| 字段 | 类型候选 | 必填 | 默认值候选 | 含义 | 证据等级 |
|---|---|---:|---|---|---|
| `id` | TEXT | 是 | 无 | 图片检测记录 UUID | 数据库文档确认 |
| `user_id` | INTEGER | 是 | 无 | 用户 ID | 数据库文档确认 |
| `model_id` | TEXT | 是 | 无 | 模型 ID | 数据库文档确认 |
| `original_image_bucket` | TEXT | 是 | 无 | 原图 bucket | 数据库文档确认 |
| `original_image_object_key` | TEXT | 是 | 无 | 原图 object key | 数据库文档确认 |
| `result_image_bucket` | TEXT | 否 | NULL | 标注结果图 bucket | 数据库文档确认 |
| `result_image_object_key` | TEXT | 否 | NULL | 标注结果图 object key | 数据库文档确认 |
| `detection_result` | TEXT | 否 | NULL | 检测结果 JSON | 数据库文档确认 |
| `confidence_threshold` | REAL | 否 | 0.5 | 置信度阈值 | 数据库文档确认 |
| `create_time` | TEXT | 是 | 无 | 创建时间 | 数据库文档确认 |
| `title` | TEXT | 否 | NULL | 标题 | 数据库文档确认 |
| `description` | TEXT | 否 | NULL | 描述 | 数据库文档确认 |
| `enhanced_image_bucket` | TEXT | 否 | NULL | 增强图 bucket | 数据库文档确认 |
| `enhanced_image_object_key` | TEXT | 否 | NULL | 增强图 object key | 数据库文档确认 |
| `analysis_result` | TEXT | 否 | NULL | Qwen-VL 分析结果文本 | 数据库文档确认 |
| `suggestions` | TEXT | 否 | NULL | 治理建议文本 | 数据库文档确认 |

## 7. detection_crops 表候选契约

| 字段 | 类型候选 | 必填 | 默认值候选 | 含义 | 证据等级 |
|---|---|---:|---|---|---|
| `id` | TEXT | 是 | 无 | 裁剪图 UUID | 数据库文档确认 |
| `record_id` | TEXT | 是 | 无 | 图片检测记录 ID | 数据库文档确认 |
| `object_index` | INTEGER | 是 | 无 | 目标序号 | 数据库文档确认 |
| `class_name` | TEXT | 是 | 无 | 英文类别名 | 数据库文档确认 |
| `chinese_name` | TEXT | 是 | 无 | 中文类别名 | 数据库文档确认 |
| `confidence` | REAL | 是 | 无 | 置信度 | 数据库文档确认 |
| `bbox` | TEXT | 是 | 无 | bbox JSON，候选 `[x1,y1,x2,y2]` | 数据库文档确认 |
| `image_bucket` | TEXT | 是 | 无 | 裁剪图 bucket | 数据库文档确认 |
| `image_object_key` | TEXT | 是 | 无 | 裁剪图 object key | 数据库文档确认 |
| `create_time` | TEXT | 是 | 无 | 创建时间 | 数据库文档确认 |

## 8. video_detection_records 表候选契约

| 字段 | 类型候选 | 必填 | 默认值候选 | 含义 | 证据等级 |
|---|---|---:|---|---|---|
| `id` | TEXT | 是 | 无 | 视频记录 UUID | 数据库文档确认 |
| `user_id` | INTEGER | 是 | 无 | 用户 ID | 数据库文档确认 |
| `model_id` | TEXT | 是 | 无 | 模型 ID | 数据库文档确认 |
| `original_video_bucket` | TEXT | 是 | 无 | 原视频 bucket | 数据库文档确认 |
| `original_video_object_key` | TEXT | 是 | 无 | 原视频 object key | 数据库文档确认 |
| `result_video_bucket` | TEXT | 否 | NULL | 结果视频 bucket | 数据库文档确认 |
| `result_video_object_key` | TEXT | 否 | NULL | 结果视频 object key | 数据库文档确认 |
| `detection_result` | TEXT | 否 | NULL | 视频检测结果 JSON | 数据库文档确认 |
| `confidence_threshold` | REAL | 否 | 0.5 | 置信度阈值 | 数据库文档确认 |
| `frame_rate` | INTEGER | 否 | 30 | 处理帧率 | 数据库文档确认 |
| `total_frames` | INTEGER | 否 | NULL | 视频总帧数 | 数据库文档确认 |
| `processed_frames` | INTEGER | 否 | NULL | 已读取帧数 | 数据库文档确认 |
| `target_frames` | INTEGER | 否 | NULL | 需处理帧数 | 数据库文档确认 |
| `actual_processed_frames` | INTEGER | 否 | 0 | 实际 AI 处理帧数 | 数据库文档确认 |
| `create_time` | TEXT | 是 | 无 | 创建时间 | 数据库文档确认 |
| `start_time` | TEXT | 否 | NULL | 开始处理时间 | 数据库文档确认 |
| `complete_time` | TEXT | 否 | NULL | 完成处理时间 | 数据库文档确认 |
| `status` | INTEGER | 否 | 0 | 视频任务状态 | 数据库文档确认 |
| `title` | TEXT | 否 | NULL | 标题 | 数据库文档确认 |
| `description` | TEXT | 否 | NULL | 描述 | 数据库文档确认 |

## 9. video_detection_frames 表候选契约

| 字段 | 类型候选 | 必填 | 默认值候选 | 含义 | 证据等级 |
|---|---|---:|---|---|---|
| `id` | TEXT | 是 | 无 | 关键帧 UUID | 数据库文档确认 |
| `record_id` | TEXT | 是 | 无 | 视频记录 ID | 数据库文档确认 |
| `frame_index` | INTEGER | 是 | 无 | 帧索引 | 数据库文档确认 |
| `video_timestamp` | REAL | 是 | 无 | 视频时间戳秒 | 数据库文档确认 |
| `image_bucket` | TEXT | 是 | 无 | 关键帧 bucket | 数据库文档确认 |
| `image_object_key` | TEXT | 是 | 无 | 关键帧 object key | 数据库文档确认 |
| `detections` | TEXT | 是 | 无 | 该帧检测结果 JSON | 数据库文档确认 |
| `create_time` | TEXT | 是 | 无 | 创建时间 | 数据库文档确认 |

## 10. evaluation_records 表候选契约

| 字段 | 类型候选 | 必填 | 默认值候选 | 含义 | 证据等级 |
|---|---|---:|---|---|---|
| `id` | TEXT | 是 | 无 | 评估记录 UUID | 数据库文档确认 |
| `user_id` | INTEGER | 是 | 无 | 用户 ID | 数据库文档确认 |
| `model_id` | TEXT | 是 | 无 | 模型 ID | 数据库文档确认 |
| `origin_image_bucket` | TEXT | 是 | 无 | 原始评估图 bucket | 数据库文档确认 |
| `origin_image_object_key` | TEXT | 是 | 无 | 原始评估图 object key | 数据库文档确认 |
| `compare_image_bucket` | TEXT | 否 | NULL | 对比图 bucket | 数据库文档确认 |
| `compare_image_object_key` | TEXT | 否 | NULL | 对比图 object key | 数据库文档确认 |
| `label_content` | TEXT | 否 | NULL | YOLO 标签文本 | 数据库文档确认 |
| `detection_result` | TEXT | 否 | NULL | 预测检测结果 JSON | 数据库文档确认 |
| `metrics` | TEXT | 否 | NULL | 精度指标 JSON | 数据库文档确认 |
| `score` | INTEGER | 否 | 0 | 用户评分 | 数据库文档确认 |
| `comment` | TEXT | 否 | NULL | 用户评语 | 数据库文档确认 |
| `create_time` | TEXT | 是 | 无 | 创建时间 | 数据库文档确认 |

metrics 候选字段：`precision`、`recall`、`mAP50`、`avg_iou`；`mAP50-95` 为模型总指标候选扩展。证据等级：数据库文档确认 / 文档推断。

## 11. realtime_detection_sessions 表候选契约

| 字段 | 类型候选 | 必填 | 默认值候选 | 含义 | 证据等级 |
|---|---|---:|---|---|---|
| `id` | TEXT | 是 | 无 | 实时检测会话 UUID | 数据库文档确认 |
| `user_id` | INTEGER | 是 | 无 | 用户 ID | 数据库文档确认 |
| `model_id` | TEXT | 是 | 无 | 模型 ID | 数据库文档确认 |
| `confidence_threshold` | REAL | 否 | 0.5 | 置信度阈值 | 数据库文档确认 |
| `start_time` | TEXT | 是 | 无 | 开始时间 | 数据库文档确认 |
| `end_time` | TEXT | 否 | NULL | 结束时间 | 数据库文档确认 |
| `status` | INTEGER | 否 | 0 | 会话状态 | 数据库文档确认 |
| `total_detections` | INTEGER | 否 | 0 | 总检测数量 | 数据库文档确认 |
| `create_time` | TEXT | 是 | 无 | 创建时间 | 数据库文档确认 |

## 12. realtime_detection_detections 表候选契约

| 字段 | 类型候选 | 必填 | 默认值候选 | 含义 | 证据等级 |
|---|---|---:|---|---|---|
| `id` | TEXT | 是 | 无 | 实时目标记录 UUID | 数据库文档确认 |
| `session_id` | TEXT | 是 | 无 | 会话 ID | 数据库文档确认 |
| `frame_number` | INTEGER | 是 | 无 | 帧序号 | 数据库文档确认 |
| `frame_result_image_bucket` | TEXT | 是 | 无 | 帧结果图 bucket | 数据库文档确认 |
| `frame_result_image_object_key` | TEXT | 是 | 无 | 帧结果图 object key | 数据库文档确认 |
| `track_id` | INTEGER | 是 | 无 | ByteTrack 跟踪 ID | 数据库文档确认 |
| `class_name` | TEXT | 是 | 无 | 英文类别名 | 数据库文档确认 |
| `chinese_name` | TEXT | 是 | 无 | 中文类别名 | 数据库文档确认 |
| `confidence` | REAL | 是 | 无 | 置信度 | 数据库文档确认 |
| `bbox` | TEXT | 是 | 无 | bbox JSON | 数据库文档确认 |
| `detection_result` | TEXT | 否 | NULL | 完整检测结果 JSON | 数据库文档确认 |
| `detection_time` | TEXT | 是 | 无 | 检测时间 | 数据库文档确认 |
| `cropped_image_bucket` | TEXT | 是 | 无 | 裁剪图 bucket | 数据库文档确认 |
| `cropped_image_object_key` | TEXT | 是 | 无 | 裁剪图 object key | 数据库文档确认 |
| `create_time` | TEXT | 是 | 无 | 创建时间 | 数据库文档确认 |

## 13. 枚举字段候选

| 表 | 字段 | 值候选 | 含义 | 证据等级 |
|---|---|---|---|---|
| `user` | `role` | `0` | 普通用户 | 数据库文档确认 |
| `user` | `role` | `1` | 管理员 | 数据库文档确认 |
| `user` | `status` | `0` | 禁用 | 数据库文档确认 |
| `user` | `status` | `1` | 启用 | 数据库文档确认 |
| `datasets` | `status` | `0` | 待验证 | 数据库文档确认 |
| `datasets` | `status` | `1` | 验证通过 | 数据库文档确认 |
| `datasets` | `status` | `2` | 验证失败 | 数据库文档确认 |
| `models` | `status` | `0` | 新建 | 数据库文档确认 |
| `models` | `status` | `1` | 训练中 | 数据库文档确认 |
| `models` | `status` | `2` | 训练完成 | 数据库文档确认 |
| `models` | `status` | `3` | 已发布 | 数据库文档确认 |
| `video_detection_records` | `status` | `0` | 待处理 | 数据库文档确认 |
| `video_detection_records` | `status` | `1` | 处理中 | 数据库文档确认 |
| `video_detection_records` | `status` | `2` | 已完成 | 数据库文档确认 |
| `video_detection_records` | `status` | `3` | 失败 | 数据库文档确认 |
| `video_detection_records` | `status` | `4` | 取消 | 文档推断，数据库文档未定义 |
| `realtime_detection_sessions` | `status` | `0` | 进行中 | 数据库文档确认 |
| `realtime_detection_sessions` | `status` | `1` | 已结束 | 数据库文档确认 |

## 14. 索引与关系候选

关系候选：

| 关系 | 含义 | 证据等级 |
|---|---|---|
| `user.id` -> `detection_records.user_id` | 用户图片检测记录 | 数据库文档确认 |
| `user.id` -> `video_detection_records.user_id` | 用户视频检测记录 | 数据库文档确认 |
| `user.id` -> `evaluation_records.user_id` | 用户评估记录 | 数据库文档确认 |
| `user.id` -> `realtime_detection_sessions.user_id` | 用户实时会话 | 数据库文档确认 |
| `datasets.id` -> `models.dataset_id` | 数据集训练模型 | 数据库文档确认 |
| `models.id` -> detection/video/realtime/evaluation model fields | 模型被业务记录引用 | 数据库文档确认 |
| `detection_records.id` -> `detection_crops.record_id` | 图片记录包含裁剪图 | 数据库文档确认 |
| `video_detection_records.id` -> `video_detection_frames.record_id` | 视频记录包含关键帧 | 数据库文档确认 |
| `realtime_detection_sessions.id` -> `realtime_detection_detections.session_id` | 会话包含实时检测目标 | 数据库文档确认 |

索引候选：

| 索引领域 | 字段候选 | 目的 | 证据等级 |
|---|---|---|---|
| 用户记录查询 | `user_id` | 按用户隔离与查询 | 数据库文档确认 |
| 模型记录查询 | `model_id` | 按模型筛选检测/评估记录 | 数据库文档确认 |
| 数据集模型关系 | `dataset_id` | 模型按数据集筛选 | 数据库文档确认 |
| 图片裁剪图 | `record_id`, `object_index` | 查询记录下裁剪目标 | 数据库文档确认 |
| 视频状态 | `status` | 查询任务状态 | 数据库文档确认 |
| 时间排序 | `create_time` | 历史记录排序 | 数据库文档确认 |
| 实时会话 | `session_id` | 查询会话检测记录 | 数据库文档确认 |
| 实时去重 | `session_id`, `track_id`, `class_name` | 避免同一目标重复入库 | 数据库文档确认 / 文档推断 |

## 15. 待源码 / DB 初始化确认项

- 实际 SQLite 文件是否存在，路径是否为 `web-flask/yyxz_sqlite.db`。
- DB 初始化代码、执行入口、默认数据种子是否存在。
- 实际建表字段是否与数据库文档完全一致。
- 外键是否实际启用，SQLite 是否执行外键开关。
- 索引是否实际创建。
- 默认用户、默认数据集、默认模型是否实际初始化。
- 密码 MD5 是否为真实实现。
- 是否存在迁移策略或版本记录表。
- 删除记录时是否级联删除文件或仅删除 DB。
- `detection_result`、`metrics`、`structure_info` 等 TEXT JSON 的真实结构。
- `video_detection_records.status=4` 是否可加入取消状态，当前数据库文档未定义。

