import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="AI Phóng Viên 2026", layout="wide")

with st.sidebar:
    st.header("⚙️ Cấu hình")
    api_key = st.text_input("Nhập API Key mới", type="password")
    # Tự động lấy danh sách model để tránh lỗi 404
    model_name = "models/gemini-1.5-flash" 
    if api_key:
        try:
            genai.configure(api_key=api_key)
            models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            model_name = st.selectbox("Chọn Model", models if models else ["models/gemini-1.5-flash"])
        except:
            st.error("Key bị Google chặn tạm thời. Hãy thử Key mới!")

st.title("📰 Phóng Viên AI: Biên Tập 5W1H")

data = st.text_area("Nhập thông tin (Hội nghị, Kinh tế, Xã hội...)", height=250)

if st.button("🚀 XUẤT BẢN BÀI VIẾT"):
    if not api_key or not data:
        st.error("Vui lòng điền đủ Key và Nội dung!")
    else:
        with st.spinner("Đang biên tập văn phong báo chí cao cấp..."):
            try:
                model = genai.GenerativeModel(model_name)
                # Prompt ép cấu trúc 5W1H và ngôn từ chuyên nghiệp
                prompt = f"""Viết bài báo chuyên nghiệp từ dữ liệu: {data}. 
                YÊU CẦU: 
                1. Cấu trúc 5W1H đầy đủ. 
                2. Tiêu đề sắc sảo, nội dung mạch lạc, giàu cảm xúc. 
                3. Sử dụng từ ngữ báo chí như: 'thay da đổi thịt', 'điểm sáng', 'tinh thần khẩn trương'. 
                Viết bằng tiếng Việt."""
                
                response = model.generate_content(prompt)
                st.markdown("### Tác phẩm hoàn chỉnh:")
                st.write(response.text)
            except Exception as e:
                st.error("Google đang quá tải. Đợi đúng 60 giây hãy bấm lại!")
