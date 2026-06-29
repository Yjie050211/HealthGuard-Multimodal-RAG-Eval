import csv
import json
from pathlib import Path
from typing import Dict, List


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SAMPLE_PATH = PROJECT_ROOT / "data" / "samples.json"
FEATURE_PATH = Path(__file__).resolve().parent / "features.csv"


KEYWORDS = {
    "fall_keyword_count": ["跌倒", "摔倒", "倒地", "卧倒"],
    "static_keyword_count": ["静止", "未明显移动", "没有明显移动", "长时间", "很久"],
    "night_keyword_count": ["夜间", "晚上", "光线较暗"],
    "bed_sleep_keyword_count": ["床", "平躺", "睡眠"],
    "occlusion_keyword_count": ["遮挡", "家具", "只能看到", "无法判断"],
    "low_visibility_keyword_count": ["弱光", "模糊", "光线较暗", "轮廓"],
    "wandering_keyword_count": ["徘徊", "反复", "来回", "走廊"],
    "multi_person_keyword_count": ["两个人", "多人", "另一人"],
    "recovery_keyword_count": ["自行站起", "继续正常行走", "恢复"],
    "posture_keyword_count": ["前倾", "低头", "姿态", "坐姿"],
}


def load_samples(path: Path = SAMPLE_PATH) -> List[Dict]:
    return json.loads(path.read_text(encoding="utf-8"))


def keyword_count(text: str, words: List[str]) -> int:
    return sum(text.count(word) for word in words)


def extract_feature_row(sample: Dict) -> Dict:
    text = sample["event_description"]
    row = {
        "sample_id": sample["id"],
        "label_is_abnormal": int(sample["ground_truth"]["is_abnormal"]),
        "event_type": sample["ground_truth"]["event_type"],
        "risk_level": sample["ground_truth"]["risk_level"],
        "char_length": len(text),
        "digit_count": sum(char.isdigit() for char in text),
        "has_time_signal": int(any(token in text for token in ["分钟", "小时", "超过", "长时间"])),
        "has_uncertainty_signal": int(any(token in text for token in ["疑似", "无法", "难以", "可能"])),
    }
    for feature_name, words in KEYWORDS.items():
        row[feature_name] = keyword_count(text, words)
    return row


def write_features(samples: List[Dict], output_path: Path = FEATURE_PATH) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    rows = [extract_feature_row(sample) for sample in samples]
    fieldnames = list(rows[0].keys())
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return output_path


def main():
    output_path = write_features(load_samples())
    print(f"wrote {output_path}")


if __name__ == "__main__":
    main()
