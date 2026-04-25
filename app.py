import streamlit as st
import google.generativeai as genai
import time

# Cấu hình giao diện chuẩn tòa soạn
st.set_page_config(page_title="AI Phóng Viên Tòa Soạn", layout="wide")

if "messages" not in st.session_state:
    st.session_state.messages = []

# ======================
# SIDEBAR: GIẢI QUYẾT LỖI 404 & 400
# ======================
with st.sidebar:
    st.header("📰 Cấu hình tòa soạn")
    api_key = st.text_input("Nhập Google API Key mới", type="password")
    
    style = st.selectbox("Chọn phong cách báo", [
        "Báo Nhân Dân",
        "Báo Quân đội Nhân dân",
        "VnExpress"
    ])

    # TỰ ĐỘNG CHỌN MODEL ĐÚNG (Fix lỗi 404)
    model_choice = "models/gemini-2.0-flash" # Mặc định an toàn
    if api_key:
        try:
            genai.configure(api_key=api_key)
            # Lấy danh sách model thực tế từ tài khoản của bạn
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            if available_models:
                # Ưu tiên các dòng Flash (2.0 hoặc 1.5) để tránh lỗi 429
                flash_models = [m for m in available_models if "flash" in m]
                model_choice = st.selectbox("Chọn Model AI", flash_models if flash_models else available_models)
        except Exception:
            st.error("API Key không hợp lệ hoặc đang bị Google tạm khóa.")

# ======================
# PROMPT CHUẨN 5W1H & CẢM XÚC
# ======================
def build_prompt(style, user_input):
    base_instruction = "Viết bài báo đầy đủ 5W1H (Who, What, Where, When, Why, How). Văn phong mạch lạc, giàu cảm xúc, khắc họa sự chuyển mình mạnh mẽ."
    
    if style == "Báo Nhân Dân":
        return f"Bạn là phóng viên Báo Nhân Dân. Viết về: {user_input}. {base_instruction} Phong cách chính luận, trang trọng, dùng cụm 'khẳng định vai trò', 'tạo động lực'."
    elif style == "Báo Quân đội Nhân dân":
        return f"Bạn là phóng viên Báo Quân đội. Viết về: {user_input}. {base_instruction} Phong cách mạnh mẽ, kỷ luật, dùng cụm 'sẵn sàng nhiệm vụ', 'tinh thần chiến sĩ'."
    else: # VnExpress
        return f"Bạn là phóng viên VnExpress. Viết về: {user_input}. {base_instruction} Phong cách hiện đại, câu ngắn gọn, tiêu đề hấp dẫn."

# ======================
# GIAO DIỆN CHÍNH
# ======================
st.title("📰 AI Phóng Viên: Chấp bút chuẩn 5W1H")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Nhập nội dung bài báo (ví dụ: Hội nghị sơ kết, mô hình kinh tế...)...")

if user_input:
    if not api_key:
        st.error("Vui lòng điền API Key ở thanh bên trái!")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        model = genai.GenerativeModel(model_choice)
        prompt = build_prompt(style, user_input)

        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_text = ""
            # Stream=True để hiện chữ dần dần chuyên nghiệp
            response = model.generate_content(prompt, stream=True)
            for chunk in response:
                if hasattr(chunk, "text"):
                    full_text += chunk.text
                    placeholder.markdown(full_text)
            
            st.session_state.messages.append({"role": "assistant", "content": full_text})
            st.download_button("📥 Tải bài báo", full_text, file_name="bai_bao.txt")

    except Exception as e:
        if "429" in str(e):
            st.error("🚫 Quá giới hạn 5 lần/phút. Vui lòng đợi 60 giây và KHÔNG nhấn nút liên tục.")
        else:
            st.error(f"Lỗi: {str(e)}")
