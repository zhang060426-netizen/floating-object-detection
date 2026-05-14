# AI Phase 1 Audit

## 1. 已确认事实

本审计范围为：

- `1项目代码/floating-objects-detect-web/other/model_train/detect/`
- 根目录规划文档
- `3项目文档/4模型训练文档.txt`
- `3项目文档/3系统使用注意事项.txt`

已确认事实：

| 事项 | 结论 | 来源标注 |
|---|---|---|
| AI 训练目录存在 | `other/model_train/detect/` 下存在 `code/`、`dataset/`、`weights/`、`output/` | 已由源码确认 |
| 当前脚本类型 | 存在 `train.py`、`val.py`、`predict.py` 三个离线脚本 | 已由源码确认 |
| 当前可见数据集 | `dataset/small_dataset/` 是可见预览数据集，包含 train/valid/test | 已由源码确认 |
| 完整数据集 | 文档描述完整数据集总样本 5544，train 4032，valid 907，test 605 | 文档推断 |
| 完整 all_dataset | `dataset/all_dataset/` 当前仅有“预览版项目未放置完整数据集”占位文件 | 已由源码确认 |
| 类别定义 | `nc: 1`，类别名为 `floating_object` | 已由源码确认 |
| 基础权重 | `weights/` 下存在 `yolov8n.pt`、`yolo11n.pt`、`yolo12n.pt`、`yolo26n.pt` | 已由源码确认 |
| 已训练权重 | `output/已经训练好的模型和测试结果/train/weights/` 当前没有真实 `best.pt`，只有占位文件 | 已由源码确认 |
| 测试集指标 | P 0.889，R 0.827，mAP50 0.915，mAP50-95 0.659 | 已由输出文件确认 |
| 后端源码完整性 | `web-flask/` 当前可见文件不足以确认真实推理封装、Qwen-VL 字段、评估 API | 待后端源码确认 |

约束执行情况：

- 未训练模型。
- 未运行验证或预测。
- 未替换、删除或修改任何权重文件。
- 未修改类别定义。
- 未修改前后端业务代码。

## 2. 模型训练目录结构

审计目标目录：

```text
1项目代码/floating-objects-detect-web/other/model_train/detect/
├── code/
│   ├── train.py
│   ├── val.py
│   └── predict.py
├── dataset/
│   ├── 数据集介绍.txt
│   ├── all_dataset/
│   │   └── 预览版项目未放置完整数据集
│   └── small_dataset/
│       ├── data.yaml
│       ├── train/
│       ├── valid/
│       └── test/
├── weights/
│   ├── yolov8n.pt
│   ├── yolo11n.pt
│   ├── yolo12n.pt
│   ├── yolo26n.pt
│   └── reference
└── output/
    └── 已经训练好的模型和测试结果/
        ├── train/
        └── val/
```

目录职责：

| 目录 | 职责 | 状态 |
|---|---|---|
| `code/` | 离线 YOLO 训练、验证、预测脚本入口 | 已由源码确认 |
| `dataset/` | YOLO 格式数据集与数据集说明 | 已由源码确认 |
| `dataset/small_dataset/` | 预览小数据集，可用于脚本演示或最小验证 | 已由源码确认 |
| `dataset/all_dataset/` | 文档中的完整数据集位置，但当前包未放置完整数据 | 已由源码确认 |
| `weights/` | 基础 YOLO 权重文件存放位置 | 已由源码确认 |
| `output/` | 训练、验证、预测产物和历史指标图表 | 已由源码确认 |

## 3. train/val/predict 脚本说明

### `code/train.py`

职责：

- 使用 Ultralytics `YOLO` 加载基础模型。
- 基于 YOLO 数据集配置执行训练。
- 输出训练结果到指定目录。

当前脚本参数：

```python
model = YOLO("weights/yolo26n.pt")
results = model.train(data="dataset/small_dataset/data.yaml", epochs=50, imgsz=640, save_dir="output/train")
```

审计结论：

- 当前脚本加载 `weights/yolo26n.pt`。
- 当前脚本训练数据指向 `dataset/small_dataset/data.yaml`。
- 当前脚本 epoch 为 50，图像尺寸为 640。
- 历史训练产物 `args.yaml` 显示曾使用 `dataset/all_dataset/data.yaml`、`epochs: 100`，与当前 `train.py` 不完全一致。

### `code/val.py`

职责：

- 加载训练产出的 `best.pt`。
- 使用指定数据集 split 执行模型验证或测试。
- 打印 mAP 指标。

当前脚本参数：

```python
model = YOLO("output/train/weights/best.pt")
metrics = model.val(data="dataset/small_dataset/data.yaml", split="test", save_dir="output/val")
print(metrics.box.map)
print(metrics.box.map50)
print(metrics.box.map75)
print(metrics.box.maps)
```

审计结论：

- 当前脚本默认依赖 `output/train/weights/best.pt`。
- 当前脚本验证数据指向 `small_dataset` 的 `test` split。
- 当前可见目录中没有运行该脚本生成的新 `output/train/weights/best.pt`。

### `code/predict.py`

职责：

- 加载已训练模型。
- 对单张示例图片执行预测。
- 保存预测可视化结果并打印结果对象。

当前脚本参数：

```python
model = YOLO("output/已经训练好的模型和测试结果/train/weights/best.pt")
image_path = "dataset/small_dataset/train/images/0137.jpg"
results = model(image_path, save=True, imgsz=640, save_dir="output_test/predict")
```

审计结论：

- 当前脚本指向历史已训练模型路径。
- 当前可见 `output/已经训练好的模型和测试结果/train/weights/` 下没有真实 `best.pt`，只有预览占位文件。
- 脚本包含未使用导入 `from tkinter import image_names`，但本阶段不做代码修改。

## 4. 数据集与模型指标

### 数据集

`dataset/small_dataset/data.yaml`：

```yaml
train: ../train/images
val: ../valid/images
test: ../test/images

nc: 1

names: ['floating_object']
```

当前可见小数据集规模：

| split | images | labels | 来源标注 |
|---|---:|---:|---|
| train | 40 | 40 | 已由源码确认 |
| valid | 9 | 9 | 已由源码确认 |
| test | 6 | 6 | 已由源码确认 |

文档记录完整数据集规模：

| split | 样本数 | 来源标注 |
|---|---:|---|
| train | 4032 | 文档推断 |
| valid | 907 | 文档推断 |
| test | 605 | 文档推断 |
| total | 5544 | 文档推断 |

类别定义：

| class_id | class_name | 说明 | 来源标注 |
|---:|---|---|---|
| 0 | `floating_object` | 水面漂浮物/漂浮垃圾 | 已由源码确认 |

### 权重文件

当前基础权重：

| 文件 | 职责 | 来源标注 |
|---|---|---|
| `weights/yolov8n.pt` | YOLOv8 nano 基础权重 | 已由源码确认 |
| `weights/yolo11n.pt` | YOLO11 nano 基础权重 | 已由源码确认 |
| `weights/yolo12n.pt` | YOLO12 nano 基础权重 | 已由源码确认 |
| `weights/yolo26n.pt` | YOLO26 nano 基础权重，当前 `train.py` 默认加载 | 已由源码确认 |

已训练权重状态：

- 历史结果目录引用 `output/已经训练好的模型和测试结果/train/weights/best.pt`。
- 当前可见目录中该位置没有真实 `best.pt`，仅有“预览版项目未放置训练好的模型权重”占位。
- 因此本轮不能确认已训练权重文件随当前包实际存在。

### 指标

测试集指标：

| Images | Instances | Precision | Recall | mAP50 | mAP50-95 | 来源标注 |
|---:|---:|---:|---:|---:|---:|---|
| 605 | 4190 | 0.889 | 0.827 | 0.915 | 0.659 | 已由输出文件确认 |

验证集指标：

| Images | Instances | Precision | Recall | mAP50 | mAP50-95 | 来源标注 |
|---:|---:|---:|---:|---:|---:|---|
| 907 | 5743 | 0.904 | 0.845 | 0.927 | 0.675 | 已由输出文件确认 |

## 5. 待后端确认项

以下内容当前无法仅凭 AI 训练目录完全确认，需要 Backend Agent 在完整后端源码中核对：

1. 应用内 YOLO 推理封装位置。
2. 后端实际加载哪个模型权重，以及是否区分“基础权重”和“已发布模型权重”。
3. 模型懒加载/缓存是否已实现。
4. 图片检测真实 `detection_result` JSON 结构。
5. 检测框坐标格式：`xyxy`、`xywh`、归一化或像素坐标。
6. 裁剪图、标注图、原图、报告文件的真实存储路径和 URL 生成方式。
7. CLAHE 增强是否参与模型输入、Qwen-VL 输入，还是仅用于展示。
8. Qwen-VL 配置文件、prompt 模板、超时、重试、降级和错误字段。
9. Word 报告使用的检测字段与 AI 分析字段。
10. 视频检测任务状态机、进度字段、关键帧保存规则。
11. 实时检测是否使用 ByteTrack，具体 tracker 参数和目标去重策略。
12. 模型评估 API 的返回结构、指标计算逻辑和 artifacts 字段。
13. 模型发布后前端可选模型列表的后端过滤逻辑。

## 6. Phase 2/3 建议任务

### Phase 2：共享契约固化与可运行基线

建议 AI Agent 与 Backend/Frontend/Docs 协作完成：

1. 固化 YOLO 输出 JSON schema。
   - 建议字段：`schema_version`、`source`、`model`、`detections`、`summary`、`artifacts`、`timing_ms`。
   - 检测框同时保留像素 `bbox_xyxy` 与归一化 `bbox_xywhn`。

2. 固化 Qwen-VL 分析字段。
   - 建议字段：`analysis_version`、`provider`、`model`、`prompt_version`、`input_context`、`pollution_description`、`risk_level`、`risk_reasons`、`governance_suggestions`、`limitations`、`raw_response`、`error`。

3. 固化 evaluation metrics schema。
   - 建议字段：`model`、`dataset`、`overall`、`per_class`、`artifacts`、`params`、`review`。
   - 指标命名统一为 `precision`、`recall`、`map50`、`map50_95`。

4. 建立模型权重生命周期说明。
   - 区分基础权重、训练产物、已发布权重、系统默认权重。
   - 明确当前预览包中没有真实历史 `best.pt` 的状态。

5. 建立最小冒烟验证 checklist。
   - 图片检测：返回目标框、标注图、记录。
   - 视频检测：任务完成、关键帧存在、进度合理。
   - 实时检测：会话可启动/停止、摄像头释放。
   - 模型评估：指标结构可展示。

### Phase 3：核心链路稳定化

建议任务：

1. 视频关键帧筛选策略。
   - 只从有检测结果的帧中候选。
   - 保留每个目标轨迹的 `first_seen`、`best_confidence`、`last_seen`。
   - 增加时间间隔去重和相似帧去重。
   - 关键帧记录建议包含 `frame_index`、`timestamp_ms`、`reason`、`detections`、`image_key`。

2. 实时检测性能基线。
   - 记录输入分辨率、模型、`imgsz`、设备、FPS、p50/p95 延迟、CPU/GPU/内存占用。
   - 对比 `640x480 + imgsz640`、`640x480 + imgsz416`、`跳帧=2/3`。
   - 验证连续运行 5/15/30 分钟后的资源释放。

3. 模型加载与缓存核对。
   - 后端确认是否重复加载模型。
   - 若未缓存，Phase 3 可设计单进程模型缓存策略。

4. 检测结果兼容性治理。
   - 不改变 `class_id=0` 和 `floating_object` 定义。
   - 若新增字段，采用向后兼容方式追加。
   - 变更必须同步 Frontend、Backend、Docs/Test。

5. 评估产物工程化。
   - 指标文本、曲线图、混淆矩阵、样例预测图统一登记为 artifacts。
   - 模型发布前建议关联一次固定测试集评估记录。

