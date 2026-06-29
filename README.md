# CareEvent-VLM-RAG-Eval

面向健康监护场景的多模态异常事件理解与可信问答评测原型。

当前版本是一个**实验性、离线可复现的小规模原型**，不是临床系统，也不是生产级医疗告警系统。项目重点是把异常事件从简单分类扩展为结构化回答，并对回答进行可追溯评测和失败案例分析。

## 1. 当前真实进度

| 模块 | 状态 | 说明 |
|---|---|---|
| 样例数据 | 已小规模构建 | 10 条文本化模拟健康监护事件样例，不含真实图像/视频 |
| 多模态/大模型解释 | 已小规模验证 | 已保存一次 Qwen 兼容 API 输出到 `results/vlm_outputs.jsonl`；当前离线评测默认回放该文件 |
| 健康知识库 | 已小规模构建 | `data/health_knowledge.md` 含 24 条演示知识条目 |
| RAG 检索 | 已实现轻量版 | 本地 TF-IDF 字符向量检索，BM25 可回退；无向量数据库 |
| 结构化回答 | 已实现离线版 | 输出异常类型、视觉证据、风险等级、建议和知识引用 |
| 评测指标 | 已实现基础版 | accuracy、误报率、precision/recall/F1、字段一致性、离线延迟 |
| 失败案例 | 已实现基础版 | 从真实预测与标注不一致的样本自动生成 |
| SVM baseline | 已小规模验证 | 使用可解释文本特征 + `StandardScaler` + scikit-learn `SVC`；不是从零实现 SVM 求解器 |
| ST-GCN baseline | 尚未实现 | 当前仅适合表述为方法调研/后续开源复现计划 |
| GraphRAG | 尚未实现完整系统 | 当前只能表述为参考 GraphRAG 做知识组织探索 |

## 2. 项目结构

```text
CareEvent-VLM-RAG-Eval/
├── config.yaml
├── run_eval.py
├── requirements.txt
├── .env.example
├── data/
│   ├── samples.json
│   ├── health_knowledge.md
│   ├── care_knowledge.md
│   └── label_schema.md
├── src/
│   ├── config.py
│   ├── vlm_client.py
│   ├── rag_pipeline.py
│   ├── evaluator.py
│   ├── run_full_pipeline.py
│   └── run_rag_demo.py
├── outputs/
│   ├── predictions.jsonl
│   ├── metrics.json
│   ├── latency.csv
│   ├── failure_cases.md
│   └── confusion_matrix.png
├── results/
│   ├── vlm_outputs.jsonl
│   ├── eval_report.md
│   └── ablation_table.md
├── baselines/
│   ├── svm/
│   └── st_gcn/
└── docs/
    ├── audit_report.md
    ├── dataset_card.md
    ├── error_analysis.md
    ├── interview_qa.md
    ├── ppt_truthfulness_review.md
    └── plans/
```

## 3. 环境安装

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\activate
pip install -r requirements.txt
```

当前验证环境：

```text
Python 3.14.5
openai 2.41.0
rank-bm25 0.2.2
scikit-learn 1.9.0
```

## 4. API Key 配置

离线评测不需要 API Key。

如果需要重新调用 Qwen 兼容 API：

```powershell
Copy-Item .env.example .env
```

然后在 `.env` 中填写自己的密钥。`.env.example` 只保留占位符，不应写入真实密钥。

## 5. 数据格式

当前数据位于 `data/samples.json`，共 10 条，均为模拟文本事件描述。

核心字段：

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

数据说明见 `docs/dataset_card.md`。

## 6. 一键离线运行

推荐用于展示和复现：

```bash
python run_eval.py --config config.yaml
```

该命令不会访问网络。它会读取：

- `data/samples.json`
- `results/vlm_outputs.jsonl`
- `data/health_knowledge.md`

并生成：

```text
outputs/
├── predictions.jsonl
├── metrics.json
├── latency.csv
├── failure_cases.md
├── confusion_matrix.png
├── confusion_matrix_labels.json
└── eval_report.md
```

## 7. 当前结果

基于 10 条样例与已有真实预测文件，当前离线复算结果为：

| 指标 | 数值 |
|---|---:|
| Abnormal detection accuracy | 0.9 |
| Event type accuracy | 0.7 |
| Risk level accuracy | 0.8 |
| False alarm rate | 0.3333 |
| Precision abnormal | 0.875 |
| Recall abnormal | 1.0 |
| F1 abnormal | 0.9333 |
| Explanation consistency | 0.6 |
| Parse error count | 0 |

误报率口径：

```text
实际正常但被判断为异常的样本数 / 实际正常样本总数
```

当前 3 条正常样本中有 1 条被误报为异常：`case_008`。

## 8. 失败案例

真实失败案例来自 `results/vlm_outputs.jsonl` 与 `data/samples.json` 的字段对比，见 `outputs/failure_cases.md` 和 `docs/error_analysis.md`。

当前主要失败：

- `case_002`：长时间静止风险等级偏低。
- `case_007`：短暂跌倒后恢复被归为普通跌倒。
- `case_008`：正常睡眠被误判为长时间静止异常。
- `case_010`：多人正常场景被简化为 normal，丢失细分类别。

## 9. 当前限制

- 样本量只有 10 条，不能支撑统计意义上的模型结论。
- 输入是文本化事件描述，不是真实图像或视频。
- 离线评测回放已有 API 输出，不能代表实时 API 延迟。
- RAG 使用本地 TF-IDF/BM25 检索，没有接入向量数据库。
- GraphRAG、图数据库、动态图增量计算、分布式图计算均未实现。
- SVM 只完成了极小样本文本特征二分类流程验证，测试集只有 3 条，不能作为可靠模型效果。
- ST-GCN baseline 尚未在当前代码中完成。
- 结果仅用于项目展示和方法训练，不可用于真实医疗决策。

## 10. SVM 小规模基线

运行：

```bash
python baselines/svm/extract_features.py
python baselines/svm/train_svm.py
python baselines/svm/evaluate_svm.py
```

输出：

```text
baselines/svm/
├── features.csv
├── model.pkl
├── split.json
└── results/
    ├── predictions.jsonl
    ├── metrics.json
    └── confusion_matrix.png
```

当前 SVM 使用文本描述的可解释数值特征，标签为 `ground_truth.is_abnormal`。它使用 scikit-learn `SVC`，不是从零实现 SVM 优化求解器。由于样本极少，指标只说明流程可运行。

## 11. AI 辅助与开源说明

本项目代码和文档整理过程中使用了 AI 辅助。应诚实表述为：

- 本人负责问题定义、字段设计、流程拆解、实验口径确认、运行验证和结果分析。
- AI 辅助生成和整理了部分脚本、文档、Prompt、工具函数和调试代码。
- 当前 SVM/ST-GCN 没有从零实现，也没有成熟训练结果。
- `rank-bm25`、`scikit-learn`、`openai` 等依赖为开源库或官方 SDK。
- 所有可展示结果应以当前代码和输出文件为准。
