# Model Asset Baseline

阶段：Phase 2A 系统契约与重建基线  
角色：AI Agent  
边界：本文档只记录模型资产基线；不训练模型、不验证模型、不替换模型权重、不修改类别定义、不修改脚本。

证据等级统一使用：

- 已源码确认：有 `train.py` / `val.py` / `predict.py` 等源码证据。
- 已资源确认：有 `data.yaml`、weights、output、测试包等资源证据。
- 历史输出确认：来自 `output/` 中历史结果、指标文件。
- 文档推断：来自训练文档、系统文档、规划文档。
- 待后端源码确认：必须等 `web-flask` 推理调用链补齐后确认。
- 冲突/差异：脚本、历史输出、文档之间存在不一致。

## 1. 当前模型资产目录

| 路径 | 内容 | 状态 | 证据等级 |
|---|---|---|---|
| `other/model_train/detect/code/` | `train.py`、`val.py`、`predict.py` | 存在 | 已源码确认 |
| `other/model_train/detect/dataset/` | `small_dataset`、`all_dataset` 占位、数据集说明 | 存在 | 已资源确认 |
| `other/model_train/detect/weights/` | 基础权重文件 | 存在 | 已资源确认 |
| `other/model_train/detect/output/` | 历史训练/验证输出 | 存在 | 历史输出确认 |
| `output/已经训练好的模型和测试结果/train/weights/` | 历史训练权重目录 | 缺少真实 `best.pt` | 已资源确认 |

## 2. 基础权重文件清单

| 文件 | 大小 | 用途候选 | 证据等级 |
|---|---:|---|---|
| `weights/yolov8n.pt` | 6549796 bytes | 基础 YOLOv8 nano 权重 | 已资源确认 |
| `weights/yolo11n.pt` | 5613764 bytes | 基础 YOLO11 nano 权重 | 已资源确认 |
| `weights/yolo12n.pt` | 5595063 bytes | 基础 YOLO12 nano 权重 | 已资源确认 |
| `weights/yolo26n.pt` | 5544453 bytes | 基础 YOLO26 nano 权重，当前 `train.py` 默认加载 | 已资源确认 + 已源码确认 |
| `weights/reference` | 273 bytes | 权重参考说明文件 | 已资源确认 |

## 3. 已训练权重状态

| 项目 | 当前状态 | 证据等级 |
|---|---|---|
| `output/已经训练好的模型和测试结果/train/weights/best.pt` | 文件系统中未发现 | 已资源确认 |
| `output/已经训练好的模型和测试结果/train/weights/预览版项目未放置训练好的模型权重` | 占位文件存在 | 已资源确认 |
| `predict.py` 引用历史 `best.pt` | 脚本引用存在，但不能证明文件存在 | 已源码确认 + 冲突/差异 |
| 训练文档称“已经训练好的模型权重” | 文档存在描述，但当前文件系统未确认真实权重 | 文档推断 + 冲突/差异 |
| 后端实际使用权重 | 当前无法确认 | 待后端源码确认 |

## 4. best.pt 缺失风险

| 风险 | 影响 | 建议 | 证据等级 |
|---|---|---|---|
| 历史 `best.pt` 缺失 | `predict.py` 按当前路径运行会找不到模型文件 | Phase 2B 前补齐真实已训练权重或改为明确降级策略 | 已资源确认 |
| 不能复现历史指标 | 历史 P/R/mAP 不能在当前包内重新验证 | 不得声明当前环境可达到历史精度 | 冲突/差异 |
| 基础权重与训练权重混淆 | 基础权重可存在但不等于已训练业务模型 | 文档和后端模型管理需区分 `base_weight` 与 `trained_weight` | 文档推断 |
| 模型发布流程受阻 | 文档要求训练成功模型点击发布后才能识别使用 | 后端需确认上传/发布权重逻辑 | 文档推断 + 待后端源码确认 |

## 5. 数据集配置

| 项目 | 当前值 | 证据等级 |
|---|---|---|
| `small_dataset/data.yaml train` | `../train/images` | 已资源确认 |
| `small_dataset/data.yaml val` | `../valid/images` | 已资源确认 |
| `small_dataset/data.yaml test` | `../test/images` | 已资源确认 |
| `nc` | `1` | 已资源确认 |
| `names` | `['floating_object']` | 已资源确认 |
| 当前可见 `small_dataset/train` | 40 images / 40 labels | 已资源确认 |
| 当前可见 `small_dataset/valid` | 9 images / 9 labels | 已资源确认 |
| 当前可见 `small_dataset/test` | 6 images / 6 labels | 已资源确认 |
| 完整 `all_dataset` | 文档记录 5544 张，当前目录仅占位 | 文档推断 + 已资源确认 |

## 6. 类别定义

| 字段 | 当前值 | 说明 | 证据等级 |
|---|---|---|---|
| `class_id` | `0` | 当前唯一类别 ID | 已资源确认 |
| `class_name` | `floating_object` | 当前唯一类别名 | 已资源确认 |
| 中文说明 | 漂浮物/水面漂浮垃圾等漂浮物 | 文档描述 | 文档推断 |
| 变更策略 | Phase 2A/2B 不允许修改类别定义 | 协作边界 | 文档推断 |
| 多类别扩展 | 只能作为 Phase 6 受控扩展候选 | 当前非目标 | 文档推断 |

## 7. 历史验证集指标

| Images | Instances | Precision | Recall | mAP50 | mAP50-95 | 来源 | 证据等级 |
|---:|---:|---:|---:|---:|---:|---|---|
| 907 | 5743 | 0.904 | 0.845 | 0.927 | 0.675 | `output/已经训练好的模型和测试结果/train/验证集精度.txt` | 历史输出确认 |

## 8. 历史测试集指标

| Images | Instances | Precision | Recall | mAP50 | mAP50-95 | 来源 | 证据等级 |
|---:|---:|---:|---:|---:|---:|---|---|
| 605 | 4190 | 0.889 | 0.827 | 0.915 | 0.659 | `output/已经训练好的模型和测试结果/val/测试集精度.txt` | 历史输出确认 |

## 9. Phase 2B 降级策略

| 场景 | 降级策略 | 输出声明 | 证据等级 |
|---|---|---|---|
| 真实 `best.pt` 仍缺失 | 使用基础权重仅作开发占位，或阻塞推理基线直到权重补齐 | 必须声明“不代表历史精度/生产效果” | 文档推断 |
| 后端模型管理源码仍缺失 | 不实现推理优化，只保留 schema 和门禁 | 标注待后端源码确认 | 待后端源码确认 |
| 只需前后端契约联调 | 可用 mock detection 结构，但不得伪称为模型输出 | 标注 mock / 文档推断 | 文档推断 |
| 需要评估冒烟 | 使用测试包图片/标签做流程验证前，必须确认模型权重和后端评估 API | 不得运行当前禁止的验证动作 | 待后端源码确认 |
| 类别不一致 | 立即阻塞，不自动迁移类别 | 需要 Leader + AI + Backend + Frontend 同步 | 冲突/差异 |

## 10. 禁止变更项

| 禁止项 | 说明 | 证据等级 |
|---|---|---|
| 禁止训练模型 | 不运行 `train.py` 或任何训练命令 | 文档推断 |
| 禁止验证模型 | 不运行 `val.py` 或任何验证命令 | 文档推断 |
| 禁止预测 | 不运行 `predict.py` 或任何推理脚本 | 文档推断 |
| 禁止替换/删除权重 | 不修改 `weights/` 或 `output/` 下权重文件 | 文档推断 |
| 禁止修改类别定义 | 不改 `data.yaml` 的 `nc` / `names` | 已资源确认 + 文档推断 |
| 禁止修改训练脚本 | 不改 `train.py`、`val.py`、`predict.py` | 已源码确认 + 文档推断 |
| 禁止修改后端推理代码 | 当前只写 AI 文档交付物 | 文档推断 |
| 禁止替换 Qwen-VL API | 只定义字段，不替换大模型供应商 | 文档推断 |

