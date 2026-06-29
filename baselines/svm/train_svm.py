import csv
import json
from pathlib import Path

import joblib
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

from extract_features import FEATURE_PATH, load_samples, write_features


BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model.pkl"
SPLIT_PATH = BASE_DIR / "split.json"
RANDOM_SEED = 42


def read_feature_rows(path: Path = FEATURE_PATH):
    if not path.exists():
        write_features(load_samples(), path)
    with path.open("r", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def get_feature_columns(rows):
    excluded = {"sample_id", "label_is_abnormal", "event_type", "risk_level"}
    return [name for name in rows[0].keys() if name not in excluded]


def main():
    rows = read_feature_rows()
    feature_columns = get_feature_columns(rows)
    sample_ids = [row["sample_id"] for row in rows]
    x = [[float(row[column]) for column in feature_columns] for row in rows]
    y = [int(row["label_is_abnormal"]) for row in rows]

    train_ids, test_ids, x_train, x_test, y_train, y_test = train_test_split(
        sample_ids,
        x,
        y,
        test_size=0.3,
        random_state=RANDOM_SEED,
        stratify=y,
    )

    model = Pipeline([
        ("scaler", StandardScaler()),
        ("svc", SVC(kernel="linear", class_weight="balanced", random_state=RANDOM_SEED)),
    ])
    model.fit(x_train, y_train)

    joblib.dump({
        "model": model,
        "feature_columns": feature_columns,
        "label": "ground_truth.is_abnormal",
        "implementation": "scikit-learn SVC; not a from-scratch SVM solver",
        "random_seed": RANDOM_SEED,
    }, MODEL_PATH)

    SPLIT_PATH.write_text(json.dumps({
        "random_seed": RANDOM_SEED,
        "train_ids": train_ids,
        "test_ids": test_ids,
        "label": "ground_truth.is_abnormal",
        "feature_columns": feature_columns,
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps({
        "model_path": str(MODEL_PATH),
        "split_path": str(SPLIT_PATH),
        "train_size": len(train_ids),
        "test_size": len(test_ids),
        "feature_count": len(feature_columns),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
