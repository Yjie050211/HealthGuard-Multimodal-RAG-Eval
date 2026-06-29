# 最终交付清单

## 1. 项目审计报告

- `docs/audit_report.md`
- 说明当前已实现、已小规模验证、仅方案设计和尚未实现的模块。

## 2. 修改后的目录树

关键新增：

```text
config.yaml
run_eval.py
outputs/
baselines/svm/
baselines/st_gcn/README.md
docs/audit_report.md
docs/dataset_card.md
docs/interview_qa.md
docs/ppt_truthfulness_review.md
docs/final_delivery_checklist.md
```

## 3. 可运行命令

离线主流程：

```bash
python run_eval.py --config config.yaml
```

SVM 小规模基线：

```bash
python baselines/svm/extract_features.py
python baselines/svm/train_svm.py
python baselines/svm/evaluate_svm.py
```

RAG 检索演示：

```bash
python src/rag_pipeline.py
```

## 4. 实验结果

主流程输出：

- `outputs/predictions.jsonl`
- `outputs/metrics.json`
- `outputs/latency.csv`
- `outputs/failure_cases.md`
- `outputs/confusion_matrix.png`

当前主流程指标：

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

SVM 输出：

- `baselines/svm/features.csv`
- `baselines/svm/model.pkl`
- `baselines/svm/split.json`
- `baselines/svm/results/metrics.json`
- `baselines/svm/results/confusion_matrix.png`

SVM 仅为 10 条模拟文本样例上的流程验证，不代表可靠模型效果。

## 5. 失败案例

- `outputs/failure_cases.md`
- `docs/error_analysis.md`

当前真实失败/不一致样例：

- `case_002`：长时间静止风险等级偏低。
- `case_007`：短暂跌倒后恢复被归为普通跌倒。
- `case_008`：正常睡眠被误判为长时间静止异常。
- `case_010`：多人正常场景被简化为 normal。

## 6. README

- `README.md`

README 已改为当前真实能力版，包含环境安装、数据格式、运行命令、输出说明、限制和 AI 辅助说明。

补充技术报告：

- `docs/technical_report.md`

## 7. PPT 逐页修改建议与修订版

- 修改建议：`docs/ppt_truthfulness_review.md`
- 修订版 PPT：`娄有杰_面试展示PPT真实性修订版.pptx`

修订版已将 SVM/ST-GCN/GraphRAG 相关高风险表述降级为真实边界。

## 8. 30 秒与 2 分钟话术

- `docs/interview_qa.md`

包含 30 秒介绍、2 分钟介绍、代码展示话术和许老师方向衔接说法。

## 9. 技术追问题库

- `docs/interview_qa.md`

包含 20 个重点追问及可复述答案。

## 10. AI 辅助与能力边界说明

- `README.md`
- `docs/interview_qa.md`

核心边界：

- AI 辅助了脚本框架、Prompt、文档草稿和调试。
- 本人负责问题定义、字段设计、运行验证和结果解释。
- SVM 使用 scikit-learn，不是从零实现求解器。
- ST-GCN 尚未实现训练或推理。
- GraphRAG 尚未实现完整图系统。

## 验证记录

已验证：

- `python run_eval.py --config config.yaml`
- `python src/rag_pipeline.py`
- Python 文件编译检查
- 密钥扫描未发现真实 `sk-...` 格式密钥
- SVM 特征抽取、训练、评估三步
- 主流程与 SVM 混淆矩阵图片可打开
