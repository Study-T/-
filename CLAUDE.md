# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

3D 虚拟试衣数字人系统 — 用户上传衣服照片，AI 提取服装特征映射到 3D 数字人上，浏览器实时查看试穿效果。解决电商买衣无法真实感知上身效果导致退货率高的问题。

## 技术架构

系统分三大核心模块 + 协调层：

- **3D 数字人生成** — 上传照片自动生成（首选 LHM）或手动调参
- **虚拟试穿** — AI 将服装穿到数字人上（首选 FASHN VTON），360°查看
- **动画 & 场景** — Mixamo 骨骼动画 + 多场景切换
- **协调 Agent** — Agent 间任务调度、结果校验、异常回退

## 技术栈

| 层 | 方案 |
|---|------|
| 前端 | React 18 + TypeScript + Three.js (WebGL 2.0) |
| 后端 | FastAPI + Celery + Redis |
| 数据库 | PostgreSQL 16 + MinIO/S3 |
| AI 引擎 | LHM（数字人生成）、FASHN VTON v1.5（虚拟试穿） |
| Web 3D 渲染 | LAM_WebRender (MIT) — 高斯泼溅，手机端 120FPS |
| 人体模型 | SMPL-X |
| 布料物理 | drape (MIT) — Three.js 实时仿真 |
| GPU | NVIDIA T4/L4 (16-24GB VRAM) |

## 关键开源依赖

| 用途 | 方案 | 许可证 | 要点 |
|------|------|--------|------|
| 数字人生成 | LHM (阿里) | 开源 | ICCV 2025，单照片→SMPL-X全身模型 |
| 虚拟试穿 | FASHN VTON v1.5 | Apache 2.0 | 8GB显存，mask-free |
| Web 3D | LAM_WebRender | MIT | NPM 包，WebGL 高斯泼溅 |

## 知识库

项目相关技术调研和决策记录在 `~/Desktop/知识库/wiki/`，关键页面：
- `concepts/3d-digital-human-virtual-tryon.md` — 产品方案与架构
- `concepts/lhm-avatar-generation.md` — LHM 选型依据
- `concepts/fashn-vton.md` — 虚拟试穿引擎
- `concepts/lam-webrender.md` — Web 3D 渲染方案

## 开发约定

- 语言：中文沟通，代码命名和注释用英文
- 后端 Python，前端 TypeScript
- 不引入不必要的依赖和抽象
