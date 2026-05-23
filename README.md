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

## Phase 2B Batch4 Step 3 Post-Tag Archive

```text
latest stable baseline: phase2b-batch4-step3-detection-records-stable
stable commit: bfe3dc9298cdcb0cb405b4189b6db151d2fea1c6
Step 3 status: CLOSED / VERIFIED / TAGGED
Step 3 completed: Detection Records Management Enhancement
Step 3 implementation commit: cfe8d75
Step 3 frontend merge commit: e5a7b59
Step 3 checklist commit: 1c5d415
Step 3 stable tag commit: bfe3dc9
build: npm.cmd run build PASS
backend: read-only verification PASS
backend records API: supports page/page_size and returns items/total/page/page_size
backend detail API: exists
backend implementation required: NO
detection_result.v1: PRESERVED
forbidden scope:
  - no backend change
  - no Docker change
  - no DB schema change
  - no runtime/storage change
  - no model/weights/classes/training change
  - no Dashboard / Word / video / realtime
  - no delete / bulk delete / edit records
push: NOT DONE
Step 4: NOT AUTHORIZED
```

This is a documentation-only post-tag archive. It records the already-created Step 3 stable tag and does not create a new tag, push, or authorize Step 4 implementation.

## Phase 2B Batch4 Step 4 Post-Tag Archive

```text
Step 4 stable tag: phase2b-batch4-step4-detail-readability-stable
tag commit: 66349abc9ba3f8ad4a31afe85d5430a52b0a4393
master HEAD before archive: 66349ab
Step 4 status: CLOSED / VERIFIED / TAGGED
push: NOT DONE
Step 5: NOT AUTHORIZED
```

Implementation summary:

- Detection record detail page readability enhancement.
- Fixed timing Chinese label garbling.
- Added file name display.
- Added detection status `el-tag`.
- Displayed timing information as an independent section.
- Compatible with missing `detection_result`, missing timing, legacy `timing_ms`, empty detections, and old records.
- Preserved JSON collapse, image display, API contract, and `detection_result.v1` semantics.

This is a documentation-only post-tag archive. It records the already-created Step 4 stable tag and does not push, create a new tag, edit business code, or authorize Step 5 implementation.

## Phase 2B Batch4 Step 5 Word Report Closeout Archive (2026-05-22)

```text
Step 5 scope: Word Report Export MVP
Step 5 status: CLOSED / VERIFIED / DOCS ARCHIVED
master HEAD: ae596ef
Backend merge commit: a24bd56
Frontend merge commit: ae596ef
Backend implementation commit: a916e4a
Frontend implementation commit: 353b98a
verification: compileall PASS; pytest PASS, 21 passed, 130 warnings; npm.cmd run build PASS; git diff --check PASS; git status clean before docs closeout
Step 5 stable tag: NOT CREATED
recommended stable tag: phase2b-batch4-step5-word-report-stable
recommended tag target: after evidence merge, not yet created
push: NOT DONE
Step 6: NOT AUTHORIZED
```

Step 5 closed the narrow single-record Word Report Export MVP. Backend added `GET /api/detection/records/<record_id>/report.docx` with JWT / permission / path-safety reuse and in-memory `.docx` generation. Frontend added the detection-record-detail Word export button and authenticated blob download handling.

Formal evidence:

```text
agent_outputs/docs/PHASE2B_BATCH4_STEP5_WORD_REPORT_VERIFICATION_EVIDENCE.md
agent_outputs/docs/PHASE2B_BATCH4_STEP5_WORD_REPORT_CLOSEOUT.md
```

This archive does not push, does not create a tag, and does not authorize Step 6.

## Phase 2B Batch4 Step 5 Post-Tag Archive (2026-05-22)

```text
Step 5 scope: Word Report Export MVP
Step 5 status: CLOSED / VERIFIED / TAGGED
Step 5 stable tag: phase2b-batch4-step5-word-report-stable
tag target: 645f2dccb7f32963123c8d16fac9f6a8044f906d
master HEAD before archive: 645f2dc
push: NOT DONE
Step 6: NOT AUTHORIZED
```

Implementation summary:

- Backend Word report API: `GET /api/detection/records/<record_id>/report.docx`.
- JWT auth.
- Permission reuse via `get_record`.
- `resolve_object_path` path safety.
- `python-docx>=1.1`.
- `BytesIO` no persistent report file.
- Frontend `DetectionRecordDetail.vue` ??? Word ?????.
- `requestBlob()`.
- `exportDetectionRecordWordReport(id)`.
- `saveBlob()`.
- `Content-Disposition` filename parsing.

Verification:

- backend compileall PASS.
- pytest PASS, 21 passed, 130 warnings.
- frontend npm build PASS.
- git diff --check PASS.
- working tree clean.

Confirmed NOT changed:

- DB schema.
- Dockerfile / `docker-compose.yml`.
- runtime/storage structure.
- model / weights / class / training.
- `detection_result.v1` semantics.
- image detection main flow semantics.
- auth/login semantics.
- Dashboard implementation.
- video detection implementation.
- realtime detection implementation.

This is a documentation-only post-tag archive. It records the already-created Step 5 stable tag and does not push, create a new tag, edit business code, or authorize Step 6.

## Phase 2B Batch4 Step 6 Dashboard Closeout Archive (2026-05-22)

```text
Step 6 scope: Dashboard 可视化增强 MVP
Step 6 status: CLOSED / VERIFIED / DOCS ARCHIVED
master HEAD: 9ac4644
Backend merge commit: 3a9d462
Backend implementation commit: a05e09c
Frontend merge commit: 9ac4644
Frontend implementation commits: 251ade6, 59bc851
verification: compileall PASS; pytest PASS, 26 passed, 152 warnings; npm.cmd run build PASS; git diff --check PASS; git status clean before docs closeout
Step 6 stable tag: NOT CREATED
recommended stable tag: phase2b-batch4-step6-dashboard-stable
recommended tag target: after evidence merge, not yet created
push: NOT DONE
Step 7: NOT AUTHORIZED
```

Step 6 closed the Dashboard visualization enhancement MVP: backend `GET /api/detection/dashboard/summary` with JWT and role-scoped aggregation; frontend `/dashboard` entry with summary cards, status stats, recent records table, loading/error/empty states, and API field mapping fixes.

Formal evidence:

```text
agent_outputs/docs/PHASE2B_BATCH4_STEP6_DASHBOARD_VERIFICATION_EVIDENCE.md
agent_outputs/docs/PHASE2B_BATCH4_STEP6_DASHBOARD_CLOSEOUT.md
```

This archive does not push, does not create a tag, and does not authorize Step 7.

## Phase 2B Batch4 Step 6 Post-Tag Archive (2026-05-22)

```text
Step 6 stable tag: phase2b-batch4-step6-dashboard-stable
tag target: 708a61a
tag target commit message: Merge Phase 2B Batch4 Step6 dashboard verification evidence
Step 6 status: CLOSED / STABLE / ARCHIVED
push: NOT DONE
Step 7: NOT AUTHORIZED
```

Step 6 implementation summary:

- Backend Dashboard summary API.
- `GET /api/detection/dashboard/summary`.
- JWT auth.
- admin all / normal user own records.
- `recent_records` default 5 max 10.
- Frontend `Dashboard.vue`.
- `/dashboard` route.
- `/` redirect to `/dashboard`.
- `AppLayout` Dashboard / ????.
- API field mapping fix.
- unified verification PASS.

Unified verification:

- compileall PASS.
- pytest PASS, 26 passed, 152 warnings.
- `npm.cmd run build` PASS.
- git diff --check PASS.
- git status clean.

Confirmed NOT changed:

- DB schema.
- Docker/runtime/storage.
- model/weights/class/training.
- `detection_result.v1` semantics.
- video/realtime implementation.
- AI Agent / LLM feature.

This is a documentation-only post-tag archive. It records the already-created Step 6 stable tag and does not push, create a new tag, edit business code, or authorize Step 7.

## Phase 2B Batch4 Step 7 Record Filter Closeout Archive (2026-05-23)

```text
Step 7 scope: Detection Records Filter/Search Enhancement
Step 7 status: CLOSED / VERIFIED / DOCS ARCHIVED
Current HEAD / master implementation baseline before docs closeout: 224e12d
Backend merge commit: 35d4950
Frontend merge commit: 224e12d
GO Decision merge commit: aef6c18
Planning merge commit: 1d81d33
latest previous stable tag: phase2b-batch4-step6-dashboard-stable -> 708a61a
verification: git diff --check HEAD~1..HEAD PASS; git diff --check PASS; backend compileall PASS; backend pytest PASS, 48 passed, 263 warnings; npm.cmd run build PASS; vue-tsc --noEmit PASS; vite build PASS; master working tree clean; git tag --points-at HEAD empty
Step 7 stable tag: NOT CREATED
recommended stable tag: phase2b-batch4-step7-record-filter-stable
recommended tag target: 224e12d
push: NOT DONE
Step 8: NOT AUTHORIZED
```

Step 7 adds optional records-list search/filter parameters (`keyword`, `model_id`, `detection_status`, `date_start`, `date_end`) to the existing JWT-protected API, preserves role-scoped visibility and pagination response shape, and adds corresponding server-side filter controls to `DetectionRecords.vue`. Dashboard, Detail, Word report, router, menu, DB schema, Docker/runtime/storage, model/training assets, and `detection_result.v1` semantics are unchanged.

Formal evidence:

```text
agent_outputs/docs/PHASE2B_BATCH4_STEP7_RECORD_FILTER_VERIFICATION_EVIDENCE.md
agent_outputs/docs/PHASE2B_BATCH4_STEP7_RECORD_FILTER_CLOSEOUT.md
```

Rollback reference: revert frontend merge `224e12d` and backend merge `35d4950` if needed; previous stable baseline is `phase2b-batch4-step6-dashboard-stable` -> `708a61a`.

This is a documentation-only closeout archive. It does not push, create a tag, edit business code, or authorize Step 8.

## Phase 2B Batch4 Step 7 Stable Tag Post-Tag Archive Update (2026-05-23)

```text
Step 7 stable tag: CREATED
stable tag: phase2b-batch4-step7-record-filter-stable -> 25c9f43
tag commit: 25c9f43 Merge Phase 2B Batch4 Step7 record filter verification evidence
final verification before tag: PASS; backend compileall PASS; backend pytest PASS, 48 passed, 263 warnings; frontend npm.cmd run build PASS; git diff --check PASS; master clean
post-tag archive commit at start of this docs update: NOT CREATED
post-tag archive outcome: this docs-only archive commit advances HEAD beyond the tag commit after commit
push: NOT DONE
new tag created by this archive update: NO
business code modified after tag: NO
FLOATING_OBJECT_PROJECT_CONTEXT_MASTER.md: NOT FOUND; NOT CREATED
Step 8: NOT AUTHORIZED
next allowed step: Phase 2B Batch4 Step 8 Planning / Gate only; direct implementation is NOT AUTHORIZED
```

The earlier recommended target `224e12d` remains as historical pre-tag evidence. The actual stable tag points at `25c9f43`, which includes the merged verification evidence and closeout documentation.
