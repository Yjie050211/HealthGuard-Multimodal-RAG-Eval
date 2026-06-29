# Ablation / Baseline Status

当前文件是对比实验规划与状态表，不是已完成的大规模消融实验。

| 方法 | 当前状态 | 已有证据 | 可展示表述 |
|---|---|---|---|
| Rule Baseline | 仅方案设计 | 暂无独立代码 | 已形成规则基线方案，后续补代码验证 |
| SVM Baseline | 已小规模验证 | `baselines/svm/results/metrics.json` | 使用文本特征 + StandardScaler + scikit-learn SVC；仅证明流程可运行 |
| ST-GCN Baseline | 尚未实现 | 无骨骼关键点、无训练/推理日志 | 已完成方法调研，后续基于开源实现做推理验证 |
| Pure VLM/LLM | 已小规模验证 | `results/vlm_outputs.jsonl` | 基于文本化事件描述完成一次 API 输出验证 |
| VLM + Local RAG | 已小规模验证 | `run_eval.py` 与 `outputs/` | 完成离线 RAG 检索与引用回答闭环 |
| LightRAG / GraphRAG | 仅方案探索 | 无图构建和图检索代码 | 参考相关思想做知识组织探索 |

## 当前观察

已有结果只能说明最小流程可运行：文本事件输入、结构化解释回放、健康知识检索、引用回答、指标计算、失败案例提取，以及一个 scikit-learn SVM 小样本二分类基线。由于样本只有 10 条，且 ST-GCN 未实现，不能声称已经完成充分的传统模型对比实验。
