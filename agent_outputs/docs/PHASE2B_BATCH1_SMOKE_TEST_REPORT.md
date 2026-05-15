# Phase 2B Batch1 Smoke Test Report

更新时间：2026-05-15  
阶段：Phase 2B Batch1 / Smoke Test Report  
报告状态：部分可联调，关键链路阻塞，**Batch1 全量 PASS 不授予**。  
边界：本报告只记录 Leader Gate Review 与 `PHASE2B_BATCH1_SMOKE_TEST_PLAN.md` 对应的可执行、已验证、阻塞项；不修改业务代码、不初始化数据库、不训练模型、不移动或替换权重。

## 0. 结论摘要

```text
Phase 2B Batch1 Gate: BLOCKED / FULL PASS NOT GRANTED

可联调范围：health / auth / model / records
关键阻塞：图片检测成功链路 BLOCKED，原因为 missing .pt
全量 PASS：不授予
下一步：补齐或明确 Batch1 使用的 .pt 权重策略后，重新执行图片检测、文件 URL、detection_result、记录详情闭环 smoke。
```

## 1. 输入依据

| 输入 | 路径/来源 | 使用方式 | 证据等级 |
|---|---|---|---|
| Leader Gate Review | 当前任务指令摘要 | 作为本报告的最新 Gate 判定来源：health/auth/model/records 可联调；图片检测因 missing .pt 阻塞；Batch1 全量 PASS 不授予 | 文档推断 |
| Smoke Test Plan | `agent_outputs/docs/PHASE2B_BATCH1_SMOKE_TEST_PLAN.md` | 用例 ID 与判定范围来源 | 文档推断 |
| Gate Checklist | `agent_outputs/docs/PHASE2B_GATE_CHECKLIST.md` | Gate 状态口径来源：没有证据不得标记 PASS | 文档推断 |
| Contract Index | `agent_outputs/docs/CONTRACT_INDEX.md` | Batch1 范围与契约边界来源 | 文档推断 |

> 注：本报告只记录当前已知 Gate Review 结果；若后续 Frontend/Backend/AI 提供命令日志、HTTP 响应、截图或 commit 证据，应追加到本文件而不是覆盖当前阻塞结论。

## 2. 执行环境记录

| 项 | 当前记录 |
|---|---|
| Docs worktree | `E:/MM/floating-worktrees/docs-worktree` |
| Docs branch | `docs-rebuild` |
| Baseline commit | `9970720` |
| 报告文件 | `agent_outputs/docs/PHASE2B_BATCH1_SMOKE_TEST_REPORT.md` |
| 是否修改业务代码 | 否 |
| 是否执行训练/验证/批量预测 | 否 |
| 是否替换/移动/删除权重 | 否 |

## 3. Smoke 用例判定总览

| 分组 | 对应用例 | 当前判定 | 说明 |
|---|---|---|---|
| Health | BE-H-01, BE-H-02 | 可联调 | Leader Gate Review 指示 health 可联调；本报告未收到具体 HTTP 响应证据，因此不升级为全量 PASS。 |
| Auth | AUTH-01 ~ AUTH-05 | 可联调 | 登录、登录失败、me、未授权访问属于可联调范围；待补充命令和响应摘要后可逐项判定 PASS/FAIL。 |
| Model | MODEL-01 ~ MODEL-03 | 可联调 / 存在权重阻塞风险 | 模型接口可联调；但图片检测链路报告 missing .pt，说明模型权重可用性仍阻塞检测成功链路。 |
| Image Detection | DET-01 ~ DET-07 | BLOCKED | 成功链路因 missing .pt 无法完成；不得标记图片检测 PASS。 |
| File URL | FILE-01 ~ FILE-04 | BLOCKED | 依赖 DET-01 成功产出 `original_image.url` / `result_image.url`；当前图片检测阻塞。 |
| Records | REC-01 ~ REC-05 | 可联调 | records 可联调；若仅验证列表/详情接口可记录局部结果，但依赖图片检测生成记录的闭环仍受 DET 阻塞影响。 |
| Frontend | FE-01 ~ FE-06 | 未记录 / 待证据 | 当前指令未提供 build、页面操作、截图或网络请求证据。 |
| 暂缓功能 | X-01 ~ X-05 | N/A / 需持续确认 | 视频、实时、Word、dashboard、训练、完整数据集管理不属于 Batch1 PASS 条件。 |

## 4. 详细记录

### 4.1 Health

| 用例 ID | 当前判定 | 证据/说明 | 后续需要 |
|---|---|---|---|
| BE-H-01 | 可联调 | Leader Gate Review：health 可联调。 | 补充 `GET /api/health` 命令、HTTP 状态、响应 JSON。 |
| BE-H-02 | 可联调 | health 应按计划无需 token；当前未收到实际响应证据。 | 补充无 token 请求结果。 |

### 4.2 Auth

| 用例 ID | 当前判定 | 证据/说明 | 后续需要 |
|---|---|---|---|
| AUTH-01 | 可联调 | Leader Gate Review：auth 可联调。 | 补充默认账号登录命令与脱敏 token 响应。 |
| AUTH-02 | 可联调 | 属 auth 可联调范围。 | 补充错误密码响应。 |
| AUTH-03 | 可联调 | 属 auth 可联调范围。 | 补充携带 token 请求 `/api/auth/me` 响应。 |
| AUTH-04 | 可联调 | 属 auth 可联调范围。 | 补充无 token 请求 `/api/auth/me` 的 401 响应。 |
| AUTH-05 | 可联调 | 属 auth 可联调范围。 | 补充无 token 请求受保护接口响应。 |

### 4.3 Model

| 用例 ID | 当前判定 | 证据/说明 | 后续需要 |
|---|---|---|---|
| MODEL-01 | 可联调 | Leader Gate Review：model 可联调。 | 补充 `/api/models/published` 响应摘要。 |
| MODEL-02 | 可联调 | 字段级验证仍待证据。 | 补充 `id/name/base_model/weight_path/status/is_dev_placeholder` 字段检查。 |
| MODEL-03 | BLOCKED 风险 | 图片检测阻塞原因为 missing .pt，说明权重路径或权重文件可用性未满足成功链路。 | 明确缺失 `.pt` 文件名、期望路径、实际路径、是否允许使用开发占位权重。 |

### 4.4 Image Detection

| 用例 ID | 当前判定 | 证据/说明 | 后续需要 |
|---|---|---|---|
| DET-01 | BLOCKED | 图片检测成功链路 BLOCKED：missing .pt。 | 补齐/确认 `.pt` 后重测上传检测。 |
| DET-02 | BLOCKED | 依赖 DET-01 成功响应。 | 重测后检查 `detection_result.model`。 |
| DET-03 | BLOCKED | 依赖 DET-01 成功响应。 | 重测后检查图片 width/height/filename。 |
| DET-04 | BLOCKED | 依赖 DET-01 成功响应。 | 重测后检查 `detections[]` 与 `0/floating_object`。 |
| DET-05 | BLOCKED | 依赖 DET-01 成功响应。 | 重测后检查 bbox 格式。 |
| DET-06 | BLOCKED | 依赖 DET-01 成功响应。 | 重测后检查空检测兼容。 |
| DET-07 | 未记录 | 错误上传用例未提供证据。 | 后续补充非法文件/空文件上传结果。 |

### 4.5 File URL

| 用例 ID | 当前判定 | 证据/说明 | 后续需要 |
|---|---|---|---|
| FILE-01 | BLOCKED | 原图 URL 访问依赖 DET-01 产出记录。 | 图片检测成功后验证。 |
| FILE-02 | BLOCKED | 结果图 URL 访问依赖 DET-01 产出结果图。 | 图片检测成功后验证。 |
| FILE-03 | BLOCKED | 依赖具体文件 URL。 | 图片检测成功后验证无 token 拒绝。 |
| FILE-04 | 未记录 | 路径穿越防护未提供证据。 | 后续补充非法 object_key 请求结果。 |

### 4.6 Records

| 用例 ID | 当前判定 | 证据/说明 | 后续需要 |
|---|---|---|---|
| REC-01 | 部分 BLOCKED | records 可联调，但自动保存记录依赖 DET-01 成功。 | 图片检测成功后验证 `record_id`。 |
| REC-02 | 可联调 | Leader Gate Review：records 可联调。 | 补充列表接口命令与响应摘要。 |
| REC-03 | 可联调 | records 可联调；详情是否能读取检测 JSON 待证据。 | 补充详情接口响应摘要。 |
| REC-04 | 部分 BLOCKED | `detection_result` 闭环依赖图片检测成功记录。 | 图片检测成功后验证 JSON 可解析。 |
| REC-05 | 可联调 | 不存在记录 ID 错误处理可独立联调。 | 补充 404/统一错误响应。 |

### 4.7 Frontend

| 用例 ID | 当前判定 | 证据/说明 | 后续需要 |
|---|---|---|---|
| FE-01 | 未记录 | 未收到前端 build 证据。 | 补充 `npm run build` 日志与 exit code。 |
| FE-02 | 未记录 | 未收到页面访问截图/控制台摘要。 | 补充登录页访问证据。 |
| FE-03 | 未记录 | 未收到前端登录操作证据。 | 补充截图或网络请求摘要。 |
| FE-04 | BLOCKED | 图片检测后端成功链路 missing .pt，前端完整检测展示无法闭环。 | 后端 DET 成功后重测。 |
| FE-05 | 部分 BLOCKED | 记录接口可联调，但图片检测生成记录闭环未通。 | 补充记录列表/详情页面证据。 |
| FE-06 | 未记录 | 未收到 token 失效/未登录处理证据。 | 补充页面或网络请求证据。 |

### 4.8 暂缓功能

| 用例 ID | 当前判定 | 说明 |
|---|---|---|
| X-01 | N/A | 视频检测不属于 Batch1 全量 PASS 条件。 |
| X-02 | N/A | 实时检测不属于 Batch1 全量 PASS 条件。 |
| X-03 | N/A | Word 报告不属于 Batch1 全量 PASS 条件。 |
| X-04 | N/A | dashboard/大屏/训练/完整数据集管理不属于 Batch1 全量 PASS 条件。 |
| X-05 | N/A | 本报告未执行训练、验证、批量预测，未修改权重。 |

## 5. 阻塞项

| 阻塞项 | 影响范围 | 严重性 | 当前结论 | 解除条件 |
|---|---|---|---|---|
| missing .pt | 模型加载到推理、图片检测、结果图、文件 URL、自动保存记录闭环 | 高 | Batch1 全量 PASS 不授予 | 明确并补齐期望 `.pt`，或由 Leader 批准使用存在的开发占位权重并更新 model 配置，再重跑 DET/FILE/REC/FE 相关用例。 |
| 缺少逐项命令/响应证据 | health/auth/model/records 只能记录为“可联调”，不能升级为 PASS | 中 | 局部 PASS 暂不授予 | 追加 HTTP 命令、状态码、响应 JSON 摘要、日志/截图。 |

## 6. 契约偏差与风险

| 契约域 | 偏差/风险 | 当前处理 |
|---|---|---|
| AI 权重 | 模型接口可联调但检测成功链路缺少 `.pt`，可能是路径、文件名或权重分发策略不一致 | 标记 BLOCKED，不在 docs worktree 修改权重或业务配置。 |
| detection_result | 因 DET-01 阻塞，无法验证实际 `detection_result` 字段与 schema 一致性 | 保持待验证。 |
| File API | 因 DET-01 阻塞，无法验证原图/结果图 URL | 保持待验证。 |
| Records | records 可联调，但检测自动保存闭环未验证 | 区分独立 records 接口可联调与检测记录闭环 BLOCKED。 |
| Frontend | 未收到 build/页面证据，且图片检测闭环阻塞 | 不授予前端 runtime PASS。 |

## 7. Gate 判定

```text
Phase 2B Batch1 Gate: BLOCKED
Full PASS: NOT GRANTED

可联调：
- health
- auth
- model
- records

阻塞：
- 图片检测成功链路 BLOCKED: missing .pt
- File URL 与 detection_result 闭环依赖图片检测成功，随 DET 阻塞
- 前端完整图片检测展示依赖 DET 成功，随 DET 阻塞

不得声明：
- Batch1 全量 PASS
- 图片检测已通过
- 模型推理已完成 runtime 验证
- result_image.url / original_image.url 已通过
- detection_records 自动保存闭环已通过
```

## 8. 后续动作

1. Backend/AI 明确 missing `.pt` 的具体文件名、期望路径、实际可用权重路径。
2. Leader 判定是否允许使用 `PHASE2B_PRE_DEV_FREEZE.md` 中的开发占位权重策略。
3. 权重问题解除后，按 `PHASE2B_BATCH1_SMOKE_TEST_PLAN.md` 重跑：DET-01~DET-06、FILE-01~FILE-03、REC-01/REC-04、FE-04/FE-05。
4. health/auth/model/records 若要升级为 PASS，需追加命令、HTTP 状态码、响应 JSON 摘要或截图/日志证据。
5. 在所有关键用例有证据前，维持 `BLOCKED / FULL PASS NOT GRANTED`。

## 9. 回滚方式

本次只新增/更新 docs 报告文件。若需回滚，只回滚：

```text
agent_outputs/docs/PHASE2B_BATCH1_SMOKE_TEST_REPORT.md
```

不得回滚或修改业务代码、数据库、模型权重、训练脚本或测试资源。
