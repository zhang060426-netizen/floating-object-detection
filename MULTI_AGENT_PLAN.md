# MULTI_AGENT_PLAN.md

## 1. 协作目标

后续多 Agent 协作不是为了并行“大改”，而是为了在清晰边界下小步推进工程化升级。所有 Agent 必须优先读取 `AGENTS.md`、`PROJECT_CONTEXT.md`、`README.md` 和与任务相关的专项文档。

## 2. Agent 角色与职责

### Frontend Agent

目录：`web-vue/` 或当前 `1项目代码/floating-objects-detect-web/web-vue/`。

任务：Vue3 页面与路由梳理、Element Plus UI 统一、检测结果可视化、图片/视频/实时检测页面体验优化、模型/数据集/评估管理页面、ECharts 指标展示、API 调用封装与错误提示。

不做：后端业务逻辑、DB 字段、YOLO 推理逻辑。

### Backend Agent

目录：`web-flask/` 或当前 `1项目代码/floating-objects-detect-web/web-flask/`。

任务：Flask routes/services/db 分层、JWT 鉴权、文件上传与存储结构、图片/视频/实时检测 API、异步视频任务状态机、模型/数据集/评估生命周期、Word 报告导出。

不做：Vue UI、训练脚本、权重替换。

### AI Agent

目录：`other/model_train/detect/`。

任务：YOLO 训练/验证/预测脚本维护、模型输出格式说明、CLAHE、ByteTrack、推理性能建议、Qwen-VL 分析链与 prompt 结构建议、模型评估指标解释和脚本化。

不做：前端业务页面、后端 DB/API 改动，除非先同步契约。

### Documentation Agent

目录：根目录文档、`3项目文档/`、`4测试包/`。

任务：README、架构、API、数据库、测试、部署、任务拆分、ER 图、流程图、文档与源码差异清单。

不做：未验证源码级结论，不覆盖业务代码。

## 3. Worktree 与分支建议

所有 Agent 禁止共享同一工作目录。建议：

| Agent | Worktree | Branch |
|---|---|---|
| Frontend | `../frontend-worktree` | `feature/frontend-ui-contracts` |
| Backend | `../backend-worktree` | `feature/backend-contracts` |
| AI | `../ai-worktree` | `feature/ai-pipeline-baseline` |
| Docs/Test | `../docs-worktree` | `docs/engineering-planning` |

当前对话未实际创建 worktree；这是后续团队执行规范。

## 4. 并行开发批次

### Batch 0：文档与契约

| 任务 | Owner | 依赖 | 输出 |
|---|---|---|---|
| 复核 7 份规划文档 | Docs | 当前文档 | 修改建议 |
| 补齐源码结构清单 | Frontend/Backend | 完整源码 | 目录地图 |
| 固化共享契约模板 | Docs + Backend + AI | DB/API/AI 文档 | schema/API checklist |

### Batch 1：源码确认与基线

| 任务 | Owner | 依赖 | 输出 |
|---|---|---|---|
| 前端页面/API 调用映射 | Frontend | web-vue 源码 | 页面-接口矩阵 |
| 后端路由/服务/DB 映射 | Backend | web-flask 源码 | API-服务-表矩阵 |
| AI 推理/评估入口映射 | AI | AI 源码/训练目录 | 推理链路图 |
| 测试资源映射 | Docs/Test | 4测试包 | 测试用例目录 |

### Batch 2：核心优化执行

| 方向 | Owner | 协作方 | 优先级 |
|---|---|---|---|
| UI 统一和交互反馈 | Frontend | Backend | P1 |
| 视频检测状态机 | Backend | Frontend/AI | P1 |
| 实时检测性能基线 | AI + Backend | Frontend | P1 |
| 模型管理发布校验 | Backend | AI/Frontend | P1 |
| 文档/测试同步 | Docs/Test | 全部 | P0-P1 |

## 5. Agent 交付模板

每个 Agent 完成任务时必须输出：修改/分析范围、涉及文件、影响的共享契约、风险点、验证步骤、回滚方案、待其他 Agent 确认项。

## 6. 冲突处理规则

API/DB/AI 输出格式冲突由 Backend Agent 牵头，Frontend/AI/Docs 共同确认；UI 与 API 能力不匹配时 Frontend 提需求，Backend 判断实现边界；模型输出变化时 AI Agent 必须提供兼容方案和评估结果；文档与源码不一致时 Documentation Agent 建立差异清单。

## 7. 后续任务拆分建议

| Agent | 第一批可执行任务 |
|---|---|
| Frontend | 建立页面清单、API 调用清单、统一检测结果组件设计、UI 风格问题列表 |
| Backend | 建立 API 清单、DB 表使用清单、视频任务状态机设计、文件存储路径规范 |
| AI | 梳理训练/推理/评估脚本、输出 JSON schema、Qwen-VL 分析字段、性能基线方案 |
| Documentation | 对齐文档与代码、整理测试包说明、建立验收 checklist、维护 ROADMAP |
