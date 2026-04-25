import streamlit as st
import google.generativeai as genai
import time

# ========================
# CONFIG UI
# ========================
st.set_page_config(page_title="AI Phóng Viên 5W1H", layout="wide")

# ========================
# SESSION (chống spam)
# ========================
if "last_click" not in st.session_state:
    st.session_state.last_click = 0

# ========================
# SIDEBAR
# ========================
with st.sidebar:
    st.header("⚙️ Trung tâm điều hành")
    api_key = st.text_input("Nhập Google API Key", type="password")

    selected_model = ""

    if api_key:
        try:
            genai.configure(api_key=api_key)

            models = genai.list_models()

            # Lọc model an toàn
            available_models = [
                m.name for m in models
                if hasattr(m, "supported_generation_methods")
                and any("generate" in method.lower() for method in m.supported_generation_methods)
            ]

            if not available_models:
                st.error("Không tìm thấy model phù hợp.")
            else:
                # Ưu tiên Flash (tránh lỗi quota)
                preferred = [m for m in available_models if "flash" in m.lower()]
                if preferred:
                    available_models = preferred

                selected_model = st.selectbox("Chọn Model AI", available_models)

        except Exception as e:
            st.error(f"API Key lỗi hoặc bị giới hạn: {str(e)}")

# ========================
# MAIN UI
# ========================
st.title("📰 Phóng Viên AI: Biên Tập Viên 5W1H")
st.caption("Chuyên sâu Hội nghị - Kinh tế - Xã hội vùng biên")

col1, col2 = st.columns([1, 1.2])

# ========================
# INPUT
# ========================
with col1:
    st.markdown("### 📥 Dữ liệu tác nghiệp")

    topic = st.selectbox(
        "Chủ đề bài viết",
        ["Hội nghị & Sự kiện", "Kinh tế - Phát triển", "Xã hội & Dân sinh", "Gương sáng Đoàn thể"]
    )

    raw_input = st.text_area(
        "Nhập thông tin thô (Ai, cái gì, ở đâu, khi nào...)",
        height=300,
        placeholder="Ví dụ: Hội nghị sơ kết 737, mô hình lúa nước Ea Súp..."
    )

    style = st.select_slider(
        "Sắc thái",
        options=["Trang trọng", "Mạch lạc", "Truyền cảm hứng"]
    )

    btn_generate = st.button("🚀 XUẤT BẢN BÀI VIẾT")

# ========================
# OUTPUT
# ========================
with col2:
    st.markdown("### 📜 Tác phẩm hoàn chỉnh")

    if btn_generate:
        # chống spam click
        now = time.time()
        if now - st.session_state.last_click < 5:
            st.warning("⏳ Đừng bấm quá nhanh, đợi vài giây nhé!")
            st.stop()
        st.session_state.last_click = now

        # validate input
        if not api_key:
            st.error("Vui lòng nhập API Key.")
            st.stop()

        if not selected_model:
            st.error("Không có model hợp lệ.")
            st.stop()

        if not raw_input.strip():
            st.warning("Hãy nhập dữ liệu đầu vào.")
            st.stop()

        # ========================
        # GENERATE
        # ========================
        with st.spinner("🧠 AI đang viết bài..."):
            try:
                model = genai.GenerativeModel(model_name=selected_model)

                prompt = f"""
Bạn là một nhà báo chuyên nghiệp.

Viết bài báo chủ đề: {topic}

Dữ liệu đầu vào:
{raw_input}

YÊU CẦU:
- Viết theo cấu trúc 5W1H rõ ràng (Ai, Cái gì, Ở đâu, Khi nào, Tại sao, Như thế nào)
- Có tiêu đề hấp dẫn
- Độ dài: 300-500 từ
- Không lặp ý, không lan man
- Văn phong: {style}
- Có cảm xúc báo chí (trang trọng, sinh động)
"""

                response = model.generate_content(prompt)

                # kiểm tra response
                if response and getattr(response, "text", None):
                    result = response.text
                    st.markdown(result)

                    st.download_button(
                        "📥 Tải bản thảo",
                        result,
                        file_name="bai_bao_5w1h.txt"
                    )
                else:
                    st.error("AI không trả về nội dung.")

            except Exception as e:
                if "429" in str(e):
                    st.error("🚫 Quá giới hạn (5 request/phút). Đợi ~60s rồi thử lại.")
                else:
                    st.error(f"❌ Lỗi hệ thống: {str(e)}")
