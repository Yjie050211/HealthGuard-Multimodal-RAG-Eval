# 真实失败案例分析

本文件只记录当前真实运行结果中的失败案例。依据文件：

- 标注：`data/samples.json`
- 模型输出：`results/vlm_outputs.jsonl`
- 自动整理：`outputs/failure_cases.md`

## Case 1: case_002

- 样例ID：case_002
- 输入：老人坐在沙发上超过两小时未明显移动，但处于正常坐姿。
- 真实标签：`is_abnormal=true`, `event_type=long_static`, `risk_level=medium`
- 模型输出：`is_abnormal=true`, `event_type=long_static`, `risk_level=low`
- 错误类型：风险等级偏低
- 可能原因：长时间静止但姿态正常，风险等级依赖时间段、历史活动规律和语音确认结果。
- 改进方向：补充语音确认、时间段和历史活动特征；在风险规则中明确“长时间静止但姿态正常”的中风险边界。

## Case 2: case_007

- 样例ID：case_007
- 输入：老人疑似摔倒后很快自行站起，并继续正常行走。
- 真实标签：`event_type=fall_recovery`
- 模型输出：`event_type=fall`
- 错误类型：事件类型粒度不一致
- 可能原因：短暂跌倒后恢复与普通跌倒在文本表述上相近，模型没有保留“恢复”这一细粒度状态。
- 改进方向：增加 `fall_recovery` 样例；在提示词中要求区分“持续卧倒”和“短时恢复”。

## Case 3: case_008

- 样例ID：case_008
- 输入：老人夜间平躺在床上，长时间没有明显移动。
- 真实标签：`is_abnormal=false`, `event_type=sleeping`, `risk_level=low`
- 模型输出：`is_abnormal=true`, `event_type=long_static`, `risk_level=medium`
- 错误类型：误报；事件类型错误；风险等级错误
- 可能原因：夜间睡眠与长时间静止语义相近，模型未充分利用“夜间、床上、平躺”这些正常睡眠条件。
- 改进方向：在知识库与提示词中强化睡眠场景规则；增加正常睡眠负样本；单独统计睡眠误报。

## Case 4: case_010

- 样例ID：case_010
- 输入：画面中有两个人，其中一人蹲下捡东西，另一人正常站立。
- 真实标签：`event_type=normal_multi_person`
- 模型输出：`event_type=normal`
- 错误类型：细分类别丢失
- 可能原因：模型判断“无异常”正确，但没有保留多人场景这一细分类别。
- 改进方向：在标签体系中明确 normal 与 normal_multi_person 的关系；如果展示时只讲异常检测，可说明该样本异常判断正确但细粒度类型不一致。
