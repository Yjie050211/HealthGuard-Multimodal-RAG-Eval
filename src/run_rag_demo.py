import json
from openai import OpenAI

from config import BASE_URL, LLM_MODEL, require_api_key
from prompts import RAG_QA_SYSTEM_PROMPT, RAG_QA_USER_PROMPT
from rag_pipeline import SimpleHealthRAG
from vlm_client import safe_json_loads


def create_client() -> OpenAI:
    return OpenAI(
        api_key=require_api_key(),
        base_url=BASE_URL
    )


def answer_with_rag(question: str):
    rag = SimpleHealthRAG()
    retrieved = rag.retrieve(question, top_k=2)

    context = "\n\n".join([chunk for chunk, score in retrieved])  # score先扔着，后面做消融再拿出来比

    user_prompt = RAG_QA_USER_PROMPT.format(
        context=context,
        question=question
    )

    client = create_client()
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": RAG_QA_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2
    )

    content = response.choices[0].message.content

    return {
        "question": question,
        "retrieved_context": context,
        "answer": safe_json_loads(content)
    }


if __name__ == "__main__":
    question = "检测到老人疑似跌倒后，系统应该如何处理？"
    result = answer_with_rag(question)
    print(json.dumps(result, ensure_ascii=False, indent=2))
