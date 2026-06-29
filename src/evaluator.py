import json
from pathlib import Path
from typing import Dict, List


def load_samples(path: str = "data/samples.json") -> List[Dict]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_jsonl(path: str) -> List[Dict]:
    source = Path(path)
    if not source.exists():
        return []
    return [
        json.loads(line)
        for line in source.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def normalize_bool(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in ["true", "yes", "1", "是"]
    return False


def _round(value, digits: int = 4):
    return round(value, digits) if value is not None else "N/A"


def evaluate_predictions(samples: List[Dict], predictions: List[Dict]) -> Dict:
    total = len(samples)

    abnormal_correct = 0
    event_type_correct = 0
    risk_level_correct = 0
    parse_error_count = 0
    explanation_consistent = 0

    tp = fp = tn = fn = 0
    details = []
    confusion: Dict[str, Dict[str, int]] = {}

    pred_map = {item["id"]: item for item in predictions}

    for sample in samples:
        sid = sample["id"]
        gt = sample["ground_truth"]
        pred_record = pred_map.get(sid, {})
        pred = pred_record.get("prediction", {})

        if pred.get("parse_error"):
            parse_error_count += 1

        gt_abnormal = gt["is_abnormal"]
        pred_abnormal = normalize_bool(pred.get("is_abnormal", False))

        gt_event_type = gt["event_type"]
        pred_event_type = pred.get("event_type", "")

        gt_risk_level = gt["risk_level"]
        pred_risk_level = pred.get("risk_level", "")
        pred_evidence = str(pred.get("visual_evidence", "")).strip()

        abnormal_match = gt_abnormal == pred_abnormal
        event_type_match = gt_event_type == pred_event_type
        risk_level_match = gt_risk_level == pred_risk_level
        evidence_present = bool(pred_evidence)
        explanation_match = event_type_match and risk_level_match and evidence_present

        abnormal_correct += int(abnormal_match)
        event_type_correct += int(event_type_match)
        risk_level_correct += int(risk_level_match)
        explanation_consistent += int(explanation_match)

        if gt_abnormal and pred_abnormal:
            tp += 1
        elif not gt_abnormal and pred_abnormal:
            fp += 1
        elif not gt_abnormal and not pred_abnormal:
            tn += 1
        elif gt_abnormal and not pred_abnormal:
            fn += 1

        confusion.setdefault(gt_event_type, {})
        confusion[gt_event_type][pred_event_type or "missing"] = (
            confusion[gt_event_type].get(pred_event_type or "missing", 0) + 1
        )

        mismatched_fields = []
        if not abnormal_match:
            mismatched_fields.append("is_abnormal")
        if not event_type_match:
            mismatched_fields.append("event_type")
        if not risk_level_match:
            mismatched_fields.append("risk_level")

        details.append({
            "id": sid,
            "scenario": sample["scenario"],
            "abnormal_match": abnormal_match,
            "event_type_match": event_type_match,
            "risk_level_match": risk_level_match,
            "explanation_consistent": explanation_match,
            "mismatched_fields": mismatched_fields,
            "gt_abnormal": gt_abnormal,
            "pred_abnormal": pred_abnormal,
            "gt_event_type": gt_event_type,
            "pred_event_type": pred_event_type,
            "gt_risk_level": gt_risk_level,
            "pred_risk_level": pred_risk_level
        })

    normal_total = sum(1 for sample in samples if not sample["ground_truth"]["is_abnormal"])
    precision = tp / (tp + fp) if (tp + fp) else None
    recall = tp / (tp + fn) if (tp + fn) else None
    f1 = (2 * precision * recall / (precision + recall)) if precision is not None and recall is not None and (precision + recall) else None

    return {
        "total": total,
        "abnormal_accuracy": _round(abnormal_correct / total if total else None),
        "event_type_accuracy": _round(event_type_correct / total if total else None),
        "risk_level_accuracy": _round(risk_level_correct / total if total else None),
        "false_alarm_rate": _round(fp / normal_total if normal_total else None),
        "false_positive_count": fp,
        "normal_total": normal_total,
        "precision_abnormal": _round(precision),
        "recall_abnormal": _round(recall),
        "f1_abnormal": _round(f1),
        "explanation_consistency": _round(explanation_consistent / total if total else None),
        "explanation_consistency_definition": "event_type match AND risk_level match AND non-empty predicted visual_evidence",
        "parse_error_count": parse_error_count,
        "confusion_matrix": confusion,
        "details": details
    }


def extract_failure_cases(samples: List[Dict], predictions: List[Dict]) -> List[Dict]:
    metrics = evaluate_predictions(samples, predictions)
    sample_map = {item["id"]: item for item in samples}
    pred_map = {item["id"]: item for item in predictions}
    failures = []

    for detail in metrics["details"]:
        if not detail["mismatched_fields"]:
            continue
        sample = sample_map[detail["id"]]
        prediction = pred_map.get(detail["id"], {}).get("prediction", {})
        gt = sample["ground_truth"]
        failures.append({
            "sample_id": detail["id"],
            "input": sample["event_description"],
            "ground_truth": {
                "is_abnormal": gt.get("is_abnormal"),
                "event_type": gt.get("event_type"),
                "risk_level": gt.get("risk_level"),
                "visual_evidence": gt.get("visual_evidence")
            },
            "model_output": {
                "is_abnormal": prediction.get("is_abnormal"),
                "event_type": prediction.get("event_type"),
                "risk_level": prediction.get("risk_level"),
                "visual_evidence": prediction.get("visual_evidence"),
                "suggested_action": prediction.get("suggested_action"),
                "uncertainty": prediction.get("uncertainty")
            },
            "error_type": ", ".join(detail["mismatched_fields"]),
            "possible_reason": infer_failure_reason(detail),
            "improvement": infer_improvement(detail)
        })
    return failures


def infer_failure_reason(detail: Dict) -> str:
    if detail["id"] == "case_008":
        return "夜间睡眠与长时间静止语义相近，模型未充分利用睡眠场景条件。"
    if detail["id"] == "case_007":
        return "短暂跌倒后恢复与普通跌倒边界相近，事件类型粒度不稳定。"
    if detail["id"] == "case_010":
        return "多人正常动作被简化为 normal，未保留 normal_multi_person 细分类别。"
    if detail["id"] == "case_002":
        return "长时间静止但姿态正常，风险等级边界依赖时间段和确认信息。"
    return "当前文本描述信息有限，模型输出与标注字段存在边界差异。"


def infer_improvement(detail: Dict) -> str:
    if detail["id"] == "case_008":
        return "在提示词和知识库中强化睡眠区域、夜间时段与正常睡眠的区分规则。"
    if detail["id"] == "case_007":
        return "增加 fall_recovery 样例，并要求模型区分持续卧倒与短时恢复。"
    if detail["id"] == "case_010":
        return "保留多人场景标签，并在评测中单独统计多人误判。"
    if detail["id"] == "case_002":
        return "补充语音确认结果、历史活动规律或时间段信息，降低风险等级主观性。"
    return "补充样本和字段约束，并对失败样例进行回归测试。"


def save_eval_report(metrics: Dict, path: str = "results/eval_report.md"):
    lines = []
    lines.append("# Evaluation Report")
    lines.append("")
    lines.append("## Overall Metrics")
    lines.append("")
    lines.append(f"- Total samples: {metrics['total']}")
    lines.append(f"- Abnormal detection accuracy: {metrics['abnormal_accuracy']}")
    lines.append(f"- Event type accuracy: {metrics['event_type_accuracy']}")
    lines.append(f"- Risk level accuracy: {metrics['risk_level_accuracy']}")
    lines.append(f"- False alarm rate: {metrics['false_alarm_rate']} ({metrics['false_positive_count']}/{metrics['normal_total']})")
    lines.append(f"- Precision abnormal: {metrics['precision_abnormal']}")
    lines.append(f"- Recall abnormal: {metrics['recall_abnormal']}")
    lines.append(f"- F1 abnormal: {metrics['f1_abnormal']}")
    lines.append(f"- Explanation consistency: {metrics['explanation_consistency']}")
    lines.append(f"- Explanation consistency definition: {metrics['explanation_consistency_definition']}")
    lines.append(f"- Parse error count: {metrics['parse_error_count']}")
    lines.append("")
    lines.append("## Case Details")
    lines.append("")
    lines.append("| ID | Scenario | Abnormal | Event Type | Risk Level | Explanation | Mismatches |")
    lines.append("|---|---|---|---|---|---|---|")

    for item in metrics["details"]:
        mismatches = ", ".join(item["mismatched_fields"]) or "-"
        lines.append(
            f"| {item['id']} | {item['scenario']} | "
            f"{item['abnormal_match']} | {item['event_type_match']} | "
            f"{item['risk_level_match']} | {item['explanation_consistent']} | {mismatches} |"
        )

    Path(path).write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    print("Evaluator module loaded.")
