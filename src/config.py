import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY", "sk-788913e92eb24f5dbc3b9e172b0aff00")
BASE_URL = os.getenv("BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
VLM_MODEL = os.getenv("VLM_MODEL", "qwen-vl-plus")
LLM_MODEL = os.getenv("LLM_MODEL", "qwen-plus")