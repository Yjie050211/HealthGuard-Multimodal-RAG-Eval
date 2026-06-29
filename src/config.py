import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
# VLM 用于多模态（图+文），LLM 用于纯文本 RAG 问答
VLM_MODEL = os.getenv("VLM_MODEL", "qwen-vl-plus")
LLM_MODEL = os.getenv("LLM_MODEL", "qwen-plus")


def require_api_key() -> str:
    """Return the configured API key or fail before any network request."""
    if not API_KEY or API_KEY == "your_api_key_here":
        raise RuntimeError("API_KEY is not configured. Copy .env.example to .env and set your own key.")
    return API_KEY
