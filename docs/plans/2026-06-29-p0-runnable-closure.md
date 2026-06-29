# CareEvent P0 Runnable Closure Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a truthful, offline-runnable minimum evaluation loop for the current CareEvent-VLM-RAG-Eval prototype.

**Architecture:** Keep the existing API-based scripts, but add a reproducible offline path that replays the existing real VLM output file, runs local health-knowledge retrieval, generates cited structured answers, computes metrics, and writes standard output artifacts. Security fixes remove hardcoded secrets and make network-dependent API usage explicit.

**Tech Stack:** Python 3.14, standard library, rank-bm25, scikit-learn TF-IDF, existing OpenAI-compatible API client.

---

### P0 Task 1: Remove Secret Defaults

**Files:**
- Modify: `.env.example`
- Modify: `src/config.py`

**Steps:**
1. Replace the example API key with `your_api_key_here`.
2. Remove the hardcoded API key fallback in `src/config.py`.
3. Keep API scripts usable when `API_KEY` is provided via `.env`.
4. Verify with `rg --hidden -n "sk-" . -g "!/.git/**" -g "!/.venv/**"` returning no project secret matches.

**Acceptance:**
- No real-looking API key remains in tracked project files.
- API-dependent scripts fail clearly if no key is configured instead of silently using a committed key.

### P0 Task 2: Add Reproducible Config and Offline Entry

**Files:**
- Create: `config.yaml`
- Create: `run_eval.py`

**Steps:**
1. Add a flat YAML-like config that uses `results/vlm_outputs.jsonl` as offline model output.
2. Implement `python run_eval.py --config config.yaml`.
3. Load samples from `data/samples.json`.
4. Retrieve Top-K knowledge for each sample locally.
5. Generate a deterministic structured answer with internal knowledge references.
6. Write all standard artifacts under `outputs/`.

**Acceptance:**
- `python run_eval.py --config config.yaml` completes without network access.
- It produces `outputs/predictions.jsonl`, `outputs/metrics.json`, `outputs/latency.csv`, `outputs/failure_cases.md`, and `outputs/confusion_matrix.png`.

### P0 Task 3: Strengthen Local RAG

**Files:**
- Modify: `src/rag_pipeline.py`
- Modify: `data/health_knowledge.md`

**Steps:**
1. Expand the health-monitoring knowledge base to 20-50 clearly scoped internal entries.
2. Parse each Markdown section as a retrievable entry with an id/title/source.
3. Add TF-IDF vector retrieval as the default local vectorization path, with BM25 as fallback.
4. Preserve the old simple `retrieve(query, top_k)` API shape for existing scripts.

**Acceptance:**
- At least 20 knowledge entries are available.
- Retrieval returns Top-K entries with ids/titles/scores.
- Existing `python src/rag_pipeline.py` still runs.

### P0 Task 4: Compute Truthful Metrics and Failures

**Files:**
- Modify: `src/evaluator.py`
- Create: `outputs/` artifacts by running the pipeline

**Steps:**
1. Compute abnormal accuracy, event type accuracy, risk level accuracy, false alarm rate, parse errors, and simple field-based explanation consistency.
2. Record latency for retrieval and total offline pipeline; mark model latency as replay/offline rather than API timing.
3. Extract real failure cases from mismatches in current predictions.
4. Generate a confusion matrix PNG without adding unavailable plotting dependencies.

**Acceptance:**
- Metrics are derived from `data/samples.json` and `results/vlm_outputs.jsonl`.
- Failure cases include real sample ids and observed mismatched fields.
- No fabricated experiment numbers are added.

### P0 Task 5: Align Docs and Interview Claims

**Files:**
- Modify: `README.md`
- Modify: `docs/error_analysis.md`
- Create: `docs/audit_report.md`
- Create: `docs/interview_qa.md`
- Create: `docs/ppt_truthfulness_review.md`

**Steps:**
1. Document current implemented, small-scale verified, design-only, and not-yet-implemented features.
2. Replace SVM/ST-GCN/GraphRAG overclaims with truthful boundary wording.
3. Turn error analysis into real failures from current outputs.
4. Add interview talk tracks and Q&A consistent with code evidence.

**Acceptance:**
- README run command matches the actual command.
- Docs explicitly state SVM and ST-GCN are not implemented in this code snapshot.
- GraphRAG is described as knowledge-organization exploration, not a complete system.

### P1 Task 6: SVM Baseline

**Files:**
- Create: `baselines/svm/extract_features.py`
- Create: `baselines/svm/train_svm.py`
- Create: `baselines/svm/evaluate_svm.py`

**Acceptance:**
- Uses scikit-learn `SVC` and `StandardScaler`.
- Clearly states this is not a from-scratch SVM solver.
- Saves predictions, metrics, model, and confusion matrix.

### P1 Task 7: ST-GCN Reproduction Boundary

**Files:**
- Create: `baselines/st_gcn/README.md`

**Acceptance:**
- Records paper/repository candidates and required input tensor format.
- Does not claim training or inference until a real run exists.

### P2 Task 8: Later Graph Extensions

**Files:**
- Future: graph schema, graph visualization, graph database adapter, incremental update notes.

**Acceptance:**
- Only implemented after real graph construction/query evidence exists.
