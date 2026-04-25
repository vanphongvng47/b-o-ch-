import streamlit as st
import google.generativeai as genai
import time

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="AI Phóng Viên Chat", layout="wide")

# =========================
# SESSION STATE
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "is_running" not in st.session_state:
    st.session_state.is_running = False

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.header("⚙️ Cấu hình")

    api_key = st.text_input("Google API Key", type="password")

    selected_model = ""

    if api_key:
        try:
            genai.configure(api_key=api_key)

            models = genai.list_models()
            available_models = [
                m.name for m in models
                if hasattr(m, "supported_generation_methods")
                and any("generate" in method.lower() for method in m.supported_generation_methods)
            ]

            # ưu tiên flash
            preferred = [m for m in available_models if "flash" in m.lower()]
            if preferred:
                available_models = preferred

            if available_models:
                selected_model = st.selectbox("Model", available_models)

        except Exception as e:
            st.error(f"Lỗi API key: {e}")

    st.divider()
    if st.button("🧹 Xoá hội thoại"):
        st.session_state.messages = []

# =========================
# HEADER
# =========================
st.title("📰 AI Phóng Viên Chat")
st.caption("Trải nghiệm mượt như ChatGPT")

# =========================
# HIỂN THỊ CHAT
# =========================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# =========================
# INPUT
# =========================
user_input = st.chat_input("Nhập nội dung bài báo...")

# =========================
# HANDLE CHAT
# =========================
if user_input:

    if not api_key:
        st.error("Nhập API key trước")
        st.stop()

    if not selected_model:
        st.error("Chưa chọn model")
        st.stop()

    if st.session_state.is_running:
        st.warning("⏳ Đang xử lý...")
        st.stop()

    # lưu user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # hiển thị user message
    with st.chat_message("user"):
        st.markdown(user_input)

    st.session_state.is_running = True

    try:
        model = genai.GenerativeModel(model_name=selected_model)

        # prompt chuẩn báo chí
        prompt = f"""
Bạn là nhà báo chuyên nghiệp.

Viết bài báo từ nội dung sau:
{user_input}

Yêu cầu:
- Theo cấu trúc 5W1H
- Có tiêu đề
- 300-500 từ
- Văn phong báo chí
"""

        # placeholder cho streaming
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_text = ""

            response = model.generate_content(prompt, stream=True)

            for chunk in response:
                if hasattr(chunk, "text") and chunk.text:
                    for char in chunk.text:
                        full_text += char
                        message_placeholder.markdown(full_text)
                        time.sleep(0.005)

        # lưu assistant message
        st.session_state.messages.append({
            "role": "assistant",
            "content": full_text
        })

    except Exception as e:
        if "429" in str(e):
            st.error("🚫 Quá giới hạn, đợi ~60s rồi thử lại")
        else:
            st.error(str(e))

    finally:
        st.session_state.is_running = False
