# TASK_PHASE2B_BATCH1 — Frontend Agent

## 0. 状态恢复

- Baseline commit: `9970720`
- Worktree: `E:/MM/floating-worktrees/frontend-worktree`
- Branch: `frontend-rebuild`
- 当前阶段: `Phase 2B PRE-DEV FROZEN`
- 本批次定位: Phase 2B 最小可运行前端重建任务派发；只在 Gate 已满足后进入业务代码实现。

> 禁止重新 deep-interview、replan、生成 Phase 1/2A 文档。禁止修改后端、AI、数据库与模型权重。

## 1. 必读输入

按顺序读取并在任务记录中勾选：

- [ ] `AGENTS.md`
- [ ] `PROJECT_CONTEXT.md`
- [ ] `PHASE2B_PRE_DEV_FREEZE.md`
- [ ] `PHASE2A_MASTER_SUMMARY.md`
- [ ] `agent_outputs/frontend/FRONTEND_PAGE_MAP.md`
- [ ] `agent_outputs/frontend/FRONTEND_CONTRACT_REVIEW.md`
- [ ] `agent_outputs/frontend/FRONTEND_PHASE2B_GATE.md`
- [ ] `agent_outputs/backend/API_CONTRACT.md`
- [ ] `agent_outputs/backend/DETECTION_RESULT_SCHEMA.md`
- [ ] `agent_outputs/backend/FILE_STORAGE_CONTRACT.md`
- [ ] `agent_outputs/ai/AI_OUTPUT_SCHEMA.md`
- [ ] `agent_outputs/docs/SMOKE_TEST_RESOURCE_MAP.md`

## 2. 写入边界

允许写入：

- `web-vue/`
- 必要的前端本地说明文件，例如 `web-vue/README.md`

禁止写入：

- `web-flask/`
- `other/model_train/detect/`
- `agent_outputs/backend/`、`agent_outputs/ai/`
- 数据库文件、模型权重、训练脚本

跨边界需求必须向 Leader 报告，不得自行修改共享契约。

## 3. Batch1 目标

在不扩展 Phase 2B 冻结范围的前提下，重建最小前端可运行骨架，对接后端最小 API 契约：

1. Vue3 最小工程入口可启动。
2. 登录页可提交账号密码并保存 JWT。
3. 图片检测页可上传单张图片，选择/使用默认模型，展示检测结果图与目标列表。
4. 检测记录页可查看列表与详情。
5. 基础路由、鉴权守卫、API client、错误提示具备最小可用能力。

## 4. 明确不做

- 不做视频检测页面完整实现。
- 不做实时检测页面完整实现。
- 不做 Word 报告导出。
- 不做大屏美化、ECharts 大规模可视化、主题大改。
- 不做训练、完整数据集管理、模型评估 UI。
- 不自行发明 API 字段；以后端契约为准。

## 5. 推荐任务拆分

### FE-1 工程骨架

- 创建/修复 `web-vue/package.json`、`index.html`、`src/main.*`、`src/App.*`。
- 使用 Vue3 + Vite + Element Plus + Pinia + Vue Router。
- 保持依赖最小化；除既有/必要依赖外不新增复杂库。

验收：

- `npm install` 后 `npm run build` 可执行。
- 未连接后端时页面仍能显示明确错误，而不是空白崩溃。

### FE-2 API Client 与鉴权

- 封装 API baseURL 配置。
- 实现 JWT 保存、读取、清除。
- 对 401 进行统一处理。
- 对接冻结契约中的 auth、model、detection、file endpoints。

验收：

- 登录成功后进入主界面。
- 刷新页面 token 不丢失。
- 未登录访问业务页会跳转登录页。

### FE-3 登录与主框架

- 最小登录页：用户名、密码、提交、错误提示。
- 最小布局：导航到图片检测、检测记录。
- 保留暂缓功能入口时必须标明“Phase 2B 暂不开放”，不得做假实现。

验收：

- 默认账号流程与后端契约匹配。
- UI 简洁一致，无大屏化扩展。

### FE-4 图片检测页

- 支持图片选择、预览、上传检测。
- 展示检测结果：结果图、置信度、类别、bbox、推理耗时/模型名（若 API 返回）。
- 对无目标、推理失败、后端不可用给出清晰提示。

验收：

- 能消费 `DETECTION_RESULT_SCHEMA.md` 中的 detection_result。
- 不依赖视频/实时/报告功能。

### FE-5 检测记录页

- 实现记录列表：时间、文件名、模型、目标数量、状态。
- 实现记录详情：原图/结果图、目标列表、原始 JSON 折叠展示。
- 文件 URL 访问遵循 `FILE_STORAGE_CONTRACT.md`。

验收：

- 可查看后端保存的 image detection records。
- 缺图/404 有降级提示。

## 6. 验证要求

完成前至少运行：

```powershell
cd E:/MM/floating-worktrees/frontend-worktree/web-vue
npm run build
```

如依赖未安装，先记录并在允许网络/本地依赖可用时安装；不能把未安装依赖伪装为通过。

## 7. 交付物

- 前端源码改动，仅限 `web-vue/`。
- `web-vue/README.md` 或等价说明，包含启动、配置、已实现/未实现功能。
- 最终报告包含：修改内容、影响范围、风险点、验证命令与结果、回滚方式。

## 8. 回滚方案

在 `frontend-worktree` 中回滚本批次前端改动；不得影响 backend/ai/docs worktree。若 API 契约不匹配，停止扩展实现并向 Leader 提交契约差异清单。
