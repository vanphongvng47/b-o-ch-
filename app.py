import streamlit as st
import google.generativeai as genai
import time

# Cấu hình giao diện
st.set_page_config(page_title="AI Phóng Viên 5W1H", layout="wide")

with st.sidebar:
    st.header("⚙️ Trung tâm điều hành")
    api_key = st.text_input("Nhập Google API Key", type="password")
    
    # Tự động lấy danh sách model thực tế từ tài khoản của bạn
    selected_model = "models/gemini-1.5-flash"
    if api_key:
        try:
            genai.configure(api_key=api_key)
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            if available_models:
                # Ưu tiên hiển thị bản Flash để tránh lỗi 429
                selected_model = st.selectbox("Chọn Model AI", available_models, index=0)
        except Exception:
            st.error("Key chưa đúng hoặc bị Google tạm khóa.")

st.title("📰 Phóng Viên AI: Biên Tập Viên 5W1H")
st.caption("Chuyên sâu Hội nghị - Kinh tế - Xã hội vùng biên")

col1, col2 = st.columns([1, 1.2])

with col1:
    st.markdown("### 📥 Dữ liệu tác nghiệp")
    topic = st.selectbox("Chủ đề bài viết", 
                          ["Hội nghị & Sự kiện", "Kinh tế vùng biên", "Xã hội & Dân sinh", "Gương sáng Đoàn thể"])
    
    raw_input = st.text_area("Nhập thông tin thô (Ai, cái gì, ở đâu, khi nào...)", height=300)
    
    style = st.select_slider("Sắc thái", options=["Trang trọng", "Mạch lạc", "Truyền cảm hứng"])
    
    btn_generate = st.button("🚀 XUẤT BẢN BÀI VIẾT")

with col2:
    st.markdown("### 📜 Tác phẩm hoàn chỉnh")
    if btn_generate:
        if not api_key:
            st.error("Vui lòng điền API Key!")
        elif not raw_input:
            st.warning("Hãy cung cấp thông tin để AI viết bài.")
        else:
            with st.spinner("Đang biên tập bài viết chuẩn 5W1H..."):
                try:
                    model = genai.GenerativeModel(model_name=selected_model)
                    
                    prompt = f"""
                    Bạn là nhà báo lão thành, viết bài chuẩn cấu trúc 5W1H cho chuyên mục {topic}.
                    Dữ liệu: {raw_input}. Phong cách: {style}.
                    
                    YÊU CẦU:
                    1. Tiêu đề: Giật tít hay, đúng trọng tâm.
                    2. Cấu trúc: Có Sapo, thân bài mạch lạc và kết bài giàu cảm xúc.
                    3. Ngôn ngữ: Sử dụng từ ngữ báo chí hiện đại như 'sức bật', 'thay da đổi thịt', 'tinh thần quyết tâm'.
                    4. 5W1H: Phải thể hiện rõ Ai, Cái gì, Ở đâu, Khi nào, Tại sao và Như thế nào.
                    """
                    
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
                    st.download_button("📥 Tải bài viết", response.text, file_name="bai_bao.txt")
                except Exception as e:
                    if "429" in str(e):
                        st.error("Google AI đang bận (Quá giới hạn Free). Vui lòng đợi 60 giây rồi nhấn lại!")
                    else:
                        # Dòng 51 đã được sửa sạch sẽ, không còn văn bản thừa
                        st.error(f"Lỗi: {str(e)}")
