# REPLAN.md — 系统级执行路线与多 Agent 工程化升级计划

> 依据：deep-interview 结果、`AGENTS.md`、`PROJECT_CONTEXT.md`、`prompt.md`、`README.md`、`ROADMAP.md`、`ARCHITECTURE.md`、`MODULE_BOUNDARIES.md`、`MULTI_AGENT_PLAN.md`、`AI_PIPELINE_ANALYSIS.md`、`SYSTEM_OPTIMIZATION_PLAN.md`。  
> 阶段定位：规划 / replan；不直接实现功能代码；不训练模型；不重构数据库；不更换大模型 API。

## 1. Replan 决策摘要

### 1.1 当前首要判断

当前项目已经具备完整产品雏形与文档基础，但当前工作区前后端源码不完整。因此，工程化升级不能直接进入大规模重构，而应按以下顺序推进：

1. **先固化协作规则与执行计划**：以本文件和 7 份规划文档作为后续 Agent 的共同事实源。
2. **再补齐/确认源码结构**：Frontend / Backend Agent 分别确认实际源码目录、页面、API、服务层、数据层。
3. **再固化共享契约**：API 返回结构、数据库字段、模型输出 JSON、文件存储结构、JWT 字段、`detection_result`、evaluation metrics。
4. **再建立可运行基线**：用最小启动、图片检测、视频检测、实时检测、模型评估、报告导出做端到端验证。
5. **最后分 Agent 小步并行优化**：UI 统一、视频流程、实时性能、AI 链路、文档/测试体系。

### 1.2 当前阶段非目标

- 不直接大规模修改代码。
- 不立即运行或重新训练模型。
- 不强行补写缺失源码。
- 不重构数据库。
- 不更换 Qwen-VL / 阿里云百炼 API。
- 不做微服务化、Kubernetes、云原生、多摄像头集群、商业支付、移动端 App。
- 不承诺源码级 100% 精确分析结论。

## 2. RALPLAN-DR Summary

### 2.1 Principles

1. **文档与契约先行**：架构、API、数据库、AI 链路、模型结构变更必须先有文档。
2. **目录即边界**：Frontend / Backend / AI / Docs Agent 默认只修改各自目录。
3. **小步可验证**：每个阶段都必须有可运行或可审查的验证产物。
4. **兼容优先**：模型输出、API、DB、文件路径、JWT 等共享契约保持向后兼容。
5. **先基线后优化**：未建立可运行基线前，不进入 UI 大改、性能调优或架构改造。

### 2.2 Decision Drivers

| Driver | 说明 |
|---|---|
| 源码缺口 | 当前 `web-vue` / `web-flask` 源码不完整，必须先做确认与差异审计。 |
| 多 Agent 协作风险 | 并行开发容易覆盖共享契约，必须先建立 worktree、职责边界和 review 流程。 |
| AI 链路复杂度 | YOLO、CLAHE、Qwen-VL、视频、实时、评估链路跨前后端与 AI，需要稳定 schema。 |

### 2.3 Viable Options

| 方案 | 做法 | 优点 | 缺点 | 结论 |
|---|---|---|---|---|
| A：直接进入功能开发 | 让各 Agent 直接修 UI/后端/AI | 看似推进快 | 源码不完整、契约不稳，极易返工 | 拒绝 |
| B：先做完整源码审计再规划 | 等所有源码补齐后重新分析 | 精度高 | 当前规划无法推进，协作准备滞后 | 部分采用：Phase 1 做审计 |
| C：先形成执行型 replan，再按阶段补齐源码与契约 | 当前输出执行路线，后续按 Phase 推进 | 兼顾当前可执行性与风险控制 | 需要严格遵守阶段门禁 | 采纳 |

## 3. 系统级执行路线总览

```text
Phase 0 规划与协作基线
  ↓
Phase 1 源码补齐 / 结构确认 / 差异审计
  ↓
Phase 2 共享契约固化 / 可运行基线
  ↓
Phase 3 核心链路稳定化：图片、视频、实时、模型管理、评估
  ↓
Phase 4 工程质量提升：测试、日志、错误处理、文档同步
  ↓
Phase 5 体验与性能优化：UI 统一、视频体验、实时推理性能
  ↓
Phase 6 受控扩展：多类别、GPU、告警、大屏、网络摄像头等
```

## 4. Milestones

| Milestone | 阶段 | 目标 | 验收产物 | Gate |
|---|---|---|---|---|
| M0 | Phase 0 | 完成规划和协作基线 | 7 份规划文档 + `REPLAN.md` | 所有 Agent 可按文档拆任务 |
| M1 | Phase 1 | 补齐/确认源码结构 | 前端目录地图、后端目录地图、AI 入口地图、文档-源码差异清单 | 明确哪些结论由源码确认 |
| M2 | Phase 2 | 固化共享契约和可运行基线 | API schema、DB 字段核对、AI 输出 schema、启动 checklist | 最小端到端流程可验证 |
| M3 | Phase 3 | 稳定核心业务链路 | 图片/视频/实时/评估/报告流程验收记录 | 不破坏现有功能 |
| M4 | Phase 4 | 建立工程质量体系 | 测试清单、日志/错误处理规范、回归测试说明 | 可重复验证 |
| M5 | Phase 5 | 完成体验和性能优化 | UI 风格规范、视频状态机、实时性能基线 | 用户体验明显稳定 |
| M6 | Phase 6 | 进入能力扩展 | 扩展 PRD/技术方案 | 仅在 M1-M5 完成后启动 |

## 5. Worktree 开发策略

### 5.1 分支与目录

| Agent | Worktree | 分支 | 主职责 |
|---|---|---|---|
| Frontend Agent | `../frontend-worktree` | `feature/frontend-structure-ui` | 前端结构确认、UI 统一、页面/API 映射 |
| Backend Agent | `../backend-worktree` | `feature/backend-contracts-baseline` | 后端 API、DB、文件存储、任务状态机 |
| AI Agent | `../ai-worktree` | `feature/ai-pipeline-baseline` | YOLO/CLAHE/Qwen-VL/评估链路基线 |
| Documentation Agent | `../docs-worktree` | `docs/replan-contracts-tests` | 文档、测试、差异清单、验收 checklist |

### 5.2 创建策略（后续执行时使用）

```powershell
# 示例：仅在进入执行阶段且当前仓库已初始化 git 后使用
git worktree add ../frontend-worktree -b feature/frontend-structure-ui
git worktree add ../backend-worktree -b feature/backend-contracts-baseline
git worktree add ../ai-worktree -b feature/ai-pipeline-baseline
git worktree add ../docs-worktree -b docs/replan-contracts-tests
```

### 5.3 合并策略

1. Docs/Test 先合并纯文档与契约模板。
2. Backend 合并 API/DB/AI schema 基线。
3. Frontend 基于已确认 API schema 合并 UI/API 映射。
4. AI 合并模型输出与评估基线文档或脚本。
5. 每次合并前必须说明影响范围、风险、验证步骤和回滚方案。

## 6. Agent 任务拆分

### 6.1 Frontend Agent

#### Phase 1：结构确认

| ID | 任务 | 输入 | 输出 | 依赖 | 优先级 |
|---|---|---|---|---|---|
| FE-1 | 确认 `web-vue` 实际目录结构 | 完整源码 | 前端目录地图 | 源码补齐 | P0 |
| FE-2 | 建立页面-路由-API 调用矩阵 | `src/router`、views、api | `docs/frontend-page-api-map.md` | FE-1 | P0 |
| FE-3 | 标注当前 UI 风格不一致点 | 页面截图/源码 | UI 问题清单 | FE-1 | P1 |

#### Phase 2-3：契约对齐与核心体验

| ID | 任务 | 输出 | 协作方 | 优先级 |
|---|---|---|---|---|
| FE-4 | 对齐 API 返回结构和错误处理 | 前端 API 契约清单 | Backend | P0 |
| FE-5 | 统一图片/视频/实时检测结果展示模型 | 检测结果组件设计 | Backend + AI | P1 |
| FE-6 | 统一模型管理、数据集管理、评估页面信息架构 | 页面优化任务列表 | Backend + Docs | P1 |
| FE-7 | 建立基础 UI 规范 | 色彩、表格、表单、状态标签规范 | Docs | P1 |

### 6.2 Backend Agent

#### Phase 1：结构确认

| ID | 任务 | 输入 | 输出 | 依赖 | 优先级 |
|---|---|---|---|---|---|
| BE-1 | 确认 `web-flask` 实际目录结构 | 完整源码 | 后端目录地图 | 源码补齐 | P0 |
| BE-2 | 建立 API-服务-数据库表映射 | routes/services/db | `docs/backend-api-db-map.md` | BE-1 | P0 |
| BE-3 | 核对数据库文档与实际初始化代码 | DB 文档 + 源码 | DB 差异清单 | BE-1 | P0 |

#### Phase 2-3：契约与核心流程

| ID | 任务 | 输出 | 协作方 | 优先级 |
|---|---|---|---|---|
| BE-4 | 固化统一 API 响应格式 | API schema | Frontend + Docs | P0 |
| BE-5 | 固化 `detection_result` JSON | detection_result schema | AI + Frontend | P0 |
| BE-6 | 设计视频检测任务状态机 | 状态机文档 / 待实现任务 | Frontend + AI | P1 |
| BE-7 | 规范文件存储结构 | 文件路径/bucket/object_key 规范 | Frontend + Docs | P1 |
| BE-8 | 梳理权限边界和 JWT 字段 | 权限/JWT 契约 | Frontend | P1 |

### 6.3 AI Agent

#### Phase 1：AI 入口确认

| ID | 任务 | 输入 | 输出 | 依赖 | 优先级 |
|---|---|---|---|---|---|
| AI-1 | 梳理训练/验证/预测脚本 | `other/model_train/detect/code` | AI 脚本说明 | 已存在 | P0 |
| AI-2 | 确认应用内推理封装位置 | 后端源码 | 推理入口地图 | BE-1 | P0 |
| AI-3 | 梳理模型权重与指标 | weights/output | 模型基线说明 | 已存在 | P0 |

#### Phase 2-3：AI 契约与稳定性

| ID | 任务 | 输出 | 协作方 | 优先级 |
|---|---|---|---|---|
| AI-4 | 定义 YOLO 输出 JSON schema | 模型输出契约 | Backend + Frontend | P0 |
| AI-5 | 梳理 Qwen-VL prompt 与返回字段 | AI 分析字段契约 | Backend + Docs | P0 |
| AI-6 | 建立实时检测性能基线方案 | FPS/延迟测试方案 | Backend | P1 |
| AI-7 | 建立视频采样与关键帧策略 | 采样策略文档 | Backend + Frontend | P1 |
| AI-8 | 规划模型评估脚本化 | 评估脚本任务清单 | Docs/Test | P2 |

### 6.4 Documentation Agent

#### Phase 1：差异审计与文档体系

| ID | 任务 | 输入 | 输出 | 依赖 | 优先级 |
|---|---|---|---|---|---|
| DOC-1 | 建立文档-源码差异清单 | 7 份规划文档 + 源码 | `DOC_SOURCE_GAP_REPORT.md` | FE-1/BE-1 | P0 |
| DOC-2 | 建立共享契约目录 | API/DB/AI/文件/JWT | `docs/contracts/` | BE/AI/FE | P0 |
| DOC-3 | 建立测试资源说明 | `4测试包/` | 测试资源索引 | 已存在 | P0 |

#### Phase 2-4：测试与验收体系

| ID | 任务 | 输出 | 协作方 | 优先级 |
|---|---|---|---|---|
| DOC-4 | 建立启动 checklist | 启动验证文档 | Backend + Frontend | P0 |
| DOC-5 | 建立冒烟测试 checklist | 图片/视频/实时/评估/报告测试 | 全部 | P1 |
| DOC-6 | 更新架构图/ER 图/流程图 | 维护文档 | Backend + AI | P1 |
| DOC-7 | 维护 ROADMAP 与 Milestone 状态 | 进度文档 | 全部 | P1 |

## 7. 多 Agent 并行开发方案

### 7.1 并行批次设计

| 批次 | 可并行任务 | 串行门禁 |
|---|---|---|
| Batch A：结构确认 | FE-1、BE-1、AI-1、AI-3、DOC-3 | 必须先补齐源码；AI 训练目录可先做 |
| Batch B：映射与差异 | FE-2、BE-2、BE-3、AI-2、DOC-1 | 依赖 Batch A 输出 |
| Batch C：共享契约 | FE-4、BE-4、BE-5、AI-4、AI-5、DOC-2 | Backend/AI 先出 schema，Frontend 再对齐 |
| Batch D：可运行基线 | DOC-4、图片检测冒烟、视频检测冒烟、实时检测冒烟、模型评估冒烟 | 契约稳定后执行 |
| Batch E：核心优化 | FE-5/6/7、BE-6/7/8、AI-6/7、DOC-5/6 | 基线通过后执行 |

### 7.2 并行约束

- Frontend 不直接改 API 返回结构，只提出需求。
- Backend 不直接改模型类别或模型输出格式，只协调 AI Agent。
- AI Agent 不直接替换生产模型权重，不改变类别定义。
- Documentation Agent 不覆盖代码，只维护契约、差异、验收。
- 任一共享契约变更必须更新 `docs/contracts/` 或对应根文档。

## 8. Phase 1 → Phase N 工程化升级路线

### Phase 1：源码结构确认与差异审计

目标：把“推断”变成“源码确认”。

交付：

- 前端目录地图
- 后端目录地图
- AI 入口地图
- 文档-源码差异清单
- 测试资源索引

验收：

- 清楚哪些模块已源码确认，哪些仍待确认。
- 清楚页面、API、DB、AI 入口之间的关系。

### Phase 2：共享契约固化与可运行基线

目标：先稳定协作边界，再做优化。

交付：

- API 响应 schema
- `detection_result` schema
- AI 分析返回字段
- DB 字段核对表
- 文件存储规范
- JWT 字段说明
- 启动与冒烟测试 checklist

验收：

- 图片检测、视频检测、实时检测、模型评估、报告导出具备最小验证路径。

### Phase 3：核心流程稳定化

目标：修复影响主流程稳定性的工程问题。

重点：

- 图片检测结果展示和报告字段稳定。
- 视频检测任务状态机、进度、失败恢复。
- 实时检测模型缓存、摄像头释放、目标去重。
- 模型发布与选择逻辑清楚。

### Phase 4：工程质量与测试体系

目标：让系统可以持续维护。

重点：

- 后端错误码、日志、异常处理。
- 前端统一错误提示、loading、鉴权失效处理。
- 测试包驱动的冒烟测试和回归清单。
- 文档与源码同步流程。

### Phase 5：体验与性能优化

目标：提升用户体验和实时/视频处理体验。

重点：

- UI 风格统一。
- 检测结果组件化。
- 视频关键帧筛选和进度体验。
- 实时检测 FPS/延迟优化。
- 模型评估可视化。

### Phase 6：受控扩展

仅在 Phase 1-5 完成后启动。

候选方向：

- 多类别检测
- GPU 推理优化
- 实时告警系统
- 水域治理数据分析
- 网络摄像头接入
- UI 大屏化

仍不优先：微服务、Kubernetes、云原生、大规模分布式、商业支付、移动端 App。

## 9. 风险与依赖关系

| 风险 | 依赖/触发 | 影响 | 缓解 |
|---|---|---|---|
| 前后端源码仍未补齐 | Phase 1 | 无法源码级确认 | 保持推断边界，不进入实现 |
| 共享契约未固化 | Phase 2 | 并行开发互相破坏 | Backend/AI 先出 schema，Frontend 再接入 |
| 模型输出格式变化 | AI 优化 | 前端展示、报告、评估失效 | 保持兼容，版本化 schema |
| 数据库字段变更 | 后端优化 | 历史数据不兼容 | 当前不重构 DB，后续需迁移方案 |
| 视频/实时性能问题 | Phase 3/5 | 卡顿、任务失败、资源占用 | 建立基线、状态机、资源释放验证 |
| Qwen-VL API 不稳定 | AI 分析链 | 分析失败或超时 | 超时、重试、降级提示、日志脱敏 |
| 多 Agent 文件冲突 | 并行开发 | 覆盖彼此改动 | 独立 worktree、分支、共享契约 review |

## 10. 后续实施顺序

1. **确认本 replan 文档作为 Phase 0 输出**。
2. 准备 Git worktree：frontend/backend/ai/docs 四条独立工作线。
3. 若已补齐完整源码，进入 Phase 1；若未补齐，则先停留在文档与契约准备阶段。
4. Phase 1 中四个 Agent 并行做结构确认和差异审计。
5. Phase 2 由 Backend + AI 牵头固化契约，Frontend 和 Docs 跟进对齐。
6. Phase 2 结束前必须完成最小启动和冒烟测试 checklist。
7. Phase 3 开始核心流程稳定化，优先视频检测、实时检测、模型管理、检测结果展示。
8. Phase 4 建立测试/日志/错误处理/文档同步体系。
9. Phase 5 做 UI 统一和性能体验优化。
10. Phase 6 只在基础稳定后启动扩展能力。

## 11. Acceptance Criteria

本 replan 完成标准：

- [x] 有系统级执行路线。
- [x] 有 Frontend / Backend / AI / Documentation Agent 任务拆分。
- [x] 有多 Agent 并行批次方案。
- [x] 有阶段性 Milestone。
- [x] 有 worktree 开发策略。
- [x] 有后续实施顺序。
- [x] 有风险与依赖关系。
- [x] 有 Phase 1 → Phase N 工程化升级路线。
- [x] 未进入功能代码实现。

## 12. ADR

### Decision

采用“先 replan 与契约、再源码确认、再可运行基线、再并行优化”的工程化升级路线。

### Drivers

- 当前前后端源码在工作区不完整。
- 多 Agent 并行需要强边界和共享契约。
- AI 链路跨前端、后端、模型、报告和测试，必须先稳定 schema。

### Alternatives Considered

- 直接进入功能开发：拒绝，风险过高。
- 等源码补齐后再做全部规划：部分采纳为 Phase 1，但不阻塞当前 replan。
- 立即微服务化或云原生改造：拒绝，违反当前非目标。

### Consequences

- 短期会增加文档与契约工作量。
- 中期能降低多 Agent 并行冲突和返工。
- 长期形成可维护的工程文档体系和升级路线。

### Follow-ups

- 补齐完整 `web-vue` / `web-flask` 源码后执行 Phase 1。
- 建立 `docs/contracts/` 目录沉淀 API/DB/AI schema。
- 用 `4测试包/` 建立冒烟和回归验证。
