# Label Schema

每条健康监护异常事件样本包含以下字段：

| 字段 | 含义 |
|---|---|
| id | 样本编号 |
| scenario | 场景类型 |
| input_type | 输入类型，包括 text、image、video_description |
| event_description | 事件描述 |
| image_path | 可选图像路径 |
| is_abnormal | 是否异常 |
| event_type | 异常类型 |
| risk_level | 风险等级，low / medium / high |
| visual_evidence | 判断依据 |
| suggested_action | 处理建议 |
| uncertainty | 是否存在不确定性 |
| need_rag | 是否需要知识库辅助 |
```
