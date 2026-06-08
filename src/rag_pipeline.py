from pathlib import Path
from rank_bm25 import BM25Okapi


def load_knowledge(path: str = "data/health_knowledge.md"):
    text = Path(path).read_text(encoding="utf-8")
    raw_chunks = text.split("## ")
    chunks = []

    for chunk in raw_chunks:
        chunk = chunk.strip()
        if not chunk:
            continue
        if chunk.startswith("#"):
            continue
        chunks.append(chunk)

    return chunks


def tokenize_zh(text: str):
    """
    简易中文字符级 tokenization。
    后续可替换为 jieba、bge embedding 或向量数据库。
    """
    return list(text)


class SimpleHealthRAG:
    def __init__(self, knowledge_path: str = "data/health_knowledge.md"):
        self.chunks = load_knowledge(knowledge_path)
        self.tokenized_chunks = [tokenize_zh(chunk) for chunk in self.chunks]
        self.bm25 = BM25Okapi(self.tokenized_chunks)

    def retrieve(self, query: str, top_k: int = 2):
        scores = self.bm25.get_scores(tokenize_zh(query))
        ranked = sorted(
            zip(self.chunks, scores),
            key=lambda x: x[1],
            reverse=True
        )
        return ranked[:top_k]


if __name__ == "__main__":
    rag = SimpleHealthRAG()
    results = rag.retrieve("老人跌倒后应该如何处理？", top_k=2)

    for chunk, score in results:
        print("SCORE:", round(float(score), 4))
        print(chunk)
        print("-" * 80)