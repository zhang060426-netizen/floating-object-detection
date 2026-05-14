# Phase 2A Master Summary

更新时间：2026-05-13  
角色：Leader / Coordinator  
阶段：Phase 2A：系统契约与重建基线  
边界：本汇总只读取和汇总 Phase 2A 文档交付物；不写业务代码、不补源码、不训练模型、不修改数据库。

## 1. 输入交付物读取结果

### 1.1 Frontend Agent

| 文件 | 状态 | 结论 |
|---|---|---|
| `agent_outputs/frontend/FRONTEND_PAGE_MAP.md` | 已存在 | 已给出前端页面、路由、API 依赖、状态管理和共享契约依赖候选；均以文档推断/待源码确认为主 |
| `agent_outputs/frontend/FRONTEND_SOURCE_RECOVERY_TASKS.md` | 已存在 | 已列出 `web-vue/src`、入口文件、路由/API/views 等恢复或重建任务 |
| `agent_outputs/frontend/FRONTEND_PHASE2B_GATE.md` | 已存在 | 明确 Frontend Phase 2B Gate 当前为 `BLOCKED` |
| `agent_outputs/frontend/FRONTEND_CONTRACT_REVIEW.md` | 已存在 | 已从前端消费视角 review API、检测结果、AI 输出、DB、文件存储契约 |

### 1.2 Backend Agent

| 文件 | 状态 | 结论 |
|---|---|---|
| `agent_outputs/backend/API_CONTRACT.md` | 已存在 | 已覆盖 user、detection、video、realtime、dataset、model、evaluation、file、health 候选 API |
| `agent_outputs/backend/DETECTION_RESULT_SCHEMA.md` | 已存在 | 已定义图片/视频/实时检测结果候选 schema |
| `agent_outputs/backend/DB_CONTRACT.md` | 已存在 | 已基于数据库文档整理 10 张核心表候选契约 |
| `agent_outputs/backend/FILE_STORAGE_CONTRACT.md` | 已存在 | 已定义图片、视频、裁剪图、报告、模型、数据集等文件存储候选契约 |
| `agent_outputs/backend/BACKEND_SOURCE_RECOVERY_TASKS.md` | 已存在 | 已列出后端启动入口、routes、services、DB、鉴权、推理封装等恢复任务 |
| `agent_outputs/backend/BACKEND_PHASE2B_GATE.md` | 已存在 | 明确 Backend Phase 2B Gate 当前为 `BLOCKED` |

### 1.3 AI Agent

| 文件 | 状态 | 结论 |
|---|---|---|
| `agent_outputs/ai/AI_OUTPUT_SCHEMA.md` | 已存在 | 已定义 YOLO 输出候选 schema |
| `agent_outputs/ai/QWEN_VL_ANALYSIS_SCHEMA.md` | 已存在 | 已定义 Qwen-VL 分析字段、错误、降级候选 schema |
| `agent_outputs/ai/EVALUATION_METRICS_SCHEMA.md` | 已存在 | 已定义 overall/per-class/IoU/artifacts/params 候选指标 schema |
| `agent_outputs/ai/MODEL_ASSET_BASELINE.md` | 已存在 | 已确认基础权重、类别、历史指标，并记录 `best.pt` 缺失风险 |
| `agent_outputs/ai/AI_PHASE2B_GATE.md` | 已存在 | AI 侧契约完成，但建议在后端源码和权重缺口未解决前保持 Gate `BLOCKED` 或仅允许 mock/占位联调 |

### 1.4 Documentation/Test Agent

| 文件 | 状态 | 结论 |
|---|---|---|
| `agent_outputs/docs/DOC_SOURCE_GAP_REPORT.md` | 已存在 | 已汇总文档与源码/资源差异 |
| `agent_outputs/docs/CONTRACT_INDEX.md` | 已存在 | 已索引契约责任和证据等级，但“当前状态”仍写有“待输出”，与实际文件已存在不一致 |
| `agent_outputs/docs/SYSTEM_REBUILD_PLAN.md` | 已存在 | 已定义源码恢复路线、最小重建路线、worktree 策略和分阶段顺序 |
| `agent_outputs/docs/PHASE2B_GATE_CHECKLIST.md` | 已存在 | 已定义 Phase 2B Gate，但部分“当前状态”仍停留在“待输出” |
| `agent_outputs/docs/SMOKE_TEST_RESOURCE_MAP.md` | 已存在 | 已映射图片、视频、评估测试资源和实时检测限制 |
| `agent_outputs/docs/EVIDENCE_LEVELS.md` | 已存在 | 已定义证据等级、禁止声明规则、差异类型和输出模板 |

---

## 2. Phase 2A 是否完成

**判定：Phase 2A 文档交付物已齐套；Phase 2A 质量状态为“有条件完成”，需要一次文档状态校准。**

### 2.1 完成项

- Frontend、Backend、AI、Docs/Test 预定的 21 份文档均已存在。
- API、检测结果、AI 输出、Qwen-VL、评估指标、DB、文件存储、页面地图、源码恢复、重建计划、Gate checklist 均已形成草案。
- 禁止项未被突破：未写业务代码、未补前后端源码、未训练模型、未修改数据库、未替换大模型 API。

### 2.2 未完全闭合项

| 问题 | 影响 | 处理建议 |
|---|---|---|
| `CONTRACT_INDEX.md` 仍记录多个契约为“待输出” | 与实际交付物已存在不一致，影响 Phase 2A 完成证据 | Docs/Test Agent 后续应更新为“已输出 / 待源码确认” |
| `PHASE2B_GATE_CHECKLIST.md` 部分契约门禁仍写“待 Backend/AI/Frontend 输出” | 与当前文件状态不一致，但不改变 Phase 2B BLOCKED 总判定 | Docs/Test Agent 后续应同步本 Master Summary 的判定 |
| 各契约仍主要是文档推断、数据库文档确认、资源确认 | 不能作为已实现事实进入代码实现 | Phase 2B 必须通过源码恢复或最小重建范围冻结后再执行 |

因此：

```text
Phase 2A Deliverables: COMPLETE
Phase 2A Quality Closure: CONDITIONAL COMPLETE
Required Cleanup Before Phase 2B Re-check: update CONTRACT_INDEX and PHASE2B_GATE_CHECKLIST current statuses
```

---

## 3. 各契约是否齐全

**判定：契约文件齐全，但证据等级仍不足以证明系统已实现。**

| 契约 | 文件 | 是否齐全 | 当前最高证据等级 | 说明 |
|---|---|---:|---|---|
| API_CONTRACT | `agent_outputs/backend/API_CONTRACT.md` | 是 | 文档推断 / 待源码确认 | API 分组和候选路径齐全，但 Flask routes 缺失 |
| DETECTION_RESULT_SCHEMA | `agent_outputs/backend/DETECTION_RESULT_SCHEMA.md` | 是 | 文档推断 + AI 资源确认 / 待源码确认 | 可用于重建参考，不能声明真实返回结构 |
| AI_OUTPUT_SCHEMA | `agent_outputs/ai/AI_OUTPUT_SCHEMA.md` | 是 | 已资源确认 + 待后端源码确认 | 离线 YOLO 资源可确认，应用内输出待确认 |
| QWEN_VL_ANALYSIS_SCHEMA | `agent_outputs/ai/QWEN_VL_ANALYSIS_SCHEMA.md` | 是 | 文档推断 / 待源码确认 | LLM 配置和调用链源码缺失 |
| EVALUATION_METRICS_SCHEMA | `agent_outputs/ai/EVALUATION_METRICS_SCHEMA.md` | 是 | 历史输出确认 + 文档推断 | 历史指标存在，本轮未执行评估 |
| DB_CONTRACT | `agent_outputs/backend/DB_CONTRACT.md` | 是 | 数据库文档确认 / 待源码确认 | 10 张表已整理，实际 DB 初始化缺失 |
| FILE_STORAGE_CONTRACT | `agent_outputs/backend/FILE_STORAGE_CONTRACT.md` | 是 | 数据库文档确认 + 文档推断 / 待源码确认 | 真实目录、URL、清理策略待源码确认 |
| FRONTEND_PAGE_MAP | `agent_outputs/frontend/FRONTEND_PAGE_MAP.md` | 是 | 文档推断 / 待源码确认 | 页面/路由/API 依赖齐全，但无前端源码 |
| SYSTEM_REBUILD_PLAN | `agent_outputs/docs/SYSTEM_REBUILD_PLAN.md` | 是 | 调度计划 / 文档推断 | 已定义恢复路线、最小重建路线和 worktree 策略 |

---

## 4. 是否满足进入 Phase 2B 的 Gate

**判定：Phase 2B Gate = BLOCKED。**

理由：虽然 Phase 2A 契约文档已经齐套，但 Phase 2B 是“最小代码重建 / 可运行基线”阶段。当前仍缺少进入代码重建前必须明确的关键证据：

- 完整 `web-vue` 源码仍缺失。
- 完整 `web-flask` 源码仍缺失。
- 前端可运行入口仍未确认。
- 后端 Flask 启动入口仍未确认。
- 后端 routes/services/DB 初始化仍未确认。
- 应用内 YOLO 推理封装仍未确认。
- 实际 DB 文件或初始化脚本仍未确认。
- 文件存储真实路径和 URL 生成规则仍未源码确认。
- `best.pt` 真实已训练权重存在性仍有风险。

```text
Phase 2B Gate: BLOCKED
Gate Owner: Leader / Coordinator
Primary Reason: source/runtime baseline is missing, despite contract documents being available
```

---

## 5. BLOCKED 阻塞项

| 阻塞项 | 领域 | 当前证据 | 影响 | 解除条件 |
|---|---|---|---|---|
| `web-vue/src` 缺失 | Frontend | Frontend Phase 1/2A 审计 | 无法构建、运行、确认页面/路由/API | 恢复完整源码，或冻结最小重建范围 |
| `index.html`、`vite.config.*`、`src/main.*` 缺失 | Frontend | Frontend Gate | 无法建立前端启动基线 | 恢复或明确最小重建入口 |
| Flask 启动入口缺失 | Backend | Backend Phase 1/2A 审计 | 无法启动后端服务 | 恢复 `app.py` 或等价启动模块，或冻结最小重建入口 |
| routes/services 缺失 | Backend | Backend Gate | 无法确认 API 和业务链路 | 恢复 routes/services，或冻结最小 routes 范围 |
| DB 初始化/SQLite 文件缺失 | Backend/DB | Backend Gate、DB_CONTRACT | 无法确认表结构、默认账号、JSON 字段 | 恢复 DB 初始化源码/DB 文件，或明确临时开发 DB 策略 |
| 应用内 YOLO 推理封装缺失 | Backend/AI | AI/Backend Gate | 无法确认真实 `detection_result` | 恢复推理封装，或定义 Phase 2B mock/占位联调策略 |
| 文件存储实现缺失 | Backend | FILE_STORAGE_CONTRACT、Backend Gate | 无法确认图片、视频、报告、权重、数据集路径 | 恢复 file route/service，或冻结最小存储策略 |
| LLM 配置/调用链缺失 | Backend/AI | QWEN_VL schema、Docs gap | 无法确认 Qwen-VL prompt、超时、降级、脱敏 | 恢复配置/调用链，或 Phase 2B 暂不接真实大模型 |
| `best.pt` 状态不明 | AI | MODEL_ASSET_BASELINE | 不能声明历史精度可复现 | 补齐真实已训练权重，或明确开发占位权重不代表生产精度 |
| `CONTRACT_INDEX.md` 状态滞后 | Docs/Test | Master 汇总发现 | Phase 2A 完成证据不够干净 | 更新状态为“已输出 / 待源码确认” |
| `PHASE2B_GATE_CHECKLIST.md` 状态滞后 | Docs/Test | Master 汇总发现 | Gate 文档与实际交付物不完全一致 | 更新契约门禁状态并保留 BLOCKED 判定 |

---

## 6. 如果 PASS，Phase 2B 最小重建任务

当前 Gate 不通过，因此以下任务**不得立即执行**。它们仅作为 Gate 解除后的 Phase 2B 最小重建任务预案。

### 6.1 Phase 2B 最小重建任务预案

| 优先级 | 任务 | 主责 Agent | 前置条件 |
|---:|---|---|---|
| P0 | 创建独立 Git worktree / 分支 | Leader + Git/各 Agent | Gate PASS |
| P0 | 恢复或最小重建前端启动入口 | Frontend Agent | `frontend-worktree` 已创建；前端范围冻结 |
| P0 | 恢复或最小重建后端启动入口 | Backend Agent | `backend-worktree` 已创建；后端范围冻结 |
| P0 | 建立最小 DB 初始化策略 | Backend + Docs/Test | `DB_CONTRACT.md` 已冻结；禁止破坏性迁移 |
| P0 | 建立 health / user / detection / file 最小 API | Backend Agent | API_CONTRACT 已冻结 |
| P0 | 建立前端 login / detection / record / model-select 最小页面 | Frontend Agent | API_CONTRACT、FRONTEND_PAGE_MAP 已冻结 |
| P0 | 建立 YOLO 推理占位或真实封装策略 | Backend + AI | AI_OUTPUT_SCHEMA、DETECTION_RESULT_SCHEMA 已冻结 |
| P1 | 建立最小文件存储目录与 URL 策略 | Backend + Docs/Test | FILE_STORAGE_CONTRACT 已冻结 |
| P1 | 执行图片检测最小冒烟 | Docs/Test + Frontend + Backend + AI | 前后端启动成功 |
| P1 | 执行评估资源最小冒烟 | Docs/Test + Backend + AI | evaluation 最小接口存在 |
| P2 | 视频/实时检测最小链路 | Backend + AI + Frontend | 图片检测链路稳定后 |

### 6.2 Phase 2B 首批不应做的任务

- 不做 UI 大屏优化。
- 不做视频性能优化。
- 不做实时检测性能优化。
- 不做模型训练。
- 不做数据库重构。
- 不做大模型 API 替换。
- 不做多类别扩展。
- 不做 Kubernetes / 微服务 / 云原生。

---

## 7. 是否需要创建 Git Worktree

**判定：Phase 2A 不需要；Phase 2B 一旦进入任何源码恢复或最小重建，必须创建 Git worktree。**

### 7.1 必须创建 worktree 的任务

| Worktree | 适用任务 | 主责 |
|---|---|---|
| `frontend-worktree` | 恢复/最小重建 `web-vue` 启动入口、页面、路由、API 封装 | Frontend Agent |
| `backend-worktree` | 恢复/最小重建 Flask 启动入口、routes、services、DB 初始化、文件存储 | Backend Agent |
| `ai-worktree` | 修改 AI 推理适配、评估脚本、模型加载封装时使用；训练仍需另行批准 | AI Agent |
| `docs-worktree` | 更新正式契约、Gate、测试 checklist、系统重建文档 | Documentation/Test Agent |

### 7.2 当前不应创建 worktree 的情况

- 仅阅读和汇总文档。
- 仅修改 `PHASE2A_MASTER_SUMMARY.md`。
- 仅做 Leader Gate 判定。

---

## 8. Phase 2B 应由哪些 Agent 执行

当前 Gate 为 `BLOCKED`，所以以下是 Gate 解除后的执行配置。

| Agent | Phase 2B 职责 | 是否进入首批 |
|---|---|---|
| Frontend Agent | 恢复/最小重建前端启动入口、基础布局、登录、图片检测、检测记录、模型选择页面；只按契约接入 | 是 |
| Backend Agent | 恢复/最小重建 Flask 启动入口、health/user/detection/file API、DB 初始化、文件存储、推理封装 | 是 |
| AI Agent | 提供 YOLO 输出适配建议、权重策略、推理字段核对；不训练模型 | 是，协作 Backend |
| Documentation/Test Agent | 维护契约冻结、Gate 记录、冒烟用例、测试结果、差异回填 | 是 |
| Leader / Coordinator | 管理 worktree、冻结契约、裁决 scope、判定 Gate、整合验收 | 是 |

首批建议执行组合：

```text
Frontend Agent + Backend Agent + AI Agent + Documentation/Test Agent
```

但必须在 Leader 给出：

```text
Phase 2B Gate: PASS
```

之后才允许进入源码恢复或最小重建。

---

## 9. 下一步具体执行指令

### 9.1 当前立即执行：Phase 2A 收尾，不进入代码

1. Documentation/Test Agent 更新：
   - `agent_outputs/docs/CONTRACT_INDEX.md`
   - `agent_outputs/docs/PHASE2B_GATE_CHECKLIST.md`

   将其中“待输出”状态修正为：

   ```text
   已输出 / 待源码确认
   ```

   同时保留 Phase 2B Gate 为：

   ```text
   BLOCKED
   ```

2. Leader 保留本文件作为当前 Phase 2A 总判定：

   ```text
   PHASE2A_MASTER_SUMMARY.md
   ```

3. Frontend / Backend 不得开始创建源码文件。

4. AI 不得训练、验证、预测或替换权重。

5. Backend 不得修改数据库或创建迁移。

### 9.2 Gate 解除前的唯一允许任务

允许：

- 搜索真实 `web-vue` / `web-flask` 源码是否存在于其他目录、压缩包或历史交付包。
- 如果只是搜索和记录，不需要修改业务代码。
- 若找到源码，先报告路径和内容清单，不立即导入。
- 若要导入或恢复源码，必须先创建对应 worktree，并由 Leader 重新判定 Gate。

禁止：

- 直接新建 `src/`。
- 直接新建 Flask app。
- 直接写 API。
- 直接初始化 DB。
- 直接运行训练。
- 直接替换权重。

### 9.3 下一次 Leader Gate 复查输入

下一次复查必须提供：

- 已更新的 `CONTRACT_INDEX.md`
- 已更新的 `PHASE2B_GATE_CHECKLIST.md`
- 前端源码恢复/最小重建范围说明
- 后端源码恢复/最小重建范围说明
- worktree 创建方案
- 禁止项未违反声明

复查输出：

```text
Phase 2B Gate: PASS / BLOCKED
```

---

## 10. 最终结论

| 问题 | Leader 判定 |
|---|---|
| 1. Phase 2A 是否完成 | 文档交付物齐套；有条件完成，需要修正 Docs/Test 状态滞后 |
| 2. 各契约是否齐全 | 齐全，但均需保留证据等级，不能声明为实现事实 |
| 3. 是否满足进入 Phase 2B Gate | 不满足，Gate = `BLOCKED` |
| 4. 如果 BLOCKED，阻塞项 | 前后端源码缺失、启动入口缺失、DB 初始化缺失、推理封装缺失、文件存储实现缺失、权重状态风险、Docs 状态滞后 |
| 5. 如果 PASS，Phase 2B 最小重建任务 | 本轮不 PASS；已给出 Gate 解除后的预案 |
| 6. 是否需要创建 Git Worktree | Phase 2A 不需要；Phase 2B 源码恢复/最小重建必须创建 |
| 7. Phase 2B 应由哪些 Agent 执行 | Frontend、Backend、AI、Documentation/Test，在 Leader 协调下执行 |
| 8. 下一步具体执行指令 | Docs/Test 先修正索引和 Gate 状态；各 Agent 只能搜索/报告源码位置，不得写代码 |

