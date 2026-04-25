import os
import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv

# ===== LOAD ENV =====
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("Thiếu GEMINI_API_KEY trong .env")

genai.configure(api_key=API_KEY)

MODEL_NAME = "models/gemini-2.5-flash"

app = FastAPI()

# ===== MEMORY STORE =====
last_request_time = {}
cache = {}

COOLDOWN = 15  # giây

# ===== REQUEST MODEL =====
class RequestData(BaseModel):
    user_id: str
    topic: str
    content: str
    style: str

# ===== AI CALL (retry) =====
def call_ai(prompt, retries=3):
    model = genai.GenerativeModel(MODEL_NAME)
    for i in range(retries):
        try:
            return model.generate_content(prompt)
        except Exception as e:
            if "429" in str(e):
                time.sleep(5)
            else:
                raise e
    return None

# ===== API =====
@app.post("/generate")
def generate(data: RequestData):
    now = time.time()

    # ===== RATE LIMIT =====
    if data.user_id in last_request_time:
        if now - last_request_time[data.user_id] < COOLDOWN:
            raise HTTPException(
                status_code=429,
                detail=f"Đợi {int(COOLDOWN - (now - last_request_time[data.user_id]))}s"
            )

    last_request_time[data.user_id] = now

    # ===== CACHE =====
    cache_key = f"{data.topic}-{data.content}-{data.style}"
    if cache_key in cache:
        return {"result": cache[cache_key], "cached": True}

    # ===== PROMPT =====
    prompt = f"""
Bạn là nhà báo chuyên nghiệp.

Chủ đề: {data.topic}

Dữ liệu:
{data.content}

Yêu cầu:
- Viết theo cấu trúc 5W1H
- 300-500 từ
- Có tiêu đề
- Văn phong: {data.style}
"""

    response = call_ai(prompt)

    if not response or not getattr(response, "text", None):
        raise HTTPException(status_code=500, detail="AI không trả dữ liệu")

    result = response.text

    # lưu cache
    cache[cache_key] = result

    return {"result": result, "cached": False}
