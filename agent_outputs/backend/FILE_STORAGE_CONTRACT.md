# File Storage Contract Candidate

阶段：Phase 2A：系统契约与重建基线  
角色：Backend Agent  
边界：本文档只定义文件存储候选契约，不创建目录、不移动文件、不实现上传下载接口。

## 1. 文件类型总览

| 文件类型 | 业务模块 | DB 字段候选 | 存储方式候选 | 证据等级 |
|---|---|---|---|---|
| 原图 | 图片检测 | `original_image_bucket`, `original_image_object_key` | bucket + object_key | 数据库文档确认 |
| 检测结果图 | 图片检测 | `result_image_bucket`, `result_image_object_key` | bucket + object_key | 数据库文档确认 |
| 增强图 | 图片检测 | `enhanced_image_bucket`, `enhanced_image_object_key` | bucket + object_key | 数据库文档确认 |
| 裁剪图 | 图片检测 / 实时检测 | `image_bucket`, `image_object_key`, `cropped_image_*` | bucket + object_key | 数据库文档确认 |
| 原始视频 | 视频检测 | `original_video_bucket`, `original_video_object_key` | bucket + object_key | 数据库文档确认 |
| 结果视频 | 视频检测 | `result_video_bucket`, `result_video_object_key` | bucket + object_key | 数据库文档确认 |
| 关键帧 | 视频检测 | `image_bucket`, `image_object_key` | bucket + object_key | 数据库文档确认 |
| Word 报告 | 图片检测报告 | 未在 DB 文档中明确 | 文件引用或直接下载 | 文档推断 / 待源码确认 |
| 模型权重 | 模型管理 | `model_bucket`, `model_object_key` | bucket + object_key | 数据库文档确认 |
| 数据集 ZIP | 数据集管理 | `zip_bucket`, `zip_object_key` | bucket + object_key | 数据库文档确认 |
| 训练过程图片/文件 | 模型管理 | `train_images`, `train_files` | JSON 数组记录文件引用 | 数据库文档确认 |

当前冲突/差异：

| 项 | 文档描述 | 当前可见文件 | 证据等级 |
|---|---|---|---|
| `web-flask/file_store/` | 文档期望存在 | 当前未发现 | 冲突/差异 |
| `web-flask/temp/` | 文档期望存在 | 当前未发现 | 冲突/差异 |
| 文件 URL 生成工具 | 文档提到 file client / file route | 当前未发现源码 | 待源码确认 |

## 2. 原图存储候选

| 项 | 候选契约 | 证据等级 |
|---|---|---|
| 适用模块 | 图片检测、模型评估 | 数据库文档确认 |
| DB 字段 | `detection_records.original_image_bucket`, `detection_records.original_image_object_key` | 数据库文档确认 |
| 评估 DB 字段 | `evaluation_records.origin_image_bucket`, `evaluation_records.origin_image_object_key` | 数据库文档确认 |
| bucket 候选 | `images` / `original-images` | 文档推断 |
| object_key 候选 | 按日期、用户、记录 ID 分层 | 文档推断 |
| URL 生成 | 由 file API 或静态文件路由生成 | 文档推断 / 待源码确认 |

待确认：上传大小限制、允许格式、是否保存原始文件名、是否去重、是否压缩。证据等级：待源码确认。

## 3. 检测结果图存储候选

| 项 | 候选契约 | 证据等级 |
|---|---|---|
| 适用模块 | 图片检测 | 数据库文档确认 |
| DB 字段 | `result_image_bucket`, `result_image_object_key` | 数据库文档确认 |
| 内容 | 带检测框和标签的结果图 | 文档推断 |
| bucket 候选 | `images` / `result-images` | 文档推断 |
| object_key 候选 | 与 detection record ID 关联 | 文档推断 |

待确认：是否使用中文标签绘制、图像编码格式、是否覆盖旧结果图。证据等级：待源码确认。

## 4. 增强图存储候选

| 项 | 候选契约 | 证据等级 |
|---|---|---|
| 适用模块 | 图片检测 CLAHE 增强 | 数据库文档确认 / 文档推断 |
| DB 字段 | `enhanced_image_bucket`, `enhanced_image_object_key` | 数据库文档确认 |
| 内容 | CLAHE 增强后的图片 | 文档推断 |
| bucket 候选 | `images` / `enhanced-images` | 文档推断 |
| 是否参与模型输入 | 未确认，候选为仅展示或 Qwen-VL 输入 | 待源码确认 |

待确认：CLAHE 参数、增强图生命周期、失败时是否允许空值。证据等级：待源码确认。

## 5. 裁剪图存储候选

| 项 | 候选契约 | 证据等级 |
|---|---|---|
| 图片裁剪 DB 字段 | `detection_crops.image_bucket`, `detection_crops.image_object_key` | 数据库文档确认 |
| 实时裁剪 DB 字段 | `realtime_detection_detections.cropped_image_bucket`, `cropped_image_object_key` | 数据库文档确认 |
| 内容 | 目标 bbox 周边裁剪图，文档候选含 10% padding | 数据库文档确认 / 文档推断 |
| bucket 候选 | `crops` / `images` | 文档推断 |
| object_key 候选 | record/session + object_index/track_id 分层 | 文档推断 |

待确认：裁剪边界处理、padding 比例、裁剪图是否必定生成。证据等级：待源码确认。

## 6. 视频上传文件存储候选

| 项 | 候选契约 | 证据等级 |
|---|---|---|
| 适用模块 | 视频检测 | 数据库文档确认 |
| DB 字段 | `original_video_bucket`, `original_video_object_key` | 数据库文档确认 |
| 支持格式候选 | MP4 | 文档推断 |
| bucket 候选 | `videos` / `original-videos` | 文档推断 |
| object_key 候选 | user + video record ID + original filename | 文档推断 |

待确认：最大文件大小、支持编码、上传后是否转码、临时文件位置。证据等级：待源码确认。

## 7. 视频结果文件存储候选

| 项 | 候选契约 | 证据等级 |
|---|---|---|
| 适用模块 | 视频检测 | 数据库文档确认 |
| DB 字段 | `result_video_bucket`, `result_video_object_key` | 数据库文档确认 |
| 内容 | 带检测框的视频结果 | 文档推断 |
| 编码候选 | 文档描述 avc1 -> mp4v -> H264 回退 | 文档推断 |
| bucket 候选 | `videos` / `result-videos` | 文档推断 |

待确认：真实编码器、失败回退、是否保留无检测帧、结果视频清理规则。证据等级：待源码确认。

## 8. 关键帧存储候选

| 项 | 候选契约 | 证据等级 |
|---|---|---|
| 适用模块 | 视频检测 | 数据库文档确认 |
| DB 字段 | `video_detection_frames.image_bucket`, `image_object_key` | 数据库文档确认 |
| 元数据字段 | `frame_index`, `video_timestamp`, `detections` | 数据库文档确认 |
| bucket 候选 | `video-frames` / `images` | 文档推断 |
| 筛选策略候选 | 有目标帧、最高置信度、间隔去重 | 文档推断 |

待确认：关键帧保存频率、去重策略、最大数量、是否只保存有检测结果的帧。证据等级：待源码确认。

## 9. Word 报告存储候选

| 项 | 候选契约 | 证据等级 |
|---|---|---|
| 适用模块 | 图片检测报告导出 | 文档推断 |
| API 候选 | `POST /api/detection/export-word` | 文档推断 |
| DB 字段 | 数据库文档未定义专门 report bucket/object_key | 数据库文档确认 |
| 返回方式候选 | 直接返回 docx 附件，或生成文件引用 | 文档推断 |
| bucket 候选 | `reports` | 文档推断 |

待确认：报告是否入库、模板字段、临时文件清理、是否支持历史报告重下。证据等级：待源码确认。

## 10. 模型权重存储候选

| 项 | 候选契约 | 证据等级 |
|---|---|---|
| 适用模块 | 模型管理 | 数据库文档确认 |
| DB 字段 | `models.model_bucket`, `models.model_object_key` | 数据库文档确认 |
| 训练过程图片 | `models.train_images` JSON 数组 | 数据库文档确认 |
| 训练过程文件 | `models.train_files` JSON 数组 | 数据库文档确认 |
| 基础权重资源 | `weights/yolov8n.pt`, `yolo11n.pt`, `yolo12n.pt`, `yolo26n.pt` | 已资源确认 |
| bucket 候选 | `models` / `weights` | 文档推断 |

风险：当前 AI 审计确认历史已训练 `best.pt` 在当前可见包中未真实提供。证据等级：已资源确认 / 冲突/差异。

## 11. 数据集 ZIP 存储候选

| 项 | 候选契约 | 证据等级 |
|---|---|---|
| 适用模块 | 数据集管理 | 数据库文档确认 |
| DB 字段 | `datasets.zip_bucket`, `datasets.zip_object_key` | 数据库文档确认 |
| 文件大小字段 | `datasets.file_size` | 数据库文档确认 |
| 结构字段 | `datasets.structure_info` | 数据库文档确认 |
| bucket 候选 | `datasets` | 文档推断 |
| 测试 ZIP | `4测试包/数据集/small_dataset.zip` | 已资源确认 |

待确认：上传后是否解压、验证失败是否保留 ZIP、下载权限、删除策略。证据等级：待源码确认。

## 12. URL 生成候选规则

| 规则项 | 候选规则 | 证据等级 |
|---|---|---|
| 文件引用主键 | bucket + object_key | 数据库文档确认 |
| 前端可访问 URL | 后端根据 bucket/object_key 生成 | 文档推断 |
| URL 生命周期 | 可为稳定 URL 或临时签名 URL | 待源码确认 |
| 权限控制 | 登录用户只能访问自己记录相关文件，管理员可访问全部候选 | 文档推断 |
| 公开访问 | 不建议默认公开，真实策略待确认 | 待源码确认 |
| Base URL | `http://localhost:5000` 为后端候选地址 | 文档推断 |

URL 候选形态：

| 形态 | 示例含义 | 证据等级 |
|---|---|---|
| `/api/file/{bucket}/{object_key}` | 通过 API 读取文件 | 文档推断 / 待源码确认 |
| `/static/{bucket}/{object_key}` | 静态文件服务 | 待源码确认 |
| 返回附件 | Word、模型、数据集下载候选 | 文档推断 |

## 13. 清理策略候选

| 文件类型 | 清理触发候选 | 是否级联 DB | 证据等级 |
|---|---|---|---|
| 图片原图 / 结果图 / 增强图 | 删除检测记录 | 候选同步删除 | 文档推断 |
| 裁剪图 | 删除检测记录或裁剪记录 | 候选同步删除 | 文档推断 |
| 视频原文件 / 结果视频 | 删除视频记录 | 候选同步删除 | 文档推断 |
| 关键帧 | 删除视频记录 | 候选同步删除 | 文档推断 |
| 实时帧截图 / 裁剪图 | 删除实时会话或单条记录 | 候选同步删除 | 数据库文档确认 / 文档推断 |
| Word 报告 | 生成后临时清理或持久保存 | 待确认 | 待源码确认 |
| 模型权重 | 删除模型时谨慎处理，已发布权重不应误删 | 文档推断 |
| 数据集 ZIP | 删除数据集时清理 | 候选同步删除 | 文档推断 |
| temp 文件 | 任务完成、失败、取消时清理 | 文档推断 |

约束：当前阶段不删除任何文件。证据等级：Phase 2A 边界。

## 14. 待源码确认项

- `file_store/` 的真实路径是否存在，是否位于 `web-flask/file_store/`。
- bucket 枚举是否固定，真实名称是什么。
- object_key 命名规则、是否包含日期、用户 ID、记录 ID、扩展名。
- 文件上传服务、file API、静态文件服务是否存在。
- URL 是直接静态 URL、鉴权 API 代理，还是临时链接。
- 删除记录时是否真实删除磁盘文件。
- 视频任务失败或取消时是否清理临时视频和关键帧。
- Word 报告是否落盘、是否入库、是否临时生成。
- 模型权重删除和发布状态保护策略。
- 数据集 ZIP 验证失败后的保留或清理策略。
- 文件大小、格式白名单、MIME 校验和路径穿越防护。

