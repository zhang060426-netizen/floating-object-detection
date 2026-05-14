# Deep Interview Spec — 水面漂浮物检测系统工程化规划

## Metadata

- Profile: standard
- Final ambiguity: 2.9%
- Threshold: 20%
- Context type: brownfield-preview-or-partial-source
- Context snapshot: `.omx/context/unspecified-floating-yolo-20260513T013749Z.md`

## Intent

对已有「YOLO目标检测 + 多模态AI分析」水面漂浮物检测平台进行系统级梳理、工程化优化规划、多 Agent 协作拆分与架构升级设计。当前阶段不是编码实现，而是形成可长期维护、可供后续 Agent 执行的工程文档体系。

## Desired Outcome

在项目根目录生成 7 份工程化规划文档：`README.md`、`ROADMAP.md`、`ARCHITECTURE.md`、`MODULE_BOUNDARIES.md`、`MULTI_AGENT_PLAN.md`、`AI_PIPELINE_ANALYSIS.md`、`SYSTEM_OPTIMIZATION_PLAN.md`。

文档要兼顾阅读展示与工程执行，但优先让后续 Frontend Agent、Backend Agent、AI Agent、Documentation Agent 能直接拆任务、协作开发。

## In Scope

- 系统整体架构梳理
- 模块职责与目录边界划分
- 前端、后端、YOLO模型训练/推理、多模态大模型分析、数据库、测试包、文档之间的边界分析
- 图片、视频、实时检测、模型训练/评估、多模态分析链路梳理
- 工程化升级方向与优先级
- 多 Agent 并行开发拆分方案
- 依赖关系、风险点、阶段目标、后续路线
- 对缺失源码做基于文档和结构的合理推断，并明确标注推断边界和待源码确认部分

## Out of Scope / Non-goals

不直接大规模修改代码；不立即运行或重新训练模型；不强行补写缺失源码；不重构数据库；不更换大模型 API；不进行微服务化或云原生改造；不承诺源码级 100% 精确分析结论。

## Acceptance Criteria

- 明确模块边界、目录职责、数据流、AI 分析链。
- 明确任务拆分、阶段目标、依赖关系、优先级、风险点、后续执行路线。
- 明确 Frontend/Backend/AI/Documentation Agent 的职责、禁止事项、协作契约。
- 明确源码缺失导致的推断边界与待确认项。
- 文档结构清晰，适合项目展示、长期维护和工程文档体系沉淀。

## Evidence vs Inference

证据来自 `AGENTS.md`、`PROJECT_CONTEXT.md`、`prompt.md`、`3项目文档/`、`web-flask/requirements.txt`、`web-vue/package.json`、`other/model_train/detect/` 和 `4测试包/`。当前本地 `web-vue` 与 `web-flask` 缺少完整源码树，因此前后端内部实现细节均标注为待源码确认。
