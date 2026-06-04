# HealthGuard-Multimodal-RAG-Eval

## 项目简介

A lightweight research prototype for multimodal abnormal event understanding and RAG-based trustworthy QA evaluation in health monitoring scenarios.
面向健康监护场景的多模态异常事件理解与可信问答评测原型系统。

本项目面向居家养老与远程健康监护场景，围绕跌倒、长时间静止、异常徘徊、遮挡误判等典型异常事件，构建一个轻量级的多模态异常事件理解与可信问答评测原型系统。

项目基于国家级大创“中云智护”的应用背景，当前重点聚焦算法侧预研，不依赖深度相机、激光雷达或机器人实物硬件，主要通过公开图像/视频样例、模拟事件数据和健康监护知识库完成多模态理解、RAG 问答与评测流程验证。

## 研究问题

1. 传统行为识别模型通常只能输出“是否异常”，如何进一步生成可解释的异常事件描述？
2. 多模态大模型在健康监护场景下是否容易产生错误解释、误报分析不足或不可靠建议？
3. RAG / GraphRAG 思路能否提升健康监护建议的可追溯性、可信度与场景一致性？
4. 如何构建一个轻量级评测流程，对比传统识别模型、纯 VLM、VLM + RAG、VLM + GraphRAG 的差异？

## 技术路线

### 1. 异常事件建模

围绕健康监护场景中的典型异常事件构建小规模样本，包括：

* 跌倒事件
* 长时间静止
* 异常徘徊
* 遮挡误判
* 弱光误判
* 正常活动场景

每条样本包含异常类型、风险等级、视觉/行为证据、可能误报原因与建议处理方式等字段。

### 2. 多模态异常事件理解

引入 Qwen-VL / VideoLLaMA 等多模态大模型，对图像、视频样例或模拟事件描述进行语义理解，输出结构化异常分析结果：

* 是否异常
* 异常类型
* 风险等级
* 视觉/行为证据
* 可能误报原因
* 建议处理方式

### 3. 健康监护知识增强问答

构建轻量级健康监护知识库，覆盖跌倒处理、长时间静止判断、异常徘徊风险、遮挡误判、弱光场景、海外部署与隐私合规等内容。

基于 RAG / GraphRAG 思路，将模型回答与知识库内容进行关联，探索提升回答可追溯性、降低大模型幻觉与增强场景可信度的方法。

### 4. 评测与误差分析

从以下维度对不同方法进行对比：

* 异常判断准确性
* 解释一致性
* 回答可追溯性
* 风险等级判断合理性
* 误报原因分析能力
* 推理延迟与实现成本

对比方法包括：

* ST-GCN / SVM baseline
* 纯多模态大模型
* VLM + 向量 RAG
* VLM + GraphRAG

## 项目结构

```text
HealthGuard-Multimodal-RAG-Eval/
├── README.md
├── data/
│   ├── samples.json
│   └── health_monitoring_knowledge.md
├── docs/
│   ├── research_plan.md
│   ├── system_architecture.md
│   └── error_analysis.md
├── src/
│   ├── prompt_templates.py
│   ├── vlm_inference.py
│   ├── rag_pipeline.py
│   └── evaluator.py
├── results/
│   └── ablation_plan.md
└── requirements.txt
```

## 当前进度

* [x] 完成项目选题与任务定义
* [x] 完成小规模样本字段设计
* [x] 完成健康监护知识库初版
* [x] 完成 README 与项目结构规划
* [ ] 完成 VLM 输出格式化
* [ ] 完成 RAG 检索模块
* [ ] 完成评测脚本与初步实验表格
* [ ] 完成误差分析报告
* [ ] 完成技术报告初版

## 项目关键词

Multimodal Large Language Model, Vision-Language Model, Retrieval-Augmented Generation, GraphRAG, LLM Evaluation, Health Monitoring, Abnormal Event Understanding, Trustworthy QA

## 项目定位

本项目不是完整硬件系统部署项目，而是基于健康监护应用场景的算法侧预研原型。项目重点关注多模态大模型、RAG 知识增强与垂直场景评测方法在异常事件理解任务中的结合，为后续真实设备接入、端云协同部署与智能健康监护系统优化提供算法验证基础。
