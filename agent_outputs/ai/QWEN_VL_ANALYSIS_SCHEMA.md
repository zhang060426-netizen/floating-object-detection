# Qwen-VL Analysis Schema

阶段：Phase 2A 系统契约与重建基线  
角色：AI Agent  
边界：本文档仅定义 Qwen-VL 多模态分析字段候选，不替换大模型 API，不调用 API，不修改后端推理/LLM 代码。

证据等级统一使用：

- 已源码确认：有 `train.py` / `val.py` / `predict.py` 等源码证据。
- 已资源确认：有 `data.yaml`、weights、output、测试包等资源证据。
- 历史输出确认：来自 `output/` 中历史结果、指标文件。
- 文档推断：来自训练文档、系统文档、规划文档。
- 待后端源码确认：必须等 `web-flask` 推理调用链补齐后确认。
- 冲突/差异：脚本、历史输出、文档之间存在不一致。

## 1. 范围与边界

| 项目 | 内容 | 证据等级 |
|---|---|---|
| 覆盖链路 | 图片检测后的多模态分析：YOLO 结果 + 图片/增强图 + prompt -> Qwen-VL 分析 | 文档推断 |
| 使用场景 | 图片识别检测模块，不作为训练、验证、预测脚本的一部分 | 文档推断 |
| API 提供方 | 文档说明使用阿里云百炼平台的大语言模型 API / Qwen-VL | 文档推断 |
| 后端配置 | 文档提到 `web-flask/algo/llm/config.py`，当前可见后端源码未发现该路径 | 文档推断 + 待后端源码确认 |
| 禁止事项 | 不替换大模型 API，不调用 API，不写后端代码，不记录真实密钥 | 文档推断 |

## 2. Qwen-VL 分析输入候选

| 字段 | 类型候选 | 含义 | 必填候选 | 证据等级 |
|---|---|---|---|---|
| `analysis_input_version` | string | 分析输入 schema 版本 | 是 | 文档推断 |
| `record_id` | string/integer/null | 图片检测记录 ID | 可选 | 待后端源码确认 |
| `image_key` | string/null | 原图或结果图文件 key | 是，业务场景 | 待后端源码确认 |
| `image_base64` | string/null | 发给多模态模型的图像内容 | 可选，不建议持久化 | 文档推断 + 待后端源码确认 |
| `enhanced_image_key` | string/null | CLAHE 增强图 key | 可选 | 文档推断 + 待后端源码确认 |
| `detections` | array | YOLO 检测目标摘要 | 是 | 文档推断 |
| `detection_summary` | object | 目标数量、类别统计、置信度摘要 | 是 | 文档推断 |
| `scene_context` | string/null | 水域、时间、人工备注等上下文 | 可选 | 文档推断 |
| `language` | string | 输出语言，例如 `zh-CN` | 推荐 | 文档推断 |

## 3. prompt 元信息候选

| 字段 | 类型候选 | 含义 | 必填候选 | 证据等级 |
|---|---|---|---|---|
| `prompt_version` | string | prompt 版本号 | 是 | 文档推断 |
| `prompt_name` | string | prompt 名称，如 `water_pollution_analysis` | 是 | 文档推断 |
| `prompt_template_id` | string/null | 模板 ID | 可选 | 待后端源码确认 |
| `prompt_dimensions` | array | 分析维度，如水面状态、污染程度、污染源、生态影响、清理建议 | 推荐 | 文档推断 |
| `model_provider` | string | `dashscope` / `aliyun_bailian` 等 | 推荐 | 文档推断 |
| `llm_model` | string/null | 实际大模型名称 | 是，调用时 | 待后端源码确认 |
| `temperature` | number/null | 生成温度 | 可选 | 待后端源码确认 |
| `max_tokens` | integer/null | 最大输出长度 | 可选 | 待后端源码确认 |
| `request_id` | string/null | LLM 调用请求 ID | 可选 | 待后端源码确认 |

## 4. 污染描述字段候选

| 字段 | 类型候选 | 含义 | 必填候选 | 证据等级 |
|---|---|---|---|---|
| `pollution_description` | string | 总体污染描述 | 是 | 文档推断 |
| `water_surface_status` | string/null | 水面状态描述 | 推荐 | 文档推断 |
| `floating_object_description` | string/null | 漂浮物形态、数量、分布描述 | 推荐 | 文档推断 |
| `pollution_source_hypothesis` | string/null | 可能污染源，必须标注为推测 | 可选 | 文档推断 |
| `ecological_impact` | string/null | 生态影响说明 | 可选 | 文档推断 |
| `evidence_from_yolo` | array | 引用 YOLO 目标数量、类别和置信度 | 推荐 | 文档推断 |
| `visual_evidence` | array | 基于图片的可见证据摘要 | 推荐 | 文档推断 |

## 5. 风险等级字段候选

| 字段 | 类型候选 | 取值候选 | 含义 | 证据等级 |
|---|---|---|---|---|
| `risk_level` | enum | `low`、`medium`、`high`、`unknown` | 风险等级 | 文档推断 |
| `risk_score` | number/null | `0-100` 或 `0-1` | 风险分值，需定义量纲 | 文档推断 |
| `risk_basis` | string | `visual_only`、`yolo_plus_visual`、`manual_context` | 风险依据来源 | 文档推断 |
| `risk_confidence` | enum/number/null | `low`、`medium`、`high` 或数值 | LLM 对风险判断的置信度 | 文档推断 |
| `requires_manual_review` | boolean | `true/false` | 是否建议人工复核 | 文档推断 |

## 6. 风险原因字段候选

| 字段 | 类型候选 | 含义 | 必填候选 | 证据等级 |
|---|---|---|---|---|
| `risk_reasons` | array[string] | 风险原因列表 | 是 | 文档推断 |
| `reason_code` | string/null | 标准化原因码，如 `dense_floater`、`large_area` | 可选 | 文档推断 |
| `related_detection_ids` | array | 关联 YOLO detection id | 可选 | 文档推断 |
| `related_artifacts` | array | 关联图片、裁剪图、增强图 key | 可选 | 待后端源码确认 |
| `uncertainty_notes` | array[string] | 因画质、遮挡、漏检导致的不确定性 | 推荐 | 文档推断 |

## 7. 治理建议字段候选

| 字段 | 类型候选 | 含义 | 必填候选 | 证据等级 |
|---|---|---|---|---|
| `governance_suggestions` | array[object] | 治理建议列表 | 是 | 文档推断 |
| `suggestion_id` | string/null | 建议 ID | 可选 | 文档推断 |
| `category` | enum/string | `immediate_cleanup`、`process_optimization`、`prevention`、`long_term_plan`、`environmental_benefit` | 推荐 | 文档推断 |
| `priority` | enum | `low`、`medium`、`high` | 推荐 | 文档推断 |
| `action` | string | 具体建议动作 | 是 | 文档推断 |
| `rationale` | string | 建议理由 | 推荐 | 文档推断 |
| `expected_effect` | string/null | 预期效果 | 可选 | 文档推断 |
| `manual_review_required` | boolean | 是否需要人工确认 | 推荐 | 文档推断 |

## 8. 限制说明字段候选

| 字段 | 类型候选 | 含义 | 必填候选 | 证据等级 |
|---|---|---|---|---|
| `limitations` | array[string] | 分析限制说明 | 是 | 文档推断 |
| `image_quality_notes` | array[string] | 光照、模糊、遮挡等图像问题 | 可选 | 文档推断 |
| `model_limitations` | array[string] | YOLO 漏检、误检、单类别限制 | 推荐 | 文档推断 |
| `llm_limitations` | array[string] | 大模型推断不等于事实，需人工复核 | 推荐 | 文档推断 |
| `unsupported_claims` | array[string] | 无证据支撑的推断应单独列出或避免输出 | 推荐 | 文档推断 |

## 9. raw_response 与脱敏策略候选

| 字段 | 类型候选 | 含义 | 持久化建议 | 证据等级 |
|---|---|---|---|---|
| `raw_response` | string/object/null | 大模型原始返回 | 可选保存，便于审计 | 文档推断 |
| `raw_response_redacted` | string/object/null | 脱敏后的原始返回 | 推荐保存 | 文档推断 |
| `redaction_applied` | boolean | 是否已脱敏 | 推荐 | 文档推断 |
| `redaction_rules` | array[string] | 脱敏规则，如移除 API key、Authorization、Base64 大图 | 推荐 | 文档推断 |
| `store_image_base64` | boolean | 是否持久化图片 Base64 | 建议默认 false | 文档推断 |
| `sensitive_fields_removed` | array[string] | 已移除敏感字段 | 推荐 | 文档推断 |
| `log_trace_id` | string/null | 日志追踪 ID，不含密钥 | 可选 | 待后端源码确认 |

## 10. error / timeout / fallback 字段候选

| 字段 | 类型候选 | 含义 | 必填候选 | 证据等级 |
|---|---|---|---|---|
| `status` | enum | `success`、`failed`、`timeout`、`fallback`、`skipped` | 是 | 文档推断 |
| `error_code` | string/null | 错误码 | 失败时必填 | 文档推断 |
| `error_message` | string/null | 用户可读错误摘要 | 失败时必填 | 文档推断 |
| `provider_error` | string/object/null | 大模型供应商错误，需脱敏 | 可选 | 待后端源码确认 |
| `timeout_ms` | integer/null | 超时时间 | 可选 | 待后端源码确认 |
| `elapsed_ms` | integer/null | 实际耗时 | 推荐 | 文档推断 |
| `retry_count` | integer | 重试次数 | 推荐 | 文档推断 |
| `fallback_used` | boolean | 是否使用降级策略 | 推荐 | 文档推断 |
| `fallback_summary` | string/null | 降级说明，例如只返回 YOLO 摘要 | 可选 | 文档推断 |

## 11. 待后端源码确认项

| 编号 | 确认项 | 当前状态 | 证据等级 |
|---|---|---|---|
| QWEN-BE-001 | `web-flask/algo/llm/config.py` 是否存在 | 当前可见后端源码未发现 | 待后端源码确认 |
| QWEN-BE-002 | 实际 Qwen-VL 客户端、模型名、provider SDK | 当前只有文档描述 | 待后端源码确认 |
| QWEN-BE-003 | prompt 模板与版本管理 | 当前只有候选字段 | 待后端源码确认 |
| QWEN-BE-004 | 分析结果是否结构化 JSON 或纯文本 | 当前只有候选 schema | 待后端源码确认 |
| QWEN-BE-005 | 超时、重试、fallback 策略 | 当前只有建议 | 待后端源码确认 |
| QWEN-BE-006 | raw_response 是否落库及脱敏规则 | 当前只有建议 | 待后端源码确认 |
| QWEN-BE-007 | Word 报告消费哪些 Qwen-VL 字段 | 当前只有文档推断 | 待后端源码确认 |
| QWEN-BE-008 | CLAHE 增强图是否参与 Qwen-VL 输入 | 当前文档描述存在，源码未确认 | 待后端源码确认 |

