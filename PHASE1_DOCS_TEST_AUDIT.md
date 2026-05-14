# Phase 1 Documentation/Test Audit

更新时间：2026-05-13
角色：Documentation/Test Agent
阶段：Phase 1：源码结构确认与差异审计

## 1. 审计边界

本文件只记录文档体系、测试资源、差异审计模板和验收清单。不写业务代码，不修改模型，不修改数据库，不声明未由当前可见文件验证的源码级结论。

已读取的根目录文档：

- `AGENTS.md`
- `PROJECT_CONTEXT.md`
- `prompt.md`
- `REPLAN.md`
- `README.md`
- `ROADMAP.md`
- `ARCHITECTURE.md`
- `MODULE_BOUNDARIES.md`
- `MULTI_AGENT_PLAN.md`
- `AI_PIPELINE_ANALYSIS.md`
- `SYSTEM_OPTIMIZATION_PLAN.md`
- `PHASE1_AUDIT_STATUS.md`

已检查目录：

- `3项目文档/`
- `4测试包/`
- `1项目代码/floating-objects-detect-web/`

## 2. 文档体系覆盖度

| 文档/目录 | 覆盖内容 | 当前状态 | 待确认点 |
|---|---|---|---|
| `AGENTS.md` | Agent 职责、共享契约、AI 安全、Git/worktree、Definition of Done | 已确认 | 后续执行需在独立 worktree 中落地 |
| `PROJECT_CONTEXT.md` | 项目背景、系统能力、AI 链路、数据集规模、模型指标 | 已确认为上下文文档 | 指标和能力需由源码/运行结果复核 |
| `README.md` | 项目总览、文档索引、逻辑模块地图、推断边界 | 已确认 | 前后端源码补齐后更新推断边界 |
| `REPLAN.md` | Phase 0-N 路线、Agent 拆分、worktree 策略、风险 | 已确认 | Phase 1 后用事实审计结果回填 |
| `ROADMAP.md` | 阶段目标、优先级、近期执行顺序 | 已确认 | Phase 1/2 完成状态待更新 |
| `ARCHITECTURE.md` | 分层架构、图片/视频/实时流、DB 表概览、待确认项 | 已确认 | routes/services/db/algo 需源码确认 |
| `MODULE_BOUNDARIES.md` | 模块所有权、共享契约、跨模块变更流程 | 已确认 | 需各 Agent 输出实际目录地图后复核 |
| `MULTI_AGENT_PLAN.md` | 多 Agent 分工、批次、交付模板 | 已确认 | 需与实际 worktree/分支一致 |
| `AI_PIPELINE_ANALYSIS.md` | YOLO/CLAHE/Qwen-VL/视频/实时/评估链路 | 已确认 | 应用内推理封装、prompt、报告字段待源码确认 |
| `SYSTEM_OPTIMIZATION_PLAN.md` | 工程结构、前后端、AI、DB、测试优化方向 | 已确认 | 优化任务需等可运行基线后执行 |
| `prompt.md` | 原始需求澄清工作规则 | 已确认为历史输入 | 不作为当前 Phase 1 执行入口 |
| `3项目文档/1系统介绍文档.md` | 技术架构、目录结构、功能、API 文档、核心流程 | 已确认存在 | 其中代码片段/接口需源码确认 |
| `3项目文档/5数据库开发文档.md` | 10 张表、字段、索引、关系、初始化数据、建表 SQL | 已确认存在 | 实际 DB 初始化/迁移/索引代码待确认 |
| `3项目文档/4模型训练文档.txt` | 数据集、训练命令、权重、输出路径、指标 | 已确认存在 | 训练脚本参数需 AI Agent 确认 |
| `3项目文档/3系统使用注意事项.txt` | 发布模型、管理员权限、LLM 配置、本地摄像头限制、默认账号 | 已确认存在 | `web-flask/algo/llm/config.py` 当前源码未发现 |
| `3项目文档/1系统图备份/` | ER 图、架构交互图、时序图、数据流图、UML、功能模块图 HTML | 已确认存在 | 图内容与最终源码结构需复核 |
| `3项目文档/2系统图.pptx` | 系统图 PPT | 已确认存在 | 未解析 PPT 内容，仅确认文件存在 |

覆盖结论：

- 文档体系已覆盖项目总览、架构、模块边界、多 Agent 计划、AI 链路、数据库、训练说明、系统图和测试资源方向。
- 当前缺口不在“是否有规划文档”，而在“规划/说明文档与实际源码的对应关系尚未完全确认”。
- 前后端业务源码缺失导致 API、页面、路由、服务层、DB 初始化、LLM 配置和报告字段仍不能声明为源码事实。

## 3. 当前可见源码/资源确认

实际源码/资源根目录：

```text
1项目代码/floating-objects-detect-web/
```

当前可见结构：

| 区域 | 当前可见文件/目录 | 结论 |
|---|---|---|
| 前端 | `web-vue/package.json`、`web-vue/2须知.txt` | 仅能确认 Vue/Vite 依赖与说明文件，未发现 `src/`、`router/`、`views/`、`api/` |
| 后端 | `web-flask/requirements.txt`、`web-flask/1须知.txt` | 仅能确认依赖与说明文件，未发现 Flask app/routes/services/db/algo 源码 |
| AI 训练 | `other/model_train/detect/code/train.py`、`val.py`、`predict.py` | 训练/验证/预测脚本存在，具体逻辑由 AI Agent 审计 |
| AI 数据集 | `dataset/small_dataset/data.yaml`、train/valid/test images + labels | 小数据集存在，`nc: 1`，`names: ['floating_object']` |
| AI 权重 | `weights/yolov8n.pt`、`yolo11n.pt`、`yolo12n.pt`、`yolo26n.pt` | 预训练/权重文件存在，不修改、不替换 |
| AI 输出 | `output/已经训练好的模型和测试结果/` | 训练/验证图表与指标文件存在 |

依赖文件确认：

- `web-vue/package.json`：包含 Vue 3、Vite、Element Plus、Pinia、Vue Router、Axios、ECharts、flv.js 等依赖。
- `web-flask/requirements.txt`：包含 Flask-CORS、PyJWT、ultralytics、openai、python-docx、lap、openpyxl 等依赖。

## 4. 文档描述 vs 源码确认：差异审计模板

后续 Frontend / Backend / AI / Docs Agent 统一使用以下模板记录差异。所有“源码确认”必须给出文件路径；不能确认时标记为“待源码确认”。

| 编号 | 领域 | 文档描述 | 文档来源 | 当前可见源码/资源 | 确认状态 | 差异类型 | 影响共享契约 | 负责人 | 下一步 |
|---|---|---|---|---|---|---|---|---|---|
| GAP-001 | 示例：前端路由 | 系统存在图片/视频/实时/模型/数据集/评估页面 | `3项目文档/1系统介绍文档.md` | 当前未发现 `web-vue/src/router` | 待源码确认 | 源码缺失 | 页面-API 矩阵 | Frontend | 补齐源码后确认路由表 |
| GAP-002 | 示例：后端 API | `/api/detection` 等接口存在 | `3项目文档/1系统介绍文档.md` | 当前未发现 Flask routes | 待源码确认 | 源码缺失 | API 返回结构 | Backend | 补齐源码后输出 API 清单 |
| GAP-003 | 示例：DB | 文档定义 10 张核心表 | `3项目文档/5数据库开发文档.md` | 当前未发现 DB 初始化/迁移代码 | 待源码确认 | 实现待核对 | DB 字段 | Backend + Docs | 找到初始化 SQL/ORM 后逐表核对 |

状态枚举：

- 已源码确认：有明确文件路径和可读实现证据。
- 已资源确认：有文件/目录/配置/测试资源证据，但非业务源码。
- 文档已覆盖：文档存在并描述完整，但尚无源码证据。
- 待源码确认：当前缺少源码或入口文件，不能声明实现事实。
- 文档缺失：当前文档体系没有覆盖该主题。
- 冲突/差异：文档与源码或资源明确不一致。

差异类型：

- 路径差异
- 源码缺失
- 接口/字段待核对
- 依赖存在但实现待确认
- 测试资源存在但自动化入口缺失
- 文档缺失
- 文档过期

## 5. 测试资源索引

### 5.1 `4测试包/` 总览

| 类型 | 路径 | 数量 | 总大小 | 用途 | 当前状态 |
|---|---|---:|---:|---|---|
| 数据集压缩包 | `4测试包/数据集/small_dataset.zip` | 1 | 28.91 MB | 数据集导入/训练包/管理功能测试 | 已确认存在 |
| 测试图片 | `4测试包/测试图片/` | 15 | 约 38.03 MB | 图片检测冒烟、报告导出、AI 分析入口 | 已确认存在 |
| 测试视频 | `4测试包/测试视频/` | 6 | 约 104.40 MB | 视频检测上传、进度、关键帧、结果视频冒烟 | 已确认存在 |
| 评估图片 | `4测试包/评估测试/评估图片/` | 40 | 约 21.97 MB | 模型评估测试 | 已确认存在 |
| 评估标签 | `4测试包/评估测试/对应标签文件/` | 40 | 约 0.01 MB | YOLO 标签，和评估图片同名匹配 | 已确认存在 |

评估图片与标签文件同名基线已检查：40 张图片与 40 个标签文件的 basename 一致。

评估标签类别分布：

| 类别 ID | 目标框数量 |
|---|---:|
| `0` | 309 |

### 5.2 测试图片

| 文件 | 大小 |
|---|---:|
| `1.png` | 2.97 MB |
| `2.png` | 2.70 MB |
| `3.png` | 2.83 MB |
| `4.png` | 1.83 MB |
| `5.png` | 1.55 MB |
| `6.png` | 2.49 MB |
| `7.png` | 2.18 MB |
| `8.png` | 1.87 MB |
| `9.png` | 2.10 MB |
| `10.png` | 1.92 MB |
| `11.png` | 7.52 MB |
| `12.png` | 8.03 MB |
| `13.webp` | 0.01 MB |
| `14.jpeg` | 0.02 MB |
| `15.webp` | 0.01 MB |

建议用途：

- `1.png` 至 `12.png`：常规图片检测冒烟。
- `11.png`、`12.png`：大图上传、推理耗时、报告生成压力样例。
- `13.webp`、`15.webp`、`14.jpeg`：格式兼容性样例。

### 5.3 测试视频

| 文件 | 大小 |
|---|---:|
| `1.mp4` | 3.28 MB |
| `2.mp4` | 4.16 MB |
| `3.mp4` | 11.50 MB |
| `4.mp4` | 11.52 MB |
| `5.mp4` | 11.59 MB |
| `6.mp4` | 62.34 MB |

建议用途：

- `1.mp4`、`2.mp4`：视频检测最小冒烟。
- `3.mp4` 至 `5.mp4`：中等体积视频任务进度/关键帧测试。
- `6.mp4`：较大视频上传、异步任务、超时、资源释放风险测试。

### 5.4 训练目录小数据集

路径：`1项目代码/floating-objects-detect-web/other/model_train/detect/dataset/small_dataset/`

| split | images | labels |
|---|---:|---:|
| train | 40 | 40 |
| valid | 9 | 9 |
| test | 6 | 6 |

`data.yaml`：

```yaml
train: ../train/images
val: ../valid/images
test: ../test/images

nc: 1
names: ['floating_object']
```

当前小数据集标签类别分布：

| 类别 ID | 目标框数量 |
|---|---:|
| `0` | 388 |

## 6. Phase 1 验收 checklist

### 6.1 全局

- [x] 根目录指定文档已读取并归档到审计范围。
- [x] `3项目文档/` 已检查，文档与图备份存在。
- [x] `4测试包/` 已盘点，测试图片/视频/评估图片/标签/数据集包已索引。
- [x] 实际源码根路径已确认：`1项目代码/floating-objects-detect-web/`。
- [x] 前端当前可见文件已确认：`package.json`、`2须知.txt`。
- [x] 后端当前可见文件已确认：`requirements.txt`、`1须知.txt`。
- [x] AI 训练目录、脚本、权重、数据集、输出目录已资源确认。
- [x] 文档描述 vs 源码确认差异审计模板已建立。
- [ ] Frontend Agent 输出前端目录地图和源码缺失清单。
- [ ] Backend Agent 输出后端目录地图和源码缺失清单。
- [ ] AI Agent 输出训练/验证/预测脚本说明和模型基线说明。
- [ ] 各 Agent 使用统一报告格式提交 Phase 1 结果。

### 6.2 Gate

- [ ] 明确标注每一条结论是“源码确认”“资源确认”“文档覆盖”还是“待源码确认”。
- [ ] 不把文档描述直接写成源码事实。
- [ ] 不进入功能实现、不修改共享契约、不修改模型权重。
- [ ] 若前后端源码仍未补齐，Phase 1 输出以缺失清单和复核任务为主。

## 7. Phase 2 可运行基线 checklist

Phase 2 必须在 Phase 1 输出完成、前后端源码补齐或可运行入口明确后执行。

### 7.1 启动基线

- [ ] 前端安装依赖成功。
- [ ] 前端开发服务可启动。
- [ ] 后端 Python 环境可创建。
- [ ] 后端依赖安装成功。
- [ ] 后端服务可启动。
- [ ] 前后端代理/API 地址配置明确。
- [ ] 默认账号 `admin / 123456`、`test / 123456` 可用于登录验证，若实际实现不同需更新文档。

### 7.2 共享契约基线

- [ ] API 统一响应结构有 schema。
- [ ] JWT 字段有说明。
- [ ] DB 实际表结构与 `3项目文档/5数据库开发文档.md` 已逐表核对。
- [ ] `detection_result` JSON 有 schema。
- [ ] YOLO 输出坐标、类别、置信度格式有 schema。
- [ ] Qwen-VL 分析返回字段有说明。
- [ ] 文件存储路径、URL 生成、清理策略有说明。
- [ ] evaluation metrics 格式有说明。

### 7.3 冒烟基线

- [ ] 图片检测：使用 `4测试包/测试图片/1.png` 完成上传、检测、结果展示。
- [ ] 图片格式兼容：使用 `.jpeg`、`.webp` 样例确认支持范围。
- [ ] 报告导出：基于一条图片检测记录生成 Word 文件。
- [ ] 视频检测：使用 `4测试包/测试视频/1.mp4` 完成任务创建、进度更新、结果产物生成。
- [ ] 视频压力样例：使用 `4测试包/测试视频/6.mp4` 记录耗时、失败原因或资源释放情况。
- [ ] 模型评估：使用 `4测试包/评估测试/评估图片` 与 `对应标签文件` 完成一次评估流程。
- [ ] 实时检测：本地 USB 摄像头可开始/停止，会话结束后资源释放。
- [ ] 权限：管理员功能与普通用户功能边界符合文档。

## 8. 统一报告格式

Frontend / Backend / AI Agent 提交 Phase 1 报告时使用以下结构。

```markdown
# Phase 1 <Frontend|Backend|AI> Source Audit Report

## 1. 审计范围

- Agent：
- 审计目录：
- 只读/修改说明：

## 2. 已源码确认

| 编号 | 结论 | 文件路径 | 证据摘要 | 影响契约 |
|---|---|---|---|---|

## 3. 已资源确认

| 编号 | 资源 | 路径 | 数量/版本/配置 | 用途 |
|---|---|---|---|---|

## 4. 文档描述但待源码确认

| 编号 | 文档描述 | 文档来源 | 缺失/待确认源码 | 风险 |
|---|---|---|---|---|

## 5. 文档与源码差异

| 编号 | 文档描述 | 源码事实 | 差异类型 | 影响 | 建议处理 |
|---|---|---|---|---|---|

## 6. 共享契约影响

- API 返回结构：
- DB 字段：
- 模型输出 JSON：
- 文件存储结构：
- JWT 字段：
- detection_result：
- evaluation metrics：

## 7. 风险点

- 

## 8. 验证方式

- 已运行：
- 未运行原因：
- 下一步验证：

## 9. 待其他 Agent 确认

- Frontend：
- Backend：
- AI：
- Docs/Test：
```

## 9. 已确认文档、缺失文档、待源码确认内容

### 9.1 已确认文档

- 根目录工程规划文档：`README.md`、`ROADMAP.md`、`ARCHITECTURE.md`、`MODULE_BOUNDARIES.md`、`MULTI_AGENT_PLAN.md`、`AI_PIPELINE_ANALYSIS.md`、`SYSTEM_OPTIMIZATION_PLAN.md`、`REPLAN.md`。
- 项目文档：`3项目文档/1系统介绍文档.md`、`3项目文档/3系统使用注意事项.txt`、`3项目文档/4模型训练文档.txt`、`3项目文档/5数据库开发文档.md`。
- 图备份：`3项目文档/1系统图备份/` 下的架构交互图、算法流程图、图片/视频/实时检测时序图、数据流图、UML 类图、功能模块图、ER 图 HTML。

### 9.2 缺失文档

当前未发现以下独立可执行文档，应在 Phase 2 前补齐或由已有文档拆分：

- `docs/contracts/api-schema.md`
- `docs/contracts/db-field-diff.md`
- `docs/contracts/detection-result-schema.md`
- `docs/contracts/ai-analysis-schema.md`
- `docs/contracts/file-storage-schema.md`
- `docs/contracts/jwt-fields.md`
- `docs/contracts/evaluation-metrics-schema.md`
- `docs/testing/startup-checklist.md`
- `docs/testing/smoke-test-checklist.md`
- `docs/testing/regression-resource-index.md`

说明：以上为建议目标路径；当前仓库尚未建立 `docs/contracts/` 与 `docs/testing/` 目录。

### 9.3 待源码确认内容

- 前端 `src/`、`router/`、`views/`、`api/`、`stores/`、`components/` 实际结构。
- 前端页面-路由-API 调用矩阵。
- 后端 Flask app 入口、routes、services、dao/models、DB 初始化、错误码、鉴权装饰器。
- API 实际 URL、请求参数、响应结构、错误结构。
- `detection_result` 真实 JSON 结构。
- 文件上传、静态文件访问、报告导出路径。
- Qwen-VL 配置、prompt、超时、重试、降级、日志脱敏策略。
- 应用内 YOLO 推理封装、模型加载缓存、并发策略。
- 视频检测后台任务实现方式和状态机。
- 实时检测摄像头释放、ByteTrack 参数、目标去重策略。
- Word 报告模板字段。
- 自动化测试入口和 CI/脚本化验证方式。

## 10. 影响范围、风险与回滚

影响范围：

- 本文件仅影响文档/测试审计交付，不影响业务代码、模型权重或数据库。
- 为 Frontend / Backend / AI Agent 提供统一 Phase 1 输出格式。

风险点：

- 前后端源码未补齐前，任何页面/API/DB 结论都只能标记为“文档覆盖”或“待源码确认”。
- `3项目文档/1系统介绍文档.md` 中包含接口和实现片段，但当前没有对应源码证据，不能作为最终实现事实。
- `4测试包/` 资源已存在，但当前未发现自动化测试入口。

回滚方案：

- 如后续发现本审计文档与补齐源码不一致，直接按源码证据更新本文件中的差异清单和待确认项。
- 本文件不改动业务代码、模型、数据库，因此回滚只需删除或修订该文档。
