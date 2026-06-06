from rag_pipeline import SimpleRAG
from prompts import EVENT_UNDERSTANDING_PROMPT, RAG_QA_PROMPT


def main():
    event_description = "老人从站立状态突然倒地，随后长时间未恢复站立。"

    print("=== Step 1: Event Understanding Prompt ===")
    print(EVENT_UNDERSTANDING_PROMPT.format(
        event_description=event_description
    ))

    print("\n=== Step 2: Retrieve Care Knowledge ===")
    rag = SimpleRAG()
    retrieved = rag.retrieve("老人跌倒后应该如何处理？", top_k=2)

    context = "\n\n".join([chunk for chunk, score in retrieved])
    print(context)

    print("\n=== Step 3: RAG QA Prompt ===")
    print(RAG_QA_PROMPT.format(
        context=context,
        question="检测到疑似跌倒后，系统应如何给出建议？"
    ))


if __name__ == "__main__":
    main()