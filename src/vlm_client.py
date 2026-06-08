import json
from openai import OpenAI

from config import API_KEY, BASE_URL, VLM_MODEL, LLM_MODEL
from prompts import EVENT_UNDERSTANDING_SYSTEM_PROMPT, EVENT_UNDERSTANDING_USER_PROMPT


client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)


def safe_json_loads(text: str) -> dict:
    """
    尽量从模型输出中解析 JSON。
    如果模型输出包含 markdown 代码块，也尝试清洗。
    """
    text = text.strip()

    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {
            "parse_error": True,
            "raw_output": text
        }


def analyze_event_with_llm(event_description: str, model: str = None) -> dict:
    """
    # 路线 A 的低成本版本：
    先用文本化事件描述调用 LLM/VLM API，验证结构化输出流程。
    后续如果有图像，再扩展 image_url / base64 输入。
    """
    model = model or VLM_MODEL

    user_prompt = EVENT_UNDERSTANDING_USER_PROMPT.format(
        event_description=event_description
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": EVENT_UNDERSTANDING_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2
    )

    content = response.choices[0].message.content
    return safe_json_loads(content)


if __name__ == "__main__":
    demo = "老人从站立状态突然倒地，随后长时间未恢复站立。"
    result = analyze_event_with_llm(demo)
    print(json.dumps(result, ensure_ascii=False, indent=2))