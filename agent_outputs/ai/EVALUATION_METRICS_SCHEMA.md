# Evaluation Metrics Schema

阶段：Phase 2A 系统契约与重建基线  
角色：AI Agent  
边界：本文档仅定义模型评估指标候选契约，不执行验证、不运行 `val.py`、不修改评估代码、不修改模型权重。

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
| 覆盖范围 | 模型评估、历史验证/测试指标、前端评估展示候选字段 | 文档推断 |
| 当前不做 | 不执行 `val.py`、不重新计算指标、不运行预测、不生成新图表 | 文档推断 |
| 可用历史输出 | `output/已经训练好的模型和测试结果/train/验证集精度.txt` 与 `val/测试集精度.txt` | 历史输出确认 |
| 可用测试资源 | `4测试包/评估测试/评估图片` 40 张，`对应标签文件` 40 个 | 已资源确认 |
| 当前限制 | 后端评估 API、IoU 匹配实现、metrics 落库格式均未源码确认 | 待后端源码确认 |

## 2. 已确认历史指标

| split | Images | Instances | Precision | Recall | mAP50 | mAP50-95 | 来源 | 证据等级 |
|---|---:|---:|---:|---:|---:|---:|---|---|
| validation | 907 | 5743 | 0.904 | 0.845 | 0.927 | 0.675 | `train/验证集精度.txt` | 历史输出确认 |
| test | 605 | 4190 | 0.889 | 0.827 | 0.915 | 0.659 | `val/测试集精度.txt` | 历史输出确认 |

补充差异：

| 差异 | 说明 | 证据等级 |
|---|---|---|
| 当前 `val.py` 指向 `small_dataset` 的 `test` split | 当前脚本不等同于历史完整测试集结果 | 冲突/差异 |
| 历史 `args.yaml` 指向 `dataset/all_dataset/data.yaml`、`epochs: 100` | 当前 `train.py` 指向 `small_dataset`、`epochs=50` | 冲突/差异 |
| 当前目录未确认真实历史 `best.pt` 存在 | 不能复跑或声明生产权重存在 | 已资源确认 |

## 3. overall metrics 字段候选

| 字段 | 类型候选 | 含义 | 是否必填候选 | 证据等级 |
|---|---|---|---|---|
| `schema_version` | string | 指标 schema 版本，例如 `evaluation_metrics.v1` | 是 | 文档推断 |
| `evaluation_id` | string/integer/null | 评估记录 ID | 业务保存时必填 | 待后端源码确认 |
| `model_id` | string/integer/null | 被评估模型 ID | 是 | 待后端源码确认 |
| `dataset_id` | string/integer/null | 被评估数据集 ID | 可选 | 待后端源码确认 |
| `split` | string | `train`、`val`、`test`、`custom` | 是 | 已源码确认 + 文档推断 |
| `images` | integer | 参与评估图片数 | 是 | 历史输出确认 |
| `instances` | integer | GT 目标实例数 | 推荐 | 历史输出确认 |
| `precision` | number | 精确率 | 是 | 历史输出确认 |
| `recall` | number | 召回率 | 是 | 历史输出确认 |
| `map50` | number | IoU=0.5 平均精度 | 是 | 历史输出确认 |
| `map50_95` | number/null | IoU=0.5:0.95 平均精度 | 推荐 | 历史输出确认 |
| `map75` | number/null | IoU=0.75 平均精度 | 可选 | 已源码确认 |
| `avg_iou` | number/null | 平均 IoU | 推荐用于业务评估 | 文档推断 |
| `gt_count` | integer/null | GT 框数量 | 推荐 | 文档推断 |
| `pred_count` | integer/null | 预测框数量 | 推荐 | 文档推断 |
| `match_count` | integer/null | 匹配成功数量 | 推荐 | 文档推断 |

## 4. per_class metrics 字段候选

| 字段 | 类型候选 | 含义 | 是否必填候选 | 证据等级 |
|---|---|---|---|---|
| `class_id` | integer | 类别 ID，当前仅 `0` | 是 | 已资源确认 |
| `class_name` | string | 类别名，当前仅 `floating_object` | 是 | 已资源确认 |
| `images` | integer/null | 该类别涉及图片数 | 可选 | 历史输出确认 |
| `instances` | integer/null | 该类别 GT 实例数 | 可选 | 历史输出确认 |
| `precision` | number/null | 类别精确率 | 推荐 | 文档推断 |
| `recall` | number/null | 类别召回率 | 推荐 | 文档推断 |
| `map50` | number/null | 类别 mAP50 | 推荐 | 文档推断 |
| `map50_95` | number/null | 类别 mAP50-95 | 推荐 | 已源码确认 |
| `map75` | number/null | 类别 mAP75 | 可选 | 已源码确认 |
| `support` | integer/null | 类别样本/实例数 | 可选 | 文档推断 |

## 5. IoU / match 字段候选

| 字段 | 类型候选 | 含义 | 是否必填候选 | 证据等级 |
|---|---|---|---|---|
| `iou_threshold` | number | 匹配阈值，系统文档示例为 0.5 | 是 | 文档推断 |
| `nms_iou` | number/null | NMS IoU，历史训练参数为 0.7 | 可选 | 历史输出确认 |
| `matches` | array | GT 与预测框匹配详情 | 可选，详情页推荐 | 文档推断 |
| `match.gt_box` | object | GT 框，建议包含 `class_id`、`bbox_xyxy`、`bbox_xywhn` | 可选 | 文档推断 |
| `match.pred_box` | object | 预测框，建议包含 `class_id`、`confidence`、`bbox_xyxy` | 可选 | 文档推断 |
| `match.iou` | number | 单次匹配 IoU | 可选 | 文档推断 |
| `false_positive_count` | integer/null | 误检数 | 推荐 | 文档推断 |
| `false_negative_count` | integer/null | 漏检数 | 推荐 | 文档推断 |
| `true_positive_count` | integer/null | 正确检出数 | 推荐 | 文档推断 |

## 6. artifacts 字段候选

| 字段 | 类型候选 | 含义 | 证据等级 |
|---|---|---|---|
| `confusion_matrix_key` | string/null | 混淆矩阵图 key | 历史输出确认 |
| `confusion_matrix_normalized_key` | string/null | 归一化混淆矩阵图 key | 历史输出确认 |
| `pr_curve_key` | string/null | PR 曲线图 key | 历史输出确认 |
| `p_curve_key` | string/null | Precision 曲线图 key | 历史输出确认 |
| `r_curve_key` | string/null | Recall 曲线图 key | 历史输出确认 |
| `f1_curve_key` | string/null | F1 曲线图 key | 历史输出确认 |
| `results_csv_key` | string/null | 训练结果 CSV | 历史输出确认 |
| `results_png_key` | string/null | 训练结果总览图 | 历史输出确认 |
| `sample_prediction_keys` | array | `val_batch*_pred.jpg` 等样例预测图 | 历史输出确认 |
| `compare_image_key` | string/null | GT/预测对比图 | 文档推断 + 待后端源码确认 |

## 7. evaluation params 字段候选

| 字段 | 类型候选 | 含义 | 证据等级 |
|---|---|---|---|
| `imgsz` | integer | 评估输入尺寸，脚本/历史参数为 640 | 已源码确认 + 历史输出确认 |
| `conf_threshold` | number/null | 置信度阈值 | 待后端源码确认 |
| `iou_threshold` | number | 匹配阈值，建议默认 0.5 | 文档推断 |
| `nms_iou` | number/null | NMS IoU，历史参数为 0.7 | 历史输出确认 |
| `max_det` | integer/null | 最大检测数，历史参数为 300 | 历史输出确认 |
| `split` | string | `test`、`val` 或自定义上传评估集 | 已源码确认 + 文档推断 |
| `device` | string/null | 评估设备 | 待后端源码确认 |
| `model_weight` | string/null | 评估权重文件 | 待后端源码确认 |
| `class_map` | object | `{ "0": "floating_object" }` | 已资源确认 |

## 8. 与测试包评估资源的关系

| 资源 | 当前事实 | 对 metrics schema 的影响 | 证据等级 |
|---|---|---|---|
| `4测试包/评估测试/评估图片` | 40 张评估图片 | 可作为 Phase 2B 最小评估冒烟输入 | 已资源确认 |
| `4测试包/评估测试/对应标签文件` | 40 个标签文件，basename 与图片一致 | 支持 GT 标签解析和 IoU/match 字段 | 已资源确认 |
| 评估标签类别 | Phase 1 文档确认类别 ID 仅发现 `0` | per_class 当前只需兼容 `floating_object` | 已资源确认 |
| 评估标签目标数 | Phase 1 文档记录目标框数量 309 | 可作为后续冒烟校验参考，不等同于模型指标 | 已资源确认 |
| 后端评估 API | 当前后端源码缺失 | 无法确认上传字段、返回格式、落库字段 | 待后端源码确认 |

## 9. 与前端展示的关系

| 前端需求候选 | metrics 字段 | 证据等级 |
|---|---|---|
| 指标卡片 | `precision`、`recall`、`map50`、`map50_95`、`avg_iou` | 文档推断 |
| 图表展示 | PR/P/R/F1 曲线、混淆矩阵、results 图 | 历史输出确认 |
| 评估记录列表 | `evaluation_id`、`model_id`、`score`、`created_at` | 待后端源码确认 |
| 详情对比 | `matches`、GT 框、预测框、IoU、对比图 | 文档推断 |
| 筛选 | `model_id`、`score_min`、`score_max` | 文档推断 |
| 单类别展示 | `per_class[0].class_name=floating_object` | 已资源确认 |

## 10. 待源码确认项

| 编号 | 确认项 | 当前状态 | 证据等级 |
|---|---|---|---|
| EVAL-BE-001 | `/api/evaluation` 实际接口 | 当前后端源码缺失 | 待后端源码确认 |
| EVAL-BE-002 | 评估时实际加载权重路径 | 当前无法确认 | 待后端源码确认 |
| EVAL-BE-003 | IoU 匹配算法实现 | 当前仅系统文档伪代码 | 待后端源码确认 |
| EVAL-BE-004 | `metrics` 字段真实 JSON | 当前仅候选 | 待后端源码确认 |
| EVAL-BE-005 | GT/预测对比图保存路径 | 当前仅文档推断 | 待后端源码确认 |
| EVAL-BE-006 | 是否计算 `mAP50_95` 到业务评估记录 | 历史输出有该指标，业务评估文档主要提 mAP50 | 冲突/差异 |
| EVAL-BE-007 | 用户评分和评语字段 | 文档描述存在，源码未确认 | 待后端源码确认 |

