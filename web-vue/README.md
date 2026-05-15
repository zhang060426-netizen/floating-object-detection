# web-vue Phase 2B Batch1

## 范围

本目录为 Phase 2B Batch1 前端最小可运行重建，仅实现：

- Vue3 + Vite + Element Plus + Pinia + Vue Router 工程入口
- 登录页：提交账号密码，保存 JWT
- 基础布局：图片检测、检测记录导航与退出
- 图片检测页：选择已发布模型、上传单张图片、展示结果图与目标列表
- 检测记录页：列表与详情、原图/结果图、目标列表、原始 JSON

暂不实现视频检测、实时检测、Word 报告、大屏美化、训练/数据集/评估完整 UI；对应入口会提示“Phase 2B 暂不开放”。

## 启动与配置

```powershell
cd E:/MM/floating-worktrees/frontend-worktree/web-vue
npm install
npm run dev
```

构建验证：

```powershell
npm run build
```

环境变量：

- `VITE_API_BASE_URL`：生产/直连 API 地址，默认空字符串，使用当前源下的 `/api`
- `VITE_DEV_PROXY_TARGET`：Vite dev server `/api` 代理目标，默认 `http://localhost:5000`

## 对接的冻结接口

- `POST /api/auth/login`
- `GET /api/auth/me`
- `GET /api/models/published`
- `POST /api/detection/image`
- `GET /api/detection/records`
- `GET /api/detection/records/:id`
- 文件 URL 优先消费后端返回的 `url`；若仅有 `bucket/object_key`，按 `/api/files/:bucket/*object_key` 生成。

统一响应兼容 `code === 0` 与 `code === 200`，消息字段兼容 `message` 与 `msg`。

## 已知限制

- 真实联调依赖后端 Phase 2B 最小 API 可运行。
- 默认登录表单按冻结契约填入 `admin / admin123`；如后端使用其他默认密码，以后端契约为准。
- 无后端时页面应显示清晰错误，不应空白崩溃。
