# TASK_PHASE2B_BATCH1 — Backend Agent

## 0. 状态恢复

- Baseline commit: `9970720`
- Worktree: `E:/MM/floating-worktrees/backend-worktree`
- Branch: `backend-rebuild`
- 当前阶段: `Phase 2B PRE-DEV FROZEN`
- 本批次定位: Phase 2B 最小 Flask API / DB / 文件 / 单图检测服务重建。

> 禁止重新 deep-interview、replan、生成 Phase 1/2A 文档。禁止修改前端 UI、AI 训练脚本、模型权重。

## 1. 必读输入

- [ ] `AGENTS.md`
- [ ] `PROJECT_CONTEXT.md`
- [ ] `PHASE2B_PRE_DEV_FREEZE.md`
- [ ] `PHASE2A_MASTER_SUMMARY.md`
- [ ] `agent_outputs/backend/API_CONTRACT.md`
- [ ] `agent_outputs/backend/DB_CONTRACT.md`
- [ ] `agent_outputs/backend/DETECTION_RESULT_SCHEMA.md`
- [ ] `agent_outputs/backend/FILE_STORAGE_CONTRACT.md`
- [ ] `agent_outputs/backend/BACKEND_PHASE2B_GATE.md`
- [ ] `agent_outputs/ai/AI_OUTPUT_SCHEMA.md`
- [ ] `agent_outputs/ai/MODEL_ASSET_BASELINE.md`
- [ ] `agent_outputs/docs/SMOKE_TEST_RESOURCE_MAP.md`

## 2. 写入边界

允许写入：

- `web-flask/`
- 必要的后端本地说明文件，例如 `web-flask/README.md`

禁止写入：

- `web-vue/`
- `other/model_train/detect/` 训练代码
- 模型权重的替换、移动、删除
- 前端页面、AI 类别定义、Phase 1/2A 文档

## 3. Batch1 目标

建立最小可运行 Flask 后端：

1. App 可启动并提供 `/health`。
2. 提供最小 auth/JWT 流程。
3. 初始化 SQLite 最小 schema。
4. 提供模型列表/当前模型信息读取。
5. 支持单张图片上传检测，调用 AI 封装或安全占位路径，保存原图、结果图、detection_records。
6. 提供检测记录列表/详情与文件访问接口。

必须保持 API、DB、文件、detection_result 契约与 Phase 2A 输出兼容。

## 4. 明确不做

- 不做视频检测。
- 不做实时检测。
- 不做 Word 报告。
- 不做完整模型生命周期管理。
- 不做训练、验证、权重替换。
- 不做复杂 RBAC；只实现 Phase 2B 默认账号/JWT 最小能力。

## 5. 推荐任务拆分

### BE-1 工程骨架

- 创建/修复 Flask 应用入口。
- 组织 routes/services/db/config/storage 的最小结构。
- 支持环境变量配置：secret、db path、upload path、model path。

验收：

- 后端可启动。
- `/health` 返回稳定 JSON。

### BE-2 Auth/JWT

- 实现默认账号登录。
- 签发 JWT，包含冻结契约要求字段。
- 保护业务接口。

验收：

- 正确账号可登录。
- 错误账号失败。
- 未带 token 访问受保护接口返回 401。

### BE-3 DB 初始化与 Repository

- 按 `DB_CONTRACT.md` 实现 users、models、detection_records 等最小表。
- 提供可重复执行的初始化脚本或启动初始化。
- 不破坏后续扩展字段兼容性。

验收：

- 空库可自动/手动初始化。
- detection_records 可写入并查询。

### BE-4 文件存储

- 按 `FILE_STORAGE_CONTRACT.md` 创建上传/结果目录。
- 保存原图、结果图；返回可访问 URL。
- 做文件类型、大小、路径穿越防护。

验收：

- 上传图片可保存。
- 文件访问接口可读取已保存文件。
- 非法路径不能逃逸存储根目录。

### BE-5 单图检测服务

- 与 AI Agent 的 `AI_OUTPUT_SCHEMA.md` 对齐。
- 默认类别保持 `0 -> floating_object`。
- 输出 detection_result，包含 boxes/classes/confidence/summary/model/file metadata。
- 若真实 YOLO 依赖不可用，可实现明确标记的安全失败/占位错误，不得伪造检测成功。

验收：

- 有模型和依赖时可执行单图检测。
- 无模型/依赖时返回可诊断错误，前端可显示。
- 成功检测会保存记录。

### BE-6 Records API

- 列表、详情接口按契约返回。
- 支持按用户隔离最小查询。
- 原始 JSON 可回放。

验收：

- 前端可消费列表和详情。
- 字段与 `API_CONTRACT.md` 一致。

## 6. 验证要求

完成前至少运行：

```powershell
cd E:/MM/floating-worktrees/backend-worktree/web-flask
python -m compileall .
python -m pytest
```

如果测试框架尚未存在，创建最小 smoke tests：health、login、unauthorized、DB init、records schema。不得把未执行测试报告为通过。

## 7. 交付物

- 后端源码改动，仅限 `web-flask/`。
- 初始化/启动说明。
- 最小 smoke test 或手动验证记录。
- 最终报告包含：修改内容、影响范围、风险点、验证命令与结果、回滚方式。

## 8. 回滚方案

在 `backend-worktree` 中回滚 `web-flask/` 改动；保留模型权重原状。若发现契约冲突，停止扩展实现并输出 API/DB/schema 差异清单。
