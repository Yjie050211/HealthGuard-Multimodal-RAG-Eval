# 项目真实性审计报告

审计日期：2026-06-29

## 1. 已审计材料

- `CareEvent-VLM-RAG-Eval.zip`
- `F:\myproject\CareEvent-VLM-RAG-Eval`
- `娄有杰_面试展示PPT临时版.pptx`
- `娄有杰_许瑞琦老师面试指导.md`
- README、代码、数据、配置、输出、技术报告草稿类文档

ZIP 包包含 `.git/` 和 `.venv/`，导致体积较大。审计以已解压项目目录为主，并用 ZIP 清单辅助核对。

## 2. 技术栈

| 项 | 当前情况 |
|---|---|
| Python | 3.14.5 |
| API SDK | openai 2.41.0，兼容 DashScope/OpenAI Chat Completions |
| 检索 | TF-IDF 字符向量检索，BM25 回退 |
| 评测 | 自定义 Python 脚本 |
| 数据 | 10 条模拟文本事件 |
| 知识库 | 24 条 Markdown 健康监护演示知识 |
| 图数据库 | 未接入 |
| 向量数据库 | 未接入 |
| SVM | 已完成 scikit-learn 小规模二分类基线 |
| ST-GCN | 未实现 |
| GraphRAG | 未实现完整系统 |

## 3. 主运行链路

```text
data/samples.json
→ results/vlm_outputs.jsonl 离线回放
→ data/health_knowledge.md 本地检索
→ run_eval.py 结构化回答与评测
→ outputs/
```

运行命令：

```bash
python run_eval.py --config config.yaml
```

## 4. 实现状态判定

| PPT或README中的声明 | 对应代码文件 | 是否真实实现 | 运行证据 | 风险 | 建议表述 |
|---|---|---|---|---|---|
| 多模态异常解释 | `src/vlm_client.py`, `results/vlm_outputs.jsonl` | 已小规模验证 | 10 条 API 输出已保存 | 当前输入是文本描述，不是真图像/视频 | 基于文本化事件描述完成结构化解释验证 |
| 健康知识检索 | `src/rag_pipeline.py` | 已实现轻量版 | `python src/rag_pipeline.py` 可运行 | 不是向量数据库或 GraphRAG | 本地 TF-IDF/BM25 健康知识检索 |
| 有引用回答 | `run_eval.py`, `outputs/predictions.jsonl` | 已实现离线版 | 每条输出含 `knowledge_reference` | 引用为内部知识库条目 | 生成带内部知识来源的结构化回答 |
| 准确率 | `src/evaluator.py`, `outputs/metrics.json` | 已实现 | abnormal accuracy 0.9 | 样本仅 10 条 | 小规模样例准确率 |
| 误报率 | `src/evaluator.py`, `outputs/metrics.json` | 已实现 | false alarm rate 0.3333 | 分母只有 3 条正常样本 | 按正常样本误报口径计算 |
| 推理延迟 | `outputs/latency.csv` | 部分实现 | 记录检索和总流程离线时间 | 不含实时 API 网络请求 | 离线回放延迟，不代表模型 API 延迟 |
| 解释一致性 | `src/evaluator.py` | 基础字段指标 | explanation consistency 0.6 | 非人工语义评分 | 字段匹配式解释一致性 |
| 失败案例 | `outputs/failure_cases.md` | 已实现 | 4 个真实失败/不一致样例 | 样本少 | 从当前输出自动提取失败案例 |
| SVM baseline | `baselines/svm/` | 已小规模验证 | `baselines/svm/results/metrics.json` | 样本极少，不能夸大效果 | 使用 scikit-learn SVC 完成流程验证，非从零实现 |
| ST-GCN baseline | 无 | 尚未实现 | 无 | 高风险表述 | 已调研，后续基于开源实现验证 |
| GraphRAG系统 | 无 | 尚未实现 | 无 | 高风险表述 | 参考 GraphRAG 思路进行知识组织探索 |

## 5. 当前真实指标

| 指标 | 值 |
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

## 6. 安全与可复现性

- 已移除 `.env.example` 与 `src/config.py` 中的硬编码密钥默认值。
- 离线评测不需要 API Key。
- API 调用需要用户自行创建 `.env`。
- `config.yaml` 固定输入、知识库、检索方法和输出目录。
- 生成产物位于 `outputs/`。

## 7. 主要缺失模块

- ST-GCN 开源推理复现。
- 图结构构建、图查询和 GraphRAG。
- 真实图像/视频输入。
- 自动语义级解释一致性评价。
- 大样本实验和统计显著性分析。

## 8. 修改优先级

P0 已完成：

- 密钥修复。
- 离线一键运行。
- 24 条知识库。
- RAG 引用回答。
- 指标、延迟、失败案例和混淆矩阵输出。
- README 与真实性文档修正。

P1 建议继续：

- ST-GCN 开源实现推理验证。
- 技术报告 PDF/PPT 版本修订。

P2 后续：

- GraphRAG 图结构可视化。
- 图数据库接入。
- 动态图更新与增量计算实验。
