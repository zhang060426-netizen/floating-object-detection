# Doc Source Gap Report

更新时间：2026-05-13  
阶段：Phase 2A：系统契约与重建基线  
边界：仅汇总文档描述、当前可见源码/资源事实和差异；不写业务代码、不补源码、不执行测试。

## 1. 范围与输入

| 输入 | 用途 | 当前结论 | 证据等级 |
|---|---|---|---|
| `PHASE2A_SYSTEM_CONTRACT_REBUILD_PLAN.md` | Phase 2A 任务与边界 | 明确只做契约与重建基线，不进入实现 | 文档推断 |
| `PHASE1_MASTER_SUMMARY.md` | Phase 1 总结 | 前后端源码事实不足，AI/测试资源相对完整 | 文档推断 |
| `PHASE1_AUDIT_STATUS.md` | Leader 调度记录 | 实际源码根为 `1项目代码/floating-objects-detect-web/` | 文档推断 |
| `agent_outputs/frontend/FE_PHASE1_AUDIT.md` | 前端审计 | 当前仅确认 `package.json` 和 `2须知.txt` | 已资源确认 |
| `agent_outputs/backend/BE_PHASE1_AUDIT.md` | 后端审计 | 当前仅确认 `requirements.txt` 和 `1须知.txt` | 已资源确认 |
| `agent_outputs/ai/AI_PHASE1_AUDIT.md` | AI 审计 | 训练脚本、数据集、基础权重、历史指标已确认 | 已资源确认 |
| `agent_outputs/docs/DOC_TEST_PHASE1_AUDIT.md` | Docs/Test 审计 | 测试资源索引与差异模板已建立 | 已资源确认 |
| 根目录规划文档 | 架构、边界、路线、协作计划 | 可作为设计预期，不是源码事实 | 文档推断 |
| `3项目文档/1系统介绍文档.md` | 系统功能、API、流程、目录候选 | 描述完整系统，但需源码复核 | 文档推断 |
| `3项目文档/5数据库开发文档.md` | DB 表、字段、索引、SQL | 可作为数据库文档定义 | 数据库文档确认 |
| `4测试包/` | 图片、视频、评估图片/标签、数据集包 | 资源存在，可映射冒烟场景 | 已资源确认 |

## 2. 总体差异结论

| 领域 | 总体差异 | 影响 | Phase 2A 处理 | 证据等级 |
|---|---|---|---|---|
| 前端 | 文档描述完整 Vue3 工程，当前未发现 `src/`、入口、路由、页面、API 封装 | 阻断页面/API 源码确认和前端运行 | 只能建立页面地图草案和源码恢复任务 | 冲突/差异 |
| 后端 | 文档描述完整 Flask 工程，当前未发现 `app.py`、routes、services、DB 初始化、algo | 阻断 API、DB、鉴权、推理链源码确认 | 只能建立 API/DB/文件/JWT 候选契约 | 冲突/差异 |
| AI | 离线训练目录存在，但应用内推理封装依赖后端源码 | 阻断业务推理输出与报告字段确认 | 可建立 YOLO/Qwen-VL/metrics 候选 schema | 已资源确认 |
| 数据库 | DB 文档定义 10 张表，但当前未发现 DB 初始化代码或 SQLite 文件 | 阻断真实表结构比对 | 只能标记为数据库文档确认 | 数据库文档确认 |
| 测试 | 测试资源存在，但无可运行前后端入口且本阶段禁止执行冒烟测试 | 阻断 PASS/FAIL 测试结论 | 只能建立资源映射和 checklist | 已资源确认 |

## 3. 前端差异表

| 编号 | 文档描述 | 当前可见文件/资源 | 差异类型 | 影响 | 下一步 | 证据等级 |
|---|---|---|---|---|---|---|
| FE-GAP-001 | `web-vue/src/` 下应有 api、components、views、stores、types、utils、router | 当前 `web-vue/` 仅有 `package.json`、`2须知.txt` | 源码缺失 | 无法确认页面、路由、组件、状态管理 | 定位或恢复完整前端源码 | 冲突/差异 |
| FE-GAP-002 | 前端应有 Vite 入口 `index.html`、`vite.config.ts`、`src/main.ts` | 当前未发现这些入口 | 源码缺失 | 无法启动或构建前端 | Phase 2B 前明确恢复或最小重建范围 | 冲突/差异 |
| FE-GAP-003 | 系统介绍列出登录、检测、视频、实时、模型、数据集、评估页面 | 当前无页面源码 | 接口/字段待核对 | 无法输出源码确认版页面-API 矩阵 | 先保持文档推断，不进入 UI 实现 | 待源码确认 |
| FE-GAP-004 | 技术栈包含 Vue、Pinia、Element Plus、Axios、ECharts | `package.json` 中依赖存在 | 依赖存在但实现待确认 | 可确认依赖意图，不能确认实际使用 | 补齐源码后核对使用情况 | 已资源确认 |

## 4. 后端差异表

| 编号 | 文档描述 | 当前可见文件/资源 | 差异类型 | 影响 | 下一步 | 证据等级 |
|---|---|---|---|---|---|---|
| BE-GAP-001 | `web-flask/app.py` 为主应用入口 | 当前未发现 `app.py` | 源码缺失 | 无法启动后端或确认 Flask app 创建方式 | 定位或恢复后端源码 | 冲突/差异 |
| BE-GAP-002 | `routes/` 包含 user、detection、video、realtime、dataset、model、file 等路由 | 当前未发现 `routes/` | 源码缺失 | API 契约只能按文档草案处理 | Backend 输出 API_CONTRACT 草案并标注待确认 | 冲突/差异 |
| BE-GAP-003 | `utils/db.py`、`utils/models.py`、DB 文件等应支撑数据库 | 当前未发现 DB 初始化源码或 SQLite 文件 | 源码缺失 | 不能核对实际表结构 | 基于 DB 文档建立 DB_CONTRACT 草案 | 待源码确认 |
| BE-GAP-004 | LLM 配置位于 `web-flask/algo/llm/config.py` | 当前未发现 `algo/llm/config.py` | 路径差异/源码缺失 | Qwen-VL 配置、密钥、超时、降级策略无法确认 | 后端源码恢复后复核 | 冲突/差异 |
| BE-GAP-005 | `requirements.txt` 包含 Flask-CORS、PyJWT、ultralytics、openai、python-docx、lap | 依赖文件存在 | 依赖存在但实现待确认 | 可确认依赖意图，不能确认实现 | 后续核对实际导入与调用链 | 已资源确认 |

## 5. AI 链路差异表

| 编号 | 文档描述 | 当前可见文件/资源 | 差异类型 | 影响 | 下一步 | 证据等级 |
|---|---|---|---|---|---|---|
| AI-GAP-001 | 离线训练/验证/预测脚本存在 | `code/train.py`、`val.py`、`predict.py` 存在 | 无差异 | 可建立 AI 资产基线 | AI Agent 输出 schema 时引用脚本证据 | 已源码确认 |
| AI-GAP-002 | 类别为 `0: floating_object` | `data.yaml` 中 `nc: 1`、`names: ['floating_object']` | 无差异 | 类别契约可资源确认 | 不改类别定义 | 已资源确认 |
| AI-GAP-003 | 历史测试指标 P 0.889、R 0.827、mAP50 0.915、mAP50-95 0.659 | 历史 output / 指标文件记录存在 | 无差异 | 可作为历史指标，不可当作本轮测试结果 | 不执行测试，仅标注历史输出 | 历史输出确认 |
| AI-GAP-004 | 应用内 YOLO 推理、缓存、并发、异常处理 | 后端源码缺失，无法确认 | 接口/字段待核对 | `detection_result` 真实结构未知 | Phase 2B 需确认后端推理封装 | 待源码确认 |
| AI-GAP-005 | 历史 `best.pt` 路径应存在已训练权重 | 当前可见历史权重目录只有占位说明 | 历史产物缺口 | 不得宣称已训练权重随包存在 | 等真实权重补齐或明确降级策略 | 冲突/差异 |

## 6. 数据库差异表

| 编号 | 文档描述 | 当前可见文件/资源 | 差异类型 | 影响 | 下一步 | 证据等级 |
|---|---|---|---|---|---|---|
| DB-GAP-001 | DB 文档定义 `user`、`datasets`、`models` 等 10 张表 | `3项目文档/5数据库开发文档.md` 存在完整表结构 | 无源码实现证据 | 只能作为文档定义 | Backend 输出 DB_CONTRACT 草案 | 数据库文档确认 |
| DB-GAP-002 | 文档定义建表 SQL 与索引 | 当前未发现 DB 初始化脚本 | 源码缺失 | 无法确认实际执行 | Phase 2B 前需恢复 DB 初始化入口 | 待源码确认 |
| DB-GAP-003 | 默认用户 `admin/test`、默认数据集、默认模型 | DB 文档和使用注意事项描述 | 实现待核对 | 不能声明当前 DB 已有数据 | 后端源码/DB 文件恢复后核对 | 数据库文档确认 |
| DB-GAP-004 | 文件存储使用 bucket/object_key 模式 | DB 字段文档存在 | 实现待核对 | 不能确认实际目录和 URL 生成 | 建立 FILE_STORAGE_CONTRACT 草案 | 数据库文档确认 |

## 7. 测试资源差异表

| 编号 | 文档描述 | 当前可见文件/资源 | 差异类型 | 影响 | 下一步 | 证据等级 |
|---|---|---|---|---|---|---|
| TEST-GAP-001 | 测试包包含图片、视频、评估资源 | `4测试包/` 有 15 张测试图片、6 个视频、40 张评估图片和 40 个标签 | 无差异 | 可建立冒烟资源映射 | 写入 `SMOKE_TEST_RESOURCE_MAP.md` | 已资源确认 |
| TEST-GAP-002 | 模型评估可用图片+标签执行 | 评估图片与标签 basename 一致 | 测试不可执行 | 可映射资源，但不能给出测试结论 | Phase 2B 启动后执行 | 已资源确认 |
| TEST-GAP-003 | 实时检测依赖本地 USB 摄像头 | 使用注意事项明确限制 | 环境依赖 | 当前文件系统无法验证 | 写明暂不可执行 | 文档推断 |
| TEST-GAP-004 | 端到端冒烟测试 | 当前无前后端可运行入口，且 Phase 2A 禁止执行 | 测试入口缺失 | 不能声明 PASS/FAIL | 仅建立 checklist | 待源码确认 |

## 8. 共享契约缺口

| 契约 | 当前缺口 | 影响模块 | Phase 2A 输出要求 | 证据等级 |
|---|---|---|---|---|
| API_CONTRACT | API 仅有文档描述，缺少 routes 源码 | Frontend、Backend、Docs/Test | Backend 草案，Docs 索引 | 待源码确认 |
| DETECTION_RESULT_SCHEMA | 缺少业务推理封装和前端解析源码 | Frontend、Backend、AI、报告 | Backend+AI 草案 | 待源码确认 |
| AI_OUTPUT_SCHEMA | 离线 YOLO 可推断，业务输出待后端确认 | Backend、AI | AI 草案 | 已资源确认 |
| DB_CONTRACT | 只有 DB 文档，缺少实际初始化代码 | Backend、Docs/Test | Backend+Docs 草案 | 数据库文档确认 |
| FILE_STORAGE_CONTRACT | bucket/object_key 字段有文档，实际路径缺失 | Frontend、Backend、Docs | Backend 草案 | 数据库文档确认 |
| QWEN_VL_ANALYSIS_SCHEMA | 文档有流程，配置和调用源码缺失 | Backend、AI、Frontend | AI 草案 | 待源码确认 |
| EVALUATION_METRICS_SCHEMA | 文档/历史指标存在，接口返回待确认 | Frontend、Backend、AI | AI 草案 | 历史输出确认 |

## 9. 对 Phase 2B 的影响

| 影响项 | Phase 2B 阻塞条件 | 可进入条件 | 证据等级 |
|---|---|---|---|
| 前端实现 | 没有 `index.html`、`vite.config.*`、`src/main.*`、`src/router`、`src/views` | 源码恢复或最小重建范围冻结 | 待源码确认 |
| 后端实现 | 没有 Flask 入口、routes、services、DB 初始化 | 源码恢复或最小重建范围冻结 | 待源码确认 |
| API 对接 | API_CONTRACT 尚未完成或未被 Frontend review | 契约草案完成并标注证据等级 | 文档推断 |
| 数据库 | DB_CONTRACT 未完成且无初始化策略 | DB 文档草案和初始化计划明确 | 数据库文档确认 |
| AI 接入 | 应用内推理封装位置未知 | 最小推理输入/输出 schema 明确 | 已资源确认 |
| 冒烟测试 | 无可运行系统且禁止测试 | Phase 2B 启动后再执行 | 待源码确认 |

## 10. 下一步补齐优先级

| 优先级 | 任务 | 负责人 | 输出 | 证据等级 |
|---|---|---|---|---|
| P0 | 完成 `EVIDENCE_LEVELS.md` 和 `CONTRACT_INDEX.md` | Docs/Test | 统一证据规则和契约索引 | 文档推断 |
| P0 | 输出 API、DB、detection_result、文件存储契约草案 | Backend | `agent_outputs/backend/*.md` | 待源码确认 |
| P0 | 输出 AI 输出、Qwen-VL、metrics、模型资产契约草案 | AI | `agent_outputs/ai/*.md` | 已资源确认 |
| P0 | 输出前端页面地图和源码恢复任务 | Frontend | `agent_outputs/frontend/*.md` | 待源码确认 |
| P1 | 完成 Phase 2B Gate 判定 | Leader + Docs/Test | PASS/BLOCKED 结论 | 文档推断 |
