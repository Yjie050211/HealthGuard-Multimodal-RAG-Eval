import argparse
import csv
import json
import math
import statistics
import struct
import sys
import time
import zlib
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from evaluator import extract_failure_cases, evaluate_predictions, load_jsonl, load_samples, save_eval_report
from rag_pipeline import SimpleHealthRAG


DEFAULT_CONFIG = {
    "mode": "offline_replay",
    "sample_path": "data/samples.json",
    "offline_predictions_path": "results/vlm_outputs.jsonl",
    "knowledge_path": "data/health_knowledge.md",
    "output_dir": "outputs",
    "retrieval_method": "tfidf",
    "retrieval_top_k": 3,
    "include_network_latency": False,
    "random_seed": 42,
}


def parse_scalar(value: str):
    value = value.strip().strip('"').strip("'")
    lowered = value.lower()
    if lowered in {"true", "false"}:
        return lowered == "true"
    try:
        return int(value)
    except ValueError:
        return value


def load_config(path: str) -> Dict:
    config = dict(DEFAULT_CONFIG)
    source = Path(path)
    if not source.exists():
        raise FileNotFoundError(f"Config not found: {source}")
    for raw_line in source.read_text(encoding="utf-8").splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if not line or ":" not in line:
            continue
        key, value = line.split(":", 1)
        config[key.strip()] = parse_scalar(value)
    return config


def build_query(sample: Dict, prediction: Dict) -> str:
    parts = [
        sample.get("event_description", ""),
        prediction.get("event_type", ""),
        prediction.get("risk_level", ""),
        prediction.get("visual_evidence", ""),
    ]
    return " ".join(str(part) for part in parts if part)


def build_structured_answer(sample: Dict, prediction: Dict, retrieved: List[Dict]) -> Dict:
    references = [
        {
            "id": item["id"],
            "title": item["title"],
            "source": item["source"],
            "score": item["score"],
            "score_type": item["score_type"],
        }
        for item in retrieved
    ]
    if retrieved:
        evidence = "；".join(f"{item['id']} {item['title']}" for item in retrieved)
    else:
        evidence = "N/A"

    return {
        "event_type": prediction.get("event_type", "N/A"),
        "visual_evidence": prediction.get("visual_evidence", "N/A"),
        "risk_level": prediction.get("risk_level", "N/A"),
        "recommendation": prediction.get("suggested_action", "N/A"),
        "confidence_or_uncertainty": {
            "confidence": prediction.get("confidence", "N/A"),
            "uncertainty": prediction.get("uncertainty", "N/A"),
        },
        "knowledge_basis_summary": evidence,
        "knowledge_reference": references,
        "traceable": bool(references),
    }


def percentile(values: List[float], pct: float):
    if not values:
        return "N/A"
    ordered = sorted(values)
    index = math.ceil((pct / 100) * len(ordered)) - 1
    index = max(0, min(index, len(ordered) - 1))
    return round(ordered[index], 4)


def latency_summary(records: List[Dict]) -> Dict:
    retrieval = [float(item["retrieval_latency_ms"]) for item in records]
    total = [float(item["total_latency_ms"]) for item in records]
    return {
        "model_latency": "offline_replay_not_api_latency",
        "retrieval_latency_ms": {
            "mean": round(statistics.mean(retrieval), 4) if retrieval else "N/A",
            "median": round(statistics.median(retrieval), 4) if retrieval else "N/A",
            "p95": percentile(retrieval, 95),
        },
        "total_latency_ms": {
            "mean": round(statistics.mean(total), 4) if total else "N/A",
            "median": round(statistics.median(total), 4) if total else "N/A",
            "p95": percentile(total, 95),
        },
        "includes_network_request": False,
        "test_count": len(records),
    }


def write_json(path: Path, data: Dict):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def write_jsonl(path: Path, records: Iterable[Dict]):
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def write_latency_csv(path: Path, rows: List[Dict]):
    fieldnames = [
        "sample_id",
        "mode",
        "model_latency_ms",
        "retrieval_latency_ms",
        "total_latency_ms",
        "includes_network_request",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_failure_cases(path: Path, failures: List[Dict]):
    lines = ["# Failure Cases", ""]
    if not failures:
        lines.append("当前预测与标注字段完全匹配，未提取到失败案例。")
    for index, item in enumerate(failures, 1):
        gt = item["ground_truth"]
        pred = item["model_output"]
        lines.extend([
            f"## Case {index}: {item['sample_id']}",
            "",
            f"- 样例ID：{item['sample_id']}",
            f"- 输入：{item['input']}",
            f"- 真实标签：is_abnormal={gt['is_abnormal']}, event_type={gt['event_type']}, risk_level={gt['risk_level']}",
            f"- 模型输出：is_abnormal={pred['is_abnormal']}, event_type={pred['event_type']}, risk_level={pred['risk_level']}",
            f"- 错误类型：{item['error_type']}",
            f"- 可能原因：{item['possible_reason']}",
            f"- 改进方向：{item['improvement']}",
            "",
        ])
    path.write_text("\n".join(lines), encoding="utf-8")


def png_chunk(tag: bytes, data: bytes) -> bytes:
    return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)


FONT = {
    "0": ["111", "101", "101", "101", "111"],
    "1": ["010", "110", "010", "010", "111"],
    "2": ["111", "001", "111", "100", "111"],
    "3": ["111", "001", "111", "001", "111"],
    "4": ["101", "101", "111", "001", "001"],
    "5": ["111", "100", "111", "001", "111"],
    "6": ["111", "100", "111", "101", "111"],
    "7": ["111", "001", "001", "001", "001"],
    "8": ["111", "101", "111", "101", "111"],
    "9": ["111", "101", "111", "001", "111"],
}


def draw_digit(canvas, x: int, y: int, digit: str, color=(20, 20, 20), scale: int = 3):
    pattern = FONT.get(digit)
    if not pattern:
        return
    height = len(canvas)
    width = len(canvas[0])
    for row_index, row in enumerate(pattern):
        for col_index, bit in enumerate(row):
            if bit != "1":
                continue
            for dy in range(scale):
                for dx in range(scale):
                    px = x + col_index * scale + dx
                    py = y + row_index * scale + dy
                    if 0 <= px < width and 0 <= py < height:
                        canvas[py][px] = color


def draw_number(canvas, x: int, y: int, value: int, color=(20, 20, 20), scale: int = 3):
    for offset, digit in enumerate(str(value)):
        draw_digit(canvas, x + offset * (4 * scale), y, digit, color=color, scale=scale)


def write_confusion_matrix_png(path: Path, confusion: Dict[str, Dict[str, int]]):
    labels = sorted(set(confusion.keys()) | {pred for row in confusion.values() for pred in row.keys()})
    size = max(1, len(labels))
    cell = 42
    margin = 64
    width = margin + size * cell + 20
    height = margin + size * cell + 20
    canvas = [[(255, 255, 255) for _ in range(width)] for _ in range(height)]
    max_count = max([count for row in confusion.values() for count in row.values()] or [1])

    for row_index, gt_label in enumerate(labels):
        draw_number(canvas, 8, margin + row_index * cell + 14, row_index + 1, color=(20, 20, 20), scale=2)
        draw_number(canvas, margin + row_index * cell + 14, 8, row_index + 1, color=(20, 20, 20), scale=2)
        for col_index, pred_label in enumerate(labels):
            count = confusion.get(gt_label, {}).get(pred_label, 0)
            intensity = int(255 - (190 * count / max_count))
            color = (intensity, intensity + 20 if intensity < 235 else 255, 255)
            x0 = margin + col_index * cell
            y0 = margin + row_index * cell
            for y in range(y0, y0 + cell - 2):
                for x in range(x0, x0 + cell - 2):
                    canvas[y][x] = color
            if count:
                draw_number(canvas, x0 + 14, y0 + 14, count, color=(0, 0, 0), scale=3)

    raw = b"".join(b"\x00" + b"".join(bytes(pixel) for pixel in row) for row in canvas)
    png = b"\x89PNG\r\n\x1a\n"
    png += png_chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
    png += png_chunk(b"IDAT", zlib.compress(raw, 9))
    png += png_chunk(b"IEND", b"")
    path.write_bytes(png)
    write_json(path.with_name("confusion_matrix_labels.json"), {
        "note": "PNG uses numeric class indexes because no plotting/font dependency is required.",
        "labels": {str(index + 1): label for index, label in enumerate(labels)},
    })


def run(config: Dict):
    root = Path(__file__).resolve().parent
    output_dir = root / str(config["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)

    samples = load_samples(str(root / str(config["sample_path"])))
    predictions = load_jsonl(str(root / str(config["offline_predictions_path"])))
    if len(predictions) != len(samples):
        raise RuntimeError(f"Prediction count ({len(predictions)}) does not match sample count ({len(samples)}).")

    pred_map = {item["id"]: item for item in predictions}
    rag = SimpleHealthRAG(
        knowledge_path=str(root / str(config["knowledge_path"])),
        method=str(config["retrieval_method"]),
    )

    enriched_records = []
    latency_rows = []
    for sample in samples:
        start_total = time.perf_counter()
        pred_record = pred_map[sample["id"]]
        prediction = pred_record.get("prediction", {})

        query = build_query(sample, prediction)
        start_retrieval = time.perf_counter()
        retrieved = rag.retrieve_entries(query, top_k=int(config["retrieval_top_k"]))
        retrieval_ms = (time.perf_counter() - start_retrieval) * 1000

        structured_answer = build_structured_answer(sample, prediction, retrieved)
        total_ms = (time.perf_counter() - start_total) * 1000

        latency = {
            "sample_id": sample["id"],
            "mode": config["mode"],
            "model_latency_ms": "offline_replay",
            "retrieval_latency_ms": round(retrieval_ms, 4),
            "total_latency_ms": round(total_ms, 4),
            "includes_network_request": bool(config["include_network_latency"]),
        }
        latency_rows.append(latency)

        enriched_records.append({
            "sample_id": sample["id"],
            "id": sample["id"],
            "input_path": sample.get("image_path", ""),
            "input_type": sample.get("input_type", ""),
            "event_description": sample.get("event_description", ""),
            "prediction": prediction,
            "structured_answer": structured_answer,
            "retrieved_knowledge": retrieved,
            "ground_truth": sample["ground_truth"],
            "latency": latency,
        })

    metrics = evaluate_predictions(samples, enriched_records)
    metrics["latency"] = latency_summary(latency_rows)
    metrics["run"] = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "mode": config["mode"],
        "sample_path": config["sample_path"],
        "offline_predictions_path": config["offline_predictions_path"],
        "knowledge_path": config["knowledge_path"],
        "retrieval_method": config["retrieval_method"],
        "retrieval_top_k": config["retrieval_top_k"],
    }

    failures = extract_failure_cases(samples, enriched_records)

    write_jsonl(output_dir / "predictions.jsonl", enriched_records)
    write_json(output_dir / "metrics.json", metrics)
    write_latency_csv(output_dir / "latency.csv", latency_rows)
    write_failure_cases(output_dir / "failure_cases.md", failures)
    write_confusion_matrix_png(output_dir / "confusion_matrix.png", metrics["confusion_matrix"])
    save_eval_report(metrics, str(output_dir / "eval_report.md"))

    print(json.dumps({
        "output_dir": str(output_dir),
        "total": metrics["total"],
        "abnormal_accuracy": metrics["abnormal_accuracy"],
        "event_type_accuracy": metrics["event_type_accuracy"],
        "risk_level_accuracy": metrics["risk_level_accuracy"],
        "false_alarm_rate": metrics["false_alarm_rate"],
        "failure_cases": len(failures),
    }, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Run offline CareEvent evaluation.")
    parser.add_argument("--config", default="config.yaml", help="Path to config.yaml")
    args = parser.parse_args()
    run(load_config(args.config))


if __name__ == "__main__":
    main()
