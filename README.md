# HealthGuard-Multimodal-RAG-Eval

面向健康监护场景的多模态异常事件理解与可信问答评测原型系统
A lightweight prototype for multimodal abnormal event understanding and RAG-based trustworthy QA in health monitoring scenarios.

---

## 1. 项目简介

本项目面向居家养老与远程健康监护场景，围绕跌倒、长时间静止、异常徘徊、遮挡误判、弱光误判等典型异常事件，构建一个轻量级的多模态异常事件理解与可信问答评测原型系统。

项目基于国家级大创“中云智护”的应用背景，当前重点聚焦算法侧预研，不依赖深度相机、激光雷达或机器人实物硬件，而是通过公开图像/视频样例、模拟事件数据和健康监护知识库，完成以下流程验证：

* 异常事件识别
* 多模态语义解释
* 健康监护知识检索
* 结构化问答评测
* 误差分析与可追溯性评估

项目目标是让健康监护系统从简单的“是否异常”分类判断，扩展为可解释、可追溯、可评测的健康监护决策支持原型。

---

## 2. 研究动机

传统健康监护系统通常侧重异常检测结果，例如判断“是否跌倒”或“是否长时间静止”。但在真实应用场景中，仅有分类结果远远不够，系统还需要回答：

1. 发生了什么异常？
2. 为什么判断为异常？
3. 当前风险等级如何？
4. 是否需要报警或二次确认？
5. 处理建议是否有知识依据？
6. 多模态大模型是否存在幻觉、误判或过度判断？

因此，本项目尝试将多模态大模型、RAG / GraphRAG 思路与健康监护场景结合，探索异常事件从分类识别到可信问答决策支持的实现路径。

---

## 3. 核心任务

本项目围绕以下任务展开：

| 任务           | 说明                                                       |
| -------------- | ---------------------------------------------------------- |
| 异常事件建模   | 构建跌倒、长时间静止、异常徘徊、遮挡、弱光等典型场景样本   |
| 多模态事件理解 | 使用 Qwen-VL / VideoLLaMA 等多模态大模型生成结构化异常解释 |
| 健康知识检索   | 构建健康监护知识库，使用 RAG 检索相关处置规则              |
| 可信问答生成   | 基于检索知识生成可追溯的处理建议                           |
| 对比实验评测   | 对比传统 baseline、纯 VLM、VLM + RAG 等方法                |
| 误差分析       | 分析遮挡、弱光、多人场景、长时间静止等易错情况             |

---

## 4. 技术路线

```text
公开图像/视频样例 + 模拟事件数据
        ↓
健康监护异常事件样本构建
        ↓
结构化标注
异常类型 / 风险等级 / 视觉证据 / 处理建议
        ↓
传统 baseline 与多模态大模型对比
Rule / ST-GCN / SVM / Qwen-VL / VideoLLaMA
        ↓
健康监护知识库检索
RAG / LightRAG / GraphRAG 思路
        ↓
结构化可信问答
异常类型 / 原因解释 / 风险等级 / 处理建议 / 知识依据
        ↓
评测与误差分析
准确性 / 解释一致性 / 可追溯性 / 误报分析 / 推理延迟
```

---

## 5. 系统架构

```text
HealthGuard-Multimodal-RAG-Eval
│
├── Data Layer
│   ├── Public image/video samples
│   ├── Simulated event descriptions
│   └── Health monitoring knowledge base
│
├── Event Understanding Layer
│   ├── Rule baseline
│   ├── ST-GCN / SVM baseline
│   └── Vision-Language Model
│
├── Knowledge Retrieval Layer
│   ├── BM25 retrieval
│   ├── Vector RAG
│   └── LightRAG / GraphRAG extension
│
├── Trustworthy QA Layer
│   ├── Risk-level reasoning
│   ├── Evidence-grounded answer generation
│   └── Traceable suggestion generation
│
└── Evaluation Layer
    ├── Abnormal detection accuracy
    ├── Event type accuracy
    ├── Risk level consistency
    ├── Explanation consistency
    ├── Knowledge traceability
    └── Error analysis
```

---

## 6. 项目目录结构

```text
HealthGuard-Multimodal-RAG-Eval/
├── README.md
├── requirements.txt
├── .gitignore
├── .env.example
│
├── data/
│   ├── samples.json
│   ├── health_knowledge.md
│   ├── label_schema.md
│   └── sample_images/
│       └── README.md
│
├── src/
│   ├── config.py
│   ├── prompts.py
│   ├── vlm_client.py
│   ├── rag_pipeline.py
│   ├── evaluator.py
│   ├── run_rag_demo.py
│   └── run_full_pipeline.py
│
├── results/
│   ├── vlm_outputs.jsonl
│   ├── rag_outputs.jsonl
│   ├── eval_report.md
│   └── ablation_table.md
│
├── docs/
│   ├── research_plan.md
│   ├── system_architecture.md
│   ├── error_analysis.md
│   ├── interview_qa.md
│   └── project_log.md
│
└── assets/
    └── architecture.png
```

---

## 7. 数据标注字段

每条样本包含以下字段：

| 字段              | 含义                                          |
| ----------------- | --------------------------------------------- |
| id                | 样本编号                                      |
| scenario          | 场景类型                                      |
| input_type        | 输入类型，例如 text、image、video_description |
| event_description | 事件描述                                      |
| image_path        | 可选图像路径                                  |
| is_abnormal       | 是否异常                                      |
| event_type        | 异常类型                                      |
| risk_level        | 风险等级：low / medium / high                 |
| visual_evidence   | 判断依据                                      |
| suggested_action  | 处理建议                                      |
| uncertainty       | 是否存在不确定性                              |
| need_rag          | 是否需要知识库辅助                            |

示例：

```json
{
  "id": "case_001",
  "scenario": "fall",
  "input_type": "text",
  "event_description": "老人从站立状态突然倒地，随后长时间未恢复站立。",
  "image_path": "",
  "ground_truth": {
    "is_abnormal": true,
    "event_type": "fall",
    "risk_level": "high",
    "visual_evidence": "由站立变为地面卧倒，且持续时间较长。",
    "suggested_action": "立即进行二次确认，并通知家属或护理人员。",
    "uncertainty": false,
    "need_rag": true
  }
}
```

---

## 8. 当前支持的异常场景

| 场景                     | 说明                       |
| ------------------------ | -------------------------- |
| fall                     | 跌倒事件                   |
| fall_recovery            | 跌倒后自行恢复             |
| long_static              | 长时间静止                 |
| wandering                | 异常徘徊                   |
| occlusion_uncertain      | 遮挡导致的不确定判断       |
| low_visibility_uncertain | 弱光或模糊导致的不确定判断 |
| posture_abnormal         | 坐姿、卧姿或身体姿态异常   |
| normal_activity          | 正常日常活动               |
| sleeping                 | 正常睡眠                   |
| normal_multi_person      | 多人场景下的正常行为       |

---

## 9. 快速开始

### 9.1 克隆项目

```bash
git clone https://github.com/your-username/HealthGuard-Multimodal-RAG-Eval.git
cd HealthGuard-Multimodal-RAG-Eval
```

### 9.2 创建虚拟环境

```bash
python -m venv .venv
```

Windows：

```bash
.venv\Scripts\activate
```

macOS / Linux：

```bash
source .venv/bin/activate
```

### 9.3 安装依赖

```bash
pip install -r requirements.txt
```

### 9.4 配置 API Key

复制 `.env.example` 为 `.env`：

```bash
cp .env.example .env
```

Windows PowerShell：

```powershell
Copy-Item .env.example .env
```

在 `.env` 中填写：

```env
API_KEY=your_api_key_here
BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
VLM_MODEL=qwen-vl-plus
LLM_MODEL=qwen-plus
```

---

## 10. 运行示例

### 10.1 运行健康知识库检索

```bash
python src/rag_pipeline.py
```

示例输出：

```text
SCORE: 8.2145
跌倒属于高风险异常事件。如果老人由站立、行走或坐姿突然转为地面卧倒，并且长时间未恢复站立，应优先进行二次确认。
```

### 10.2 运行 RAG 问答 Demo

```bash
python src/run_rag_demo.py
```

示例问题：

```text
检测到老人疑似跌倒后，系统应该如何处理？
```

输出内容包括：

* 检索到的知识片段
* 基于知识库生成的回答
* 风险提醒
* 是否可追溯

### 10.3 运行完整评测流程

```bash
python src/run_full_pipeline.py
```

运行后会生成：

```text
results/vlm_outputs.jsonl
results/eval_report.md
```

---

## 11. 评测指标

本项目初步使用以下指标：

| 指标                        | 含义                             |
| --------------------------- | -------------------------------- |
| Abnormal Detection Accuracy | 是否正确判断异常                 |
| Event Type Accuracy         | 是否正确识别异常类型             |
| Risk Level Accuracy         | 是否正确判断风险等级             |
| Explanation Consistency     | 解释是否与事件描述一致           |
| Knowledge Traceability      | 回答是否能追溯到知识库依据       |
| Parse Error Count           | 模型结构化 JSON 输出解析错误次数 |
| False Alarm Analysis        | 误报与过度判断分析               |
| Inference Latency           | 推理延迟                         |

---

## 12. 对比实验设计

| 方法                      | 异常判断 | 解释能力 | 可追溯性 | 误报分析 | 推理成本 | 当前状态         |
| ------------------------- | -------- | -------- | -------- | -------- | -------- | ---------------- |
| Rule Baseline             | 中       | 弱       | 无       | 弱       | 低       | 已设计           |
| ST-GCN / SVM Baseline     | 中       | 弱       | 无       | 中       | 中       | 作为传统方法对比 |
| Pure VLM                  | 中高     | 中       | 无       | 中       | 中       | API 原型验证     |
| VLM + BM25 RAG            | 中高     | 较强     | 中       | 较强     | 中       | 轻量版实现       |
| VLM + LightRAG / GraphRAG | 预期较强 | 强       | 强       | 强       | 中高     | 后续扩展         |

---

## 13. 初步误差分析方向

本项目重点关注以下易错场景：

1. 正常休息被误判为长时间静止风险
2. 遮挡导致跌倒误判
3. 弱光下模型输出过度自信
4. 多人场景中蹲下、弯腰等正常动作被误判为跌倒
5. 短暂跌倒后自行恢复的风险等级不稳定
6. RAG 检索到语义不匹配的知识片段
7. 模型生成缺乏依据的处理建议

---

## 14. 当前进度

* [X] 明确项目选题与技术路线
* [X] 完成异常事件标注字段设计
* [X] 构建健康监护知识库初版
* [X] 构建小规模模拟事件样本
* [X] 实现轻量级 BM25 RAG 检索
* [X] 设计 VLM / LLM 结构化输出 Prompt
* [X] 接入 Qwen-VL API 进行多模态事件理解
* [ ] 生成 `vlm_outputs.jsonl`
* [ ] 完成 `eval_report.md`
* [ ] 扩展样本规模至 30–50 条
* [ ] 补充系统架构图与技术报告
* [ ] 扩展向量 RAG / LightRAG / GraphRAG 实现

---

## 15. 项目特点

本项目的重点不在于训练大模型，而在于构建一个轻量、可复现、可解释的算法侧评测原型。主要特点包括：

* 不依赖真实硬件设备
* 适合短期快速复现与展示
* 聚焦健康监护垂直场景
* 强调结构化输出与可追溯问答
* 引入 baseline 对比、指标设计和误差分析
* 可扩展到真实图像、视频和传感器数据
