import streamlit as st
import google.generativeai as genai
import time

# ======================
# CẤU HÌNH HỆ THỐNG
# ======================
st.set_page_config(page_title="AI Phóng Viên Tòa Soạn", layout="wide")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "is_running" not in st.session_state:
    st.session_state.is_running = False

# ======================
# SIDEBAR: FIX LỖI 404 & MODEL
# ======================
with st.sidebar:
    st.header("📰 Trung tâm Biên tập")
    api_key = st.text_input("Nhập Google API Key", type="password")
    
    style = st.selectbox("Phong cách tòa soạn", [
        "Báo Nhân Dân",
        "Báo Quân đội Nhân dân",
        "VnExpress"
    ])

    # Tự động dò tìm model để tránh lỗi 404 models/gemini-1.5-pro not found
    model_name = "models/gemini-1.5-flash" 
    if api_key:
        try:
            genai.configure(api_key=api_key)
            # Lấy danh sách model thực tế từ tài khoản
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            if available_models:
                # Ưu tiên các dòng Flash để tránh lỗi 429 Quota
                flash_models = [m for m in available_models if "flash" in m]
                model_name = st.selectbox("Chọn Model AI (Khuyên dùng Flash)", flash_models if flash_models else available_models)
        except Exception:
            st.error("API Key không hợp lệ hoặc bị chặn tạm thời.")

# ======================
# LOGIC BIÊN TẬP 5W1H & CẢM XÚC
# ======================
def build_prompt(style, user_input):
    base_req = "- Đảm bảo cấu trúc 5W1H. Ngôn từ mạch lạc, giàu cảm xúc, tránh sáo rỗng. Khắc họa rõ nét sự thay da đổi thịt và tinh thần quyết tâm."
    
    if style == "Báo Nhân Dân":
        return f"Bạn là phóng viên Báo Nhân Dân. Viết bài từ: {user_input}. {base_req}\nVăn phong chính luận, trang trọng. Dùng cụm: 'khẳng định vai trò', 'tạo động lực phát triển'."
    elif style == "Báo Quân đội Nhân dân":
        return f"Bạn là phóng viên Báo Quân đội. Viết bài từ: {user_input}. {base_req}\nVăn phong mạnh mẽ, kỷ luật. Dùng cụm: 'cán bộ chiến sĩ', 'sẵn sàng nhận nhiệm vụ'."
    else: # VnExpress
        return f"Bạn là phóng viên VnExpress. Viết bài từ: {user_input}. {base_req}\nVăn phong hiện đại, ngắn gọn, tiêu đề thu hút."

# ======================
# GIAO DIỆN CHAT & XỬ LÝ
# ======================
st.title("✍️ AI Phóng Viên: Chấp bút chuẩn 5W1H")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Nhập dữ liệu sự kiện (Hội nghị, mô hình kinh tế...)...")

if user_input:
    if not api_key:
        st.error("Vui lòng nhập API Key ở thanh bên trái!")
        st.stop()

    if st.session_state.is_running:
        st.warning("⏳ Hệ thống đang xử lý bài viết trước...")
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
            # Stream=True để tạo trải nghiệm viết bài sống động
            response = model.generate_content(prompt, stream=True)
            for chunk in response:
                if hasattr(chunk, "text"):
                    full_text += chunk.text
                    placeholder.markdown(full_text)
            
            st.session_state.messages.append({"role": "assistant", "content": full_text})
            st.download_button("📥 Tải bài báo (.txt)", full_text, file_name="bai_bao_5W1H.txt")

    except Exception as e:
        if "429" in str(e):
            st.error("🚫 Quá giới hạn (5 yêu cầu/phút). Vui lòng đợi đúng 60 giây và KHÔNG nhấn nút liên tục.")
        else:
            st.error(f"Lỗi: {str(e)}")
    finally:
        st.session_state.is_running = False
