# System Architecture

```text
Input Layer
├── Public image/video samples
├── Simulated event descriptions
└── Care knowledge documents

Event Understanding Layer
├── Rule baseline
├── ST-GCN / SVM baseline
└── Vision-Language Model

Knowledge Layer
├── Care knowledge base
├── BM25 / vector retrieval
└── LightRAG / GraphRAG extension

Decision Layer
├── Abnormal event type
├── Risk level
├── Evidence explanation
└── Suggested action

Evaluation Layer
├── Accuracy
├── Recall
├── Explanation consistency
├── Knowledge traceability
└── Error analysis
```
