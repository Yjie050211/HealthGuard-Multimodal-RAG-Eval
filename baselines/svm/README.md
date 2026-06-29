# SVM Baseline

This baseline is a small, runnable sanity check on the current 10 simulated text samples.

## Scope

- Label: `ground_truth.is_abnormal`
- Features: interpretable numeric features extracted from `event_description`
- Model: `StandardScaler + scikit-learn SVC`
- Random seed: 42
- Not implemented: from-scratch SVM optimization solver

## Run

```bash
python baselines/svm/extract_features.py
python baselines/svm/train_svm.py
python baselines/svm/evaluate_svm.py
```

## Outputs

```text
baselines/svm/
├── features.csv
├── model.pkl
├── split.json
└── results/
    ├── predictions.jsonl
    ├── metrics.json
    └── confusion_matrix.png
```

Because the dataset has only 10 samples, the metrics are only proof that the baseline pipeline runs.
