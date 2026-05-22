---
stepsCompleted: ["step-01-init", "step-02-discovery", "step-02b-vision", "step-02c-executive-summary", "step-03-success", "step-04-journeys", "step-05-domain", "step-06-innovation", "step-07-project-type", "step-08-scoping", "step-09-functional", "step-10-nonfunctional", "step-11-polish"]
classification:
  projectType: "web_app"
  domain: "ecommerce"
  complexity: "medium"
  projectContext: "greenfield"
releaseMode: "phased"
inputDocuments:
  - "docs/product-brief-3d-digital-human-virtual-tryon.md"
  - "知识库/wiki/sources/3d-virtual-tryon-tech-research.md"
  - "知识库/wiki/concepts/3d-digital-human-virtual-tryon.md"
  - "知识库/wiki/concepts/lhm-avatar-generation.md"
  - "知识库/wiki/concepts/fashn-vton.md"
  - "知识库/wiki/concepts/lam-webrender.md"
  - "知识库/wiki/concepts/smpl-x.md"
  - "CLAUDE.md"
  - "README.md"
workflowType: 'prd'
---

# Product Requirements Document — 3D 数字人虚拟试穿系统

**Author:** 项目负责人
**Date:** 2026-05-22

## Executive Summary

3D 数字人虚拟试穿系统是一套可交付的 Web 应用，面向国内及跨境电商平台、品牌直营客户。用户上传一张照片即可生成 3D 数字分身（SMPL-X 参数化模型），在浏览器中实时试穿服装和鞋子，360° 旋转查看上身效果。系统以项目形式一次性交付，支持客户私有化部署，源码可定制。

线上服装退货率 19.3%（跨境部分品类超 40%），"不合身/效果不符"是首要退货原因。Google（2026.4）、Shopify、Zara 已上线虚拟试穿，赛道正从实验品变为竞争必需品。市面方案要么 SaaS 按次收费，要么闭源黑盒无法定制——"私有化 + 买断 + 可定制"是明确的市场空白。

### What Makes This Special

- **交付模式**：一次性项目交付 + 私有化部署，客户拥有完整源码，不依赖外部 API 订阅
- **技术路线**：基于开源 AI 模型改造优化，不绑特定厂商
- **核心壁垒**：2D 试穿结果→3D 模型的 UV 纹理映射是工程核心难点——把 LHM + FASHN VTON + LAM_WebRender 打通、优化、产品化的经验，竞品不易快速复制
- **品类覆盖**：男女皆适配，上装+下装+鞋子

## Project Classification

| 维度 | 分类 |
|------|------|
| 项目类型 | Web App（React 18 SPA + Three.js） |
| 领域 | 电商 B2B 工具 |
| 复杂度 | 中等偏高（AI 推理管线 + 3D 图形 + 2D→3D 纹理映射） |
| 性质 | Greenfield（全新构建） |

### 技术栈

| 层 | 方案 | 许可 |
|---|------|------|
| 前端 | React 18 + TypeScript + Three.js + LAM_WebRender | MIT |
| 后端 | FastAPI + Celery + Redis | MIT/BSD |
| 数据库 | PostgreSQL 16 + MinIO/S3 | PostgreSQL/MIT |
| 数字人生成 | LHM（阿里，ICCV 2025），备选 GUAVA | 待确认商用 |
| 虚拟试穿 | FASHN VTON v1.5，备选 OOTDiffusion | Apache 2.0 |
| 人体模型 | SMPL-X | 学术许可 |
| GPU | NVIDIA T4/L4（16-24GB VRAM） | — |

## Success Criteria

### User Success

- 用户拍照上传后 5 秒内看到 3D 数字人，≥ 95% 满意度（>= 4/5）
- 试穿后能明确判断"买"或"不买"，bracketing 行为减少
- 新用户首次试穿完成率 > 85%

### Business Success

| 指标 | 目标 | 时间 |
|------|------|------|
| 付费客户数 | 3-5 个 | 首年 |
| 客户平台退货率降低 | ≥ 3 个百分点 | 交付后 3 个月 |
| 试穿→加购转化率 | ≥ 15% | — |
| 客户续约/扩展采购率 | ≥ 50% | 次年 |

### Technical Success

| 指标 | 目标 |
|------|------|
| 数字人生成耗时 | < 5 秒（P95） |
| 试穿效果生成耗时 | < 8 秒（P95） |
| 桌面端 3D 渲染帧率 | ≥ 60 FPS |
| 手机端 3D 渲染帧率 | ≥ 25 FPS（中端机） |
| GPU 并发任务数 | ≥ 4 并发不 OOM（T4） |
| 单次试穿 GPU 成本 | < ¥0.10（实测后校准） |
| 3D 模型首屏加载 | < 3 秒（4G 网络） |

## User Journeys

### Journey 1: 终端消费者 — 首次试穿

**小王**，28 岁，女生，经常网购但退货率高。逛某电商 App 看中一件风衣。

| 阶段 | 行为 | 情感 |
|------|------|------|
| 发现 | 商品详情页看到"3D 试穿"按钮 | 好奇 + 不确定 |
| 创建 | 拍正面全身照上传，5 秒后看到 3D 数字分身 | "这挺像我！" |
| 试穿 | 点"试穿这件"，8 秒后数字人穿上风衣，360° 旋转查看 | "版型还行，袖子有点长" |
| 决策 | 满意，加入购物车 | 确定，不纠结 |

**异常路径**：照片质量差→提示重拍→重新生成；AI 超时→排队提示→完成后通知

### Journey 2: 终端消费者 — 已有数字人重复试穿

**小李**，老用户。商品页点"试穿"直接加载已有数字人。8 秒后试穿效果出来。在试穿历史里并排对比 3 件卫衣效果，选最合适的一件下单。

### Journey 3: 平台管理员 — 部署与运维

**张工**，平台技术负责人。采购后通过 `docker compose up` 部署，30 分钟跑通。2 天完成 JS SDK 前端对接。日常监控 GPU 利用率、任务耗时 P95。队列堆积时水平扩容恢复。

### Journey 4: 卖家/品牌 — 新品试穿验证

**陈老板**，跨境品牌。上新前用预设数字人（不同体型）验证试穿效果，确认不穿模、纹理清晰后关联 SKU 上架。

### Journey Requirements Summary

| 旅程 | 需要的核心能力 |
|------|-------------|
| J1 首次试穿 | 照片上传 + LHM 生成 + 进度推送 + 失败重试引导 |
| J2 复用试穿 | 数字人持久化 + 试穿历史 + 对比查看 |
| J3 部署运维 | Docker 部署 + API 文档 + JS SDK + 监控看板 + 水平扩容 |
| J4 卖家验证 | 服装上传 + 多数字人批量试穿 + 效果审核 |

## Domain-Specific Requirements

### 隐私与合规

- 用户照片和 3D 模型视为生物特征数据，需明示同意收集、提供删除入口
- 私有化部署模式下数据存于客户服务器，符合《个人信息保护法》数据本地化要求
- 面向欧洲客户需支持 GDPR，加州客户需支持 CCPA
- v1 前确认 LHM、FASHN VTON 商用许可，必要时准备 Apache 2.0 / MIT 替代方案

### 技术约束

- GPU 兼容性：客户环境 GPU 型号可能不同（T4/L4/A10），需兼容主流 CUDA 版本
- JS SDK 安全：嵌入客户电商页面，防御 XSS/CSRF，不暴露后端内网 API
- API 通用性：保持 RESTful + JSON，轻量集成

### 风险与缓解

| 风险 | 缓解 |
|------|------|
| 开源模型许可有变 | GUAVA + OOTDiffusion 备用 |
| 客户数据隔离 | 多租户按 `client_id` 隔离 + 密钥 |
| 客户法务审计 | 提供开源依赖清单 + 许可说明文档 |

## Innovation & Novel Patterns

### 创新点

1. **2D→3D 纹理闭环**：FASHN VTON 输出 2D 试穿图，通过 UV 纹理映射回到 SMPL-X 3D 模型实现 360° 查看。市面方案几乎全是 2D 效果图，无完整 3D 闭环
2. **开源管线整合**：LHM + FASHN VTON + LAM_WebRender 三者独立存在，打通需要解决格式兼容（3DGS↔网格↔2D）、推理调度、结果后处理，工程经验构成壁垒
3. **Web 端实时高斯泼溅**：浏览器跑通 3DGS 并保持可用帧率

### 验证方式

- 纹理映射质量 SSIM ≥ 0.85（原始服装图 vs 3D 试穿结果）
- 20 人盲测"2D 效果图 vs 3D 旋转"，3D 偏好率 > 70%

### 风险与降级

| 风险 | 降级方案 |
|------|---------|
| 2D→3D 纹理映射效果不达标 | v1 同时提供 2D 效果图 + 3D 素体 |
| LAM_WebRender 手机端性能差 | 降级到传统 Three.js Mesh + 低面模型 |

## Web App Specific Requirements

### 技术架构

- SPA（React 18 + React Router），代码分割（React.lazy）
- WebSocket 推送 AI 任务进度，避免轮询
- Three.js WebGL 2.0 + LAM_WebRender 高斯泼溅渲染

### 浏览器支持

| 浏览器 | 最低版本 | 原因 |
|--------|---------|------|
| Chrome | 90+ | WebGL 2.0 + WebSocket |
| Safari | 16+ | WebGL 2.0（iOS 16+） |
| Edge | 90+ | 同 Chromium |

### 响应式

- 移动端优先：底部 TabBar，触摸手势（单指旋转、双指缩放/平移）
- 桌面端：更大 Canvas + 侧面板，键盘快捷键
- 断点：375px / 768px / 1024px

### 无障碍

- 标准 UI 组件 WCAG 2.1 AA；文字对比度 ≥ 4.5:1
- 3D 查看器提供键盘替代操作（方向键/+/-），本身作为可访问性例外

## Project Scoping & Phased Development

### Phase 1: MVP — 上线就卖

**支持的旅程**：J1 + J2 + J3

| 功能 | 优先级 |
|------|--------|
| 照片→3D 数字人生成（LHM） | 必须 |
| 手动参数微调（7 个滑块） | 必须 |
| 上装 + 下装虚拟试穿（FASHN VTON） | 必须 |
| 360° 旋转 + 缩放 | 必须 |
| WebSocket 进度推送 | 必须 |
| 私有化部署脚本 + 文档 | 必须 |
| 手机号登录 + 试穿历史 | 必须 |
| 异常路径兜底（上传失败/超时/重试） | 必须 |
| 2D 试穿效果图（纹理映射降级路径） | 应该 |

### Phase 2: Growth — 增强竞争力

- 鞋子试穿
- 骨骼动画（4 个）+ 场景切换（5 个）+ drape 布料物理
- 卖家试穿验证（多数字人批量）
- 多语言 UI（中/英）
- GPU 成本优化（量化 + 结果缓存）
- 客户定制化适配（品牌色/UI）

### Phase 3: Vision — 护城河

- 直播实时试穿（抖音/快手集成）
- AI 尺码推荐（跨国家/地区对照）
- 社交试穿分享（图片/短视频）
- 配饰试穿 + 走秀视频
- 开源基础版 + 数据飞轮

## Functional Requirements

### 用户认证

- FR1: 用户可使用手机号和验证码登录

### 数字人管理

- FR2: 用户可上传全身正面照片创建 3D 数字人
- FR3: 系统自动分析照片质量并对不合格照片给出具体提示
- FR4: 用户创建数字人时可看到实时进度
- FR5: 用户可查看所有已创建的数字人列表
- FR6: 用户可查看单个数字人的 3D 模型详情
- FR7: 用户可手动调节数字人体型参数（身高/体重/肩宽/胸围/腰围/臀围/腿长）
- FR8: 调整参数后可实时预览数字人体型变化
- FR9: 用户可删除自己的数字人
- FR10: 每个用户最多创建 3 个数字人

### 虚拟试穿

- FR11: 用户可在商品详情页发起虚拟试穿
- FR12: 无数字人用户发起试穿时系统引导先创建
- FR13: 用户选择已有数字人后发起试穿，系统显示处理进度
- FR14: 用户可查看试穿完成的 3D 效果（数字人穿着服装）
- FR15: 试穿超时或失败时通知用户并允许重试

### 3D 场景交互

- FR16: 用户可 360° 旋转查看数字人
- FR17: 用户可缩放（拉近/拉远）查看
- FR18: 桌面端支持鼠标操作，移动端支持触摸手势
- FR19: 3D 场景自适应容器尺寸
- FR20: 试穿模式下可并排对比"素体"和"试穿效果"

### 服装数据

- FR21: 平台管理员可上传服装图片并标注品类
- FR22: 卖家可用预设数字人批量验证服装试穿效果

### 试穿历史

- FR23: 用户可查看试穿历史记录
- FR24: 用户可对多次试穿结果进行并排对比
- FR25: 用户可从试穿历史跳转到对应商品页

### 私有化部署

- FR26: 客户可通过部署脚本在自有 GPU 服务器完成部署
- FR27: 客户可将试穿 JS SDK 嵌入电商平台前端
- FR28: 客户可通过管理控制台查看系统运行状态（GPU 利用率/任务队列）
- FR29: 系统支持多客户环境数据隔离

### 数据隐私

- FR30: 用户可随时删除自己的照片和 3D 模型数据
- FR31: 数据删除时同步清除关联存储文件和数据库记录
- FR32: 用户首次创建数字人时需明示同意数据收集条款

## Non-Functional Requirements

### Performance

| 指标 | 目标 | 测量 |
|------|------|------|
| 数字人生成 | P95 < 5 秒 | GPU 推理计时 |
| 试穿效果生成 | P95 < 8 秒 | GPU 推理计时 |
| 3D 渲染帧率（桌面） | ≥ 60 FPS | DevTools FPS meter |
| 3D 渲染帧率（移动端） | ≥ 25 FPS | 中端机真机测试 |
| 页面首屏加载 | < 2s（桌面）/ < 3s（4G） | Lighthouse |
| API 响应（非 AI） | P95 < 200ms | 后端打点 |

### Security

- 用户照片和 3D 模型存储加密（MinIO SSE）
- JWT 令牌有效期 7 天，可主动失效
- 多客户数据按 `client_id` 隔离
- JS SDK 仅暴露公共接口
- 敏感操作（删除数字人、导出数据）需二次确认

### Scalability

- 单 T4 GPU（16GB）支持 ≥ 4 并发 AI 任务
- GPU 队列削峰填谷，峰值排队 ≤ 30 秒
- 水平扩容：新增 GPU 节点自动注册 Celery worker
- 试穿结果缓存：同一用户+同一服装 24 小时内复用

### Accessibility

- 标准 UI 达到 WCAG 2.1 AA
- 文字对比度 ≥ 4.5:1，大文本 ≥ 3:1
- 3D 查看器提供键盘替代操作

### Integration

- RESTful JSON API + OpenAPI 3.0 文档
- 前端 JS SDK（`<script>` 或 npm）
- SDK 支持客户品牌色和 UI 主题配置
- Docker Compose 一键部署所有依赖

### Reliability

- AI 任务超时 60 秒自动失败
- 失败任务支持一键重试
- GPU 服务重启后自动加载模型，冷启动恢复 < 30 秒
- 数据库每日自动备份
