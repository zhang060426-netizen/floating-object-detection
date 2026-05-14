# Phase 1 Master Summary

更新时间：2026-05-13  
角色：Leader / Coordinator  
阶段：Phase 1：源码结构确认与差异审计  
输入报告：

- `agent_outputs/frontend/FE_PHASE1_AUDIT.md`
- `agent_outputs/backend/BE_PHASE1_AUDIT.md`
- `agent_outputs/ai/AI_PHASE1_AUDIT.md`
- `agent_outputs/docs/DOC_TEST_PHASE1_AUDIT.md`

边界声明：本汇总只做审计、判断与调度；不写业务代码、不重构、不训练模型、不替换权重、不修改数据库。

---

## 1. 总体结论

### 1.1 Phase 1 是否完成

**结论：Phase 1「审计交付」已完成；但 Phase 1「源码事实确认」未完全完成。**

理由：

| 领域 | Phase 1 审计输出 | 完成度判断 |
|---|---|---|
| Frontend | 已确认 `web-vue/` 仅有 `package.json` 与 `2须知.txt`，缺少 `src/`、路由、页面、API、入口文件 | 审计完成；源码事实不足 |
| Backend | 已确认 `web-flask/` 仅有 `requirements.txt` 与 `1须知.txt`，缺少 Flask app、routes、services、DB 初始化 | 审计完成；源码事实不足 |
| AI | 已确认训练目录、`train.py`、`val.py`、`predict.py`、数据集、权重、历史指标 | 审计基本完成 |
| Docs/Test | 已确认根文档、项目文档、测试包、评估资源，并建立差异模板和 Phase 2 checklist | 审计完成 |

因此，Phase 1 的真实结果不是“系统源码已完整确认”，而是：

> 当前包内 **前后端业务源码缺失严重**，AI 训练资源和测试资源相对完整；后续开发必须先解决前后端源码补齐/定位问题，否则只能继续做文档级契约确认。

### 1.2 是否具备进入 Phase 2 的条件

**结论：不具备进入 Phase 2「代码实现 / 可运行基线」的条件；仅具备进入 Phase 2「文档契约准备」的条件。**

可进入的部分：

- 共享契约草案：API 统一响应、JWT 字段、`detection_result`、YOLO 输出、Qwen-VL 分析字段、evaluation metrics。
- 测试 checklist：启动、图片检测、视频检测、实时检测、模型评估、报告导出。
- 差异报告：文档描述 vs 当前可见源码/资源。
- 源码补齐任务计划：确认真实前端/后端源码是否遗漏、未解压或位于其他目录。

不可进入的部分：

- 前端页面、路由、API 封装开发。
- 后端 API、DB、服务层、鉴权、文件存储实现或重构。
- 可运行基线验证。
- 冒烟测试执行。
- 视频/实时检测核心逻辑优化。
- 模型发布、权重替换、训练或重新评估。

---

## 2. 当前已确认事实

### 2.1 实际源码/资源根路径

实际项目资源位于：

```text
1项目代码/floating-objects-detect-web/
```

规划文档中的逻辑路径 `web-vue/`、`web-flask/`、`other/model_train/detect/`，在当前工作区中应对应为：

```text
1项目代码/floating-objects-detect-web/web-vue/
1项目代码/floating-objects-detect-web/web-flask/
1项目代码/floating-objects-detect-web/other/model_train/detect/
```

### 2.2 Frontend 已确认事实

当前可见：

```text
1项目代码/floating-objects-detect-web/web-vue/
├─ package.json
└─ 2须知.txt
```

已确认依赖意图：

- Vue 3
- Vue Router
- Pinia
- Axios
- Element Plus
- ECharts
- Vite
- TypeScript

未发现：

- `src/`
- `src/router/`
- `src/api/`
- `src/views/`
- `src/components/`
- `src/stores/`
- `src/types/`
- `src/utils/`
- `index.html`
- `vite.config.ts`
- `src/main.ts`

### 2.3 Backend 已确认事实

当前可见：

```text
1项目代码/floating-objects-detect-web/web-flask/
├─ requirements.txt
└─ 1须知.txt
```

已确认依赖意图：

- Flask-CORS
- PyJWT
- Ultralytics
- OpenAI
- python-docx
- lap
- openpyxl

未发现：

- `app.py`
- `config.py`
- `routes/`
- `services/`
- `models/`
- `dao/`
- `utils/`
- `algo/`
- Flask API 源码
- DB 初始化代码
- SQLite 数据库文件
- YOLO 应用内推理封装

### 2.4 AI 已确认事实

当前可见：

```text
1项目代码/floating-objects-detect-web/other/model_train/detect/
├─ code/
│  ├─ train.py
│  ├─ val.py
│  └─ predict.py
├─ dataset/
├─ output/
└─ weights/
```

已确认：

- `train.py` 当前加载 `weights/yolo26n.pt`，使用 `dataset/small_dataset/data.yaml`，`epochs=50`，`imgsz=640`。
- `val.py` 当前默认加载 `output/train/weights/best.pt`，使用 `small_dataset` 的 `test` split。
- `predict.py` 当前指向历史训练结果路径 `output/已经训练好的模型和测试结果/train/weights/best.pt`。
- 小数据集类别：`nc: 1`，`names: ['floating_object']`。
- 历史测试集指标：Precision 0.889，Recall 0.827，mAP50 0.915，mAP50-95 0.659。
- 历史验证集指标：Precision 0.904，Recall 0.845，mAP50 0.927，mAP50-95 0.675。

注意：

- 当前可见包中未确认真实历史 `best.pt` 已存在；存在“预览版项目未放置训练好的模型权重”的风险。
- 当前不允许训练模型、不替换权重、不修改类别定义。

### 2.5 Docs/Test 已确认事实

已确认：

- 根目录规划文档存在。
- `3项目文档/` 存在系统介绍、数据库开发文档、训练文档、系统图等。
- `4测试包/` 存在：
  - 1 个 small_dataset 压缩包；
  - 15 张测试图片；
  - 6 个测试视频；
  - 40 张评估图片；
  - 40 个评估标签文件。
- 评估图片与标签 basename 一致。
- 评估标签类别 ID 仅发现 `0`。

---

## 3. Phase 2 优先任务

Phase 2 应拆成两个层级：**Phase 2A：源码补齐与契约准备**，**Phase 2B：可运行基线与冒烟验证**。

### 3.1 Phase 2A：必须优先执行

| 优先级 | 任务 | 负责人 | 交付物 | 说明 |
|---:|---|---|---|---|
| P0 | 定位或补齐完整 `web-vue` 源码 | Frontend Agent | 前端源码位置确认 / 补齐清单 | 没有 `src/` 时不能做页面、路由、API 审计 |
| P0 | 定位或补齐完整 `web-flask` 源码 | Backend Agent | 后端源码位置确认 / 补齐清单 | 没有 Flask 源码时不能确认 API、DB、鉴权、推理链 |
| P0 | 建立文档-源码差异总表 | Documentation/Test Agent | `DOC_SOURCE_GAP_REPORT.md` | 先记录事实缺口，防止把文档推断当源码事实 |
| P0 | 起草共享契约目录 | Documentation/Test + Backend + AI | `docs/contracts/` 草案 | 仅做草案，不声明为实现事实 |
| P0 | 固化 AI 输出候选 schema | AI + Backend | YOLO 输出、Qwen-VL 分析、metrics 草案 | 基于 AI 目录与文档，不改变模型输出 |
| P1 | 建立 Phase 2 启动/冒烟 checklist | Documentation/Test Agent | 启动与冒烟测试 checklist | 等源码补齐后执行验证 |

### 3.2 Phase 2B：源码补齐后执行

| 优先级 | 任务 | 负责人 | 交付物 | 前置条件 |
|---:|---|---|---|---|
| P0 | 重新执行 FE-1 / FE-2 | Frontend Agent | 真实前端目录地图、页面-路由-API 矩阵 | `web-vue/src/` 存在 |
| P0 | 重新执行 BE-1 / BE-2 / BE-3 | Backend Agent | 后端目录地图、API-服务-DB 映射、DB 差异清单 | Flask 源码存在 |
| P0 | 确认应用内 YOLO 推理封装 | Backend + AI | 推理入口地图 | 后端源码存在 |
| P0 | 建立最小启动基线 | Frontend + Backend | 前端/后端启动 checklist 实测结果 | 前后端入口存在 |
| P1 | 执行图片/视频/评估冒烟路径 | Docs/Test + Backend + Frontend | 冒烟测试结果 | 启动基线通过 |
| P1 | 实时检测资源释放验证 | Backend + AI + Docs/Test | 摄像头开始/停止与资源释放记录 | 后端实时检测接口存在 |

---

## 4. 哪些任务需要 Git Worktree

> 当前审计显示项目根目录可能不是标准 Git 工作区；若正式进入多 Agent 并行修改，应先确认或初始化 Git 仓库，再按 AGENTS.md 使用独立 worktree。  
> 只读审计不强制需要 worktree；凡涉及新增/恢复/修改源码或共享契约，都应使用独立分支/worktree。

### 4.1 必须使用 Git Worktree 的任务

| 任务 | 建议 worktree | 原因 |
|---|---|---|
| 补齐或恢复完整 `web-vue` 源码 | `frontend-worktree` | 会新增/修改大量前端源码，需与后端/文档隔离 |
| 补齐或恢复完整 `web-flask` 源码 | `backend-worktree` | 会新增/修改 API、DB、服务层、鉴权、文件存储 |
| 前端页面-路由-API 对齐后的代码修改 | `frontend-worktree` | 涉及 API 调用、状态管理、UI 行为 |
| 后端 API/DB/推理封装实现或修复 | `backend-worktree` | 涉及共享契约和数据库风险 |
| AI 推理脚本、评估脚本或模型加载代码修改 | `ai-worktree` | 涉及模型路径、输出格式、性能测试 |
| 建立/修改 `docs/contracts/` 正式契约 | `docs-worktree` | 共享契约影响所有 Agent，应独立 review |
| 冒烟测试脚本化、测试入口或 CI 配置 | `docs-worktree` 或 `test-worktree` | 属于跨模块验收资产，需避免覆盖业务代码 |

### 4.2 暂时不需要 Git Worktree 的任务

以下任务可继续以只读/文档确认方式进行，不应进入业务代码修改：

- 阅读并标注文档推断边界。
- 汇总缺失清单。
- 起草契约草案但不声明为实现事实。
- 整理测试资源索引。
- 制定启动 checklist、冒烟 checklist。
- 制定源码补齐指令。
- 维护 Phase 1 / Phase 2 调度文档。

---

## 5. 哪些任务仍然只适合文档确认

在前后端源码补齐前，以下任务只能做文档级确认，不适合进入代码实现：

| 任务 | 原因 | 输出形式 |
|---|---|---|
| 页面-路由-API 矩阵 | 缺少 `web-vue/src/router`、`views`、`api` | 推断版矩阵 / 待源码确认 |
| 后端 API 清单 | 缺少 Flask routes | API 候选表 / 待源码确认 |
| API 统一响应格式 | 缺少统一响应工具源码 | schema 草案 |
| JWT payload | 缺少签发与鉴权源码 | 字段候选与风险说明 |
| DB 字段核对 | 缺少 DB 初始化/迁移代码和实际 SQLite 文件 | 文档表结构索引 |
| `detection_result` schema | 缺少后端推理封装与前端解析源码 | 候选 schema |
| Qwen-VL prompt/返回字段 | 缺少 LLM 配置和调用链源码 | 字段候选、超时/降级建议 |
| 视频任务状态机 | 缺少任务实现源码 | 状态机草案 |
| 实时检测资源释放 | 缺少接口和 tracker 生命周期源码 | 验证方案 |
| Word 报告字段 | 缺少报告模板和导出源码 | 字段候选 |
| 冒烟测试执行 | 缺少前后端可运行入口 | checklist，不执行 |

---

## 6. 当前源码缺口对后续开发的影响

### 6.1 对前端的影响

- 无法运行 `npm run dev` 或 `npm run build` 形成前端基线。
- 无法确认路由、菜单、权限守卫、登录态、token 注入。
- 无法确认实际 API 请求路径、入参、返回值解析。
- 无法审计图片/视频/实时检测结果展示模型。
- 无法做 UI 截图、风格统一或组件复用分析。
- 若直接进入 Phase 2/3 前端开发，极易基于文档假设重复造页面或破坏真实代码。

### 6.2 对后端的影响

- 无法启动 Flask 服务。
- 无法确认 API、Blueprint、统一响应、错误码、鉴权装饰器。
- 无法确认 DB 表结构与文档是否一致。
- 无法确认文件上传、文件存储、报告导出路径。
- 无法确认 YOLO 模型在业务系统中的加载、缓存、推理输出格式。
- 无法确认视频任务是否异步、进度如何计算、失败如何恢复。
- 无法确认实时检测是否正确释放摄像头/Tracker/模型资源。
- 若直接实现后端优化，风险是重写一个与原系统不兼容的新后端。

### 6.3 对 AI 链路的影响

- 离线训练脚本可审计，但应用内推理链无法确认。
- 无法确认当前业务系统加载哪个权重。
- 无法确认 `best.pt` 是否应随系统发布、由模型管理上传，还是当前预览包故意省略。
- 无法确认 YOLO 输出在后端、前端、报告、评估之间的真实字段。
- 不适合训练或替换模型；只能做模型资产和输出契约准备。

### 6.4 对测试/验收的影响

- 测试资源存在，但无法执行端到端冒烟。
- 只能建立测试用例清单，不能给出通过/失败结论。
- 图片、视频、评估、实时检测的验收路径必须等前后端可运行后再执行。

---

## 7. 是否需要先补齐 web-vue / web-flask 源码

**结论：需要。**

如果目标是进入 Phase 2 的“共享契约固化与可运行基线”，则必须先补齐或定位：

```text
1项目代码/floating-objects-detect-web/web-vue/src/
1项目代码/floating-objects-detect-web/web-vue/index.html
1项目代码/floating-objects-detect-web/web-vue/vite.config.*
1项目代码/floating-objects-detect-web/web-flask/app.py 或等价入口
1项目代码/floating-objects-detect-web/web-flask/routes/
1项目代码/floating-objects-detect-web/web-flask/services/
1项目代码/floating-objects-detect-web/web-flask/db / dao / models / init SQL
```

若暂时无法补齐，则后续只能执行：

- 文档契约草案；
- 测试 checklist；
- 源码缺口报告；
- 目录/压缩包/历史产物搜索；
- 补齐计划与交接指令。

不能执行：

- 页面开发；
- API 对接；
- DB 迁移；
- 冒烟测试；
- 核心流程优化；
- 端到端验收。

---

## 8. Phase 2 准入门槛

进入 Phase 2B（可运行基线）前，至少满足以下条件：

- [ ] 完整 `web-vue` 源码已补齐或真实位置已定位。
- [ ] 完整 `web-flask` 源码已补齐或真实位置已定位。
- [ ] 前端存在可运行入口：`index.html`、`vite.config.*`、`src/main.*`。
- [ ] 后端存在可运行入口：`app.py` 或等价启动模块。
- [ ] 后端 routes/services/db 初始化代码可审计。
- [ ] 前端 API 封装与后端 routes 可建立映射。
- [ ] AI 应用内推理封装位置已确认。
- [ ] DB 实际结构或初始化脚本已确认。
- [ ] `docs/contracts/` 至少有草案，并标注“源码确认/文档推断”。
- [ ] 启动 checklist 和冒烟 checklist 已准备好。

---

## 9. 下一步执行指令

### 9.1 Leader 指令：立即进入 Phase 2A，不进入业务实现

执行边界：

- 不写业务代码。
- 不重构。
- 不训练模型。
- 不替换权重。
- 不修改数据库。
- 不把文档推断写成源码事实。

### 9.2 Frontend Agent 指令

1. 搜索并确认完整 `web-vue` 源码是否存在于其他目录、压缩包、历史交付包或未解压资源中。
2. 若找到源码，使用独立 `frontend-worktree` 补齐/导入，再重新执行 FE-1。
3. 若未找到源码，输出 `FRONTEND_SOURCE_MISSING_REPORT.md`，列出缺失文件、影响、补齐要求。
4. 不要新建页面，不要按文档猜测实现前端。

### 9.3 Backend Agent 指令

1. 搜索并确认完整 `web-flask` 源码是否存在于其他目录、压缩包、历史交付包或未解压资源中。
2. 若找到源码，使用独立 `backend-worktree` 补齐/导入，再重新执行 BE-1/BE-2/BE-3。
3. 若未找到源码，输出 `BACKEND_SOURCE_MISSING_REPORT.md`，列出缺失 API、DB、服务层、启动入口、推理封装。
4. 不要新写 Flask 后端，不要重构 DB，不要臆造 routes。

### 9.4 AI Agent 指令

1. 保持模型权重和类别定义不变。
2. 基于当前 AI 审计输出，起草 YOLO 输出候选 schema、Qwen-VL 分析字段候选、evaluation metrics 候选。
3. 标注所有候选字段为“待后端源码确认”。
4. 不训练、不验证、不替换 `best.pt`。

### 9.5 Documentation/Test Agent 指令

1. 基于四份 Agent 报告和本汇总，生成正式 `DOC_SOURCE_GAP_REPORT.md`。
2. 建立 `docs/contracts/` 草案目录，但每份契约必须标注来源状态：
   - 已源码确认；
   - 已资源确认；
   - 文档推断；
   - 待源码确认。
3. 建立 Phase 2 启动 checklist 和冒烟 checklist。
4. 不覆盖业务代码，不移动模型权重。

### 9.6 Leader 下一轮检查点

下一轮只检查以下结果：

- 是否找到/补齐完整 `web-vue` 源码。
- 是否找到/补齐完整 `web-flask` 源码。
- `DOC_SOURCE_GAP_REPORT.md` 是否建立。
- `docs/contracts/` 是否建立草案并明确证据等级。
- 是否仍存在阻止 Phase 2B 的关键缺口。

---

## 10. 最终判定

| 问题 | 判定 |
---|---|
| 1. Phase 1 是否完成 | 审计交付完成；源码事实确认未完全完成 |
| 2. 是否具备进入 Phase 2 条件 | 仅具备进入 Phase 2A 文档契约准备；不具备进入 Phase 2B 可运行基线/代码实现 |
| 3. Phase 2 优先任务 | 先补齐/定位前后端源码；同时建立差异报告、契约草案、测试 checklist |
| 4. 哪些任务需要 Git Worktree | 凡涉及补齐/修改前端、后端、AI 代码或正式契约文件，都需要独立 worktree |
| 5. 哪些任务仍只适合文档确认 | API、JWT、DB、detection_result、Qwen-VL、状态机、冒烟测试等在源码缺失前只能文档确认 |
| 6. 源码缺口影响 | 阻断运行、构建、API/DB 核对、端到端冒烟、核心流程优化 |
| 7. 是否需要先补齐 `web-vue` / `web-flask` | 是，这是 Phase 2B 的前置条件 |
| 8. 下一步执行指令 | 进入 Phase 2A：源码定位/补齐 + 差异报告 + 契约草案 + checklist；禁止业务实现 |

