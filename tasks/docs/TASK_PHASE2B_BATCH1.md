# TASK_PHASE2B_BATCH1 — Docs/Test Agent

## 0. 状态恢复

- Baseline commit: `9970720`
- Worktree: `E:/MM/floating-worktrees/docs-worktree`
- Branch: `docs-rebuild`
- 当前阶段: `Phase 2B PRE-DEV FROZEN`
- 本批次定位: 维护 Phase 2B Batch1 契约索引、Gate 状态、烟测计划与验收记录；不写业务代码。

> 禁止重新 deep-interview、replan、生成 Phase 1/2A 文档。禁止修改前端/后端/AI 业务实现。

## 1. 必读输入

- [ ] `AGENTS.md`
- [ ] `PROJECT_CONTEXT.md`
- [ ] `REPLAN.md`
- [ ] `PHASE1_MASTER_SUMMARY.md`
- [ ] `PHASE2A_MASTER_SUMMARY.md`
- [ ] `PHASE2B_PRE_DEV_FREEZE.md`
- [ ] `agent_outputs/docs/CONTRACT_INDEX.md`
- [ ] `agent_outputs/docs/PHASE2B_GATE_CHECKLIST.md`
- [ ] `agent_outputs/docs/SMOKE_TEST_RESOURCE_MAP.md`
- [ ] `agent_outputs/docs/EVIDENCE_LEVELS.md`
- [ ] `agent_outputs/frontend/FRONTEND_PHASE2B_GATE.md`
- [ ] `agent_outputs/backend/BACKEND_PHASE2B_GATE.md`
- [ ] `agent_outputs/ai/AI_PHASE2B_GATE.md`

## 2. 写入边界

允许写入：

- `agent_outputs/docs/`
- `tasks/docs/`
- 必要的验收/烟测报告文件

禁止写入：

- `web-vue/`
- `web-flask/`
- `other/model_train/detect/` 业务/训练代码
- 模型权重、数据库运行文件

## 3. Batch1 目标

1. 将 `PHASE2B_PRE_DEV_FREEZE.md` 纳入契约索引。
2. 修正 Phase 2A 遗留的“待输出”状态：合同已输出，但源码实现仍待验证。
3. 维护 Batch1 范围边界：登录、图片检测、模型加载、检测记录保存。
4. 形成 Batch1 smoke test plan。
5. 在各 Agent 交付后记录 smoke test report 与 Gate 结果。

## 4. 明确不做

- 不重写 Phase 1/2A 总结。
- 不重新规划系统路线。
- 不实现业务代码。
- 不扩展视频、实时、Word、dashboard、训练、完整数据集管理。
- 不把文档推断当作源码事实；必须标注证据等级。

## 5. 推荐任务拆分

### DOC-1 契约索引更新

- 更新/补充 `CONTRACT_INDEX.md`：纳入 `PHASE2B_PRE_DEV_FREEZE.md`。
- 标注 API/DB/file/AI schema 的来源和证据等级。
- 将“待输出”改为“已输出 / 待源码实现确认”。

验收：

- 索引能指导 Frontend/Backend/AI Batch1。
- 不覆盖原始证据，只做状态校正。

### DOC-2 Gate Checklist 校正

- 更新 `PHASE2B_GATE_CHECKLIST.md`。
- 标记已满足项：baseline commit `9970720`、worktree 已创建、最小范围已冻结。
- 标记仍需实现后验证项：前端 build、后端 smoke、AI 推理适配、端到端图片检测。

验收：

- Gate 状态清晰区分“PRE-DEV FROZEN”和“runtime pass”。

### DOC-3 Smoke Test Plan

生成或更新 Batch1 烟测计划，覆盖：

1. 后端 health。
2. 登录成功/失败/未授权。
3. 模型列表/当前模型读取。
4. 图片上传检测。
5. 原图/结果图 URL 访问。
6. detection_records 保存、列表、详情。
7. 前端登录、图片检测、记录查看。
8. 暂缓功能未误实现：视频、实时、Word、dashboard、训练、完整数据集管理。

验收：

- 每个用例含前置条件、步骤、期望结果、证据字段。

### DOC-4 交付验收记录模板

准备 Batch1 验收报告模板，包含：

- Agent/Worktree/Branch/Commit。
- 修改范围。
- 验证命令与结果。
- 契约偏差。
- 风险与回滚方式。
- Gate 判定。

验收：

- 各 Agent 能直接填报。

### DOC-5 最终汇总（等待实现后）

在 Frontend/Backend/AI 完成后，汇总：

- build/test/smoke evidence。
- scope 是否未扩展。
- 失败项与阻塞项。
- 是否允许进入下一批次。

验收：

- 没有证据不得标记通过。

## 6. 验证要求

完成本批文档更新后至少检查：

```powershell
cd E:/MM/floating-worktrees/docs-worktree
Get-ChildItem agent_outputs/docs,tasks/docs -Recurse -File | Select-Object FullName,Length,LastWriteTime
```

并人工确认文档没有把未实现运行时能力写成已通过。

## 7. 交付物

建议输出/更新：

- `agent_outputs/docs/CONTRACT_INDEX.md`
- `agent_outputs/docs/PHASE2B_GATE_CHECKLIST.md`
- `agent_outputs/docs/PHASE2B_BATCH1_SMOKE_TEST_PLAN.md`
- `agent_outputs/docs/PHASE2B_BATCH1_ACCEPTANCE_TEMPLATE.md`
- 后续实现完成后：`agent_outputs/docs/PHASE2B_BATCH1_SMOKE_TEST_REPORT.md`

## 8. 回滚方案

只回滚 docs worktree 中本批次文档改动；不得触碰业务代码。若发现契约冲突，保留冲突记录并通知 Leader 决策，不自行改 API/DB/AI schema。
