# Phase 2A：系统契约与重建基线计划

更新时间：2026-05-13  
阶段：Phase 2A：系统契约与重建基线  
角色：Leader / Coordinator  
输入依据：

- `PHASE1_MASTER_SUMMARY.md`
- `agent_outputs/frontend/FE_PHASE1_AUDIT.md`
- `agent_outputs/backend/BE_PHASE1_AUDIT.md`
- `agent_outputs/ai/AI_PHASE1_AUDIT.md`
- `agent_outputs/docs/DOC_TEST_PHASE1_AUDIT.md`
- 根目录规划文档、`3项目文档/`、AI 训练模块、`4测试包/`

## 0. 阶段边界

Phase 2A 的目标不是补代码，而是建立后续重建或恢复系统所需的**契约层、验收基线、任务边界和执行计划**。

### 明确禁止

- 不写业务代码。
- 不补 `web-vue` / `web-flask` 业务源码。
- 不训练模型。
- 不修改数据库。
- 不替换大模型 API。
- 不替换模型权重。
- 不将文档推断声明为源码事实。

### 允许执行

- 建立契约草案。
- 建立 Agent 交付清单。
- 建立源码缺口与重建计划。
- 建立测试资源索引和冒烟 checklist。
- 基于文档、数据库文档、AI 训练目录、测试包进行“待源码确认”的 schema 设计。

---

## 1. Phase 2A 总任务看板

| ID | 任务 | 负责人 | 输出文件 | 状态 | 阻塞关系 |
|---|---|---|---|---|---|
| P2A-01 | 建立 Phase 2A 主计划与任务看板 | Leader | `PHASE2A_SYSTEM_CONTRACT_REBUILD_PLAN.md` | 本文件完成 | 无 |
| P2A-02 | 建立文档-源码差异总报告 | Documentation Agent | `agent_outputs/docs/DOC_SOURCE_GAP_REPORT.md` | 待执行 | 依赖 Phase 1 四份审计 |
| P2A-03 | 建立 API 契约草案 | Backend Agent 主责，Frontend/Docs 协作 | `agent_outputs/backend/API_CONTRACT.md` | 待执行 | 后端源码缺失，标注“文档推断/待源码确认” |
| P2A-04 | 建立 detection_result 契约草案 | Backend + AI 主责，Frontend/Docs 协作 | `agent_outputs/backend/DETECTION_RESULT_SCHEMA.md` | 待执行 | 应用内推理封装缺失 |
| P2A-05 | 建立 AI 输出契约草案 | AI Agent 主责，Backend/Docs 协作 | `agent_outputs/ai/AI_OUTPUT_SCHEMA.md` | 待执行 | 后端调用链缺失 |
| P2A-06 | 建立 DB 契约草案 | Backend + Documentation Agent | `agent_outputs/backend/DB_CONTRACT.md` | 待执行 | DB 初始化源码缺失 |
| P2A-07 | 建立前端页面地图草案 | Frontend Agent 主责，Backend/Docs 协作 | `agent_outputs/frontend/FRONTEND_PAGE_MAP.md` | 待执行 | 前端 `src/` 缺失 |
| P2A-08 | 建立系统重建计划 | Leader + Documentation Agent | `agent_outputs/docs/SYSTEM_REBUILD_PLAN.md` | 待执行 | 依赖 P2A-02 至 P2A-07 |
| P2A-09 | 建立 Phase 2B 最小代码重建门禁清单 | Documentation Agent | `agent_outputs/docs/PHASE2B_GATE_CHECKLIST.md` | 待执行 | 依赖契约草案 |
| P2A-10 | 建立测试资源到冒烟场景映射 | Documentation/Test Agent | `agent_outputs/docs/SMOKE_TEST_RESOURCE_MAP.md` | 待执行 | 可直接执行 |
| P2A-11 | 建立源码补齐/恢复指令 | Frontend + Backend + Leader | `agent_outputs/frontend/FRONTEND_SOURCE_RECOVERY_TASKS.md`、`agent_outputs/backend/BACKEND_SOURCE_RECOVERY_TASKS.md` | 待执行 | 当前源码缺失 |

---

## 2. Agent 新任务拆分

### 2.1 Frontend Agent

职责边界：

- 只做前端页面、路由、状态、API 调用的**契约草案与重建蓝图**。
- 不创建 Vue 页面。
- 不创建 `src/`。
- 不补写 API 封装。

任务：

| ID | 任务 | 输出 | 证据等级要求 |
|---|---|---|---|
| FE-P2A-01 | 基于文档建立前端页面地图草案 | `FRONTEND_PAGE_MAP.md` | 每个页面标注“文档推断/待源码确认” |
| FE-P2A-02 | 建立页面-API 依赖候选矩阵 | 合并到 `FRONTEND_PAGE_MAP.md` | 不得声明源码确认 |
| FE-P2A-03 | 建立前端源码恢复任务清单 | `FRONTEND_SOURCE_RECOVERY_TASKS.md` | 明确需要补齐的入口和目录 |
| FE-P2A-04 | 建立前端 Phase 2B 接入门禁 | `FRONTEND_PHASE2B_GATE.md` | 列出进入代码重建前最小文件条件 |

Frontend 重点输出内容：

- 页面候选：登录、注册、个人中心、用户管理、图片检测、图片检测记录、视频检测、视频检测记录、实时检测、实时检测记录、模型管理、数据集管理、模型评估。
- 路由候选。
- API 依赖候选。
- Store 候选：用户、权限、模型、检测状态。
- 类型定义候选：API response、检测结果、模型、数据集、评估记录。
- Phase 2B 前必须补齐的前端入口：`index.html`、`vite.config.*`、`src/main.*`、`src/router`、`src/api`、`src/views`。

### 2.2 Backend Agent

职责边界：

- 只做 API、DB、鉴权、文件存储、推理封装的契约草案。
- 不新写 Flask app。
- 不创建 routes/services/db 代码。
- 不修改数据库。

任务：

| ID | 任务 | 输出 | 证据等级要求 |
|---|---|---|---|
| BE-P2A-01 | 建立 API 契约草案 | `API_CONTRACT.md` | 标注文档来源和待源码确认 |
| BE-P2A-02 | 建立 detection_result 契约草案 | `DETECTION_RESULT_SCHEMA.md` | 与 AI 输出和前端展示兼容 |
| BE-P2A-03 | 建立 DB 契约草案 | `DB_CONTRACT.md` | 基于 `3项目文档/5数据库开发文档.md` |
| BE-P2A-04 | 建立文件存储与 URL 候选契约 | `FILE_STORAGE_CONTRACT.md` | 标注待源码确认 |
| BE-P2A-05 | 建立后端源码恢复任务清单 | `BACKEND_SOURCE_RECOVERY_TASKS.md` | 明确 Flask 启动入口、routes、services、DB 初始化需求 |
| BE-P2A-06 | 建立后端 Phase 2B 门禁 | `BACKEND_PHASE2B_GATE.md` | 明确最小可运行后端条件 |

Backend 重点输出内容：

- API 分组：user、detection、video-detection、realtime-detection、dataset、model、evaluation、file、health。
- 统一响应候选：成功、失败、鉴权失败、权限不足、参数错误。
- JWT payload 候选：`user_id`、`role`、`exp`，其余字段待确认。
- DB 表候选：10 张核心表。
- 文件存储候选：原图、结果图、增强图、裁剪图、视频、关键帧、报告、模型权重、数据集 zip。
- 视频任务状态机候选。

### 2.3 AI Agent

职责边界：

- 只做 AI 输出契约、模型资产基线、推理链候选字段。
- 不训练模型。
- 不替换权重。
- 不修改类别定义。
- 不改 `train.py`、`val.py`、`predict.py`。

任务：

| ID | 任务 | 输出 | 证据等级要求 |
|---|---|---|---|
| AI-P2A-01 | 建立 YOLO 输出 schema 草案 | `AI_OUTPUT_SCHEMA.md` | 基于 Ultralytics 输出与现有训练目录 |
| AI-P2A-02 | 建立 Qwen-VL 分析字段草案 | `QWEN_VL_ANALYSIS_SCHEMA.md` | 标注待后端源码确认 |
| AI-P2A-03 | 建立 evaluation metrics schema 草案 | `EVALUATION_METRICS_SCHEMA.md` | 与历史指标和测试资源对齐 |
| AI-P2A-04 | 建立模型资产基线说明 | `MODEL_ASSET_BASELINE.md` | 明确基础权重、历史指标、缺失 best.pt 风险 |
| AI-P2A-05 | 建立 AI Phase 2B 门禁 | `AI_PHASE2B_GATE.md` | 明确应用内推理封装确认前不得优化 |

AI 重点输出内容：

- 类别定义：`class_id=0`、`floating_object`。
- 检测框字段候选：`bbox_xyxy`、`bbox_xywhn`、`confidence`、`class_id`、`class_name`。
- 模型信息字段候选：`model_id`、`model_name`、`weight_path`、`imgsz`、`conf_threshold`、`device`。
- Qwen-VL 字段候选：污染描述、风险等级、风险原因、治理建议、限制说明、错误字段。
- metrics 字段候选：`precision`、`recall`、`map50`、`map50_95`、`avg_iou`、`gt_count`、`pred_count`、`match_count`。

### 2.4 Documentation/Test Agent

职责边界：

- 只做差异报告、契约目录、测试清单、Phase 2B 门禁。
- 不覆盖业务代码。
- 不移动模型权重。
- 不执行端到端测试。

任务：

| ID | 任务 | 输出 | 证据等级要求 |
|---|---|---|---|
| DOC-P2A-01 | 建立文档-源码差异总报告 | `DOC_SOURCE_GAP_REPORT.md` | 引用四份 Phase 1 审计 |
| DOC-P2A-02 | 建立契约目录索引 | `CONTRACT_INDEX.md` | 标注每份契约负责人和状态 |
| DOC-P2A-03 | 建立系统重建计划 | `SYSTEM_REBUILD_PLAN.md` | 区分恢复源码与最小重建 |
| DOC-P2A-04 | 建立 Phase 2B 门禁清单 | `PHASE2B_GATE_CHECKLIST.md` | 可检查、可阻断 |
| DOC-P2A-05 | 建立测试资源到冒烟场景映射 | `SMOKE_TEST_RESOURCE_MAP.md` | 基于 `4测试包/` |
| DOC-P2A-06 | 建立验收术语表与证据等级说明 | `EVIDENCE_LEVELS.md` | 统一“源码确认/资源确认/文档推断/待确认” |

Documentation/Test 重点输出内容：

- 所有契约文件的证据等级规范。
- Phase 2B 前必须满足的代码入口和运行条件。
- 图片、视频、评估、实时检测的冒烟资源映射。
- 从“文档推断”升级为“源码确认”的流程。

---

## 3. 每个 Agent 应写入 `agent_outputs` 的文件清单

### 3.1 Frontend Agent 输出目录

目录：

```text
agent_outputs/frontend/
```

文件清单：

| 文件 | 目的 |
|---|---|
| `FRONTEND_PAGE_MAP.md` | 前端页面、路由、API 依赖候选地图 |
| `FRONTEND_SOURCE_RECOVERY_TASKS.md` | 前端源码补齐/恢复任务清单 |
| `FRONTEND_PHASE2B_GATE.md` | 前端进入 Phase 2B 的最小门禁 |
| `FRONTEND_CONTRACT_REVIEW.md` | 对 API / detection_result / AI 输出契约的前端消费视角 review |

### 3.2 Backend Agent 输出目录

目录：

```text
agent_outputs/backend/
```

文件清单：

| 文件 | 目的 |
|---|---|
| `API_CONTRACT.md` | API 分组、路径、请求/响应、错误格式候选契约 |
| `DETECTION_RESULT_SCHEMA.md` | 图片/视频/实时检测共用检测结果 schema 草案 |
| `DB_CONTRACT.md` | 数据库表、字段、关系、枚举、索引候选契约 |
| `FILE_STORAGE_CONTRACT.md` | 文件存储路径、URL、对象类型、清理策略候选契约 |
| `BACKEND_SOURCE_RECOVERY_TASKS.md` | 后端源码补齐/恢复任务清单 |
| `BACKEND_PHASE2B_GATE.md` | 后端进入 Phase 2B 的最小门禁 |

### 3.3 AI Agent 输出目录

目录：

```text
agent_outputs/ai/
```

文件清单：

| 文件 | 目的 |
|---|---|
| `AI_OUTPUT_SCHEMA.md` | YOLO 推理输出与模型信息 schema 草案 |
| `QWEN_VL_ANALYSIS_SCHEMA.md` | Qwen-VL 分析返回字段 schema 草案 |
| `EVALUATION_METRICS_SCHEMA.md` | 评估指标 schema 草案 |
| `MODEL_ASSET_BASELINE.md` | 模型权重、数据集、历史指标、缺失项说明 |
| `AI_PHASE2B_GATE.md` | AI 链路进入 Phase 2B 的最小门禁 |

### 3.4 Documentation/Test Agent 输出目录

目录：

```text
agent_outputs/docs/
```

文件清单：

| 文件 | 目的 |
|---|---|
| `DOC_SOURCE_GAP_REPORT.md` | 文档描述 vs 当前源码/资源事实差异总表 |
| `CONTRACT_INDEX.md` | 契约文件索引、责任人、证据等级、状态 |
| `SYSTEM_REBUILD_PLAN.md` | 系统恢复/最小重建执行计划 |
| `PHASE2B_GATE_CHECKLIST.md` | 进入最小代码重建前的门禁 |
| `SMOKE_TEST_RESOURCE_MAP.md` | 测试包资源与冒烟场景映射 |
| `EVIDENCE_LEVELS.md` | 证据等级、术语、标注规范 |

---

## 4. 核心契约与计划责任归属

| 交付物 | 主责 Agent | 协作 Agent | 输出位置 | 当前证据等级 |
|---|---|---|---|---|
| `API_CONTRACT` | Backend Agent | Frontend、Docs/Test | `agent_outputs/backend/API_CONTRACT.md` | 文档推断 / 待源码确认 |
| `DETECTION_RESULT_SCHEMA` | Backend Agent | AI、Frontend、Docs/Test | `agent_outputs/backend/DETECTION_RESULT_SCHEMA.md` | 文档推断 + AI 资源确认 / 待源码确认 |
| `AI_OUTPUT_SCHEMA` | AI Agent | Backend、Docs/Test | `agent_outputs/ai/AI_OUTPUT_SCHEMA.md` | AI 资源确认 + 待应用源码确认 |
| `DB_CONTRACT` | Backend Agent | Docs/Test | `agent_outputs/backend/DB_CONTRACT.md` | 数据库文档确认 / 待源码确认 |
| `FRONTEND_PAGE_MAP` | Frontend Agent | Backend、Docs/Test | `agent_outputs/frontend/FRONTEND_PAGE_MAP.md` | 文档推断 / 待源码确认 |
| `SYSTEM_REBUILD_PLAN` | Documentation/Test Agent + Leader | Frontend、Backend、AI | `agent_outputs/docs/SYSTEM_REBUILD_PLAN.md` | 调度计划 |

补充责任：

- Leader 负责最终整合和门禁判定，不直接写业务实现。
- Documentation/Test Agent 负责统一证据等级和交付索引。
- Backend Agent 负责所有会影响 API、DB、文件存储、JWT 的契约主导。
- AI Agent 负责不改变类别与权重前提下的模型输出契约草案。
- Frontend Agent 负责消费视角，确保页面/API/状态/类型需求被显式记录。

---

## 5. Phase 2A 完成标准

Phase 2A 完成必须同时满足：

### 5.1 交付物完成

- [ ] `agent_outputs/frontend/FRONTEND_PAGE_MAP.md` 已完成。
- [ ] `agent_outputs/frontend/FRONTEND_SOURCE_RECOVERY_TASKS.md` 已完成。
- [ ] `agent_outputs/frontend/FRONTEND_PHASE2B_GATE.md` 已完成。
- [ ] `agent_outputs/backend/API_CONTRACT.md` 已完成。
- [ ] `agent_outputs/backend/DETECTION_RESULT_SCHEMA.md` 已完成。
- [ ] `agent_outputs/backend/DB_CONTRACT.md` 已完成。
- [ ] `agent_outputs/backend/FILE_STORAGE_CONTRACT.md` 已完成。
- [ ] `agent_outputs/backend/BACKEND_SOURCE_RECOVERY_TASKS.md` 已完成。
- [ ] `agent_outputs/ai/AI_OUTPUT_SCHEMA.md` 已完成。
- [ ] `agent_outputs/ai/QWEN_VL_ANALYSIS_SCHEMA.md` 已完成。
- [ ] `agent_outputs/ai/EVALUATION_METRICS_SCHEMA.md` 已完成。
- [ ] `agent_outputs/ai/MODEL_ASSET_BASELINE.md` 已完成。
- [ ] `agent_outputs/docs/DOC_SOURCE_GAP_REPORT.md` 已完成。
- [ ] `agent_outputs/docs/CONTRACT_INDEX.md` 已完成。
- [ ] `agent_outputs/docs/SYSTEM_REBUILD_PLAN.md` 已完成。
- [ ] `agent_outputs/docs/PHASE2B_GATE_CHECKLIST.md` 已完成。
- [ ] `agent_outputs/docs/SMOKE_TEST_RESOURCE_MAP.md` 已完成。
- [ ] `agent_outputs/docs/EVIDENCE_LEVELS.md` 已完成。

### 5.2 质量标准

- [ ] 每个契约字段都有来源标注：源码确认 / 资源确认 / 文档推断 / 待源码确认。
- [ ] 所有涉及 API、DB、模型输出、文件路径、JWT 的字段均有类型、含义、是否必填、兼容性说明。
- [ ] 所有契约均明确“当前不是最终实现事实，需 Phase 2B 源码确认”。
- [ ] 每个 Agent 输出均包含：范围、依据、交付物、风险、Phase 2B 前置条件。
- [ ] 不存在业务代码变更。
- [ ] 不存在模型训练产物变更。
- [ ] 不存在数据库结构变更。
- [ ] 不存在大模型 API 替换。

### 5.3 协作标准

- [ ] Frontend 已 review `API_CONTRACT`、`DETECTION_RESULT_SCHEMA`、`AI_OUTPUT_SCHEMA` 的消费需求。
- [ ] Backend 已 review `AI_OUTPUT_SCHEMA` 与 `DB_CONTRACT` 的落库/返回可行性。
- [ ] AI 已 review `DETECTION_RESULT_SCHEMA` 是否兼容 YOLO 输出。
- [ ] Docs/Test 已将所有契约汇总进 `CONTRACT_INDEX.md`。
- [ ] Leader 已基于 `PHASE2B_GATE_CHECKLIST.md` 给出是否进入 Phase 2B 的判定。

---

## 6. 进入 Phase 2B 最小代码重建前的门禁条件

Phase 2B 是“最小代码重建 / 可运行基线”阶段。进入前必须满足以下门禁：

### 6.1 源码门禁

- [ ] 已确认完整 `web-vue` 源码是否可恢复；若不可恢复，已明确“最小重建”范围。
- [ ] 已确认完整 `web-flask` 源码是否可恢复；若不可恢复，已明确“最小重建”范围。
- [ ] 若恢复源码：必须使用独立 Git worktree。
- [ ] 若最小重建：必须先冻结 Phase 2A 契约草案，不能边写边变更契约。

### 6.2 前端最小门禁

- [ ] `index.html`、`vite.config.*`、`src/main.*` 的恢复/重建计划已明确。
- [ ] `src/router`、`src/api`、`src/views` 的最小范围已明确。
- [ ] 前端页面优先级已明确：登录 -> 图片检测 -> 检测记录 -> 模型选择 -> 基础布局。
- [ ] 前端 API 消费以 `API_CONTRACT` 为唯一依据。

### 6.3 后端最小门禁

- [ ] Flask 启动入口恢复/重建计划已明确。
- [ ] routes 最小范围已明确：health、user、detection、file。
- [ ] DB 初始化或临时开发 DB 策略已明确。
- [ ] 文件存储路径策略已明确。
- [ ] YOLO 推理封装是否恢复或最小重建已明确。
- [ ] API 响应格式以 `API_CONTRACT` 为唯一依据。

### 6.4 AI 门禁

- [ ] 不改变 `class_id=0` / `floating_object`。
- [ ] 不要求重新训练模型作为 Phase 2B 前置。
- [ ] 已明确基础权重和已训练权重缺口。
- [ ] 已明确最小推理输入/输出 schema。
- [ ] 已明确 `best.pt` 缺失时的降级策略：使用基础权重仅作开发占位，或等待真实已训练权重补齐；不得宣称生产精度。

### 6.5 数据库与契约门禁

- [ ] `DB_CONTRACT.md` 已完成。
- [ ] API、检测结果、AI 输出、文件存储、JWT、metrics 的契约草案已完成。
- [ ] 所有契约字段均有证据等级。
- [ ] 未确认字段不得强制进入代码实现。

### 6.6 测试门禁

- [ ] `SMOKE_TEST_RESOURCE_MAP.md` 已完成。
- [ ] 图片检测最小冒烟资源已指定。
- [ ] 视频检测最小冒烟资源已指定。
- [ ] 模型评估最小冒烟资源已指定。
- [ ] 实时检测测试限制已写明：需要本地 USB 摄像头，不能仅凭当前文件系统验证。

### 6.7 Leader 门禁判定

进入 Phase 2B 前，Leader 必须给出书面判定：

```text
Phase 2B Gate: PASS / BLOCKED

PASS 条件：
- 契约草案齐全；
- 源码恢复或最小重建范围明确；
- worktree 策略明确；
- 测试资源与冒烟路径明确；
- 禁止项未被违反。

BLOCKED 条件：
- 前后端源码状态不明；
- 契约草案缺失；
- DB/API/AI 输出仍无最小字段定义；
- 没有可执行的最小启动路径；
- 任何 Agent 开始写业务代码但未通过门禁。
```

---

## 7. 推荐执行顺序

1. Documentation/Test Agent 先建立 `EVIDENCE_LEVELS.md` 与 `CONTRACT_INDEX.md` 模板。
2. Backend Agent 输出 `API_CONTRACT.md`、`DB_CONTRACT.md`、`DETECTION_RESULT_SCHEMA.md`。
3. AI Agent 输出 `AI_OUTPUT_SCHEMA.md`、`QWEN_VL_ANALYSIS_SCHEMA.md`、`EVALUATION_METRICS_SCHEMA.md`。
4. Frontend Agent 输出 `FRONTEND_PAGE_MAP.md` 并 review API / detection / AI schema 是否可被页面消费。
5. Documentation/Test Agent 汇总 `DOC_SOURCE_GAP_REPORT.md` 与 `SMOKE_TEST_RESOURCE_MAP.md`。
6. Leader + Documentation/Test Agent 输出 `SYSTEM_REBUILD_PLAN.md` 与 `PHASE2B_GATE_CHECKLIST.md`。
7. Leader 判定是否进入 Phase 2B。

---

## 8. 当前 Leader 指令

所有 Agent 进入 Phase 2A 后必须遵循：

1. 只写 `agent_outputs/` 下的文档交付物。
2. 所有字段必须标注证据等级。
3. 前后端源码缺失期间，不得开始页面/API/DB/服务层实现。
4. AI Agent 不训练、不换权重、不改类别。
5. Backend Agent 不修改数据库，不创建迁移。
6. Frontend Agent 不创建业务页面，不补 `src/`。
7. Documentation/Test Agent 不覆盖业务代码，不移动资源文件。
8. Leader 只做整合、冲突裁决和 Phase 2B 门禁判定。

