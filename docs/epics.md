---
stepsCompleted: []
inputDocuments:
  - "docs/prd.md"
  - "docs/architecture.md"
---

# 3D 数字人虚拟试穿系统 - Epic Breakdown

## Overview

本文档将 PRD、Architecture 中的需求分解为可执行的 Epic 和 Story。

## Requirements Inventory

### Functional Requirements

**用户认证**
- FR1: 用户可使用手机号和验证码登录

**数字人管理**
- FR2: 用户可上传全身正面照片创建 3D 数字人
- FR3: 系统自动分析照片质量并对不合格照片给出具体提示
- FR4: 用户创建数字人时可看到实时进度
- FR5: 用户可查看所有已创建的数字人列表
- FR6: 用户可查看单个数字人的 3D 模型详情
- FR7: 用户可手动调节数字人体型参数（身高/体重/肩宽/胸围/腰围/臀围/腿长）
- FR8: 调整参数后可实时预览数字人体型变化
- FR9: 用户可删除自己的数字人
- FR10: 每个用户最多创建 3 个数字人

**虚拟试穿**
- FR11: 用户可在商品详情页发起虚拟试穿
- FR12: 无数字人用户发起试穿时系统引导先创建
- FR13: 用户选择已有数字人后发起试穿，系统显示处理进度
- FR14: 用户可查看试穿完成的 3D 效果（数字人穿着服装）
- FR15: 试穿超时或失败时通知用户并允许重试

**3D 场景交互**
- FR16: 用户可 360° 旋转查看数字人
- FR17: 用户可缩放（拉近/拉远）查看
- FR18: 桌面端支持鼠标操作，移动端支持触摸手势
- FR19: 3D 场景自适应容器尺寸
- FR20: 试穿模式下可并排对比"素体"和"试穿效果"

**服装数据**
- FR21: 平台管理员可上传服装图片并标注品类
- FR22: 卖家可用预设数字人批量验证服装试穿效果

**试穿历史**
- FR23: 用户可查看试穿历史记录
- FR24: 用户可对多次试穿结果进行并排对比
- FR25: 用户可从试穿历史跳转到对应商品页

**私有化部署**
- FR26: 客户可通过部署脚本在自有 GPU 服务器完成部署
- FR27: 客户可将试穿 JS SDK 嵌入电商平台前端
- FR28: 客户可通过管理控制台查看系统运行状态
- FR29: 系统支持多客户环境数据隔离

**数据隐私**
- FR30: 用户可随时删除自己的照片和 3D 模型数据
- FR31: 数据删除时同步清除关联存储文件和数据库记录
- FR32: 用户首次创建数字人时需明示同意数据收集条款

### NonFunctional Requirements

**性能**
- NFR1: 数字人生成 P95 < 5 秒
- NFR2: 试穿效果生成 P95 < 8 秒
- NFR3: 桌面端 3D 渲染 ≥ 60 FPS
- NFR4: 手机端 3D 渲染 ≥ 25 FPS（中端机）
- NFR5: API 响应（非 AI）P95 < 200ms
- NFR6: 页面首屏加载 < 2s（桌面）/ < 3s（4G）

**安全**
- NFR7: 用户照片和 3D 模型存储加密（MinIO SSE）
- NFR8: JWT 令牌 7 天有效期，可主动失效
- NFR9: 多客户数据按 client_id 隔离
- NFR10: JS SDK 仅暴露公共接口

**可扩展性**
- NFR11: 单 T4 GPU 支持 ≥ 4 并发 AI 任务
- NFR12: GPU 队列峰值排队 ≤ 30 秒
- NFR13: 水平扩容新增 GPU 节点自动注册
- NFR14: 试穿结果缓存（同用户+同服装 24h 复用）

**无障碍**
- NFR15: 标准 UI 达到 WCAG 2.1 AA

**可靠性**
- NFR16: AI 任务超时 60 秒自动失败
- NFR17: 失败任务支持一键重试
- NFR18: GPU 服务冷启动恢复 < 30 秒
- NFR19: 数据库每日自动备份

### Additional Requirements (from Architecture)

- AR1: 项目脚手架已搭建（Vite + React 18 + FastAPI + Docker Compose + CI），作为 Epic 0 已完成
- AR2: Celery + Redis 异步任务队列用于 AI 推理调度
- AR3: WebSocket 实时推送任务进度（非轮询）
- AR4: 统一 API 错误格式 `{error: {code, message}}`
- AR5: 数据库命名：snake_case 复数表名
- AR6: Alembic 管理数据库迁移
- AR7: 前端 CSS Modules 样式隔离
- AR8: Three.js GLTFLoader 加载 3D 模型，OrbitControls 交互
- AR9: AI 引擎独立微服务（LHM :8001, FASHN VTON :8002）
- AR10: 任务状态机：pending → queued → processing → completed/failed

### UX Design Requirements

无独立 UX Design 文档。UX 需求由 PRD 用户旅程和 Web App 要求推导。

### FR Coverage Map

{{requirements_coverage_map}}

## Epic List

{{epics_list}}
