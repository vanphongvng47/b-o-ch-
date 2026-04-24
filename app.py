import streamlit as st
import google.generativeai as genai

# Cấu hình giao diện
st.set_page_config(page_title="AI Phóng Viên Pro", layout="wide")

with st.sidebar:
    st.header("⚙️ Cài đặt")
    api_key = st.text_input("Nhập Google API Key", type="password")
    # Cập nhật tên mô hình chuẩn xác
    model_choice = st.selectbox("Chọn Model", ["models/gemini-1.5-flash", "models/gemini-1.5-pro"])
    st.divider()
    st.caption("Phiên bản miễn phí dùng Google Gemini.")

st.title("✍️ AI Phóng Viên: Trợ Lý Tác Nghiệp")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📥 Dữ liệu thô")
    raw_data = st.text_area("Nhập nội dung/số liệu...", height=300)
    style = st.selectbox("Phong cách", ["Tin nhanh", "Phóng sự", "Xã luận"])
    run_btn = st.button("🚀 Chấp bút")

with col2:
    st.subheader("📰 Kết quả")
    if run_btn:
        if not api_key:
            st.error("Vui lòng nhập API Key!")
        elif not raw_data:
            st.warning("Hãy nhập dữ liệu!")
        else:
            try:
                # Cấu hình AI
                genai.configure(api_key=api_key)
                # Sử dụng tên mô hình đầy đủ để tránh lỗi 404
                model = genai.GenerativeModel(model_name=model_choice)
                
                prompt = f"Bạn là phóng viên chuyên nghiệp. Hãy viết bài báo phong cách {style} từ dữ liệu: {raw_data}. Viết tiếng Việt, tiêu đề hấp dẫn."
                
                response = model.generate_content(prompt)
                
                if response.text:
                    st.markdown(response.text)
                    st.download_button("📥 Tải bài viết", response.text, "bai_bao.txt")
            except Exception as e:
                # Nếu vẫn lỗi 404, thử tự động đổi sang mô hình mặc định
                st.error(f"Lỗi: {str(e)}")
                st.info("Mẹo: Nếu báo lỗi 404, hãy thử chọn lại model khác trong danh sách.")
