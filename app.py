import streamlit as st
import joblib
import torch
from models.sentiment_analyzer import SentimentAnalyzer
from models.recommender import ProductRecommender

# Import các component giao diện
from components import (
    render_single_user_tab,
    render_multi_user_tab,
    render_sentiment_analysis_tab
)

# Import cấu hình từ file settings
from settings import UI_SETTINGS, MODEL_PATHS, APP_CONFIG, SENTIMENT_LABELS

# Thiết lập cấu hình trang
st.set_page_config(
    page_title=UI_SETTINGS['page_title'],
    layout=UI_SETTINGS['layout']
)

def load_models():
    """Tải tất cả các mô hình cần thiết"""
    # Tải các thành phần của mô hình hybrid
    @st.cache_resource
    def load_hybrid_components():
        return joblib.load(MODEL_PATHS['hybrid_model'])
    
    # Tải mô hình phân tích cảm xúc
    @st.cache_resource
    def load_sentiment_analyzer():
        return SentimentAnalyzer()
    
    # Tải tất cả các mô hình
    try:
        hybrid_components = load_hybrid_components()
        sentiment_analyzer = load_sentiment_analyzer()
        
        # Khởi tạo bộ đề xuất sản phẩm
        recommender = ProductRecommender(
            svd_model=hybrid_components['svd_model'],
            items_df=hybrid_components['items_df'],
            user_features=hybrid_components['user_features'],
            tfidf_vectorizer=hybrid_components['tfidf_vectorizer'],
            price_scaler=hybrid_components['price_scaler']
        )
        
        return {
            'recommender': recommender,
            'sentiment_analyzer': sentiment_analyzer,
            'hybrid_components': hybrid_components
        }
    except Exception as e:
        st.error(f"Lỗi khi tải mô hình: {str(e)}")
        return None

def main():
    st.title(UI_SETTINGS['page_title'])
    
    # Tải các mô hình
    with st.spinner('Đang tải các mô hình...'):
        models = load_models()
        
        if models is None:
            st.error("Không thể tải mô hình. Vui lòng kiểm tra lại đường dẫn và thử lại.")
            return
            
        recommender = models['recommender']
        sentiment_analyzer = models['sentiment_analyzer']
    
    # Tạo các tab chính
    tab1, tab2, tab3 = st.tabs([
        "Đề xuất người dùng đơn lẻ", 
        "Đề xuất nhiều người dùng", 
        "Phân tích cảm xúc người dùng"
    ])
    
    # Hiển thị các tab
    with tab1:
        render_single_user_tab(recommender)
    
    with tab2:
        render_multi_user_tab(recommender)
    
    with tab3:
        render_sentiment_analysis_tab(sentiment_analyzer)

if __name__ == "__main__":
    main()
