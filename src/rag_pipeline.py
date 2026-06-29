from pathlib import Path
from typing import Dict, List, Tuple

from rank_bm25 import BM25Okapi
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def _split_heading(line: str, fallback_id: str) -> Tuple[str, str]:
    heading = line.strip()
    parts = heading.split(maxsplit=1)
    if parts and parts[0].upper().startswith("K") and parts[0][1:].isdigit():
        return parts[0].upper(), parts[1] if len(parts) > 1 else parts[0].upper()
    return fallback_id, heading


def load_knowledge_entries(path: str = "data/health_knowledge.md") -> List[Dict]:
    """Load Markdown sections as retrieval entries with stable local source ids."""
    text = Path(path).read_text(encoding="utf-8")
    entries: List[Dict] = []
    current_heading = None
    current_lines: List[str] = []

    def flush():
        if not current_heading:
            return
        body = "\n".join(current_lines).strip()
        if not body:
            return
        source_id, title = _split_heading(current_heading, f"K{len(entries) + 1:03d}")
        entries.append({
            "id": source_id,
            "title": title,
            "content": body,
            "source": f"health_knowledge.md#{source_id}",
            "text": f"{source_id} {title}\n\n{body}",
        })

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if line.startswith("## "):
            flush()
            current_heading = line[3:].strip()
            current_lines = []
        elif current_heading:
            current_lines.append(line)

    flush()
    return entries


def load_knowledge(path: str = "data/health_knowledge.md") -> List[str]:
    """Backward-compatible helper returning only retrieval chunk text."""
    return [entry["text"] for entry in load_knowledge_entries(path)]


def tokenize_zh(text: str):
    """Simple character-level tokenization for BM25 fallback."""
    return list(text)


class SimpleHealthRAG:
    def __init__(self, knowledge_path: str = "data/health_knowledge.md", method: str = "tfidf"):
        self.knowledge_path = knowledge_path
        self.method = method
        self.entries = load_knowledge_entries(knowledge_path)
        self.chunks = [entry["text"] for entry in self.entries]
        self.tokenized_chunks = [tokenize_zh(chunk) for chunk in self.chunks]
        self.bm25 = BM25Okapi(self.tokenized_chunks)
        self.vectorizer = TfidfVectorizer(analyzer="char", ngram_range=(1, 2))
        self.tfidf_matrix = self.vectorizer.fit_transform(self.chunks) if self.chunks else None

    def retrieve_entries(self, query: str, top_k: int = 2) -> List[Dict]:
        if not self.entries:
            return []

        if self.method == "tfidf" and self.tfidf_matrix is not None:
            query_vec = self.vectorizer.transform([query])
            scores = cosine_similarity(query_vec, self.tfidf_matrix)[0]
            score_name = "tfidf_cosine"
        else:
            scores = self.bm25.get_scores(tokenize_zh(query))
            score_name = "bm25"

        ranked = sorted(
            zip(self.entries, scores),
            key=lambda item: float(item[1]),
            reverse=True
        )

        results = []
        for entry, score in ranked[:top_k]:
            item = dict(entry)
            item["score"] = round(float(score), 6)
            item["score_type"] = score_name
            results.append(item)
        return results

    def retrieve(self, query: str, top_k: int = 2):
        """Backward-compatible API returning (chunk_text, score)."""
        return [(entry["text"], entry["score"]) for entry in self.retrieve_entries(query, top_k)]


if __name__ == "__main__":
    rag = SimpleHealthRAG()
    results = rag.retrieve_entries("老人跌倒后应该如何处理？", top_k=2)

    for item in results:
        print("SOURCE:", item["source"])
        print("TITLE:", item["title"])
        print("SCORE:", item["score"])
        print(item["content"])
        print("-" * 80)
