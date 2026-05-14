# Phase 2B Pre-Dev Freeze

更新时间：2026-05-14  
角色：Phase 2A Leader / Coordinator  
阶段：Phase 2B 前置门禁冻结  
状态：**PRE-DEV FREEZE / NO BUSINESS CODE YET**

---

## 0. 决策摘要

用户已确认：

```text
完整 web-vue 与 web-flask 业务源码无法恢复。
```

因此 Phase 2B 不再以“继续等待原源码恢复”为前置，而转为：

```text
最小可运行系统重建前置规划与门禁冻结。
```

但本文件仍不是代码实现指令。本阶段只冻结范围、契约、目录、门禁、Agent 分工与 Git/worktree 策略。

### 0.1 当前禁止项

- 不写业务代码。
- 不创建 `web-vue/src`。
- 不创建 Flask routes/services/app 源码。
- 不训练模型。
- 不修改、替换、移动、删除权重。
- 不创建或修改 SQLite 数据库文件。
- 不初始化数据库。
- 不实现视频检测、实时检测、Word 报告、大屏美化、模型训练、完整数据集管理。

### 0.2 Phase 2B 首批范围

只允许规划以下最小闭环：

1. 登录
2. 图片检测
3. 模型加载
4. 检测记录保存

### 0.3 继续暂缓范围

- 视频检测
- 实时检测
- Word 报告
- 大屏美化
- 模型训练
- 数据集管理完整流程
- 模型评估完整流程
- Qwen-VL 真实调用链

---

## 1. 最小可运行系统目录结构

以下目录结构是 **Phase 2B 代码开发前的冻结目标**，不是当前已创建事实。只有在 Gate 通过并创建对应 worktree 后，才允许由对应 Agent 实现。

### 1.1 总体目录

```text
1项目代码/floating-objects-detect-web/
  web-vue/                         # Frontend worktree 写入范围
  web-flask/                       # Backend worktree 写入范围
  other/model_train/detect/        # AI 资源与脚本，只读优先
```

### 1.2 Frontend 最小目录结构

```text
web-vue/
  package.json
  index.html
  vite.config.ts
  src/
    main.ts
    App.vue
    router/
      index.ts
    api/
      request.ts
      auth.ts
      detection.ts
      model.ts
      file.ts
    stores/
      user.ts
    views/
      Login.vue
      ImageDetect.vue
      DetectionRecords.vue
      DetectionRecordDetail.vue
    components/
      AppLayout.vue
      ImageUploader.vue
      DetectionResultPanel.vue
    types/
      api.ts
      detection.ts
      model.ts
      user.ts
    utils/
      fileUrl.ts
      format.ts
```

#### Frontend 首批页面

| 页面 | 路由候选 | 目的 |
|---|---|---|
| 登录页 | `/login` | 获取 JWT token |
| 图片检测页 | `/detect/image` | 上传图片、选择模型、展示检测结果 |
| 检测记录页 | `/records/detection` | 查看已保存的图片检测记录 |
| 检测记录详情页 | `/records/detection/:id` | 查看单条检测结果、原图、结果图、JSON |

### 1.3 Backend 最小目录结构

```text
web-flask/
  requirements.txt
  app.py
  config.py
  db/
    init_db.py
    schema.sql
    seed.py
  routes/
    health.py
    auth.py
    detection.py
    model.py
    file.py
  services/
    auth_service.py
    detection_service.py
    model_service.py
    file_storage_service.py
  ai/
    yolo_infer.py
  utils/
    response.py
    jwt_utils.py
    paths.py
  storage/
    uploads/
    results/
    models/
```

#### Backend 首批模块

| 模块 | 目的 |
|---|---|
| `app.py` | Flask 最小启动入口 |
| `routes/health.py` | 健康检查 |
| `routes/auth.py` | 登录与用户信息 |
| `routes/detection.py` | 图片检测、保存记录、查询记录 |
| `routes/model.py` | 获取可用模型列表 |
| `routes/file.py` | 文件访问 |
| `db/schema.sql` | 最小 SQLite 表结构 |
| `ai/yolo_infer.py` | YOLO 单图推理封装 |

### 1.4 AI 资源目录

AI 目录保持现状，Phase 2B 首批只读使用：

```text
other/model_train/detect/
  code/
    train.py        # 不修改
    val.py          # 不修改
    predict.py      # 不修改
  weights/
    yolov8n.pt
    yolo11n.pt
    yolo12n.pt
    yolo26n.pt
  dataset/
  output/
```

Phase 2B 首批默认使用基础权重作为开发占位模型，不声明生产精度。

---

## 2. 最小 API 契约

统一前缀候选：

```text
/api
```

统一响应格式：

```json
{
  "code": 0,
  "message": "ok",
  "data": {}
}
```

统一错误格式：

```json
{
  "code": 400,
  "message": "error message",
  "data": null
}
```

### 2.1 Health API

| 方法 | 路径 | 鉴权 | 说明 |
|---|---|---|---|
| GET | `/api/health` | 否 | 后端健康检查 |

响应：

```json
{
  "code": 0,
  "message": "ok",
  "data": {
    "status": "ok",
    "service": "web-flask"
  }
}
```

### 2.2 Auth API

| 方法 | 路径 | 鉴权 | 说明 |
|---|---|---|---|
| POST | `/api/auth/login` | 否 | 登录 |
| GET | `/api/auth/me` | 是 | 获取当前用户 |

#### POST `/api/auth/login`

请求：

```json
{
  "username": "admin",
  "password": "admin123"
}
```

响应：

```json
{
  "code": 0,
  "message": "ok",
  "data": {
    "token": "<jwt>",
    "user": {
      "id": "u_admin",
      "username": "admin",
      "role": "admin"
    }
  }
}
```

### 2.3 Model API

| 方法 | 路径 | 鉴权 | 说明 |
|---|---|---|---|
| GET | `/api/models/published` | 是 | 获取可用于图片检测的模型列表 |

响应：

```json
{
  "code": 0,
  "message": "ok",
  "data": [
    {
      "id": "m_yolo26n_dev",
      "name": "YOLO26n Dev Baseline",
      "base_model": "yolo26n",
      "weight_path": "other/model_train/detect/weights/yolo26n.pt",
      "status": "published",
      "is_dev_placeholder": true
    }
  ]
}
```

### 2.4 Image Detection API

| 方法 | 路径 | 鉴权 | 说明 |
|---|---|---|---|
| POST | `/api/detection/image` | 是 | 上传图片并执行 YOLO 检测 |
| POST | `/api/detection/records` | 是 | 保存检测记录 |
| GET | `/api/detection/records` | 是 | 查询检测记录列表 |
| GET | `/api/detection/records/:id` | 是 | 查询检测记录详情 |

#### POST `/api/detection/image`

请求类型：`multipart/form-data`

字段：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---:|---|
| `image` | file | 是 | 待检测图片 |
| `model_id` | string | 是 | 模型 ID |
| `confidence_threshold` | number | 否 | 默认 `0.5` |
| `save_record` | boolean | 否 | 是否自动保存记录，默认 `true` |

响应：

```json
{
  "code": 0,
  "message": "ok",
  "data": {
    "record_id": "dr_xxx",
    "original_image": {
      "bucket": "uploads",
      "object_key": "images/2026/05/14/xxx.jpg",
      "url": "/api/files/uploads/images/2026/05/14/xxx.jpg"
    },
    "result_image": {
      "bucket": "results",
      "object_key": "images/2026/05/14/xxx_result.jpg",
      "url": "/api/files/results/images/2026/05/14/xxx_result.jpg"
    },
    "detection_result": {
      "model": {
        "model_id": "m_yolo26n_dev",
        "model_name": "YOLO26n Dev Baseline",
        "base_model": "yolo26n",
        "confidence_threshold": 0.5
      },
      "image": {
        "width": 1280,
        "height": 720,
        "filename": "xxx.jpg"
      },
      "detections": [],
      "summary": {
        "total_detections": 0,
        "has_detections": false,
        "max_confidence": null,
        "avg_confidence": null
      },
      "artifacts": {}
    }
  }
}
```

### 2.5 File API

| 方法 | 路径 | 鉴权 | 说明 |
|---|---|---|---|
| GET | `/api/files/:bucket/*object_key` | 是 | 读取已保存文件 |

允许 bucket：

```text
uploads
results
models
```

---

## 3. 最小 SQLite 表结构

数据库文件候选：

```text
web-flask/storage/app.sqlite3
```

当前阶段不创建数据库文件；以下仅冻结 Phase 2B 首批最小 schema。

### 3.1 `users`

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| `id` | TEXT | PRIMARY KEY | 用户 ID |
| `username` | TEXT | UNIQUE NOT NULL | 登录名 |
| `password_hash` | TEXT | NOT NULL | 密码哈希 |
| `role` | TEXT | NOT NULL | `admin` / `user` |
| `created_at` | TEXT | NOT NULL | 创建时间 |
| `updated_at` | TEXT | NOT NULL | 更新时间 |

### 3.2 `models`

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| `id` | TEXT | PRIMARY KEY | 模型 ID |
| `name` | TEXT | NOT NULL | 模型名称 |
| `base_model` | TEXT | NOT NULL | `yolov8n` / `yolo11n` / `yolo12n` / `yolo26n` |
| `weight_path` | TEXT | NOT NULL | 本地权重路径 |
| `status` | TEXT | NOT NULL | `published` / `disabled` |
| `is_dev_placeholder` | INTEGER | NOT NULL DEFAULT 1 | 是否开发占位模型 |
| `created_at` | TEXT | NOT NULL | 创建时间 |
| `updated_at` | TEXT | NOT NULL | 更新时间 |

### 3.3 `detection_records`

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| `id` | TEXT | PRIMARY KEY | 检测记录 ID |
| `user_id` | TEXT | NOT NULL | 用户 ID |
| `model_id` | TEXT | NOT NULL | 模型 ID |
| `title` | TEXT | NULL | 记录标题 |
| `original_bucket` | TEXT | NOT NULL | 原图 bucket |
| `original_object_key` | TEXT | NOT NULL | 原图 object key |
| `result_bucket` | TEXT | NULL | 结果图 bucket |
| `result_object_key` | TEXT | NULL | 结果图 object key |
| `detection_result` | TEXT | NOT NULL | JSON 字符串 |
| `confidence_threshold` | REAL | NOT NULL DEFAULT 0.5 | 置信度阈值 |
| `created_at` | TEXT | NOT NULL | 创建时间 |
| `updated_at` | TEXT | NOT NULL | 更新时间 |

### 3.4 `detection_crops`

首批可选。如果 Phase 2B 第一轮不做裁剪图保存，可暂不实现，但 schema 预留如下：

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| `id` | TEXT | PRIMARY KEY | 裁剪目标 ID |
| `record_id` | TEXT | NOT NULL | 检测记录 ID |
| `object_index` | INTEGER | NOT NULL | 目标序号 |
| `class_id` | INTEGER | NOT NULL | 类别 ID |
| `class_name` | TEXT | NOT NULL | 类别名 |
| `confidence` | REAL | NOT NULL | 置信度 |
| `bbox` | TEXT | NOT NULL | JSON `[x1,y1,x2,y2]` |
| `crop_bucket` | TEXT | NULL | 裁剪图 bucket |
| `crop_object_key` | TEXT | NULL | 裁剪图 object key |
| `created_at` | TEXT | NOT NULL | 创建时间 |

---

## 4. 最小 YOLO 推理输入/输出

### 4.1 权重策略

Phase 2B 首批默认使用：

```text
other/model_train/detect/weights/yolo26n.pt
```

原因：

- 文件存在。
- `train.py` 参考该基础权重。
- 可作为开发占位模型。

限制：

- 不声明该权重为业务最优模型。
- 不声明历史训练精度可复现。
- 不替换缺失的 `best.pt`。
- 不修改 `weights/` 和 `output/` 目录。

### 4.2 输入

```json
{
  "image_path": "web-flask/storage/uploads/images/2026/05/14/xxx.jpg",
  "model_id": "m_yolo26n_dev",
  "weight_path": "other/model_train/detect/weights/yolo26n.pt",
  "confidence_threshold": 0.5,
  "imgsz": 640
}
```

### 4.3 输出

```json
{
  "model": {
    "model_id": "m_yolo26n_dev",
    "model_name": "YOLO26n Dev Baseline",
    "base_model": "yolo26n",
    "weight_name": "yolo26n.pt",
    "confidence_threshold": 0.5
  },
  "image": {
    "filename": "xxx.jpg",
    "width": 1280,
    "height": 720
  },
  "detections": [
    {
      "detection_id": "det_0",
      "class_id": 0,
      "class_name": "floating_object",
      "confidence": 0.86,
      "bbox": {
        "format": "xyxy_pixel",
        "xyxy": [100, 120, 240, 260],
        "xywhn": [0.1328, 0.2639, 0.1094, 0.1944]
      }
    }
  ],
  "summary": {
    "total_detections": 1,
    "has_detections": true,
    "max_confidence": 0.86,
    "avg_confidence": 0.86
  },
  "timing": {
    "inference_ms": 120
  }
}
```

### 4.4 类别冻结

Phase 2B 首批保持：

```text
class_id = 0
class_name = floating_object
```

不得在 Phase 2B 首批修改类别定义。

---

## 5. 文件存储路径规范

当前阶段不创建目录、不写文件；以下为 Phase 2B 实现时必须遵守的最小路径规范。

### 5.1 存储根目录

```text
web-flask/storage/
```

### 5.2 Bucket 规范

| bucket | 本地目录 | 用途 |
|---|---|---|
| `uploads` | `web-flask/storage/uploads/` | 用户上传原始文件 |
| `results` | `web-flask/storage/results/` | 检测结果图、派生文件 |
| `models` | `web-flask/storage/models/` | 后续模型上传；首批可只读占位 |

### 5.3 Object Key 规范

图片原图：

```text
images/YYYY/MM/DD/{uuid}_{safe_filename}
```

图片检测结果：

```text
images/YYYY/MM/DD/{uuid}_result.jpg
```

裁剪图预留：

```text
crops/YYYY/MM/DD/{record_id}_{object_index}.jpg
```

### 5.4 文件 URL

统一由 File API 暴露：

```text
/api/files/{bucket}/{object_key}
```

示例：

```text
/api/files/uploads/images/2026/05/14/abc_test.jpg
/api/files/results/images/2026/05/14/abc_result.jpg
```

### 5.5 文件安全规则

- `object_key` 不允许 `..`。
- 上传文件名必须安全化。
- 首批只允许图片类型：`.jpg`、`.jpeg`、`.png`。
- 单文件大小上限建议：`20 MB`。
- 不允许通过 File API 访问项目任意路径。

---

## 6. 默认账号与鉴权策略

### 6.1 默认账号

Phase 2B 首批开发环境默认账号：

```text
username: admin
password: admin123
role: admin
```

限制：

- 仅用于本地开发和冒烟测试。
- 文档和 UI 必须标注“开发默认账号”。
- 后续正式部署必须修改密码或禁用默认种子账号。

### 6.2 JWT Header

```text
Authorization: Bearer <token>
```

### 6.3 JWT Payload

```json
{
  "sub": "u_admin",
  "username": "admin",
  "role": "admin",
  "iat": 1778755155,
  "exp": 1778841555
}
```

### 6.4 鉴权规则

| API | 是否鉴权 |
|---|---|
| `GET /api/health` | 否 |
| `POST /api/auth/login` | 否 |
| `GET /api/auth/me` | 是 |
| `GET /api/models/published` | 是 |
| `POST /api/detection/image` | 是 |
| `POST /api/detection/records` | 是 |
| `GET /api/detection/records` | 是 |
| `GET /api/detection/records/:id` | 是 |
| `GET /api/files/:bucket/*object_key` | 是 |

### 6.5 密码策略

首批只冻结策略，不实现代码：

- 数据库存储 `password_hash`，不得明文存储。
- 登录接口只返回 token 和最小用户信息。
- token 过期时间建议：24 小时。

---

## 7. Phase 2B 冒烟测试清单

本清单仅用于 Phase 2B 开发完成后验证。当前不执行测试。

### 7.1 启动检查

| 编号 | 检查项 | 期望 |
|---|---|---|
| S-01 | 后端启动 | Flask 可启动，无 import error |
| S-02 | 健康检查 | `GET /api/health` 返回 `status=ok` |
| S-03 | 前端启动 | Vite dev server 可启动 |
| S-04 | 前端访问 | 浏览器可打开登录页 |

### 7.2 登录检查

| 编号 | 检查项 | 期望 |
|---|---|---|
| A-01 | 默认账号登录 | 返回 JWT token |
| A-02 | token 请求 `/api/auth/me` | 返回当前用户 |
| A-03 | 无 token 请求受保护接口 | 返回 401 |

### 7.3 模型加载检查

| 编号 | 检查项 | 期望 |
|---|---|---|
| M-01 | 查询发布模型 | 返回至少一个开发占位模型 |
| M-02 | 权重路径存在性 | `yolo26n.pt` 可被后端识别 |
| M-03 | 权重不变更 | 权重文件未被修改、移动、替换 |

### 7.4 图片检测检查

| 编号 | 检查项 | 期望 |
|---|---|---|
| D-01 | 上传测试图片 | 后端保存原图 |
| D-02 | 执行 YOLO 推理 | 返回 `detections`、`summary`、`model` |
| D-03 | 生成结果图 | 返回可访问 `result_image.url` |
| D-04 | 空检测兼容 | `detections=[]` 时仍返回成功结构 |
| D-05 | 坐标格式 | bbox 使用 `xyxy_pixel` 主格式 |

### 7.5 检测记录检查

| 编号 | 检查项 | 期望 |
|---|---|---|
| R-01 | 自动保存记录 | 图片检测后生成 `record_id` |
| R-02 | 查询记录列表 | 返回分页或数组列表 |
| R-03 | 查询记录详情 | 返回原图、结果图、检测 JSON |
| R-04 | 文件 URL 可访问 | 原图和结果图可通过 File API 访问 |

### 7.6 暂缓功能检查

| 编号 | 功能 | 期望 |
|---|---|---|
| X-01 | 视频检测 | 不在首批实现；如访问应显示未开放或无路由 |
| X-02 | 实时检测 | 不在首批实现 |
| X-03 | Word 报告 | 不在首批实现 |
| X-04 | 大屏美化 | 不在首批实现 |
| X-05 | 模型训练 | 不在首批实现 |
| X-06 | 数据集管理完整流程 | 不在首批实现 |

---

## 8. Git init 与 worktree 创建命令计划

本节是命令计划，不代表已经执行。执行前由 Leader 确认当前仓库状态。

### 8.1 是否现在执行

建议：

1. 若当前目录还不是 Git 仓库，先执行 `git init`。
2. 提交当前文档与 Phase 1/2A/2B 冻结基线。
3. 再创建 Phase 2B 各 Agent 独立 worktree。

理由：

- Phase 2B 将创建大量前后端源码，必须有可回滚基线。
- AGENTS.md 要求多 Agent 禁止共享同一工作目录。
- 不应在未提交冻结文档前开始源码重建。

### 8.2 Git 初始化计划

```powershell
git status
git init
git add AGENTS.md PROJECT_CONTEXT.md REPLAN.md PHASE1_MASTER_SUMMARY.md PHASE2A_MASTER_SUMMARY.md PHASE2A_SYSTEM_CONTRACT_REBUILD_PLAN.md PHASE2B_PRE_DEV_FREEZE.md agent_outputs .omx/plans .omx/specs .omx/interviews
git commit -m "Freeze Phase 2B minimal rebuild gates

Constraint: original web-vue and web-flask business source is unrecoverable
Rejected: start rebuilding source before freezing API DB AI file contracts | would create unreviewable assumptions
Confidence: high
Scope-risk: moderate
Directive: do not implement video realtime reports dashboard training or full dataset management in first Phase 2B slice
Tested: document presence and Phase 2A contract review
Not-tested: frontend/backend runtime because business source is intentionally not created yet"
```

### 8.3 Worktree 创建计划

建议分支与目录：

```powershell
git worktree add ../frontend-worktree -b feature/phase2b-frontend-minimal
git worktree add ../backend-worktree -b feature/phase2b-backend-minimal
git worktree add ../ai-worktree -b feature/phase2b-ai-inference-contract
git worktree add ../docs-worktree -b docs/phase2b-gate-smoke
```

### 8.4 Worktree 写入边界

| Worktree | 责任 | 允许写入 | 禁止写入 |
|---|---|---|---|
| `frontend-worktree` | 前端最小 UI | `web-vue/` | `web-flask/`、AI 权重、DB |
| `backend-worktree` | 后端最小 API/DB/文件/推理封装 | `web-flask/` | `web-vue/`、AI 训练脚本、权重 |
| `ai-worktree` | AI 推理契约适配建议 | 文档、必要适配说明 | 训练、验证、替换权重 |
| `docs-worktree` | Gate、测试、验收记录 | 文档 | 业务代码 |

---

## 9. Agent 下一步任务

以下任务为 Phase 2B 开发前的下一步，不等于立即写代码。

### 9.1 Leader / Coordinator

1. 确认 `PHASE2B_PRE_DEV_FREEZE.md` 已写入并成为门禁基线。
2. 检查当前目录是否已有 Git 仓库。
3. 若无 Git 仓库，执行 Git 初始化与基线提交。
4. 创建独立 worktree。
5. 向各 Agent 下发 Phase 2B 首批任务。
6. 保持 scope 不扩张：只做登录、图片检测、模型加载、检测记录保存。

### 9.2 Frontend Agent

前置任务：

1. 读取 `PHASE2B_PRE_DEV_FREEZE.md`。
2. 读取 `agent_outputs/frontend/FRONTEND_PAGE_MAP.md`。
3. 读取 `agent_outputs/backend/API_CONTRACT.md`。
4. 读取 `agent_outputs/backend/DETECTION_RESULT_SCHEMA.md`。
5. 读取 `agent_outputs/backend/FILE_STORAGE_CONTRACT.md`。

开发任务在 Gate 通过后才允许：

1. 重建 Vue3 最小入口。
2. 实现登录页。
3. 实现图片检测页。
4. 实现检测记录列表和详情。
5. 对接模型列表、图片检测、文件访问 API。

禁止：

- 不做视频、实时、Word、大屏、训练、完整数据集管理。
- 不自行修改后端 API 契约。

### 9.3 Backend Agent

前置任务：

1. 读取 `PHASE2B_PRE_DEV_FREEZE.md`。
2. 读取 `API_CONTRACT.md`、`DB_CONTRACT.md`、`DETECTION_RESULT_SCHEMA.md`、`FILE_STORAGE_CONTRACT.md`。
3. 确认最小 DB schema 和 API path 无冲突。

开发任务在 Gate 通过后才允许：

1. 重建 Flask 最小启动入口。
2. 实现 health、auth、model、detection、file routes。
3. 实现 SQLite 初始化脚本。
4. 实现图片上传与结果图存储。
5. 调用 AI Agent 确认的 YOLO 推理封装。
6. 保存 detection_records。

禁止：

- 不做视频检测、实时检测、Word 报告。
- 不修改训练脚本。
- 不替换权重。

### 9.4 AI Agent

前置任务：

1. 读取 `PHASE2B_PRE_DEV_FREEZE.md`。
2. 读取 `AI_OUTPUT_SCHEMA.md` 与 `MODEL_ASSET_BASELINE.md`。
3. 确认 `yolo26n.pt` 作为开发占位模型的限制说明。

开发协作任务在 Gate 通过后才允许：

1. 为 Backend 提供 YOLO 单图推理封装字段核对。
2. 确认 class 映射保持 `0 -> floating_object`。
3. 确认 bbox 输出可转换为 `xyxy_pixel` 和 `xywhn`。
4. 参与检测结果 smoke test 判读。

禁止：

- 不训练。
- 不验证。
- 不预测批量测试集作为性能声明。
- 不替换、移动、删除权重。
- 不修改类别定义。

### 9.5 Docs/Test Agent

前置任务：

1. 将 `PHASE2B_PRE_DEV_FREEZE.md` 纳入契约索引。
2. 修正 `CONTRACT_INDEX.md` 与 `PHASE2B_GATE_CHECKLIST.md` 中“待输出”状态为“已输出 / 待源码实现确认”。
3. 保持 Phase 2B 首批范围清晰。

开发后验证任务：

1. 执行登录冒烟测试。
2. 执行图片检测冒烟测试。
3. 执行检测记录保存和查询冒烟测试。
4. 记录暂缓功能未被误实现。
5. 输出 Phase 2B smoke test report。

---

## 10. Phase 2B 开发前门禁

在任何 Agent 写业务代码前，必须满足：

- [ ] 本文件已由 Leader 确认为 Phase 2B 前置冻结基线。
- [ ] Git 仓库已初始化或确认已存在。
- [ ] 当前文档基线已提交。
- [ ] 独立 worktree 已创建。
- [ ] Frontend / Backend / AI / Docs 写入边界已确认。
- [ ] 最小 API 契约已冻结。
- [ ] 最小 SQLite schema 已冻结。
- [ ] 文件存储路径规范已冻结。
- [ ] YOLO 推理输入/输出已冻结。
- [ ] 默认账号与鉴权策略已冻结。
- [ ] 冒烟测试清单已冻结。
- [ ] Leader 明确下发 Phase 2B 开发启动指令。

当前判定：

```text
Phase 2B Gate: PRE-DEV FROZEN, NOT YET PASS
Reason: minimal rebuild scope is frozen in this document, but git baseline commit and worktree creation have not yet been executed.
Allowed next actions: git status/init/baseline commit/worktree creation, then Agent task dispatch.
Still forbidden: business code, frontend src creation, backend source creation, DB initialization, model training, weight changes.
```

