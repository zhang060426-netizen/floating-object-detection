# Phase 2B Gate Checklist

更新时间：2026-05-13  
阶段：Phase 2A 输出，供 Phase 2B 准入判定使用  
边界：只写门禁清单；不执行测试、不修改代码、不修改模型、数据库或测试资源。

## 1. Gate 判定说明

| 判定项 | PASS 条件 | BLOCKED 条件 | 证据等级 |
|---|---|---|---|
| Phase 2B 准入 | 契约草案齐全、源码恢复或最小重建范围明确、测试资源映射完成、worktree 策略明确 | 任一关键契约缺失、前后端源码状态不明、无启动路径、违反禁止项 | 文档推断 |

## 2. 源码门禁

| 检查项 | PASS 条件 | 当前状态 | 证据等级 |
|---|---|---|---|
| 前端源码 | 已恢复 `index.html`、`vite.config.*`、`src/main.*`、`src/router`、`src/views`，或最小重建范围冻结 | 当前缺失 | 冲突/差异 |
| 后端源码 | 已恢复 Flask 入口、routes、services、DB 初始化，或最小重建范围冻结 | 当前缺失 | 冲突/差异 |
| 源码事实审计 | 恢复后重新执行 FE/BE 源码审计 | 未执行，等待源码 | 待源码确认 |

## 3. 契约门禁

| 检查项 | PASS 条件 | 当前状态 | 证据等级 |
|---|---|---|---|
| API_CONTRACT | 完成并标注证据等级 | 待 Backend 输出 | 待源码确认 |
| DETECTION_RESULT_SCHEMA | 完成并经 Backend/AI/Frontend review | 待 Backend 输出 | 待源码确认 |
| AI_OUTPUT_SCHEMA | 完成并区分离线输出与应用输出 | 待 AI 输出 | 已资源确认 |
| DB_CONTRACT | 完成并标注数据库文档来源 | 待 Backend 输出 | 数据库文档确认 |
| FILE_STORAGE_CONTRACT | 完成 bucket/object_key 候选规范 | 待 Backend 输出 | 数据库文档确认 |
| QWEN_VL_ANALYSIS_SCHEMA | 完成字段草案并标注配置缺失 | 待 AI 输出 | 待源码确认 |
| EVALUATION_METRICS_SCHEMA | 完成 metrics 字段草案 | 待 AI 输出 | 历史输出确认 |

## 4. 前端门禁

| 检查项 | PASS 条件 | 当前状态 | 证据等级 |
|---|---|---|---|
| 工程入口 | `index.html`、`vite.config.*`、`src/main.*` 明确 | 当前缺失 | 冲突/差异 |
| 页面最小范围 | 登录、图片检测、记录、模型选择、基础布局已在页面地图中冻结 | 待 Frontend 输出 | 文档推断 |
| API 消费 | 只以 API_CONTRACT 为依据 | 待 API_CONTRACT | 文档推断 |
| 权限状态 | token、role、当前用户状态字段明确 | 待 API/JWT 契约 | 待源码确认 |

## 5. 后端门禁

| 检查项 | PASS 条件 | 当前状态 | 证据等级 |
|---|---|---|---|
| Flask 入口 | `app.py` 或等价启动模块存在或最小重建范围冻结 | 当前缺失 | 冲突/差异 |
| 最小 routes | health、user、detection、file 范围明确 | 待 Backend 输出 | 文档推断 |
| 统一响应 | 成功/失败/鉴权失败/权限不足/参数错误格式明确 | 待 API_CONTRACT | 文档推断 |
| DB 初始化 | 初始化策略明确，不直接改现有 DB | 待 DB_CONTRACT | 数据库文档确认 |
| 文件存储 | 存储根目录、bucket/object_key、URL 候选明确 | 待 FILE_STORAGE_CONTRACT | 数据库文档确认 |

## 6. AI 门禁

| 检查项 | PASS 条件 | 当前状态 | 证据等级 |
|---|---|---|---|
| 类别定义 | 保持 `class_id=0`、`floating_object` | 已由 `data.yaml` 确认 | 已资源确认 |
| 权重安全 | 不替换、不删除、不训练模型 | Phase 2A 遵守 | 已资源确认 |
| 基础权重 | `yolov8n.pt`、`yolo11n.pt`、`yolo12n.pt`、`yolo26n.pt` 存在 | 已确认 | 已资源确认 |
| 已训练权重缺口 | `best.pt` 缺失风险已说明 | 已由 AI 审计记录 | 冲突/差异 |
| 输出 schema | YOLO/Qwen-VL/metrics 草案完成 | 待 AI 输出 | 已资源确认 |

## 7. DB 门禁

| 检查项 | PASS 条件 | 当前状态 | 证据等级 |
|---|---|---|---|
| 表结构 | 10 张核心表字段已纳入 DB_CONTRACT | 待 Backend 输出 | 数据库文档确认 |
| 初始化数据 | admin/test、默认数据集、默认模型策略明确 | 文档存在，源码待确认 | 数据库文档确认 |
| 实际 DB | DB 文件或初始化脚本已确认 | 当前缺失 | 待源码确认 |
| 迁移策略 | Phase 2B 不做破坏性迁移 | 待 Leader Gate | 文档推断 |

## 8. 测试资源门禁

| 检查项 | PASS 条件 | 当前状态 | 证据等级 |
|---|---|---|---|
| 图片资源 | 最小图片和格式兼容样例已映射 | 已映射 | 已资源确认 |
| 视频资源 | 最小视频、中等视频、压力视频已映射 | 已映射 | 已资源确认 |
| 评估资源 | 评估图片和标签同名匹配 | 已确认 | 已资源确认 |
| 实时限制 | USB 摄像头限制已写明 | 已写明 | 文档推断 |
| 测试执行 | Phase 2A 不执行测试 | 未执行 | 文档推断 |

## 9. Worktree 门禁

| 检查项 | PASS 条件 | 当前状态 | 证据等级 |
|---|---|---|---|
| Frontend worktree | 进入前端代码恢复/重建前创建独立 worktree | Phase 2A 未创建 | 文档推断 |
| Backend worktree | 进入后端代码恢复/重建前创建独立 worktree | Phase 2A 未创建 | 文档推断 |
| AI worktree | 修改 AI 脚本前创建独立 worktree | Phase 2A 不修改 | 文档推断 |
| Docs worktree | 正式契约长期维护建议独立 worktree | 当前仅写 agent_outputs/docs | 文档推断 |

## 10. 禁止项检查

| 禁止项 | 当前结果 | 说明 | 证据等级 |
|---|---|---|---|
| 禁止写业务代码 | PASS | 本轮只写 markdown 文档 | 文档推断 |
| 禁止补齐 `web-vue` / `web-flask` 源码 | PASS | 未创建源码目录 | 文档推断 |
| 禁止修改数据库 | PASS | 未修改 DB 文件或 SQL 执行入口 | 文档推断 |
| 禁止训练模型 | PASS | 未运行训练/验证/预测 | 文档推断 |
| 禁止移动、删除、替换测试资源或权重 | PASS | 未操作资源文件 | 文档推断 |
| 禁止执行端到端冒烟测试 | PASS | 只写资源映射和 checklist | 文档推断 |

## 11. PASS / BLOCKED 判定模板

```text
Phase 2B Gate: PASS / BLOCKED

判定日期：
判定人：

PASS 依据：
- 契约草案齐全：
- 源码恢复或最小重建范围明确：
- Worktree 策略明确：
- 测试资源与冒烟路径明确：
- 禁止项未被违反：

BLOCKED 依据：
- 前后端源码状态不明：
- 契约草案缺失：
- DB/API/AI 输出仍无最小字段定义：
- 没有可执行的最小启动路径：
- 有 Agent 在未通过门禁前开始业务代码实现：

后续动作：
```
