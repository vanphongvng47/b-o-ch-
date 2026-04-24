import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. Cấu hình giao diện
st.set_page_config(page_title="AI Phóng Viên Pro", layout="wide")

# 2. Sidebar cấu hình
with st.sidebar:
    st.header("⚙️ Cấu hình AI")
    api_key = st.text_input("Nhập OpenAI API Key", type="password")
    model_name = st.selectbox("Chọn Model", ["gpt-4o", "gpt-3.5-turbo"])
    temp = st.slider("Độ sáng tạo (Cảm xúc)", 0.0, 1.0, 0.7)
    st.divider()
    st.caption("Công cụ dành cho phóng viên hiện đại.")

# 3. Giao diện chính
st.title("✍️ AI Phóng Viên: Viết Báo Chuyên Nghiệp")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📥 Dữ liệu thô")
    raw_input = st.text_area("Nhập thông tin, số liệu hoặc nội dung cần viết...", height=350)
    style = st.selectbox("Chọn phong cách viết", 
                          ["Phóng sự giàu cảm xúc", "Tin nhanh chính xác", "Xã luận sắc bén", "Ký sự nhân văn"])
    btn_generate = st.button("🚀 Bắt đầu chấp bút")

with col2:
    st.subheader("📰 Bài báo hoàn chỉnh")
    if btn_generate:
        if not api_key:
            st.error("Vui lòng nhập API Key ở thanh bên trái!")
        elif not raw_input:
            st.warning("Vui lòng cung cấp dữ liệu đầu vào!")
        else:
            with st.spinner("AI đang biên tập bài viết..."):
                try:
                    # Khởi tạo AI
                    llm = ChatOpenAI(model=model_name, temperature=temp, api_key=api_key)
                    
                    # Thiết lập Prompt
                    prompt = ChatPromptTemplate.from_template("""
                    Bạn là một phóng viên chuyên nghiệp. 
                    Hãy chuyển dữ liệu thô sau thành một bài báo hoàn chỉnh theo phong cách: {style}.
                    
                    DỮ LIỆU: {data}
                    
                    YÊU CẦU:
                    - Tiêu đề hấp dẫn.
                    - Văn phong báo chí hiện đại, súc tích.
                    - Viết bằng Tiếng Việt.
                    """)
                    
                    # Chuỗi xử lý (Chain)
                    chain = prompt | llm | StrOutputParser()
                    
                    # Thực thi
                    result = chain.invoke({"style": style, "data": raw_input})
                    
                    # Hiển thị
                    st.markdown(result)
                    st.download_button("📥 Tải bài báo (.txt)", result, file_name="bai_bao.txt")
                except Exception as e:
                    st.error(f"Lỗi: {str(e)}")
    else:
        st.info("Kết quả sẽ hiển thị ở đây.")
