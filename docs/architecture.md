---
stepsCompleted: [1, 2, 3, 4, 5, 6, 7, 8]
inputDocuments:
  - "docs/prd.md"
  - "docs/product-brief-3d-digital-human-virtual-tryon.md"
  - "CLAUDE.md"
workflowType: 'architecture'
project_name: '3D 数字人虚拟试穿系统'
user_name: '项目负责人'
date: '2026-05-22'
lastStep: 8
status: 'complete'
completedAt: '2026-05-22'
---

# Architecture Decision Document — 3D 数字人虚拟试穿系统

## Project Context Analysis

### Requirements Overview

**Functional Requirements（32 条，8 个能力域）：**

| 能力域 | FR 数 | 架构含义 |
|--------|-------|---------|
| 用户认证 | FR1 | 手机号+验证码，JWT 无状态会话 |
| 数字人管理 | FR2-10 | 照片上传 + LHM 推理 + SMPL-X 参数存储 + CRUD |
| 虚拟试穿 | FR11-15 | 异步 GPU 任务 + 进度推送 + 失败重试 |
| 3D 场景交互 | FR16-20 | WebGL 渲染管线 + 触摸/鼠标双输入 |
| 服装数据 | FR21-22 | 图片上传 + 品类标注 |
| 试穿历史 | FR23-25 | 记录查询 + 对比展示 |
| 私有化部署 | FR26-29 | Docker + JS SDK + 监控 + 多租户 |
| 数据隐私 | FR30-32 | 删除/清除/明示同意 |

**NFR 驱动项：**

| 维度 | 关键需求 | 架构影响 |
|------|---------|---------|
| 性能 | GPU < 5s/< 8s，渲染 ≥ 25/60 FPS | 异步队列、LOD、缓存 |
| 安全 | JWT + 存储加密 + 多租户隔离 | 中间件、MinIO SSE、client_id |
| 扩展 | GPU 水平扩容、结果缓存 | Worker 池、Redis 缓存 |
| 集成 | REST API + JS SDK | API 版本化、SDK 打包 |
| 可靠 | 超时兜底、自动重试、日备份 | 任务状态机、CronJob |

### Scale & Complexity

- 主领域：Web 全栈 + AI 推理管线 + 3D 图形渲染
- 复杂度：中高 — 异步 GPU 任务 + WebGL + 多模态 AI 管线
- 组件估算：6-8 个（SPA、API 网关、AI 推理 ×2、任务队列、存储、监控）

### Technical Constraints

- GPU T4/L4（16GB+ VRAM），客户自有硬件
- 浏览器需 WebGL 2.0（Chrome 90+/Safari 16+）
- LHM 许可待确认（学术），FASHN VTON Apache 2.0
- 私有化部署，非 SaaS 多租户云架构

### Cross-Cutting Concerns

1. **2D→3D 纹理映射**：FASHN（2D）→ SMPL-X（3D）的 UV 映射是关键路径
2. **异步任务流**：所有 AI 操作统一状态机 + WebSocket 推送
3. **多客户隔离**：私有化部署，独立实例，存储和密钥隔离
4. **GPU 资源调度**：队列削峰 + 结果缓存 + 超时处理
5. **渐进交付**：MVP → Growth → Vision，架构需支持增量

## Starter Template Evaluation

### 技术选型与理由

| 层 | 选择 | 理由 |
|---|------|------|
| 前端框架 | React 18 + Vite 5 | 生态最成熟；Vite 5 避坑 Node 24 兼容 |
| 语言 | TypeScript（前端）+ Python 3.11（后端） | 类型安全 + AI 生态 |
| 3D 引擎 | Three.js + LAM_WebRender | 高斯泼溅 WebGL，MIT |
| 后端框架 | FastAPI | 异步 + 自动 OpenAPI + Celery 集成 |
| 任务队列 | Celery + Redis | GPU 异步调度，削峰填谷 |
| 数据库 | PostgreSQL 16 | JSONB 存 SMPL-X，成熟可靠 |
| 对象存储 | MinIO | S3 兼容，私有化部署必备 |
| AI 引擎 | LHM + FASHN VTON | 开源最优，Apache 2.0 |

已在第 0 步手动搭建完成，前后端 build 通过，CI 已配置。

## Core Architectural Decisions

### Data Architecture

| 决策 | 选择 | 理由 |
|------|------|------|
| 数据库 | PostgreSQL 16 | JSONB 存 SMPL-X 参数，成熟生态 |
| ORM | SQLAlchemy 2.0 async | FastAPI 原生支持，迁移用 Alembic |
| 文件存储 | MinIO（S3 兼容） | 私有化部署，无云厂商绑定 |
| 缓存 | Redis | 已用于 Celery broker，复用做结果缓存 |
| 数据迁移 | Alembic | SQLAlchemy 配套，版本化管理 |

### Authentication & Security

| 决策 | 选择 | 说明 |
|------|------|------|
| 认证方式 | 手机号 + 验证码 | 电商场景，无需密码 |
| 会话管理 | JWT（python-jose） | 无状态，多实例友好 |
| 令牌有效期 | 7 天 | 可配置 |
| 密码无关 | 无密码方案 | 降低安全攻击面 |
| 存储加密 | MinIO SSE | 服务端加密照片和模型 |
| 多租户隔离 | `client_id` 数据库级 | 私有化部署，独立实例 |
| API 鉴权 | Bearer Token 中间件 | FastAPI Depends 注入 |

### API & Communication

| 决策 | 选择 | 说明 |
|------|------|------|
| API 风格 | RESTful JSON | 通用，客户对接简单 |
| 实时推送 | WebSocket | AI 任务进度，非轮询 |
| 文档 | OpenAPI 3.0（FastAPI 自动生成） | 零额外维护成本 |
| 错误格式 | `{error: {code, message}}` | 统一结构 |
| SDK 交付 | JS SDK（npm + `<script>`） | 客户嵌入商品页 |
| 超时 | AI 任务 60s | 超时自动标记失败 |

### Frontend Architecture

| 决策 | 选择 | 说明 |
|------|------|------|
| 路由 | React Router v6 | SPA 客户端路由 + 代码分割 |
| 状态管理 | React Context + useReducer | 轻量，无额外依赖 |
| 样式 | CSS Modules | 零运行时，按需加载 |
| 3D 渲染 | Three.js + LAM_WebRender | WebGL 2.0 高斯泼溅 |
| 组件结构 | 按功能分 pages/components/services | 清晰分层 |
| 打包 | Vite（Rollup） | 快速 HMR + Tree Shaking |

### Infrastructure & Deployment

| 决策 | 选择 | 说明 |
|------|------|------|
| 容器化 | Docker Compose | 一键部署（PG+Redis+MinIO+API+Worker） |
| GPU 调度 | Celery + Redis | 异步任务队列，worker 绑定 GPU 节点 |
| CI/CD | GitHub Actions | lint + type check + test |
| 监控 | Celery Flower + 自定义 metrics | GPU 利用率 + 队列长度 + 任务耗时 |
| 备份 | pg_dump cron + MinIO mirror | 每日自动 |
| 水平扩容 | 新增 GPU 节点 → 注册 Celery worker | 自动发现 |

## Implementation Patterns & Consistency Rules

### Naming Conventions

| 层 | 规则 | 示例 |
|----|------|------|
| 数据库表 | snake_case 复数 | `users`, `avatars`, `tryon_tasks` |
| 数据库列 | snake_case | `user_id`, `created_at`, `model_url` |
| API 端点 | kebab-case 复数 | `/api/avatars`, `/api/tryon-tasks` |
| Python 文件 | snake_case | `avatar_service.py`, `task_worker.py` |
| Python 类 | PascalCase | `AvatarService`, `TaskWorker` |
| Python 函数 | snake_case | `create_avatar()`, `get_task_status()` |
| React 组件 | PascalCase | `ModelViewer.tsx`, `AvatarCreate.tsx` |
| CSS Module | 组件名.module.css | `ModelViewer.module.css` |
| TypeScript 接口 | PascalCase | `Avatar`, `TryOnTask`, `ApiResponse<T>` |

### API Response Format

```typescript
// 成功
{ "data": T }

// 错误
{ "error": { "code": "AVATAR_NOT_FOUND", "message": "数字人不存在" } }

// 分页
{ "data": T[], "total": number, "page": number, "pageSize": number }
```

### Error Handling Pattern

```
前端: try/catch → 解析 error.code → 用户提示/重试
后端: HTTPException → 统一 error handler 中间件 → {error: {code, message}}
AI 引擎: 超时 60s → status=failed → 记录 error_detail → 通知前端
```

### Async Task State Machine

```
pending → queued → processing → completed
                              → failed (可重试)
```

WebSocket 事件：`task:progress`（进度百分比）、`task:completed`（结果 URL）、`task:failed`（错误信息）

### Project Structure

```
Shopping-digital-human/
├── docker-compose.yml
├── .env.example
├── .github/workflows/ci.yml
│
├── frontend/                    # React 18 + Vite 5 + Three.js
│   ├── src/
│   │   ├── main.tsx             # entry
│   │   ├── App.tsx              # router
│   │   ├── index.css            # global styles
│   │   ├── components/          # shared: Layout, ModelViewer
│   │   ├── pages/               # route pages: Home, Login, Avatar*, TryOn, History
│   │   ├── services/            # api.ts (API client)
│   │   └── hooks/               # custom hooks
│   ├── public/
│   └── vite.config.ts
│
├── backend/                     # FastAPI + Celery
│   ├── app/
│   │   ├── main.py              # FastAPI app entry
│   │   ├── core/                # config, database, auth, storage
│   │   ├── models/              # SQLAlchemy models (User, Avatar, Garment, TryOnTask)
│   │   ├── api/                 # route handlers (auth, avatars, tryon, garments, upload)
│   │   ├── services/            # business logic (avatar_service, tryon_service)
│   │   ├── tasks/               # Celery tasks + workers
│   │   └── schemas/             # Pydantic request/response schemas
│   ├── tests/
│   ├── alembic/                 # DB migrations
│   └── pyproject.toml
│
├── ai-engine/
│   ├── lhm/server.py            # LHM avatar generation microservice (port 8001)
│   └── fashn-vton/server.py     # FASHN VTON try-on microservice (port 8002)
│
└── docs/                        # PRD, Architecture, etc.
```

### Requirements to Structure Mapping

| FR 域 | 前端 | 后端 API | AI 引擎 | 存储 |
|--------|------|---------|---------|------|
| 认证 | Login.tsx | api/auth/ | — | users |
| 数字人 | Avatar*.tsx | api/avatars/ | LHM | avatars + MinIO |
| 试穿 | TryOn.tsx | api/tryon/ | FASHN VTON | tryon_tasks |
| 3D 交互 | ModelViewer.tsx | — | — | — |
| 服装 | — | api/garments/ | — | garments |
| 历史 | History.tsx | api/tryon/ | — | tryon_tasks |
| 部署 | — | — | — | docker-compose |
| 隐私 | 删除按钮 | api/avatars/ DELETE | — | cascade delete |

## Architecture Validation Results

### Coherence Validation

- 所有技术栈版本兼容：React 18 + Vite 5 + FastAPI + PostgreSQL 16 + Redis 7
- FastAPI 异步 + Celery 异步任务队列天然匹配
- Three.js + LAM_WebRender 共享 WebGL 2.0 上下文
- JWT 无状态适合私有化部署多实例场景

### Requirements Coverage

- 32 条 FR 全部有对应的前端/后端/AI 组件映射
- NFR 性能指标在架构层有对应策略（队列削峰、结果缓存、LOD）
- 安全需求：JWT + MinIO SSE + client_id 隔离三层覆盖
- 渐进交付：MVP 功能集中在 frontend/ + backend/ + ai-engine/，Growth/Vision 追加不推翻

### Implementation Readiness

- 脚手架已完成，前后端 build 通过
- 数据模型已定义（SQLAlchemy models）
- API 端点已规划（8 个路由模块）
- AI 引擎 stub 已就绪
- CI pipeline 已配置

### Architecture Completeness Checklist

**Requirements Analysis**
- [x] Project context thoroughly analyzed
- [x] Scale and complexity assessed
- [x] Technical constraints identified
- [x] Cross-cutting concerns mapped

**Architectural Decisions**
- [x] Critical decisions documented with versions
- [x] Technology stack fully specified
- [x] Integration patterns defined
- [x] Performance considerations addressed

**Implementation Patterns**
- [x] Naming conventions established
- [x] Structure patterns defined
- [x] Communication patterns specified
- [x] Process patterns documented

**Project Structure**
- [x] Complete directory structure defined
- [x] Component boundaries established
- [x] Integration points mapped
- [x] Requirements to structure mapping complete

### Architecture Readiness Assessment

**Overall Status:** READY FOR IMPLEMENTATION

**Key Strengths:**
- 技术选型聚焦开源、低成本、私有化部署
- 架构分层清晰（前端→API→AI引擎→存储），边界明确
- 渐进交付设计——MVP 即可卖，Growth/Vision 叠加不重构
- AI 任务异步化，GPU 资源可弹性扩容

**Areas for Future Enhancement:**
- GPU 监控和自动扩缩容（v1 手动即可）
- 模型版本管理和 A/B 测试框架
- 多语言 i18n 基础设施
