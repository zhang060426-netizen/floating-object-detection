# 水面漂浮物智能检测平台

> 基于 **YOLO 目标检测 + 多模态 AI 分析** 的水面漂浮物检测、分析与治理辅助平台。当前阶段目标是系统级梳理、工程化升级规划与多 Agent 协作拆分，不直接进入大规模编码实现。

## 1. 项目定位

本项目面向河流、湖泊、水库等水域场景，提供水面漂浮物/垃圾的智能识别、检测记录管理、模型管理、数据集管理、模型评估、多模态分析和报告导出能力。

核心链路：

1. **视觉检测链路**：图片/视频/实时摄像头输入 → YOLO 检测/跟踪 → 目标框、关键帧、检测记录。
2. **AI 分析链路**：YOLO 检测结果 + 原图/增强图 → Qwen-VL 多模态分析 → 污染描述、治理建议、Word 报告。

## 2. 当前工程阶段

当前项目属于 **Brownfield Existing Project**：已有平台雏形与较完整文档，但前后端源码在当前工作区中不完整。

本阶段只做工程规划文档体系建设：

- 系统架构梳理
- 模块边界分析
- AI 链路分析
- 工程化升级规划
- 多 Agent 协作拆分
- 后续开发路线设计

本阶段明确不做：

- 不直接大规模修改代码
- 不立即运行或重新训练模型
- 不强行补写缺失源码
- 不重构数据库
- 不更换大模型 API
- 不进行微服务化、云原生、Kubernetes 改造
- 不承诺源码级 100% 精确结论

## 3. 文档索引

| 文档 | 用途 | 主要读者 |
|---|---|---|
| `README.md` | 项目总览与文档入口 | 所有人 |
| `ROADMAP.md` | 阶段目标、优先级、执行路线 | 项目负责人、所有 Agent |
| `ARCHITECTURE.md` | 系统架构、数据流、核心链路 | 架构/后端/AI/前端 Agent |
| `MODULE_BOUNDARIES.md` | 模块职责、目录边界、共享契约 | 所有开发 Agent |
| `MULTI_AGENT_PLAN.md` | 多 Agent 分工、worktree、协作流程 | 多 Agent 执行团队 |
| `AI_PIPELINE_ANALYSIS.md` | YOLO/CLAHE/Qwen-VL/视频/实时/评估链路 | AI Agent、Backend Agent |
| `SYSTEM_OPTIMIZATION_PLAN.md` | 工程化优化方向、风险、优先级 | 项目负责人、所有 Agent |

## 4. 逻辑模块地图

| 逻辑模块 | 当前/预期目录 | 职责 |
|---|---|---|
| 前端系统 | `1项目代码/floating-objects-detect-web/web-vue/` | Vue3 页面、Element Plus UI、ECharts、API 对接、检测/管理/评估页面 |
| 后端系统 | `1项目代码/floating-objects-detect-web/web-flask/` | Flask API、JWT、文件上传、数据库逻辑、异步任务、模型/数据集管理 |
| AI/模型训练 | `1项目代码/floating-objects-detect-web/other/model_train/detect/` | YOLO 训练、验证、预测、权重、数据集、评估产物 |
| 项目文档 | `3项目文档/` | 系统介绍、数据库设计、训练说明、系统图、使用注意事项 |
| 测试资源 | `4测试包/` | 测试图片、测试视频、评估图片、标签、数据集包 |

## 5. 推断边界

当前工作区的 `web-vue` 与 `web-flask` 只发现说明/依赖文件，未发现完整 `src/`、`routes/`、`algo/`、数据库访问层源码。本文档对前后端内部实现的描述主要来自项目文档、数据库设计、API 说明和依赖配置，需在补齐源码后复核。

## 6. 后续 Agent 使用方式

1. 所有 Agent 先读 `AGENTS.md`、`PROJECT_CONTEXT.md`、本 `README.md`。
2. 按任务类型读取专项文档。
3. 跨模块改动必须先更新文档和共享契约，再实现。
4. 补齐完整前后端源码后，先对“待源码确认”条目做复核，再进入重构或功能开发。

## Phase 2B Batch3 当前稳定版本

最新稳定基线：`phase2b-batch3-docker-compose-stable`

- Tag target：`fddb0c83486abaa3403db030c1d8d0e994331dab`
- Closeout：COMPLETE
- Final Smoke Verification：PASS
- Docker Compose config/build/up：PASS
- Backend health/db：PASS
- Frontend HTTP 200：PASS
- Login `admin/admin123`：PASS
- Image detection API / result image / records save-read：PASS
- `detection_result.v1`：PRESERVED
- Runtime model mount：PASS
- Batch4：NOT ENTERED

Final smoke 在 `E:\MM\floating-smoke-master` 执行，以规避原中文路径触发的 Docker BuildKit/buildx 非 ASCII session 问题。

下一步只允许开启 Batch4 Planning，不允许直接进入 Batch4 implementation。

# Phase 2B Batch4 Step 2 Stable Baseline Archive (2026-05-21)

```text
latest stable baseline: phase2b-batch4-step2-frontend-timing-stable
stable commit: 78b9896c133bfdf59b99a03a41348b3a372885b8
Step 2 status: CLOSED / VERIFIED / TAGGED
Step 2 completed: Frontend display backend timing metadata
Step 2 implementation commit: 6d9713f
Step 2 merge commit: 7032185
Step 2 closeout merge commit: 78b9896
detection_result.v1: PRESERVED
timing behavior:
  - detection_result.timing consumed
  - detection_result.timing_ms legacy fallback preserved
  - timing optional
  - missing timing / legacy no timing compatible
Step 3: NOT AUTHORIZED
push: NOT DONE
```

This is a documentation-only post-tag archive. It does not authorize Step 3, push, new tags, backend work, frontend implementation work, Docker work, DB schema changes, runtime/storage changes, model/weight/category/training changes, video/realtime/Word/Dashboard work.

