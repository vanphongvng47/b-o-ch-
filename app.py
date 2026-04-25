import streamlit as st
import google.generativeai as genai

# Cấu hình giao diện
st.set_page_config(page_title="AI Phóng Viên 5W1H", layout="wide")

with st.sidebar:
    st.header("⚙️ Trung tâm điều hành")
    api_key = st.text_input("Nhập Google API Key", type="password")
    
    # Tự động lấy danh sách model thực tế từ tài khoản của bạn
    selected_model = ""
    if api_key:
        try:
            genai.configure(api_key=api_key)
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            if available_models:
                # Ưu tiên hiển thị bản Flash để tránh lỗi 429 Quota
                selected_model = st.selectbox("Chọn Model AI", available_models, index=0)
        except Exception:
            st.error("Key chưa đúng hoặc đang bị Google tạm khóa do nhấn nút quá nhanh.")

st.title("📰 Phóng Viên AI: Biên Tập Viên 5W1H")
st.caption("Chuyên sâu Hội nghị - Kinh tế - Xã hội vùng biên")

col1, col2 = st.columns([1, 1.2])

with col1:
    st.markdown("### 📥 Dữ liệu tác nghiệp")
    topic = st.selectbox("Chủ đề bài viết", 
                          ["Hội nghị & Sự kiện", "Kinh tế - Phát triển", "Xã hội & Dân sinh", "Gương sáng Đoàn thể"])
    
    raw_input = st.text_area("Nhập thông tin thô (Ai, cái gì, ở đâu, khi nào...)", height=300,
                             placeholder="Ví dụ: Hội nghị sơ kết 737, mô hình lúa nước Ea Súp, không khí trang trọng...")
    
    style = st.select_slider("Sắc thái", options=["Trang trọng", "Mạch lạc", "Truyền cảm hứng"])
    
    btn_generate = st.button("🚀 XUẤT BẢN BÀI VIẾT")

with col2:
    st.markdown("### 📜 Tác phẩm hoàn chỉnh")
    if btn_generate:
        if not api_key:
            st.error("Vui lòng điền API Key vào thanh bên trái!")
        elif not raw_input:
            st.warning("Hãy cung cấp thông tin để AI bắt đầu viết.")
        else:
            with st.spinner("Đang biên tập bài viết theo chuẩn 5W1H..."):
                try:
                    model = genai.GenerativeModel(model_name=selected_model)
                    
                    prompt = f"""
                    Bạn là một nhà báo lão thành sắc bén. Hãy viết bài báo cho chuyên mục {topic} từ dữ liệu: {raw_input}.
                    
                    YÊU CẦU BẮT BUỘC:
                    1. Cấu trúc 5W1H: Phải thể hiện rõ Ai, Cái gì, Ở đâu, Khi nào, Tại sao và Như thế nào.
                    2. Tiêu đề: Phải có sức nặng, thu hút người đọc.
                    3. Ngôn ngữ: Sử dụng phong cách {style}. Dùng các cụm từ báo chí như 'luồng sinh khí mới', 'thay da đổi thịt', 'tinh thần quyết tâm'.
                    4. Cảm xúc: Tả được không khí khẩn trương, trang trọng của hội trường hoặc sức sống vùng biên.
                    """
                    
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
                    st.download_button("📥 Tải bản thảo", response.text, file_name="bai_bao_hoan_chinh.txt")
                except Exception as e:
                    if "429" in str(e):
                        st.error("Google AI đang bận (Quá giới hạn 5 lần/phút). Bạn hãy đợi đúng 60 giây rồi nhấn lại nhé!")
                    else:
                        # Dòng này đã được sửa sạch lỗi cú pháp
                        st.error(f"Lỗi hệ thống: {str(e)}")
