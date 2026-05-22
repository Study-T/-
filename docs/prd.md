---
stepsCompleted: ["step-01-init", "step-02-discovery", "step-02b-vision", "step-02c-executive-summary"]
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
