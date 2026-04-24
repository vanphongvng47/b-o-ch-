import streamlit as st
import google.generativeai as genai
import time

st.set_page_config(page_title="AI Phóng Viên Pro", layout="wide")

# Sidebar
with st.sidebar:
    st.header("⚙️ Cấu hình")
    api_key = st.text_input("Nhập Google API Key", type="password")
    
    available_models = []
    if api_key:
        try:
            genai.configure(api_key=api_key)
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        except:
            st.error("Key chưa chính xác.")
    
    model_choice = st.selectbox("Chọn Model", available_models if available_models else ["Đang đợi Key..."])

st.title("✍️ AI Phóng Viên: Trợ Lý Tác Nghiệp")

col1, col2 = st.columns(2)

with col1:
    raw_data = st.text_area("Nhập nội dung cần viết bài...", height=350, placeholder="Ví dụ: Chiến dịch Giờ Trái Đất 2026 tại Đắk Lắk...")
    style = st.selectbox("Phong cách", ["Tin nhanh", "Phóng sự", "Gương người tốt việc tốt", "Xã luận"])
    run_btn = st.button("🚀 Xuất bản ngay")

with col2:
    st.subheader("📰 Kết quả")
    if run_btn:
        if not api_key:
            st.error("Vui lòng nhập API Key!")
        else:
            with st.spinner("AI đang xử lý... Nếu quá tải, ứng dụng sẽ tự đợi vài giây."):
                try:
                    model = genai.GenerativeModel(model_name=model_choice)
                    prompt = f"Viết bài báo chuyên nghiệp phong cách {style}: {raw_data}. Viết bằng Tiếng Việt, tiêu đề hay."
                    
                    # Cơ chế thử lại nếu gặp lỗi Quota (429)
                    success = False
                    for i in range(3): # Thử tối đa 3 lần
                        try:
                            response = model.generate_content(prompt)
                            st.markdown(response.text)
                            st.download_button("📥 Tải bài viết", response.text, "bai_bao.txt")
                            success = True
                            break
                        except Exception as e:
                            if "429" in str(e):
                                st.warning(f"Hệ thống đang bận, đang thử lại lần {i+1}...")
                                time.sleep(10) # Đợi 10 giây rồi thử lại
                            else:
                                raise e
                    if not success:
                        st.error("Google AI đang quá tải. Bạn hãy đợi 1 phút rồi nhấn lại nhé!")
                except Exception as e:
                    st.error(f"Lỗi: {str(e)}")
