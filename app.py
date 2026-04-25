import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="AI Phóng Viên 5W1H", layout="wide")

# Sidebar cấu hình
with st.sidebar:
    st.header("⚙️ Cấu hình")
    api_key = st.text_input("Nhập Google API Key", type="password")
    
    # Tự động lấy danh sách model thực tế
    model_choice = "models/gemini-2.0-flash" 
    if api_key:
        try:
            genai.configure(api_key=api_key)
            models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            if models:
                model_choice = st.selectbox("Chọn Model AI", models)
        except:
            st.error("Key chưa đúng hoặc đang bị tạm khóa.")

st.title("📰 Phóng Viên AI: Biên Tập Viên 5W1H")

col1, col2 = st.columns([1, 1.2])

with col1:
    topic = st.selectbox("Chủ đề", ["Hội nghị", "Kinh tế", "Xã hội"])
    raw_input = st.text_area("Dữ liệu thô (5W1H)", height=300)
    btn_generate = st.button("🚀 XUẤT BẢN")

with col2:
    if btn_generate:
        if not api_key or not raw_input:
            st.error("Thiếu Key hoặc Dữ liệu!")
        else:
            with st.spinner("Đang viết..."):
                try:
                    model = genai.GenerativeModel(model_name=model_choice)
                    prompt = f"Viết bài báo chuẩn 5W1H về {topic}: {raw_input}. Văn phong báo chí chuyên nghiệp, mạch lạc, giàu cảm xúc."
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
                except Exception as e:
                    if "429" in str(e):
                        st.error("Google bận. Đợi 60 giây rồi bấm lại!")
                    else:
                        st.error(f"Lỗi: {str(e)}")
