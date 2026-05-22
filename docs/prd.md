---
stepsCompleted: ["step-01-init", "step-02-discovery", "step-02b-vision", "step-02c-executive-summary", "step-03-success"]
classification:
  projectType: "web_app"
  domain: "ecommerce"
  complexity: "medium"
  projectContext: "greenfield"
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

# Product Requirements Document - 3D 数字人虚拟试穿系统

**Author:** 项目负责人
**Date:** 2026-05-22

## Executive Summary

3D 数字人虚拟试穿系统是一套可交付的 Web 应用，面向国内及跨境电商平台、品牌直营客户。用户上传单张照片即可生成 3D 数字分身（SMPL-X 参数化模型），在浏览器中实时试穿服装和鞋子，360° 旋转查看上身效果。系统以项目形式一次性交付，支持客户私有化部署，源码可定制。

核心驱动力：线上服装退货率 19.3%（跨境部分品类超 40%），"不合身/效果不符"是首要退货原因。Google（2026.4）、Shopify、Zara 已上线虚拟试穿，赛道正从实验品变为竞争必需品。市面方案要么 SaaS 按次收费（长期成本不可控），要么闭源黑盒无法定制——"私有化 + 买断 + 可定制"是明确的市场空白。

目标用户是平台上的消费者（20-40 岁男女），解决了网购时无法感知"穿在自己身上什么样"的核心决策盲区。卖家端则可通过统一数字人展示多款商品，降低模特拍摄成本。

### What Makes This Special

- **交付模式**：一次性项目交付 + 私有化部署，客户拥有完整源码和试穿能力，不依赖外部 API 订阅
- **技术路线**：基于开源 AI 模型（LHM、FASHN VTON）改造优化，不绑特定厂商，不堆自研算法的资源消耗
- **核心壁垒**：2D 试穿结果→3D 模型的 UV 纹理映射是工程核心难点——把 LHM+FASHN VTON+LAM_WebRender 打通、优化、产品化的经验，竞品不易快速复制
- **品类覆盖**：男女皆适配，上装+下装+鞋子，不是单一女装上衣
- **渲染质量**：Web 3D 高斯泼溅渲染（LAM_WebRender），浏览器即开即用，移动端可用

## Project Classification

| 维度 | 分类 |
|------|------|
| 项目类型 | Web App（React 18 SPA + Three.js） |
| 领域 | 电商 B2B 工具 |
| 复杂度 | 中等偏高（AI 推理管线 + 3D 图形 + 2D→3D 纹理映射） |
| 性质 | Greenfield（全新构建，脚手架已完成） |

## 技术栈

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

- **数字人创建"爽点"**：用户拍照上传后 5 秒内看到自己 3D 数字人，95% 的人觉得"像我"（>= 4/5 满意度）
- **试穿决策"解忧"**：看到试穿效果后能明确判断"买"或"不买"，不再需要买多件退多件
- **首次完成率**：新用户从打开试穿到第一次看到效果，完成率 > 85%

### Business Success

| 指标 | 目标 | 时间 |
|------|------|------|
| 付费客户数 | 3-5 个 | 首年 |
| 客户平台退货率降低 | ≥ 3 个百分点 | 交付后 3 个月 |
| 终端用户试穿→加购转化率 | ≥ 15% | — |
| 客户续约/扩展采购率 | ≥ 50% | 次年 |

### Technical Success

| 指标 | 目标 |
|------|------|
| 数字人生成耗时 | < 5 秒（P95） |
| 试穿效果生成耗时 | < 8 秒（P95） |
| 手机端 3D 渲染帧率 | ≥ 25 FPS（中端机） |
| 桌面端 3D 渲染帧率 | ≥ 60 FPS |
| GPU 并发任务数 | ≥ 4 并发不 OOM（T4） |
| 单次试穿 GPU 成本 | < ¥0.10（T4/L4 实测后校准） |
| 3D 模型首屏加载 | < 3 秒（4G 网络） |

### Measurable Outcomes

- v1 交付后 3 个月内，至少 1 个客户平台试穿功能上线并有真实用户数据
- 终端用户试穿使用率（详情页→试穿点击率）> 5%

## Product Scope

### MVP — 上线就卖

- 照片→3D 数字人生成（LHM）
- 手动参数微调（7 个滑块）
- 上装 + 下装虚拟试穿（FASHN VTON）
- 360° 旋转 + 缩放查看
- 私有化部署脚本 + 部署文档
- 手机号登录 + 试穿历史

### Growth — 提升竞争力

- 鞋子试穿
- 4 个骨骼动画 + 5 个场景切换
- 多语言 UI 国际化
- GPU 成本优化（量化、多任务并发）
- 客户定制化适配（品牌色、UI 定制）

### Vision — 护城河

- 直播实时试穿（抖音/快手集成）
- AI 尺码推荐（跨国家/地区尺码对照）
- 社交试穿分享（图片/短视频）
- 配饰试穿 + 商品走秀视频
- 开源基础版 + 数据飞轮（脱敏试穿数据反哺）
