import streamlit as st

# Import cấu hình từ file settings
from settings import SENTIMENT_LABELS

def render_sentiment_analysis_tab(sentiment_analyzer):
    """
    Hiển thị giao diện cho tab phân tích cảm xúc người dùng
    
    Args:
        sentiment_analyzer: Đối tượng SentimentAnalyzer
    """
    st.header("Phân tích cảm xúc người dùng")
    
    # Tạo các tab con
    tab_text, tab_file = st.tabs(["Nhập văn bản", "Tải file đánh giá"])
    
    with tab_text:
        st.subheader("Phân tích văn bản")
        review_text = st.text_area(
            "Nhập đánh giá của bạn:", 
            height=150, 
            key="tab3_text_input",
            placeholder="Nhập nội dung đánh giá sản phẩm..."
        )
        
        if st.button("Phân tích", key="analyze_text_btn") and review_text.strip():
            with st.spinner('Đang phân tích...'):
                try:
                    # Phát hiện ngôn ngữ
                    language = sentiment_analyzer.detect_language(review_text)
                    language_name = "Tiếng Việt" if language == 'vi' else "Tiếng Anh"
                    
                    # Dự đoán cảm xúc
                    sentiment = sentiment_analyzer.predict_sentiment(review_text, language)
                    sentiment_label = SENTIMENT_LABELS.get(sentiment, "Không xác định")
                    
                    # Hiển thị kết quả
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Ngôn ngữ", language_name)
                    with col2:
                        sentiment_icon = "😊" if sentiment == 1 else "😞"
                        st.metric("Cảm xúc", f"{sentiment_icon} {sentiment_label}")
                    
                    # Hiển thị thêm thông tin chi tiết
                    with st.expander("Xem chi tiết phân tích"):
                        st.write("### Mẫu văn bản đã nhập:")
                        st.write(review_text[:500] + ("..." if len(review_text) > 500 else ""))
                        
                except Exception as e:
                    st.error(f"Có lỗi xảy ra khi phân tích: {str(e)}")
    
    with tab_file:
        st.subheader("Phân tích file đánh giá")
        st.info("Tính năng đang được phát triển. Vui lòng quay lại sau!")
