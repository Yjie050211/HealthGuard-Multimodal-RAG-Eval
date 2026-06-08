import json
from pathlib import Path
from typing import Dict, List # 类型提示


def load_samples(path: str = "data/samples.json") -> List[Dict]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def normalize_bool(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in ["true", "yes", "1", "是"]
    return False


def evaluate_predictions(samples: List[Dict], predictions: List[Dict]) -> Dict:
    total = len(samples)

    abnormal_correct = 0
    event_type_correct = 0
    risk_level_correct = 0
    parse_error_count = 0

    details = []

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

        abnormal_match = gt_abnormal == pred_abnormal
        event_type_match = gt_event_type == pred_event_type
        risk_level_match = gt_risk_level == pred_risk_level

        abnormal_correct += int(abnormal_match)
        event_type_correct += int(event_type_match)
        risk_level_correct += int(risk_level_match)

        details.append({
            "id": sid,
            "scenario": sample["scenario"],
            "abnormal_match": abnormal_match,
            "event_type_match": event_type_match,
            "risk_level_match": risk_level_match,
            "gt_event_type": gt_event_type,
            "pred_event_type": pred_event_type,
            "gt_risk_level": gt_risk_level,
            "pred_risk_level": pred_risk_level
        })

    return {
        "total": total,
        "abnormal_accuracy": round(abnormal_correct / total, 4) if total else 0,
        "event_type_accuracy": round(event_type_correct / total, 4) if total else 0,
        "risk_level_accuracy": round(risk_level_correct / total, 4) if total else 0,
        "parse_error_count": parse_error_count,
        "details": details
    }


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
    lines.append(f"- Parse error count: {metrics['parse_error_count']}")
    lines.append("")
    lines.append("## Case Details")
    lines.append("")
    lines.append("| ID | Scenario | Abnormal | Event Type | Risk Level |")
    lines.append("|---|---|---|---|---|")

    for item in metrics["details"]:
        lines.append(
            f"| {item['id']} | {item['scenario']} | "
            f"{item['abnormal_match']} | {item['event_type_match']} | {item['risk_level_match']} |"
        )

    Path(path).write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    print("Evaluator module loaded.")