# Backend Phase 2B Gate

阶段：Phase 2A：系统契约与重建基线  
角色：Backend Agent  
边界：本文档定义后端进入 Phase 2B 的最小门禁，不执行代码实现。

## 1. 后端进入 Phase 2B 的最小条件

Phase 2B 定义：最小代码重建 / 可运行基线阶段。后端进入 Phase 2B 前，必须先满足以下最小条件：

| 条件 | 最小证据 | 当前状态 |
|---|---|---|
| 后端源码位置明确 | 找到完整 `web-flask` 源码，或明确最小重建范围 | 当前 BLOCKED：源码缺失 |
| 启动入口明确 | `app.py` 或等价启动模块可审计 | 当前 BLOCKED：未发现 |
| API routes 明确 | 至少 health、user、detection、file 的 route 可审计 | 当前 BLOCKED：未发现 |
| DB 初始化策略明确 | 有真实 DB 初始化代码、现有 SQLite 文件，或经 Leader 批准的临时开发 DB 策略 | 当前 BLOCKED：未发现 |
| 文件存储策略明确 | bucket/object_key 与 URL 生成规则可审计 | 当前 BLOCKED：未发现 |
| AI 推理封装明确 | YOLO 加载、推理、输出字段可审计 | 当前 BLOCKED：未发现 |
| 契约草案齐全 | API、DB、detection_result、文件存储、AI 输出、metrics 至少有草案 | Backend 部分已输出，AI/Docs/Frontend 依赖待汇总 |

门禁判定候选：当前后端不具备进入 Phase 2B 条件。

## 2. 最小可启动门禁

| 门禁项 | PASS 证据 | 证据等级要求 |
|---|---|---|
| Flask 启动入口存在 | 明确启动文件和命令 | 已源码确认 |
| 依赖与源码匹配 | `requirements.txt` 能支持源码 import | 已源码确认 / 已资源确认 |
| 配置加载明确 | 端口、DB 路径、文件目录、JWT secret 来源明确 | 已源码确认 |
| CORS 策略明确 | 前端本地地址与跨域配置可审计 | 已源码确认 |
| health 路由可用 | 有最小健康检查接口或启动验证方式 | 已源码确认 |
| 不依赖生产密钥启动 | Qwen-VL 缺密钥时可降级或禁用分析功能候选 | 已源码确认 / 待源码确认 |

当前状态：未发现启动入口，最小可启动门禁 BLOCKED。

## 3. 最小 API 门禁

进入 Phase 2B 后端最小 API 范围候选：

| API | 最小能力 | PASS 证据 | 证据等级要求 |
|---|---|---|---|
| health | 服务存活检查 | route 源码与响应格式 | 已源码确认 |
| user login | 默认账号登录，返回 token | route + JWT 签发源码 | 已源码确认 |
| user current | token 校验，返回当前用户 | route + 鉴权源码 | 已源码确认 |
| detection models/published | 返回可选已发布模型 | route + DB 查询源码 | 已源码确认 |
| detection detect | 图片上传、推理、返回检测结果候选 | route + 推理封装源码 | 已源码确认 |
| file read | 根据 bucket/object_key 返回文件或 URL | route/service 源码 | 已源码确认 |

Phase 2B 扩展 API 候选：

| API | 进入条件 |
|---|---|
| video-detection | health/user/detection/file 可用后 |
| realtime-detection | 模型缓存和资源释放策略明确后 |
| dataset/model admin | 权限与 DB 初始化确认后 |
| evaluation | detection_result 与 metrics schema 确认后 |

当前状态：所有 API 实现待源码确认。

## 4. 最小 DB 门禁

| 门禁项 | PASS 证据 | 证据等级要求 |
|---|---|---|
| DB 路径明确 | SQLite 文件路径或初始化目标路径明确 | 已源码确认 |
| 10 张核心表可核对 | 表结构与 `DB_CONTRACT.md` 对比完成 | 已源码确认 |
| 默认账号可验证 | `admin/test` 初始化或替代账号说明 | 已源码确认 |
| 默认模型/数据集策略明确 | 默认数据是否存在、已发布模型如何提供 | 已源码确认 |
| 外键与索引策略明确 | 初始化代码或 DB introspection 证据 | 已源码确认 |
| JSON 字段可解析 | `detection_result`、`metrics`、`structure_info` 示例 | 已源码确认 |

当前状态：未发现 DB 文件或初始化源码，最小 DB 门禁 BLOCKED。

## 5. 最小文件存储门禁

| 门禁项 | PASS 证据 | 证据等级要求 |
|---|---|---|
| 文件根目录明确 | `file_store/` 或等价路径存在/可配置 | 已源码确认 |
| bucket 枚举明确 | images/videos/crops/models/datasets/reports 等真实名称 | 已源码确认 |
| object_key 规则明确 | 记录 ID、用户 ID、日期、扩展名等规则可审计 | 已源码确认 |
| URL 生成明确 | API 代理、静态路由或附件下载方式明确 | 已源码确认 |
| 删除策略明确 | 删除记录时是否删除文件 | 已源码确认 |
| 安全限制明确 | 扩展名、大小、路径穿越防护 | 已源码确认 |

当前状态：`file_store/`、file route、file service 均未发现，最小文件存储门禁 BLOCKED。

## 6. 最小 AI 推理门禁

| 门禁项 | PASS 证据 | 证据等级要求 |
|---|---|---|
| 类别定义不变 | `class_id=0`, `floating_object` 保持 | 已资源确认 |
| 模型权重策略明确 | 使用已发布权重、基础权重占位，或等待真实 `best.pt` | 已源码确认 / 已资源确认 |
| YOLO 加载入口明确 | 后端模型加载源码可审计 | 已源码确认 |
| 推理输出字段明确 | bbox、confidence、class_id、class_name 格式可审计 | 已源码确认 |
| 空检测处理明确 | 无目标时响应和记录格式 | 已源码确认 |
| 推理失败处理明确 | 模型缺失、文件损坏、超时失败格式 | 已源码确认 |
| Qwen-VL 降级明确 | API key 缺失、超时、失败时的行为 | 已源码确认 |

当前状态：AI 训练资源已确认，但应用内推理封装未发现，最小 AI 推理门禁 BLOCKED。

## 7. 阻塞条件

任一条件成立则后端 Phase 2B 必须 BLOCKED：

| 阻塞条件 | 当前是否存在 | 证据等级 |
|---|---:|---|
| 未找到 `web-flask` 完整业务源码 | 是 | 冲突/差异 |
| 未找到 Flask 启动入口 | 是 | 冲突/差异 |
| 未找到 routes | 是 | 冲突/差异 |
| 未找到 DB 初始化或 SQLite 文件 | 是 | 冲突/差异 |
| 未找到 YOLO 应用内推理封装 | 是 | 冲突/差异 |
| 未找到文件存储服务或目录 | 是 | 冲突/差异 |
| API / DB / detection_result 契约草案缺失 | Backend 部分已输出；跨 Agent 汇总待 Leader 确认 | 文档推断 / 待源码确认 |
| 开始写业务代码但未通过门禁 | 当前未发生 | Phase 2A 边界 |
| 尝试修改数据库或创建迁移脚本 | 当前未发生 | Phase 2A 边界 |
| 替换模型权重或大模型 API | 当前未发生 | Phase 2A 边界 |

当前后端 Gate 建议：`BLOCKED`，直到源码恢复或 Leader 明确批准最小重建范围。

## 8. Leader 判定所需证据

Leader 判定后端是否进入 Phase 2B，需要以下证据包：

| 证据 | 说明 | 目标证据等级 |
|---|---|---|
| 后端目录地图 | 完整 `web-flask` 目录树，包含源码入口 | 已源码确认 |
| 启动入口说明 | 启动文件、启动命令、端口、配置来源 | 已源码确认 |
| routes 清单 | 每个 Blueprint / route 的路径、方法、权限 | 已源码确认 |
| API 响应样例 | 成功、错误、鉴权失败、权限不足样例 | 已源码确认 |
| JWT 实现说明 | payload、过期、密钥、鉴权装饰器 | 已源码确认 |
| DB 结构核对 | 真实 DB/初始化代码与 `DB_CONTRACT.md` 对照 | 已源码确认 |
| 文件存储核对 | bucket、object_key、URL、删除规则 | 已源码确认 |
| YOLO 推理核对 | 模型加载、输出字段、bbox 格式 | 已源码确认 |
| Qwen-VL 调用核对 | provider、配置、prompt、超时、降级 | 已源码确认 |
| 最小 smoke plan | 图片检测、登录、文件访问最小验证步骤 | 已源码确认 / 已资源确认 |
| 风险与回滚说明 | 若源码恢复失败，最小重建边界 | 文档推断 / Leader 判定 |

Leader 判定格式候选：

| 判定 | 条件 |
|---|---|
| PASS | 上述最小启动、API、DB、文件、AI 推理门禁均有可审计证据，且未违反 Phase 2A 禁止项 |
| BLOCKED | 任一关键入口缺失、契约草案缺失、源码状态不明、或存在未经门禁的业务实现 |

截至本文件生成时，Backend Phase 2B Gate 建议为：`BLOCKED`。

