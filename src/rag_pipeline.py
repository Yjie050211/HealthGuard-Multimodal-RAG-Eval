from pathlib import Path
from rank_bm25 import BM25Okapi

def load_knowledge(path: str = "data/care_knowledge.md"):
    text = Path(path).read_text(encoding="utf-8")
    chunks = [chunk.strip() for chunk in text.split("## ") if chunk.strip()]
    return chunks

def tokenize(text: str):
    # 简单字符级切分，适合中文最小原型；后续可替换为jieba或embedding检索
    return list(text)

class SimpleRAG:
    def __init__(self, knowledge_path: str = "data/care_knowledge.md"):
        self.chunks = load_knowledge(knowledge_path)
        self.tokenized_chunks = [tokenize(chunk) for chunk in self.chunks]
        self.bm25 = BM25Okapi(self.tokenized_chunks)

    def retrieve(self, query: str, top_k: int = 2): # 最相关的前top_k个片段
        scores = self.bm25.get_scores(tokenize(query))
        ranked = sorted(
            zip(self.chunks, scores),
            key=lambda x: x[1],
            reverse=True
        )
        return ranked[:top_k]

if __name__ == "__main__":
    rag = SimpleRAG()
    results = rag.retrieve("老人跌倒后应该如何处理？")
    for chunk, score in results:
        print("SCORE:", score)
        print(chunk)
        print("-" * 60)