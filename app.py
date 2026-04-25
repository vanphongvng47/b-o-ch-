# ======================
# SIDEBAR - BẢN FIX LỖI MODEL & QUOTA
# ======================
with st.sidebar:
    st.header("📰 Cấu hình bài báo")
    api_key = st.text_input("Google API Key", type="password")
    
    style = st.selectbox("Chọn phong cách báo", [
        "Báo Nhân Dân",
        "Báo Quân đội",
        "VnExpress"
    ])

    model_name = "models/gemini-1.5-flash" # Mặc định an toàn nhất
    if api_key:
        try:
            genai.configure(api_key=api_key)
            # Tự động lấy model mới nhất mà tài khoản bạn có (tránh lỗi 404)
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            if available_models:
                # Ưu tiên các bản Flash để tránh lỗi 429
                flash_models = [m for m in available_models if "flash" in m]
                model_name = st.selectbox("Chọn Model (Nên chọn Flash)", flash_models if flash_models else available_models)
        except Exception as e:
            st.error("Kết nối API thất bại. Kiểm tra lại Key!")
