import streamlit as st
import google.generativeai as genai
import time

st.set_page_config(page_title="AI Viết Báo Chuẩn", layout="wide")

# ======================
# SESSION
# ======================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "is_running" not in st.session_state:
    st.session_state.is_running = False

# ======================
# SIDEBAR
# ======================
with st.sidebar:
    st.header("📰 Cấu hình bài báo")

    api_key = st.text_input("Google API Key", type="password")

    style = st.selectbox("Chọn phong cách báo", [
        "Báo Nhân Dân",
        "Báo Quân đội",
        "VnExpress"
    ])

    if api_key:
        genai.configure(api_key=api_key)
        model_name = "models/gemini-2.5-flash"

# ======================
# PROMPT THEO STYLE
# ======================
def build_prompt(style, user_input):

    if style == "Báo Nhân Dân":
        return f"""
Bạn là phóng viên Báo Nhân Dân.

Viết bài báo từ dữ liệu:
{user_input}

YÊU CẦU:
- Văn phong chính luận, trang trọng, định hướng
- Nhấn mạnh chủ trương, kết quả, ý nghĩa
- Có mở bài, thân bài, kết luận rõ
- Cấu trúc 5W1H
- Dùng các cụm: "khẳng định vai trò", "tạo động lực phát triển", "định hướng lâu dài"
- Không giật tít, không câu view
- 400-600 từ
"""

    elif style == "Báo Quân đội":
        return f"""
Bạn là phóng viên Báo Quân đội Nhân dân.

Viết bài báo từ dữ liệu:
{user_input}

YÊU CẦU:
- Văn phong mạnh mẽ, kỷ luật, giàu tinh thần tập thể
- Nhấn mạnh lực lượng, tinh thần, nhiệm vụ
- Có yếu tố hành động, thực tiễn
- Cấu trúc 5W1H
- Dùng cụm: "cán bộ chiến sĩ", "sẵn sàng nhận nhiệm vụ", "phát huy truyền thống"
- Không lan man
- 400-600 từ
"""

    else:  # VnExpress
        return f"""
Bạn là phóng viên VnExpress.

Viết bài báo từ dữ liệu:
{user_input}

YÊU CẦU:
- Văn phong hiện đại, ngắn gọn, dễ đọc
- Câu ngắn, rõ ràng
- Ưu tiên thông tin chính ngay đầu
- Có tiêu đề hấp dẫn
- Cấu trúc 5W1H
- Có thể chia đoạn rõ ràng
- 300-500 từ
"""

# ======================
# UI
# ======================
st.title("📰 AI Viết Báo Chuẩn Tòa Soạn")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Nhập thông tin sự kiện...")

# ======================
# HANDLE
# ======================
if user_input:

    if not api_key:
        st.error("Nhập API key")
        st.stop()

    if st.session_state.is_running:
        st.warning("⏳ Đang xử lý...")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    st.session_state.is_running = True

    try:
        model = genai.GenerativeModel(model_name)

        prompt = build_prompt(style, user_input)

        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_text = ""

            response = model.generate_content(prompt, stream=True)

            for chunk in response:
                if hasattr(chunk, "text") and chunk.text:
                    full_text += chunk.text
                    placeholder.markdown(full_text)
                    time.sleep(0.01)

        st.session_state.messages.append({
            "role": "assistant",
            "content": full_text
        })

        st.download_button("📥 Tải bài báo", full_text, "bai_bao.txt")

    except Exception as e:
        if "429" in str(e):
            st.error("🚫 Quá giới hạn, đợi 60s")
        else:
            st.error(str(e))

    finally:
        st.session_state.is_running = False
