import json
from pathlib import Path


def load_samples(path="data/samples.json"):
    return json.loads(Path(path).read_text(encoding="utf-8"))

"""
A simple rule-based baseline
"""
def simple_rule_predict(event_description: str):
    text = event_description

    if "倒地" in text or "跌倒" in text:
        return {
            "is_abnormal": True,
            "event_type": "fall",
            "risk_level": "high"
        }

    if "长时间" in text or "超过" in text:
        return {
            "is_abnormal": True,
            "event_type": "long_static",
            "risk_level": "medium"
        }

    if "遮挡" in text or "弱光" in text:
        return {
            "is_abnormal": True,
            "event_type": "occlusion_uncertain",
            "risk_level": "medium"
        }

    return {
        "is_abnormal": False,
        "event_type": "normal",
        "risk_level": "low"
    }


def evaluate_rule_baseline():
    samples = load_samples()
    total = len(samples)
    correct_event_type = 0
    correct_abnormal = 0

    for sample in samples:
        pred = simple_rule_predict(sample["event_description"])
        gt = sample["ground_truth"] # truly

        if pred["is_abnormal"] == gt["is_abnormal"]:
            correct_abnormal += 1

        if pred["event_type"] == gt["event_type"]:
            correct_event_type += 1

    print(f"Total samples: {total}")
    print(f"Abnormal detection accuracy: {correct_abnormal / total:.2f}")
    print(f"Event type accuracy: {correct_event_type / total:.2f}")


if __name__ == "__main__":
    evaluate_rule_baseline()