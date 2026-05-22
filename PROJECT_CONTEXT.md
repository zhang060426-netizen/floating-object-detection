# PROJECT_CONTEXT.md

本文件用于向：
- AI Agent
- Codex
- 多Agent协作系统

提供项目背景、系统能力、架构信息与当前开发阶段上下文。

所有 Agent 在进入开发前应优先阅读本文件。

# 项目目录结构

- web-vue/                     Vue3 前端
- web-flask/                   Flask 后端
- other/model_train/detect/   YOLO训练与推理
- 3项目文档/                    项目文档
- 4测试包/                      测试资源

# 当前已完成模块

当前已实现：

- 用户登录注册
- JWT鉴权
- 图片检测
- 视频检测
- 实时检测
- 模型管理
- 数据集管理
- 模型评估
- Qwen-VL多模态分析
- Word报告导出
- 检测记录管理

# 当前核心问题

当前项目存在：

- 前后端结构尚未完全工程化
- UI风格不统一
- 视频检测流程仍可优化
- 实时检测性能存在提升空间
- 多Agent协作体系尚未建立
- 文档与代码仍需进一步同步
- 部分源码结构缺失或待补全

# 项目简介

本项目是一个基于人工智能技术的：
「YOLO目标检测 + 多模态AI分析」
水面漂浮物智能检测平台。

目标：
通过计算机视觉与深度学习技术，
实现对河流、湖泊、水库等场景中的水面漂浮垃圾进行自动识别、分析与治理辅助。

# 当前系统能力

系统当前支持：

- 图片检测
- 视频检测
- 实时检测
- 模型管理
- 数据集管理
- 模型评估
- 多模态AI分析
- Word报告导出
- 用户权限管理

# 系统架构

前端：
- Vue3
- Element Plus
- Pinia
- ECharts

后端：
- Flask
- JWT
- SQLite

AI模块：
- YOLOv8/11/12/26
- ByteTrack
- OpenCV
- Qwen-VL

# AI分析链

图片检测流程：

图片上传
→ YOLO检测
→ CLAHE增强
→ Qwen-VL分析
→ 治理建议生成
→ Word报告导出

视频检测流程：

视频上传
→ 帧采样
→ YOLO逐帧检测
→ 关键帧保存
→ 结果视频导出

实时检测流程：

摄像头输入
→ ByteTrack目标跟踪
→ YOLO实时推理
→ 检测记录保存

# 数据集信息

数据来源：
https://www.modelscope.cn/datasets/Echo0174/Trash_floater

数据规模：
- 总样本：5544
- train：4032
- valid：907
- test：605

类别：
0: floating_object

# 当前模型性能

Precision: 0.889
Recall: 0.827
mAP50: 0.915
mAP50-95: 0.659

# 当前项目状态

当前项目属于：

- Brownfield Existing Project
- 已具备完整平台雏形
- 正在进行系统级梳理与工程化升级

当前重点：

1. 架构梳理
2. Agent拆分
3. UI统一
4. AI链稳定
5. 视频检测优化
6. 实时检测优化

# 已知限制

- 实时检测仅支持本地USB摄像头
- 不支持网络摄像头
- 当前训练需本地执行
- 大模型分析依赖阿里云百炼API
- 模型无法保证100%识别率

# 未来方向

- UI大屏化
- 多模型切换
- GPU推理优化
- 多类别检测
- 实时告警系统
- 水域治理数据分析

# Phase 2B Batch3 稳定基线（2026-05-20）

当前最新稳定基线：

```text
phase2b-batch3-docker-compose-stable
```

Tag target commit：

```text
fddb0c83486abaa3403db030c1d8d0e994331dab
```

Batch3 最终状态：

```text
Phase 2B Batch3 Closeout: COMPLETE
Final Smoke Verification: PASS
Current HEAD at closeout: fddb0c8
Working tree before archive: clean
Batch4: NOT ENTERED
Push: NOT DONE
```

Final smoke 摘要：

- Docker compose config: PASS
- Docker compose build --no-cache: PASS
- Docker compose up/ps: PASS
- Backend health: PASS
- Backend DB health: PASS
- Frontend HTTP 200: PASS
- Login admin/admin123: PASS
- Image detection API: PASS
- Result image: PASS
- Records save/read: PASS
- `detection_result.v1`: PRESERVED
- Runtime model mount: PASS
- Docker compose down: PASS

Final smoke 在纯英文路径执行：

```text
E:\MM\floating-smoke-master
```

原因：原中文路径触发 Docker Desktop / BuildKit / buildx 非 ASCII session 问题：

```text
x-docker-expose-session-sharedkey contains value with non-printable ASCII characters
```

上下文恢复时，应以 `phase2b-batch3-docker-compose-stable` 作为最新稳定基线。下一步只允许开启 Batch4 Planning，不允许直接进入 Batch4 implementation。

当前禁止范围：视频、实时、Word、Dashboard、大屏、训练、改类别、改权重、破坏 `detection_result.v1`。

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
