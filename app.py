import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="AI Phóng Viên Pro", layout="wide")

with st.sidebar:
    st.header("⚙️ Cấu hình")
    api_key = st.text_input("Nhập Google API Key", type="password")
    
    available_models = []
    if api_key:
        try:
            genai.configure(api_key=api_key)
            # Tự động lấy danh sách model mà API của bạn được phép dùng
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        except:
            st.error("Key không đúng hoặc lỗi kết nối.")
    
    model_choice = st.selectbox("Chọn Model khả dụng", available_models if available_models else ["Đang đợi Key..."])

st.title("✍️ AI Phóng Viên: Trợ Lý Tác Nghiệp")

col1, col2 = st.columns(2)

with col1:
    raw_data = st.text_area("Nhập dữ liệu...", height=300)
    style = st.selectbox("Phong cách", ["Tin nhanh", "Phóng sự", "Xã luận"])
    run_btn = st.button("🚀 Chấp bút")

with col2:
    if run_btn:
        if not api_key or "Đang đợi" in model_choice:
            st.error("Vui lòng kiểm tra lại Key và Model!")
        else:
            try:
                model = genai.GenerativeModel(model_name=model_choice)
                response = model.generate_content(f"Viết bài báo {style}: {raw_data}")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Lỗi: {str(e)}")
