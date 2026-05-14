# AGENTS.md

本文件定义：
- 多Agent协作规则
- 模块职责边界
- Git/worktree规范
- 开发与Review流程

所有 Agent 必须优先遵循本文件规则。

# Directory Map

项目核心目录：

- web-vue/                     前端系统
- web-flask/                   后端与推理服务
- other/model_train/detect/   YOLO训练与推理
- 3项目文档/                    项目文档
- 4测试包/                      测试资源

# Shared Contracts

以下内容属于共享契约，修改前必须通知相关 Agent：

- API返回结构
- 数据库字段
- 模型输出JSON结构
- 文件存储结构
- JWT字段
- detection_result 数据格式
- evaluation metrics 格式

# AI Safety Rules

禁止：
- 未验证直接替换生产模型
- 删除已有模型权重
- 修改模型类别定义而不通知前端
- 修改检测结果格式而不通知相关模块

模型相关改动必须：
- 保持向后兼容
- 提供测试结果
- 说明精度变化

# Definition of Done

一个任务完成必须满足：

- 功能可运行
- 无明显报错
- 不破坏已有功能
- 有验证步骤
- 有影响范围说明
- 有回滚方案

# Documentation First

涉及：
- 架构
- 数据库
- API
- AI流程
- 模型结构

的重大修改：

必须先更新文档，再进入实现阶段。

# Project Overview

本项目是一个：
「YOLO目标检测 + 多模态AI分析」的水面漂浮物智能检测平台。

项目包含：
- Vue3 前端
- Flask 后端
- YOLO 模型训练与推理
- 视频检测
- 实时检测
- 模型管理
- 数据集管理
- 多模态AI分析
- 模型评估系统
- 数据库系统
- Word报告导出

当前目标：
不是快速写功能，
而是进行系统级梳理、工程化优化、多Agent并行开发与架构升级。

# Frontend Agent

目录：
- web-vue/

职责：
- Vue3 页面开发
- Element Plus UI
- ECharts 可视化
- 图片/视频/实时检测页面
- 模型管理页面
- 数据集管理页面
- 模型评估页面
- 大屏风格优化
- API 对接

禁止：
- 修改 Flask 后端逻辑
- 修改数据库结构
- 修改 YOLO 推理逻辑

# Backend Agent

目录：
- web-flask/

职责：
- Flask API
- JWT鉴权
- 文件上传
- 数据库逻辑
- 视频异步任务
- 实时检测接口
- 数据集验证
- 模型生命周期管理

禁止：
- 修改 Vue UI
- 修改 YOLO训练代码

# AI Agent

目录：
- other/model_train/detect/

职责：
- YOLO训练
- YOLO推理
- ByteTrack
- 模型评估
- CLAHE增强
- 多模态分析链
- Qwen-VL集成

禁止：
- 修改前端UI
- 修改业务页面

# Database & Documentation Agent

职责：
- 数据库文档维护
- API文档维护
- README
- 部署文档
- 测试文档
- SQL优化
- ER图
- 架构图

# Git Rules

所有 Agent 禁止共享同一工作目录。

必须：
- 使用 git worktree
- 每个 Agent 独立目录
- 独立分支开发

禁止：
- 多 Agent 同时修改同一目录
- 直接修改 main/master

# Engineering Principles

- 不允许一次性大重构
- 先保证系统可运行
- 每次改动必须可验证
- 优先小步提交
- 优先最小可用版本
- 不允许未经确认直接删除旧逻辑

# Current Priorities

当前优先级：

1. 系统架构梳理
2. 模块边界明确
3. 前后端职责拆分
4. AI分析链稳定
5. 视频检测流程优化
6. 实时检测性能优化
7. 模型管理工程化
8. UI整体统一

# Non-goals

当前阶段不做：

- Kubernetes
- 微服务拆分
- 云原生改造
- 大规模分布式
- 多摄像头集群
- 商业支付系统
- 移动端App

# Output Rules

所有 Agent 输出：

- 先分析
- 后规划
- 再实现

禁止：
- 未分析直接写代码
- 未确认直接大改
- 未说明直接删除

# Git Worktree Rules

所有 Agent 必须使用独立 worktree。

禁止多个 Agent 共享同一目录。

推荐结构：

- frontend-worktree
- backend-worktree
- ai-worktree
- docs-worktree

所有修改必须：
- 小步提交
- 可运行
- 可回滚

# Review Rules

所有 Agent 在提交前必须：

1. 说明修改内容
2. 说明影响范围
3. 说明风险点
4. 说明验证方式

禁止：
- 未验证直接提交
- 大范围删除
- 未说明直接重构

# Communication Rules

Agent 之间禁止直接覆盖彼此文件。

跨模块修改：
必须先说明影响范围。

Frontend 与 Backend API 变更：
必须同步接口契约。