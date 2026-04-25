import streamlit as st
import google.generativeai as genai

# Cấu hình giao diện chuẩn báo chí
st.set_page_config(page_title="AI Phóng Viên 5W1H", layout="wide")

with st.sidebar:
    st.header("⚙️ Cấu hình")
    api_key = st.text_input("Nhập Google API Key", type="password")
    
    selected_model = "models/gemini-1.5-flash"
    if api_key:
        try:
            genai.configure(api_key=api_key)
            # Tự động lấy danh sách model thực tế
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            if available_models:
                selected_model = st.selectbox("Chọn Model AI", available_models)
        except:
            st.error("Lỗi: Key chưa đúng hoặc đang bị Google tạm khóa.")

st.title("📰 Phóng Viên AI: Biên Tập Viên 5W1H")
st.caption("Chuyên sâu Hội nghị - Kinh tế - Xã hội vùng biên")

col1, col2 = st.columns([1, 1.2])

with col1:
    st.markdown("### 📥 Dữ liệu tác nghiệp")
    topic = st.selectbox("Chủ đề", ["Hội nghị & Sự kiện", "Kinh tế vùng biên", "Xã hội & Dân sinh", "Đoàn thể"])
    raw_input = st.text_area("Nhập thông tin thô (Ai, cái gì, ở đâu, khi nào...)", height=300)
    style = st.select_slider("Sắc thái", options=["Trang trọng", "Mạch lạc", "Truyền cảm hứng"])
    btn_generate = st.button("🚀 XUẤT BẢN BÀI VIẾT")

with col2:
    st.markdown("### 📜 Tác phẩm hoàn chỉnh")
    if btn_generate:
        if not api_key:
            st.error("Vui lòng nhập API Key!")
        elif not raw_input:
            st.warning("Hãy nhập dữ liệu thô!")
        else:
            with st.spinner("Đang biên tập bài viết theo chuẩn 5W1H..."):
                try:
                    model = genai.GenerativeModel(model_name=selected_model)
                    prompt = f"""
                    Bạn là nhà báo lão thành. Hãy viết bài báo chuẩn 5W1H cho chuyên mục {topic}.
                    Dữ liệu: {raw_input}. Phong cách: {style}.
                    YÊU CẦU: Có tiêu đề hay, Sapo cuốn hút, thân bài mạch lạc và sử dụng từ ngữ báo chí giàu cảm xúc.
                    """
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
                    st.download_button("📥 Tải bài viết", response.text, file_name="bai_bao.txt")
                except Exception as e:
                    if "429" in str(e):
                        st.error("Google đang bận (Quá giới hạn 5 lần/phút). Bạn hãy đợi đúng 60 giây rồi nhấn lại nhé!")
                    else:
                        st.error(f"Lỗi: {str(e)}")
