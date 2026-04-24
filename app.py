import streamlit as st
import google.generativeai as genai

# 1. Cấu hình giao diện
st.set_page_config(page_title="AI Phóng Viên Pro (Free Edition)", layout="wide")

# 2. Sidebar cấu hình
with st.sidebar:
    st.header("⚙️ Cấu hình Gemini (Free)")
    google_api_key = st.text_input("Nhập Google API Key", type="password", help="Lấy tại: aistudio.google.com")
    model_name = st.selectbox("Chọn Model", ["gemini-1.5-flash", "gemini-1.5-pro"])
    st.info("Mẫu Flash sẽ chạy nhanh hơn, mẫu Pro sẽ thông minh hơn.")
    st.divider()
    st.caption("Phiên bản sử dụng Google AI miễn phí.")

# 3. Giao diện chính
st.title("✍️ AI Phóng Viên: Trợ Lý Tác Nghiệp")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📥 Dữ liệu thô")
    raw_input = st.text_area("Nhập thông tin, số liệu cần viết bài...", height=350)
    style = st.selectbox("Chọn phong cách viết", 
                          ["Phóng sự giàu cảm xúc", "Tin nhanh chính xác", "Xã luận sắc bén", "Bài viết gương người tốt việc tốt"])
    btn_generate = st.button("🚀 Bắt đầu chấp bút")

with col2:
    st.subheader("📰 Bài báo hoàn chỉnh")
    if btn_generate:
        if not google_api_key:
            st.error("Vui lòng nhập Google API Key ở bên trái!")
        elif not raw_input:
            st.warning("Vui lòng nhập dữ liệu!")
        else:
            with st.spinner("Gemini đang biên tập..."):
                try:
                    # Cấu hình Google AI
                    genai.configure(api_key=google_api_key)
                    model = genai.GenerativeModel(model_name)
                    
                    # Tạo nội dung
                    prompt = f"""
                    Bạn là một phóng viên chuyên nghiệp. 
                    Nhiệm vụ: Chuyển dữ liệu sau thành bài báo phong cách: {style}.
                    DỮ LIỆU: {raw_input}
                    YÊU CẦU: Tiêu đề hấp dẫn, văn phong hiện đại, đúng Tiếng Việt.
                    """
                    
                    response = model.generate_content(prompt)
                    
                    # Hiển thị
                    st.markdown(response.text)
                    st.download_button("📥 Tải bài báo (.txt)", response.text, file_name="bai_bao_gemini.txt")
                except Exception as e:
                    st.error(f"Lỗi hệ thống: {str(e)}")
    else:
        st.write("Nội dung sẽ xuất hiện ở đây.")
