import streamlit as st
import google.generativeai as genai

# 1. Cấu hình trang
st.set_page_config(page_title="AI Phóng Viên Pro - 5W1H", layout="wide")

# Tùy chỉnh giao diện bằng CSS để chuyên nghiệp hơn
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #ff4b4b; color: white; }
    </style>
    """, unsafe_allow_html=True)

# 2. Sidebar - Cấu hình kỹ thuật
with st.sidebar:
    st.header("⚙️ Trung tâm điều hành")
    api_key = st.text_input("Nhập Google API Key", type="password")
    
    # Tự động lấy danh sách model khả dụng để tránh lỗi 404
    selected_model = "models/gemini-1.5-flash" # Mặc định
    if api_key:
        try:
            genai.configure(api_key=api_key)
            models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            if models:
                selected_model = st.selectbox("Chọn Model AI", models)
        except:
            st.error("Key chưa đúng hoặc hết hạn.")
    
    st.divider()
    st.caption("Ứng dụng hỗ trợ viết bài chuẩn nghiệp vụ báo chí 5W1H.")

# 3. Giao diện chính
st.title("📰 Phóng Viên AI: Biên Tập Viên 5W1H")
st.subheader("Chuyên sâu Hội nghị - Kinh tế - Xã hội vùng biên")

col1, col2 = st.columns([1, 1.2])

with col1:
    st.markdown("### 📥 Dữ liệu tác nghiệp")
    topic = st.selectbox("Chủ đề bài viết", 
                          ["Hội nghị & Sự kiện chính trị", "Kinh tế - Phát triển vùng biên", "Vấn đề Xã hội & Dân sinh", "Gương sáng & Hoạt động Đoàn thể"])
    
    raw_input = st.text_area("Nhập thông tin thô (Ai, cái gì, ở đâu, khi nào...)", height=350,
                             placeholder="Ví dụ: Hội nghị sơ kết 737, mô hình lúa nước Ea Súp, không khí trang trọng, quyết tâm của tuổi trẻ...")
    
    style = st.select_slider("Sắc thái bài viết", 
                             options=["Chính luận súc tích", "Mạch lạc khách quan", "Giàu cảm xúc, truyền cảm hứng"])
    
    btn_generate = st.button("🚀 XUẤT BẢN BÀI VIẾT")

with col2:
    st.markdown("### 📜 Tác phẩm hoàn chỉnh")
    if btn_generate:
        if not api_key:
            st.error("Vui lòng điền API Key vào thanh bên trái!")
        elif not raw_input:
            st.warning("Vui lòng cung cấp dữ liệu để AI làm việc!")
        else:
            with st.spinner("Biên tập viên AI đang trau chuốt ngôn từ..."):
                try:
                    model = genai.GenerativeModel(model_name=selected_model)
                    
                    # Hệ thống Prompt chuyên sâu
                    prompt = f"""
                    Bạn là một nhà báo xuất sắc, am hiểu về tình hình kinh tế, chính trị và xã hội vùng biên giới.
                    Nhiệm vụ: Viết một bài báo chuyên nghiệp về chủ đề {topic} dựa trên dữ liệu: {raw_input}.
                    
                    YÊU CẦU CẤU TRÚC 5W1H:
                    - Bài viết phải trả lời đầy đủ: Who (Ai), What (Cái gì), Where (Ở đâu), When (Khi nào), Why (Tại sao), How (Như thế nào).
                    - Cấu trúc: Tiêu đề -> Sapo (dẫn nhập) -> Nội dung chi tiết -> Kết luận/Lời bình.

                    YÊU CẦU NGÔN NGỮ & VĂN PHONG (Phong cách: {style}):
                    1. Tiêu đề: Sáng tạo, có sức nặng, sử dụng các động từ mạnh hoặc hình ảnh ẩn dụ.
                    2. Ngôn từ: Mạch lạc, chuyên nghiệp. Sử dụng các cụm từ báo chí như 'luồng sinh khí mới', 'thay da đổi thịt', 'điểm sáng vùng biên', 'tinh thần khẩn trương'.
                    3. Cảm xúc: Nếu là hội nghị, cần tả được sự trang trọng, đồng lòng. Nếu là kinh tế, cần tả được sự phát triển sống động, thực tế.
                    4. Kết nối: Các đoạn văn phải có sự liên kết logic, nhịp điệu câu văn biến hóa.

                    QUY ĐỊNH: Viết hoàn toàn bằng Tiếng Việt, không sa đà vào kể lể, tập trung vào những chi tiết đắt giá.
                    """
                    
                    response = model.generate_content(prompt)
                    
                    if response.text:
                        st.markdown(response.text)
                        st.download_button("📥 Tải bản thảo về máy", response.text, file_name="bai_bao_hoan_chinh.txt")
                except Exception as e:
                    if "429" in str(e):
                        st.error("Google AI đang bận (Quá giới hạn Free). Bạn vui lòng đợi 60 giây rồi nhấn lại nhé!")
                    else:
                        st.error(f"Lỗi: {str(e)}")
    else:
        st.info("Nhấn 'Xuất bản ngay' để xem kết quả biên tập.")

# 4. Chân trang
st.divider()
st.caption("© 2026 - Công cụ dành cho phóng viên tác nghiệp hiện đại.")
