import csv
import json
import sys
from pathlib import Path

import joblib
from sklearn.metrics import accuracy_score, confusion_matrix, precision_recall_fscore_support

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from run_eval import write_confusion_matrix_png
from train_svm import MODEL_PATH, SPLIT_PATH, read_feature_rows


BASE_DIR = Path(__file__).resolve().parent
RESULT_DIR = BASE_DIR / "results"


def main():
    if not MODEL_PATH.exists() or not SPLIT_PATH.exists():
        raise RuntimeError("Run train_svm.py before evaluate_svm.py")

    bundle = joblib.load(MODEL_PATH)
    split = json.loads(SPLIT_PATH.read_text(encoding="utf-8"))
    rows = read_feature_rows()
    row_map = {row["sample_id"]: row for row in rows}
    feature_columns = bundle["feature_columns"]
    test_ids = split["test_ids"]

    x_test = [[float(row_map[sample_id][column]) for column in feature_columns] for sample_id in test_ids]
    y_true = [int(row_map[sample_id]["label_is_abnormal"]) for sample_id in test_ids]
    y_pred = [int(value) for value in bundle["model"].predict(x_test)]

    precision, recall, f1, _ = precision_recall_fscore_support(
        y_true,
        y_pred,
        average="binary",
        zero_division=0,
    )
    accuracy = accuracy_score(y_true, y_pred)
    matrix = confusion_matrix(y_true, y_pred, labels=[0, 1])

    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    predictions = []
    for sample_id, true_label, pred_label in zip(test_ids, y_true, y_pred):
        predictions.append({
            "sample_id": sample_id,
            "true_is_abnormal": bool(true_label),
            "pred_is_abnormal": bool(pred_label),
            "correct": true_label == pred_label,
        })

    (RESULT_DIR / "predictions.jsonl").write_text(
        "\n".join(json.dumps(item, ensure_ascii=False) for item in predictions) + "\n",
        encoding="utf-8",
    )
    metrics = {
        "implementation": bundle["implementation"],
        "label": bundle["label"],
        "train_ids": split["train_ids"],
        "test_ids": test_ids,
        "feature_columns": feature_columns,
        "accuracy": round(float(accuracy), 4),
        "precision": round(float(precision), 4),
        "recall": round(float(recall), 4),
        "f1": round(float(f1), 4),
        "confusion_matrix_labels": ["normal", "abnormal"],
        "confusion_matrix": matrix.tolist(),
        "note": "Only 10 simulated text samples are available; this is a runnable baseline sanity check, not a reliable model result.",
    }
    (RESULT_DIR / "metrics.json").write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    write_confusion_matrix_png(
        RESULT_DIR / "confusion_matrix.png",
        {
            "normal": {
                "normal": int(matrix[0][0]),
                "abnormal": int(matrix[0][1]),
            },
            "abnormal": {
                "normal": int(matrix[1][0]),
                "abnormal": int(matrix[1][1]),
            },
        },
    )

    print(json.dumps(metrics, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
