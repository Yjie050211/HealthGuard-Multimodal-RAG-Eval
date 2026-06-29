# Evaluation Report

## Overall Metrics

- Total samples: 10
- Abnormal detection accuracy: 0.9
- Event type accuracy: 0.7
- Risk level accuracy: 0.8
- False alarm rate: 0.3333 (1/3)
- Precision abnormal: 0.875
- Recall abnormal: 1.0
- F1 abnormal: 0.9333
- Explanation consistency: 0.6
- Explanation consistency definition: event_type match AND risk_level match AND non-empty predicted visual_evidence
- Parse error count: 0

## Case Details

| ID | Scenario | Abnormal | Event Type | Risk Level | Explanation | Mismatches |
|---|---|---|---|---|---|---|
| case_001 | fall | True | True | True | True | - |
| case_002 | long_static | True | True | False | False | risk_level |
| case_003 | occlusion | True | True | True | True | - |
| case_004 | normal_activity | True | True | True | True | - |
| case_005 | wandering | True | True | True | True | - |
| case_006 | weak_light | True | True | True | True | - |
| case_007 | fall_recovery | True | False | True | False | event_type |
| case_008 | sleeping | False | False | False | False | is_abnormal, event_type, risk_level |
| case_009 | chair_slump | True | True | True | True | - |
| case_010 | multiple_people | True | False | True | False | event_type |