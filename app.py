import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="AI Phóng Viên 5W1H", layout="wide")

with st.sidebar:
    st.header("⚙️ Cấu hình")
    api_key = st.text_input("Nhập API Key mới", type="password")
    
    # Tự động lấy danh sách model để tránh lỗi 404
    model_choice = "models/gemini-2.0-flash" 
    if api_key:
        try:
            genai.configure(api_key=api_key)
            models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            if models:
                model_choice = st.selectbox("Chọn Model AI", models)
        except:
            st.error("Key này đang bị Google tạm khóa. Hãy dùng Key mới!")

st.title("📰 Phóng Viên AI: Biên Tập Viên 5W1H")

data = st.text_area("Nhập dữ liệu (Ví dụ: ĐHQG TPHCM mở rộng địa bàn thi...)", height=250)

if st.button("🚀 XUẤT BẢN BÀI VIẾT"):
    if not api_key or not data:
        st.error("Thiếu Key hoặc Dữ liệu!")
    else:
        with st.spinner("Đang biên tập văn phong báo chí cao cấp..."):
            try:
                model = genai.GenerativeModel(model_choice)
                # Prompt ép cấu trúc 5W1H và ngôn từ sắc bén
                prompt = f"""Bạn là một nhà báo lão thành. Hãy viết một bài báo chuyên nghiệp từ dữ liệu này: {data}.
                YÊU CẦU:
                1. Đầy đủ 5W1H (Ai, Cái gì, Ở đâu, Khi nào, Tại sao, Như thế nào).
                2. Tiêu đề gây ấn tượng mạnh. Văn phong mạch lạc, giàu cảm xúc.
                3. Sử dụng các cụm từ báo chí như: 'Sức bật', 'Luồng sinh khí mới', 'Khẳng định vị thế'.
                Viết hoàn toàn bằng Tiếng Việt."""
                
                response = model.generate_content(prompt)
                st.markdown("---")
                st.markdown(response.text)
            except Exception as e:
                if "429" in str(e):
                    st.error("Hệ thống đang nghẽn. Bạn hãy đợi đúng 60 giây (đếm ngược) rồi mới bấm lại!")
                else:
                    st.error(f"Lỗi: {str(e)}")
