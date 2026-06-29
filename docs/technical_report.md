# CareEvent-VLM-RAG-Eval 技术报告初稿

## 摘要

本项目面向居家养老与远程健康监护场景，探索异常事件从“是否异常”的分类判断，扩展为包含异常类型、事件证据、风险等级、处理建议和知识来源的结构化可信问答流程。当前版本完成了 10 条模拟文本样例、本地健康知识库、离线模型输出回放、轻量级 RAG 检索、指标计算和失败案例分析，并补充了一个 scikit-learn SVM 小规模二分类基线。

当前系统是实验性原型，不是临床系统或生产级医疗告警系统。

## 1. 数据与任务定义

数据位于 `data/samples.json`，共 10 条模拟文本事件，覆盖跌倒、长时间静止、遮挡、弱光、异常徘徊、正常活动、睡眠、多人场景等情况。

每条样例包含：

- `event_description`
- `is_abnormal`
- `event_type`
- `risk_level`
- `visual_evidence`
- `suggested_action`
- `uncertainty`
- `need_rag`

当前没有真实图像、视频、骨骼关键点或传感器时序数据。

## 2. 方法

### 2.1 结构化异常解释

项目保留了 Qwen 兼容 API 的调用代码，并保存了一次真实输出到 `results/vlm_outputs.jsonl`。为了现场展示稳定，当前主流程默认使用离线回放，不访问网络。

### 2.2 健康知识库与 RAG

知识库位于 `data/health_knowledge.md`，包含 24 条内部知识条目。系统将 Markdown 二级标题切分为检索块，并为每条知识生成稳定编号，如 `K001`。

当前检索方法：

- 默认：TF-IDF 字符向量余弦相似度
- 回退：BM25
- Top-K：由 `config.yaml` 控制，当前为 3

该实现不是向量数据库，也不是完整 GraphRAG。

### 2.3 结构化回答

`run_eval.py` 为每条样例输出：

- `event_type`
- `visual_evidence`
- `risk_level`
- `recommendation`
- `confidence_or_uncertainty`
- `knowledge_reference`
- `traceable`

知识引用来自内部知识库条目，便于追溯。

## 3. 评测指标

当前实现的指标包括：

- Abnormal detection accuracy
- Event type accuracy
- Risk level accuracy
- False alarm rate
- Precision / Recall / F1
- Parse error count
- Field-based explanation consistency
- Offline retrieval and total latency

误报率定义：

```text
实际正常但被判断为异常的样本数 / 实际正常样本总数
```

解释一致性当前采用基础字段规则：

```text
event_type 匹配 AND risk_level 匹配 AND predicted visual_evidence 非空
```

## 4. 主流程结果

运行命令：

```bash
python run_eval.py --config config.yaml
```

当前结果：

| 指标 | 数值 |
|---|---:|
| Total samples | 10 |
| Abnormal detection accuracy | 0.9 |
| Event type accuracy | 0.7 |
| Risk level accuracy | 0.8 |
| False alarm rate | 0.3333 |
| Precision abnormal | 0.875 |
| Recall abnormal | 1.0 |
| F1 abnormal | 0.9333 |
| Explanation consistency | 0.6 |
| Parse error count | 0 |

## 5. SVM 基线

SVM 基线位于 `baselines/svm/`。

运行命令：

```bash
python baselines/svm/extract_features.py
python baselines/svm/train_svm.py
python baselines/svm/evaluate_svm.py
```

实现说明：

- 输入特征：从文本事件描述中抽取的可解释数值特征，如文本长度、跌倒关键词、静止关键词、夜间、遮挡、弱光、多人等。
- 标签：`ground_truth.is_abnormal`
- 模型：`StandardScaler + scikit-learn SVC`
- 随机种子：42
- 训练/测试划分：7/3

该基线不是从零实现 SVM 求解器。由于总样本只有 10 条，SVM 指标只能证明流程可运行，不能证明泛化能力。

## 6. 失败案例

当前自动提取 4 个真实失败或不一致样例：

| 样例 | 问题 |
|---|---|
| case_002 | 长时间静止风险等级偏低 |
| case_007 | 短暂跌倒后恢复被归为普通跌倒 |
| case_008 | 正常睡眠被误报为长时间静止异常 |
| case_010 | 多人正常场景被简化为 normal |

详细分析见 `outputs/failure_cases.md` 和 `docs/error_analysis.md`。

## 7. 工程可复现性

当前已提供：

- `requirements.txt`
- `.env.example`
- `config.yaml`
- `run_eval.py`
- 离线预测文件 `results/vlm_outputs.jsonl`
- 标准输出目录 `outputs/`
- SVM baseline 脚本和输出

离线主流程不需要 API Key。需要重跑 API 时，必须自行创建 `.env` 并配置密钥。

## 8. 当前限制

- 样本量极小。
- 输入为文本描述，不是真实图像或视频。
- 模型调用结果是离线回放，不代表实时网络延迟。
- RAG 是轻量本地检索，不是向量数据库。
- GraphRAG 未实现图构建、图存储或图查询。
- ST-GCN 未实现训练或推理。
- 当前结果不能用于真实医疗判断。

## 9. 后续工作

P1：

- 扩展样本到 30-50 条。
- 增加真实或公开图像/视频样例。
- 完善 SVM 特征和评估划分。
- 基于开源实现完成 ST-GCN 小规模推理验证。

P2：

- 设计事件-风险-建议-证据图结构。
- 增加图可视化和图检索。
- 探索动态图更新、增量计算和 GNN 系统方向。
