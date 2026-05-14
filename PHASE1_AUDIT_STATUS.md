# Phase 1 审计状态与 Leader 调度记录

更新时间：2026-05-13  
角色：Leader / Coordinator  
阶段：Phase 1：源码结构确认与差异审计

## 1. 恢复结论

已读取并恢复以下上下文：

- 根目录工程文档：`AGENTS.md`、`PROJECT_CONTEXT.md`、`README.md`、`ROADMAP.md`、`ARCHITECTURE.md`、`MODULE_BOUNDARIES.md`、`MULTI_AGENT_PLAN.md`、`AI_PIPELINE_ANALYSIS.md`、`SYSTEM_OPTIMIZATION_PLAN.md`、`REPLAN.md`
- OMX 产物：`.omx/specs/`、`.omx/plans/`、`.omx/interviews/`

当前不重新执行 deep-interview、不重新 replan；以已有 deep-interview 与 replan 作为 Phase 0 / 前置决策输入。

## 2. Phase 0 / 前置决策已完成

- deep-interview 已完成，最终模糊度记录为 2.9%。
- replan 已完成，输出系统级执行路线、Agent 任务拆分、并行批次、里程碑、worktree 策略、风险与依赖。
- Phase 1 Leader 调度已进入执行准备 / 审计状态。

## 3. 当前源码落点确认

实际源码/资源根目录不是仓库根目录下的 `web-vue/`、`web-flask/`，而是：

```text
1项目代码/floating-objects-detect-web/
```

已确认的结构：

```text
1项目代码/floating-objects-detect-web/
├─ web-vue/
│  ├─ package.json
│  └─ 2须知.txt
├─ web-flask/
│  ├─ requirements.txt
│  └─ 1须知.txt
└─ other/model_train/detect/
   ├─ code/
   │  ├─ train.py
   │  ├─ val.py
   │  └─ predict.py
   ├─ dataset/
   │  ├─ all_dataset/
   │  ├─ small_dataset/
   │  └─ 数据集介绍.txt
   ├─ output/
   └─ weights/
      ├─ yolov8n.pt
      ├─ yolo11n.pt
      ├─ yolo12n.pt
      ├─ yolo26n.pt
      └─ reference
```

## 4. 关键差异 / 阻塞点

1. 根目录规划文档中的 `web-vue/`、`web-flask/`、`other/model_train/detect/` 是逻辑路径；实际路径需加前缀 `1项目代码/floating-objects-detect-web/`。
2. 当前 `web-vue` 仅发现 `package.json` 与说明文件，未发现 `src/`、`router/`、`views/`、`api/` 等前端源码目录。
3. 当前 `web-flask` 仅发现 `requirements.txt` 与说明文件，未发现 Flask app、routes、services、db 初始化等后端源码目录。
4. AI 训练/评估/预测脚本与数据集、权重、训练输出存在，可先开展 AI-1、AI-3 与 DOC-3。
5. 因前后端源码缺失，FE-2、BE-2、BE-3、AI-2、DOC-1 需要标记为“等待前后端源码补齐/确认”或基于现有文件形成占位差异报告。

## 5. Phase 1 执行分工

### Frontend Agent

- 当前可执行：FE-1（确认 `web-vue` 实际目录结构）。
- 当前结论：仅有 `package.json` 与 `2须知.txt`；未发现可审计的 Vue 源码。
- 输出要求：前端目录地图 + 缺失清单；不要推断页面/路由/API 矩阵为事实。
- 暂缓：FE-2、FE-3，等待 `src/` 等源码补齐。

### Backend Agent

- 当前可执行：BE-1（确认 `web-flask` 实际目录结构）。
- 当前结论：仅有 `requirements.txt` 与 `1须知.txt`；未发现 Flask 应用源码。
- 输出要求：后端目录地图 + 缺失清单；不要推断 routes/services/db 为事实。
- 暂缓：BE-2、BE-3，等待 Flask 源码补齐。

### AI Agent

- 当前可执行：AI-1、AI-3。
- 已确认入口：`code/train.py`、`code/val.py`、`code/predict.py`。
- 已确认数据集配置：`dataset/small_dataset/data.yaml`，`nc: 1`，`names: ['floating_object']`。
- 已确认测试集指标：Precision 0.889、Recall 0.827、mAP50 0.915、mAP50-95 0.659。
- 输出要求：AI 脚本说明 + 模型基线说明；不得替换权重、不得修改类别定义。

### Documentation/Test Agent

- 当前可执行：DOC-3；DOC-1 可先做“文档-现有文件差异初稿”。
- 已确认测试资源：`4测试包/` 包含数据集压缩包、15 张测试图片、6 个测试视频、评估图片与标签。
- 输出要求：测试资源索引 + Phase 1 差异审计初稿。

## 6. Leader 当前调度策略

### Batch A：立即执行

- FE-1：前端目录结构确认与源码缺失清单。
- BE-1：后端目录结构确认与源码缺失清单。
- AI-1：训练/验证/预测脚本说明。
- AI-3：权重、数据集、训练输出、指标基线说明。
- DOC-3：测试资源索引。

### Batch B：受阻 / 条件执行

- FE-2：依赖前端 `src/router`、views、api 源码。
- BE-2 / BE-3：依赖 Flask routes/services/db/init 源码。
- AI-2：依赖后端源码以确认应用内推理封装位置。
- DOC-1：可先记录“规划文档 vs 当前可见源码”的差异，待源码补齐后复审。

## 7. Phase 1 验收门槛

- 明确哪些模块已经源码确认，哪些只是规划/说明/待确认。
- 明确前端、后端、AI、测试资源的实际路径与缺失项。
- 不进入功能实现、不变更共享契约、不修改模型权重。
- 若前后端源码未补齐，Phase 1 的主要交付应是差异审计与补齐清单，而非页面/API/DB 事实映射。

## 8. 回滚与风险

- 本文件仅为审计与调度记录，不修改业务代码或模型文件。
- 若后续补齐完整源码，应重新执行 Phase 1 Batch A/B 的事实审计，并更新本文件或迁移到正式 `docs/` 交付物。
