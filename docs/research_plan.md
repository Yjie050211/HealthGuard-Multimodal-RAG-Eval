# Research Plan

## 1. Background

健康监护系统不仅需要识别异常行为，还需要解释异常原因、判断风险等级，并给出可追溯的处理建议。传统行为识别模型通常侧重分类结果，而多模态大模型具备更强的语义解释能力，但也可能产生幻觉或过度判断。

## 2. Research Questions

1. 多模态大模型是否能够在健康监护场景中生成稳定的异常事件解释？
2. RAG 是否能够提升健康监护建议的可追溯性？
3. 传统分类模型、纯 VLM、VLM + RAG 在异常判断和解释一致性上有何差异？
4. 如何通过误差分析发现模型在遮挡、弱光、多人与不确定场景下的局限？

## 3. Method

- 构建小规模健康监护异常事件样本集。
- 设计结构化标注字段。
- 调用 VLM / LLM API 生成异常事件分析结果。
- 构建健康监护知识库并实现轻量级 RAG。
- 设计评测指标和误差分析流程。

## 4. Evaluation Metrics

- Abnormal Detection Accuracy
- Event Type Accuracy
- Risk Level Accuracy
- Explanation Consistency
- Knowledge Traceability
- Parse Error Count
- Inference Latency

## 5. Expected Outcome

本项目目标不是训练大模型，而是构建一个可复现、可解释、可扩展的算法侧评测原型，为健康监护场景下多模态大模型与 RAG 的结合提供初步实验依据。
