# Failure Cases

## Case 1: case_002

- 样例ID：case_002
- 输入：老人坐在沙发上超过两小时未明显移动，但处于正常坐姿。
- 真实标签：is_abnormal=True, event_type=long_static, risk_level=medium
- 模型输出：is_abnormal=True, event_type=long_static, risk_level=low
- 错误类型：risk_level
- 可能原因：长时间静止但姿态正常，风险等级边界依赖时间段和确认信息。
- 改进方向：补充语音确认结果、历史活动规律或时间段信息，降低风险等级主观性。

## Case 2: case_007

- 样例ID：case_007
- 输入：老人疑似摔倒后很快自行站起，并继续正常行走。
- 真实标签：is_abnormal=True, event_type=fall_recovery, risk_level=medium
- 模型输出：is_abnormal=True, event_type=fall, risk_level=medium
- 错误类型：event_type
- 可能原因：短暂跌倒后恢复与普通跌倒边界相近，事件类型粒度不稳定。
- 改进方向：增加 fall_recovery 样例，并要求模型区分持续卧倒与短时恢复。

## Case 3: case_008

- 样例ID：case_008
- 输入：老人夜间平躺在床上，长时间没有明显移动。
- 真实标签：is_abnormal=False, event_type=sleeping, risk_level=low
- 模型输出：is_abnormal=True, event_type=long_static, risk_level=medium
- 错误类型：is_abnormal, event_type, risk_level
- 可能原因：夜间睡眠与长时间静止语义相近，模型未充分利用睡眠场景条件。
- 改进方向：在提示词和知识库中强化睡眠区域、夜间时段与正常睡眠的区分规则。

## Case 4: case_010

- 样例ID：case_010
- 输入：画面中有两个人，其中一人蹲下捡东西，另一人正常站立。
- 真实标签：is_abnormal=False, event_type=normal_multi_person, risk_level=low
- 模型输出：is_abnormal=False, event_type=normal, risk_level=low
- 错误类型：event_type
- 可能原因：多人正常动作被简化为 normal，未保留 normal_multi_person 细分类别。
- 改进方向：保留多人场景标签，并在评测中单独统计多人误判。
