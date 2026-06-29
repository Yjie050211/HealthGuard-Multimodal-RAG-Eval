# 数据与标注说明

## 数据来源

当前数据为项目自建的模拟文本样例，用于验证健康监护异常事件理解、知识检索和评测流程。它不是临床数据，不包含真实老人图像、视频或传感器记录。

## 样本规模

- 总样本数：10
- 输入类型：text
- 图像/视频：当前无真实图像或视频，`image_path` 为空
- 划分方式：当前样本量过小，未划分训练集、验证集和测试集；全部用于流程验证

## 类别分布

| event_type | 数量 |
|---|---:|
| fall | 1 |
| fall_recovery | 1 |
| long_static | 1 |
| low_visibility_uncertain | 1 |
| normal | 1 |
| normal_multi_person | 1 |
| occlusion_uncertain | 1 |
| posture_abnormal | 1 |
| sleeping | 1 |
| wandering | 1 |

## 风险等级分布

| risk_level | 数量 |
|---|---:|
| high | 1 |
| medium | 6 |
| low | 3 |

## 统一样例字段

当前 `data/samples.json` 使用 `id` 和 `image_path`。在输出文件中统一映射为：

```json
{
  "sample_id": "case_001",
  "input_path": "",
  "event_type": "fall",
  "risk_level": "high",
  "visual_evidence": ["由站立变为地面卧倒，且持续时间较长。"],
  "recommendation": "立即进行二次确认，并通知家属或护理人员。",
  "knowledge_reference": []
}
```

## 标注方式

标注字段由项目设计者依据健康监护场景进行规则化设计，包括：

- 是否异常：`is_abnormal`
- 异常类型：`event_type`
- 风险等级：`risk_level`
- 视觉/事件证据：`visual_evidence`
- 处理建议：`suggested_action`
- 是否不确定：`uncertainty`
- 是否需要 RAG：`need_rag`

## 当前限制

- 样本均为模拟文本，不代表真实监控数据分布。
- 每个类别当前只有 1 条样例，不能用于训练稳定模型。
- 没有真实视频帧、骨骼关键点或传感器时序。
- 当前评测只说明流程可运行，不能说明模型在真实环境中的可靠性。
