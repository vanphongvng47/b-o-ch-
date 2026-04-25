import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="AI Phóng Viên 5W1H", layout="wide")

with st.sidebar:
    st.header("⚙️ Cấu hình chuyên sâu")
    api_key = st.text_input("Nhập Google API Key", type="password")
    
    # Ưu tiên Flash để tốc độ nhanh và ít lỗi quota
    model_choice = st.selectbox("Chọn Model", ["models/gemini-1.5-flash", "models/gemini-1.5-pro"])
    st.divider()
    st.info("Cấu trúc 5W1H giúp bài viết đầy đủ, khách quan và chuyên nghiệp.")

st.title("📰 Hệ Thống Biên Tập Báo Chí Chuẩn 5W1H")

col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("📥 Dữ liệu tác nghiệp")
    topic = st.selectbox("Loại hình bài viết", 
                          ["Tin sự kiện/Hội nghị", "Phóng sự kinh tế - xã hội", "Gương sáng điển hình", "Thông tin chuyên đề"])
    
    raw_data = st.text_area("Nhập thông tin cốt lõi (Số liệu, thời gian, địa điểm, nhân vật...)", height=300)
    
    style = st.radio("Sắc thái ngôn ngữ", 
                     ["Trang trọng, chính luận", "Truyền cảm hứng, nhân văn", "Sắc bén, trực diện"], horizontal=True)
    
    run_btn = st.button("🚀 Khởi tạo bài viết")

with col2:
    st.subheader("📰 Nội dung xuất bản")
    if run_btn:
        if not api_key:
            st.error("Thiếu API Key!")
        elif not raw_data:
            st.warning("Hãy nhập dữ liệu thô!")
        else:
            with st.spinner("Đang cấu trúc bài viết theo sơ đồ 5W1H..."):
                try:
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel(model_name=model_choice)
                    
                    # Prompt ép AI tuân thủ cấu trúc báo chí
                    prompt = f"""
                    Bạn là một biên tập viên báo chí cấp cao. Hãy viết một bài báo thuộc loại {topic} dựa trên dữ liệu sau:
                    {raw_data}

                    YÊU CẦU BẮT BUỘC VỀ CẤU TRÚC 5W1H:
                    1. Who (Ai): Xác định rõ chủ thể, các bên liên quan, đại biểu, nhân dân...
                    2. What (Cái gì): Sự kiện gì đã xảy ra? Mục tiêu, nội dung chính là gì?
                    3. Where (Ở đâu): Địa điểm cụ thể (hội trường, đơn vị, địa phương...).
                    4. When (Khi nào): Thời gian tổ chức, giai đoạn thực hiện (ví dụ: 2024-2026).
                    5. Why (Tại sao): Mục đích, ý nghĩa của sự kiện/vấn đề (tại sao phải làm, tầm quan trọng).
                    6. How (Như thế nào): Cách thức diễn ra, các mô hình cụ thể, kết quả đạt được.

                    YÊU CẦU VỀ NGÔN NGỮ:
                    - Tiêu đề: Đậm chất báo chí, súc tích, gợi hình.
                    - Văn phong: {style}. 
                    - Mạch lạc: Sử dụng ngôn ngữ chuyên ngành (kinh tế, đoàn thể, quân sự) một cách nhuần nhuyễn.
                    - Cảm xúc: Lồng ghép khéo léo không khí trang trọng của hội trường hoặc sức sống mãnh liệt của các mô hình kinh tế vùng biên.
                    """
                    
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
                    st.download_button("📥 Tải bản thảo (.txt)", response.text, "bai_bao_5w1h.txt")
                except Exception as e:
                    st.error(f"Lỗi: {str(e)}")
