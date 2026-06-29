# System Architecture

当前代码快照的真实架构如下：

```text
Input Layer
├── Simulated text event descriptions
└── Local health-monitoring knowledge base

Event Understanding Layer
├── Offline replay of saved Qwen-compatible API outputs
└── API client for optional rerun when API_KEY is configured

Knowledge Retrieval Layer
├── Markdown knowledge entries
├── TF-IDF character vector retrieval
└── BM25 fallback

Answer Layer
├── Event type
├── Visual/event evidence
├── Risk level
├── Suggested action
└── Internal knowledge references

Evaluation Layer
├── Abnormal detection accuracy
├── Event type accuracy
├── Risk level accuracy
├── False alarm rate
├── Precision / Recall / F1
├── Field-based explanation consistency
├── Offline latency record
└── Failure case extraction
```

## Boundary

- SVM baseline is planned but not implemented.
- ST-GCN is planned as a future open-source reproduction task; no inference/training evidence exists in this snapshot.
- GraphRAG is a future extension. Current code has no graph database, no entity-relation graph construction, and no graph traversal retrieval.
