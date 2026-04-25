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
# SIDEBAR: THAY THẾ VÀ TỰ ĐỘNG DÒ MODEL
# ======================
with st.sidebar:
    st.header("📰 Cấu hình tòa soạn")
    api_key = st.text_input("Nhập Google API Key", type="password")
    
    style = st.selectbox("Phong cách tòa soạn", [
        "Báo Nhân Dân",
        "Báo Quân đội Nhân dân",
        "VnExpress"
    ])

    # Khởi tạo mặc định với bản 1.5 hoặc 2.0 tùy theo danh sách bạn có
    # Không còn bất kỳ dòng nào chứa "2.5"
    model_name = "models/gemini-1.5-flash" 
    
    if api_key:
        try:
            genai.configure(api_key=api_key)
            # Tự động lấy danh sách model thực tế từ tài khoản (Gemini 1.5, 2.0...)
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            
            if available_models:
                # Lọc bỏ hoàn toàn các bản 2.5 nếu có, chỉ giữ lại 1.5 và 2.0
                safe_models = [m for m in available_models if "2.5" not in m]
                # Ưu tiên các bản Flash để chạy mượt, không bị lỗi Quota
                flash_models = [m for m in safe_models if "flash" in m]
                
                model_name = st.selectbox("Chọn Model (Ưu tiên 2.0 Flash hoặc 1.5 Flash)", 
                                          flash_models if flash_models else safe_models)
        except Exception:
            st.error("API Key chưa đúng hoặc đang bị Google tạm khóa.")

# ======================
# LOGIC BIÊN TẬP 5W1H
# ======================
def build_prompt(style, user_input):
    base_req = "- Đảm bảo 5W1H. Văn phong mạch lạc, giàu cảm xúc, khắc họa sự thay đổi sống động của địa phương/sự kiện."
    
    if style == "Báo Nhân Dân":
        return f"Bạn là phóng viên Báo Nhân Dân. Viết về: {user_input}. {base_req}\nVăn phong chính luận, trang trọng. Dùng cụm: 'khẳng định vai trò', 'tạo động lực phát triển'."
    elif style == "Báo Quân đội Nhân dân":
        return f"Bạn là phóng viên Báo Quân đội. Viết về: {user_input}. {base_req}\nVăn phong mạnh mẽ, kỷ luật. Dùng cụm: 'cán bộ chiến sĩ', 'sẵn sàng nhiệm vụ'."
    else: # VnExpress
        return f"Bạn là phóng viên VnExpress. Viết về: {user_input}. {base_req}\nVăn phong hiện đại, ngắn gọn, tiêu đề thu hút."

# ======================
# GIAO DIỆN CHAT & XỬ LÝ
# ======================
st.title("✍️ AI Phóng Viên: Biên Tập Chuẩn 5W1H")

# Hiển thị lịch sử chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Nhập dữ liệu (Ví dụ: Hội nghị sơ kết, mô hình kinh tế lúa nước...)")

if user_input:
    if not api_key:
        st.error("Vui lòng nhập API Key ở bên trái!")
        st.stop()

    if st.session_state.is_running:
        st.warning("⏳ Hệ thống đang viết bài, vui lòng đợi...")
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
            # Chạy chữ dần dần cho cảm giác chuyên nghiệp
            response = model.generate_content(prompt, stream=True)
            for chunk in response:
                if hasattr(chunk, "text"):
                    full_text += chunk.text
                    placeholder.markdown(full_text)
            
            st.session_state.messages.append({"role": "assistant", "content": full_text})
            st.download_button("📥 Tải bài báo chuẩn", full_text, file_name="bai_bao_5w1h.txt")

    except Exception as e:
        if "429" in str(e):
            st.error("🚫 Quá giới hạn (5 lần/phút). Vui lòng đợi 60 giây rồi thử lại.")
        else:
            st.error(f"Lỗi hệ thống: {str(e)}")
    finally:
        st.session_state.is_running = False
