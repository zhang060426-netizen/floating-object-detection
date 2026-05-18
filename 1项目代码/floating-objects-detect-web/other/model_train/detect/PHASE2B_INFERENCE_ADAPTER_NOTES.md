# Phase 2B Batch1 AI Inference Adapter Notes

更新时间：2026-05-15  
角色：AI Agent  
阶段：Phase 2B PRE-DEV FROZEN / Batch1  
范围：仅固化单图 YOLO 推理契约、模型资产核对、Backend 集成注意事项；不训练、不替换权重、不声明新精度指标。

## 1. 执行边界

- 本批次不新增训练逻辑、不执行完整测试集验证、不调用 Qwen-VL。
- 本批次不修改 `web-vue/`、`web-flask/` 业务代码。
- 本批次不删除、移动、替换任何模型权重或类别定义。
- 当前类别契约固定为：`class_id = 0`，`class_name = floating_object`。
- 当前 `yolo26n.pt` 只能作为 Phase 2B 开发占位模型使用；不得作为生产 `best.pt` 或已训练精度模型对外声明。

## 2. 必读输入核对

已按任务要求读取并对齐以下输入：

| 输入 | Batch1 采用结论 |
|---|---|
| `AGENTS.md` | 遵守 AI Agent 边界、模型安全规则、Definition of Done。 |
| `PROJECT_CONTEXT.md` | 项目是 YOLO 水面漂浮物检测平台；AI 侧保持单类别契约。 |
| `PHASE2B_PRE_DEV_FREEZE.md` | 当前仍是 PRE-DEV FROZEN；只允许最小闭环规划与契约固化。 |
| `PHASE2A_MASTER_SUMMARY.md` | 源码恢复不完整，Phase2B 以最小可运行重建为目标。 |
| `agent_outputs/ai/AI_OUTPUT_SCHEMA.md` | AI 输出保留 `detections`、`summary`、`artifacts`、`timing` 等候选结构。 |
| `agent_outputs/ai/MODEL_ASSET_BASELINE.md` | 作为模型资产预期基线；需与当前文件系统再核对。 |
| `agent_outputs/ai/AI_PHASE2B_GATE.md` | 门禁要求类别不变、权重状态明确、bbox 格式明确。 |
| `agent_outputs/backend/DETECTION_RESULT_SCHEMA.md` | Backend 存储侧建议标准化 `detection_result`。 |
| `agent_outputs/backend/API_CONTRACT.md` | 图片检测接口需要返回结果图、模型信息、检测结果。 |
| `agent_outputs/docs/SMOKE_TEST_RESOURCE_MAP.md` | 图片 smoke 首选 `4测试包/测试图片/1.png`。 |

## 3. 模型资产核对

### 3.1 文档基线与当前工作树差异

`MODEL_ASSET_BASELINE.md` 记录的预期基础权重包括：

| 基线权重 | 基线记录大小 | 基线用途 | 当前工作树核对结果 |
|---|---:|---|---|
| `weights/yolov8n.pt` | 6,549,796 bytes | 基础 YOLOv8 nano | 当前未在 AI worktree 文件系统中发现。 |
| `weights/yolo11n.pt` | 5,613,764 bytes | 基础 YOLO11 nano | 当前未在 AI worktree 文件系统中发现。 |
| `weights/yolo12n.pt` | 5,595,063 bytes | 基础 YOLO12 nano | 当前未在 AI worktree 文件系统中发现。 |
| `weights/yolo26n.pt` | 5,544,453 bytes | Phase2B 开发占位基础模型 | 当前未在 AI worktree 文件系统中发现。 |
| `weights/reference` | 约 273/281 bytes | Ultralytics YOLO26 引用说明 | 当前存在，非权重文件。 |
| `output/已经训练好的模型和测试结果/train/weights/best.pt` | 基线已标记缺失 | 历史训练 best 权重 | 当前仍不得假设存在。 |

> 结论：当前 AI worktree 中没有可直接加载的 `.pt` 权重文件；Backend Batch1 不应伪造推理成功。若 Backend 运行环境后续补齐 `yolo26n.pt`，该文件仍只能标记为开发占位模型，不能作为生产 `best.pt`。

### 3.2 Backend 模型列表建议

若 Backend Batch1 暂时暴露模型列表，应采用保守状态：

```json
{
  "id": "m_yolo26n_dev",
  "name": "YOLO26n Dev Placeholder",
  "base_model": "yolo26n",
  "weight_path": "other/model_train/detect/weights/yolo26n.pt",
  "status": "missing_or_unverified",
  "is_dev_placeholder": true,
  "is_production": false,
  "class_map": { "0": "floating_object" }
}
```

若实际部署目录补齐权重并通过只读存在性检查，则 `status` 可由 Backend 在运行时变为 `available`；AI 侧不要求也不执行复制/下载/替换权重。

## 4. 单图推理输入契约

Backend 可在 `web-flask/ai/yolo_infer.py` 或等价 adapter 中封装单图推理函数，但 Batch1 不要求 AI Agent 写后端代码。建议函数签名：

```python
def infer_single_image(
    image_path: str,
    model_path: str,
    output_dir: str | None = None,
    confidence: float = 0.5,
    device: str = "auto",
    imgsz: int = 640,
    save_annotated: bool = True,
) -> dict:
    ...
```

### 4.1 输入字段

| 字段 | 类型 | 必填 | 默认 | 说明 |
|---|---|---:|---|---|
| `image_path` | string | 是 | 无 | 本地原图绝对路径或项目内安全路径；必须存在且可被 OpenCV/PIL/Ultralytics 解码。 |
| `model_path` | string | 是 | 无 | `.pt` 权重路径；不存在时返回 `MODEL_NOT_FOUND`。 |
| `output_dir` | string/null | 否 | null | 结果图输出目录；为空时可不保存结果图。 |
| `confidence` | number | 否 | `0.5` | 置信度阈值，建议 Backend 先裁剪到 `[0.0, 1.0]`。 |
| `device` | string | 否 | `auto` | `auto` / `cpu` / `cuda:0`；GPU 不可用时必须 fallback 到 CPU 或返回明确错误。 |
| `imgsz` | integer | 否 | `640` | 推理输入尺寸；Batch1 不用它声明任何精度。 |
| `save_annotated` | boolean | 否 | `true` | 是否输出带框图片。 |

## 5. 单图推理输出契约

推荐 AI adapter 返回如下结构，Backend 可转换为 `DETECTION_RESULT_SCHEMA.md`：

```json
{
  "ok": true,
  "error": null,
  "model": {
    "model_path": "other/model_train/detect/weights/yolo26n.pt",
    "weight_name": "yolo26n.pt",
    "base_model": "yolo26n",
    "is_dev_placeholder": true,
    "class_map": { "0": "floating_object" },
    "confidence_threshold": 0.5,
    "device": "cpu"
  },
  "image": {
    "path": ".../uploads/xxx.png",
    "filename": "xxx.png",
    "width": 1280,
    "height": 720
  },
  "detections": [
    {
      "class_id": 0,
      "class_name": "floating_object",
      "confidence": 0.87,
      "bbox": {
        "format": "xyxy_pixel",
        "xyxy_pixel": [100, 50, 300, 220],
        "xywhn": [0.15625, 0.1875, 0.15625, 0.236111]
      }
    }
  ],
  "summary": {
    "total_detections": 1,
    "has_detections": true,
    "max_confidence": 0.87,
    "avg_confidence": 0.87,
    "class_counts": { "floating_object": 1 }
  },
  "artifacts": {
    "annotated_image_path": ".../results/xxx_result.jpg"
  },
  "timing": {
    "preprocess_ms": null,
    "inference_ms": null,
    "postprocess_ms": null,
    "total_ms": null
  },
  "warnings": []
}
```

### 5.1 与 Backend `detection_result` 的推荐映射

| AI adapter 字段 | Backend `detection_result` 建议字段 | 说明 |
|---|---|---|
| `model.weight_name` | `model.weight_name` 或 `model.model_name` | Backend 可补充 `model_id`、`model_name`。 |
| `model.base_model` | `model.base_model` | 当前建议 `yolo26n`。 |
| `model.confidence_threshold` | `model.confidence_threshold` | 与请求阈值一致。 |
| `image.width/height/filename` | `image.width/height/filename` | bbox 转换必须依赖宽高。 |
| `detections[]` | `detections[]` | 直接进入检测结果，类别和 bbox 不重命名。 |
| `summary` | `summary` | `mean_confidence` 如需兼容可映射为 `avg_confidence`。 |
| `artifacts.annotated_image_path` | `artifacts` 或 API 顶层 `result_image` | 文件 URL 由 Backend 文件服务生成。 |
| `timing` | `timing` | 仅链路耗时，不作为性能指标。 |

## 6. bbox 与类别转换规则

### 6.1 类别映射

- 固定 `class_id = 0`。
- 固定 `class_name = floating_object`。
- 可选中文展示名可由 Backend/Frontend 映射为 `漂浮物`，但不得替代主契约字段。
- 若模型返回其它类别 ID，Batch1 建议作为 `UNSUPPORTED_CLASS_ID` warning 或过滤，不得自动扩展多类别。

### 6.2 YOLO 输出到 `xyxy_pixel`

Ultralytics YOLO 常见输出：`result.boxes.xyxy`，每个框为浮点像素坐标 `[x1, y1, x2, y2]`。

转换策略：

1. 读取原图宽高：`width`, `height`。
2. 将每个坐标裁剪到图像范围：
   - `x1`, `x2` 裁剪到 `[0, width]`
   - `y1`, `y2` 裁剪到 `[0, height]`
3. 保证顺序：若 `x2 < x1` 或 `y2 < y1`，该框应标为异常并丢弃或修正；建议丢弃并记录 warning。
4. 四舍五入策略：
   - 对外 JSON 推荐整数像素：`round(value)` 后再裁剪一次。
   - 若后续评估需要高精度，可额外保留内部浮点值，但 Batch1 `detection_result` 主字段使用整数像素。
5. 输出字段名固定：`bbox.format = "xyxy_pixel"`，`bbox.xyxy_pixel = [x1, y1, x2, y2]`。

### 6.3 `xyxy_pixel` 到 `xywhn`

给定整数像素框 `[x1, y1, x2, y2]` 与图像尺寸 `width`, `height`：

```text
box_width  = max(0, x2 - x1)
box_height = max(0, y2 - y1)
x_center   = x1 + box_width / 2
y_center   = y1 + box_height / 2
xywhn = [
  x_center / width,
  y_center / height,
  box_width / width,
  box_height / height
]
```

归一化策略：

- 输出前裁剪到 `[0.0, 1.0]`。
- 推荐保留 6 位小数，避免前端/DB JSON 过长。
- 若 `width <= 0` 或 `height <= 0`，返回 `INVALID_IMAGE_DIMENSION`。

## 7. 错误类型与降级策略

| 错误类型 | 触发条件 | 建议 `ok` | Backend 处理建议 |
|---|---|---:|---|
| `MODEL_NOT_FOUND` | `model_path` 不存在或不是文件 | false | 返回业务错误；不要伪造空检测成功。 |
| `MODEL_LOAD_FAILED` | Ultralytics 加载权重失败、权重损坏、版本不兼容 | false | 记录错误摘要，避免泄露本机绝对路径。 |
| `DEPENDENCY_MISSING` | 未安装 `ultralytics`、`torch`、`opencv-python` 等 | false | 作为环境限制记录，不声明推理成功。 |
| `IMAGE_NOT_FOUND` | `image_path` 不存在 | false | 上传/存储链路错误。 |
| `IMAGE_DECODE_FAILED` | 图片损坏或格式无法解码 | false | 返回“图片无法识别/损坏”。 |
| `INVALID_CONFIDENCE` | 阈值非数值或越界且无法修正 | false | 建议 Backend 入参校验。 |
| `INVALID_IMAGE_DIMENSION` | 宽高为 0 或无法读取 | false | 不执行 bbox 转换。 |
| `GPU_UNAVAILABLE_FALLBACK_CPU` | 请求 GPU 但不可用，已转 CPU | true | 写入 warning；链路可继续。 |
| `NO_DETECTIONS` | 推理成功但无框超过阈值 | true | `detections=[]`，`has_detections=false`，非失败。 |
| `LOW_CONFIDENCE_ONLY` | 有低于阈值框但被过滤 | true | 可写 warning；不作为精度判断。 |

## 8. 依赖与运行注意事项

- 推荐依赖：`ultralytics`、`torch`、`opencv-python` 或 `Pillow`。
- Batch1 不新增依赖文件；由 Backend 在其 `requirements.txt` 中决定。
- `device="auto"` 推荐逻辑：若 `torch.cuda.is_available()` 则用 `cuda:0`，否则用 `cpu`。
- 若 CUDA 初始化失败，必须 fallback CPU 或返回 `MODEL_LOAD_FAILED`/运行时错误，不能卡死请求。
- 模型路径必须由 Backend 从模型表/白名单解析，不能信任用户直接传入任意路径。
- 文件产物路径由 Backend 存储服务管理，AI adapter 只返回本地结果图路径，不直接生成公网 URL。

## 9. Smoke test 判读支持

### 9.1 推荐资源

首批图片检测 smoke test 只选最小闭环资源：

| 用途 | 资源 |
|---|---|
| 图片检测最小冒烟 | `4测试包/测试图片/1.png` |
| 图片检测回归样例 | `4测试包/测试图片/2.png` |
| 格式兼容样例 | `4测试包/测试图片/13.webp`、`14.jpeg`、`15.webp` |
| 大图/超时策略样例 | `4测试包/测试图片/11.png`、`12.png` |

Batch1 首轮建议只用 `1.png`；其它资源在 Backend/Docs 门禁允许后再扩展。

### 9.2 Smoke pass/fail 口径

Smoke test 只验证：

1. 模型路径解析与错误处理正确。
2. 图片可上传/读取/解码。
3. 单图推理函数返回 JSON schema 正确。
4. `detection_result.detections[]` 中类别、置信度、bbox 字段可被 Backend 保存。
5. 无目标结果可被正确表达为 `detections=[]`。

Smoke test 不验证：precision、recall、mAP、生产可用性、多类别能力、视频/实时链路、Qwen-VL 分析。

### 9.3 当前工作树下的实际判读

由于当前 AI worktree 未发现 `.pt` 权重，若立即执行图片 smoke，预期结果应是：

- `MODEL_NOT_FOUND`：合理失败，说明错误处理链路正确。
- 不应声明“检测成功”。
- 不应生成伪造检测框或伪造精度指标。

## 10. Backend 集成最小建议

1. 模型加载前执行 `Path(model_path).is_file()`。
2. 捕获依赖导入错误，返回 `DEPENDENCY_MISSING`。
3. 捕获模型加载错误，返回 `MODEL_LOAD_FAILED`。
4. 先读取原图宽高，再执行 bbox 标准化。
5. 永远返回 `class_id=0/class_name=floating_object`，除非正式多类别迁移文档更新。
6. `NO_DETECTIONS` 是成功响应，不应写成 500。
7. 不在 Batch1 启用 Qwen-VL 必需链路；图片检测可只返回 YOLO 结果。
8. 不把 `yolo26n.pt` 的结果作为历史指标或生产指标展示。

## 11. 本批次未新增 wrapper 的原因

当前工作树缺少可加载 `.pt` 权重文件，且 Batch1 目标是为 Backend 提供契约核对与最小适配建议。新增可调用 wrapper 会在无权重/未确认依赖环境下只能返回错误，无法提升当前门禁质量。因此本批次仅交付契约说明，不新增推理代码。

## 12. 回滚方式

本批次只新增本文档：

```text
1项目代码/floating-objects-detect-web/other/model_train/detect/PHASE2B_INFERENCE_ADAPTER_NOTES.md
```

回滚时删除该文件即可；未修改权重、训练脚本、类别定义、前端或后端业务代码。
