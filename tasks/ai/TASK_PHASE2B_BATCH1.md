# TASK_PHASE2B_BATCH1 — AI Agent

## 0. 状态恢复

- Baseline commit: `9970720`
- Worktree: `E:/MM/floating-worktrees/ai-worktree`
- Branch: `ai-rebuild`
- 当前阶段: `Phase 2B PRE-DEV FROZEN`
- 本批次定位: 为 Backend Batch1 提供单图 YOLO 推理契约核对与最小适配建议；不训练、不替换权重。

> 禁止重新 deep-interview、replan、生成 Phase 1/2A 文档。禁止删除、移动、替换已有模型权重。

## 1. 必读输入

- [ ] `AGENTS.md`
- [ ] `PROJECT_CONTEXT.md`
- [ ] `PHASE2B_PRE_DEV_FREEZE.md`
- [ ] `PHASE2A_MASTER_SUMMARY.md`
- [ ] `agent_outputs/ai/AI_OUTPUT_SCHEMA.md`
- [ ] `agent_outputs/ai/MODEL_ASSET_BASELINE.md`
- [ ] `agent_outputs/ai/AI_PHASE2B_GATE.md`
- [ ] `agent_outputs/backend/DETECTION_RESULT_SCHEMA.md`
- [ ] `agent_outputs/backend/API_CONTRACT.md`
- [ ] `agent_outputs/docs/SMOKE_TEST_RESOURCE_MAP.md`

## 2. 写入边界

允许写入：

- `other/model_train/detect/` 中与推理适配说明或非破坏性 wrapper 相关文件（如确需代码）。
- AI Agent 自己的交付说明文件。

谨慎写入：

- 若需要提供 backend 可调用 wrapper，必须保持小文件、无训练副作用、无权重修改。

禁止写入：

- `web-vue/`
- `web-flask/` 业务代码
- 模型权重文件
- 类别定义的破坏性修改
- 训练、验证、批量评估脚本的行为变更

## 3. Batch1 目标

1. 核对当前可用模型资产与 Phase 2B 占位模型说明。
2. 固化单图推理输入/输出字段，确保 Backend 能转换为 `DETECTION_RESULT_SCHEMA.md`。
3. 明确类别映射保持 `0 -> floating_object`。
4. 明确 bbox 输出转换规则：`xyxy_pixel` 与 `xywhn`。
5. 提供 Backend 集成注意事项：依赖、模型路径、错误处理、CPU/GPU fallback。
6. 参与首批 smoke test 判读，但不声明性能指标。

## 4. 明确不做

- 不训练。
- 不验证完整测试集。
- 不给出新的 precision/recall/mAP 声明。
- 不替换、移动、删除权重。
- 不扩展多类别。
- 不引入 Qwen-VL 必需链路；多模态分析不在 Batch1 实现范围。

## 5. 推荐任务拆分

### AI-1 模型资产核对

- 检查 `MODEL_ASSET_BASELINE.md` 中记录的权重与实际文件是否一致。
- 标记 `yolo26n.pt` 作为开发占位模型的限制。
- 明确不能把占位模型当作生产 best.pt。

验收：

- 输出模型资产核对表。
- 无任何权重文件变更。

### AI-2 单图推理契约

- 定义 backend 调用所需输入：image_path、model_path、confidence、device 等。
- 定义输出：detections、annotated_image_path、summary、timing、errors。
- 对齐 `AI_OUTPUT_SCHEMA.md` 与 `DETECTION_RESULT_SCHEMA.md`。

验收：

- Backend Agent 可据此实现 adapter。
- 对无依赖/无权重/图片损坏有明确错误类型。

### AI-3 bbox 与类别转换说明

- 保持 `class_id=0`、`class_name=floating_object`。
- 说明从 YOLO 输出到 `xyxy_pixel` 的像素坐标转换。
- 说明从 `xyxy_pixel` 到 `xywhn` 的归一化转换。
- 说明坐标裁剪与四舍五入策略。

验收：

- 字段可直接进入 detection_result。
- 不修改类别定义。

### AI-4 Smoke 判读支持

- 从 `SMOKE_TEST_RESOURCE_MAP.md` 选择最小图片资源。
- 定义 smoke 只验证链路可运行与 schema 正确，不验证精度。
- 提供异常判定：模型缺失、依赖缺失、无目标、低置信度。

验收：

- Docs/Test Agent 可引用该判读规则。

## 6. 验证要求

至少执行只读/非破坏性检查：

```powershell
cd E:/MM/floating-worktrees/ai-worktree
Get-ChildItem -Recurse -File | Where-Object { $_.Name -match 'yolo|best|\.pt$' } | Select-Object FullName,Length,LastWriteTime
```

如新增 wrapper 代码，必须运行语法检查；如依赖缺失，记录为环境限制，不得伪造推理成功。

## 7. 交付物

- AI 推理契约核对说明，建议路径：`other/model_train/detect/PHASE2B_INFERENCE_ADAPTER_NOTES.md` 或同等位置。
- 如确需 wrapper：最小、无训练副作用、可由 Backend 调用的单图推理函数。
- 最终报告包含：修改内容、影响范围、风险点、验证命令与结果、回滚方式。

## 8. 回滚方案

回滚 AI worktree 中新增说明/wrapper 文件即可；权重与训练脚本不得变更，若误变更必须立即停止并报告 Leader。
