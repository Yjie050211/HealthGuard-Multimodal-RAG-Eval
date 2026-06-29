import json
from pathlib import Path
from tqdm import tqdm

from evaluator import load_samples, evaluate_predictions, save_eval_report
from vlm_client import analyze_event_with_llm


def ensure_dir(path: str):
    Path(path).mkdir(parents=True, exist_ok=True)


def run_vlm_on_samples():
    ensure_dir("results")

    samples = load_samples("data/samples.json")
    output_path = Path("results/vlm_outputs.jsonl")

    predictions = []

    # 逐条推，结果边跑边写 JSONL（一行一个 JSON），断了也能保留已跑完的
    with output_path.open("w", encoding="utf-8") as f:
        for sample in tqdm(samples, desc="Running VLM/LLM evaluation"):
            pred = analyze_event_with_llm(sample["event_description"])

            record = {
                "id": sample["id"],
                "scenario": sample["scenario"],
                "event_description": sample["event_description"],
                "prediction": pred,
                "ground_truth": sample["ground_truth"]
            }

            predictions.append(record)
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    return samples, predictions


def main():
    # 三步走：VLM 批量推理 → 评测 → 出报告
    samples, predictions = run_vlm_on_samples()
    metrics = evaluate_predictions(samples, predictions)

    save_eval_report(metrics, "results/eval_report.md")

    print(json.dumps(metrics, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()