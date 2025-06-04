import streamlit as st
import pandas as pd

# Import cấu hình từ file settings
from settings import UI_SETTINGS, SENTIMENT_LABELS, APP_CONFIG

def display_product(product, is_review=False):
    """
    Hiển thị thông tin sản phẩm
    
    Args:
        product: Dictionary chứa thông tin sản phẩm
        is_review: Có phải đang hiển thị trong phần đánh giá không
    """
    with st.container():
        col_img, col_info = st.columns([1, 2])
        with col_img:
            st.image(product['image'], width=100)
        with col_info:
            st.subheader(product['title'])
            st.write(f"Mã sản phẩm: {product['asin']}")
            st.write(f"Thương hiệu: {product['brand']}")
            st.write(f"Giá: ${product['price']:.2f}")
            st.write(f"Đánh giá: {product['rating']}")
            if not is_review:
                st.write(f"Tổng số đánh giá: {product.get('totalReviews', 'N/A')}")
                if 'hybrid_score' in product:
                    st.write(f"Điểm đề xuất: {product['hybrid_score']:.2f}")
            st.write(f"[Xem sản phẩm]({product['url']})")

def render_single_user_tab(recommender):
    """
    Hiển thị giao diện cho tab đề xuất người dùng đơn lẻ
    
    Args:
        recommender: Đối tượng ProductRecommender
    """
    st.header("Đề xuất người dùng đơn lẻ")
    
    # Sử dụng cấu hình từ settings
    max_upload_size = APP_CONFIG['max_upload_size']
    supported_file_types = APP_CONFIG['supported_file_types']
    
    uploaded_file = st.file_uploader(
        "Chọn một file csv", 
        type=supported_file_types,
        key="tab1_uploader",
        help=f"Hỗ trợ các định dạng: {', '.join(supported_file_types)}"
    )
    
    if uploaded_file is not None:
        # Kiểm tra kích thước file
        if uploaded_file.size > max_upload_size:
            st.error(f"Kích thước file vượt quá giới hạn cho phép ({max_upload_size / (1024*1024):.1f}MB)")
            return
            
        try:
            df = pd.read_csv(uploaded_file)
            st.write("Dữ liệu đã tải lên:")
            st.dataframe(df.head())
            
            user_ids = df['user_id'].unique()
            selected_user_id = st.selectbox("Chọn user_id để đề xuất", user_ids)
            
            if st.button("Nhận đề xuất", key="recommend_tab1"):
                with st.spinner('Đang xử lý...'):
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # Hiển thị tiến trình
                    status_text.text("Đang xử lý...")
                    progress_bar.progress(25)
                    
                    try:
                        # Lấy đề xuất
                        recommendations = recommender.get_hybrid_recommendations(selected_user_id)
                        
                        # Cập nhật giao diện
                        progress_bar.progress(100)
                        status_text.text("Hoàn thành!")
                        
                        # Hiển thị kết quả
                        st.subheader("Đề xuất sản phẩm")
                        
                        # Hiển thị sản phẩm theo grid
                        cols = st.columns(UI_SETTINGS['products_per_row'])
                        for i, product in enumerate(recommendations):
                            with cols[i % UI_SETTINGS['products_per_row']]:
                                st.write(f"### Sản phẩm {i+1}")
                                display_product(product)
                                st.write("---")
                                
                    except Exception as e:
                        st.error(f"Có lỗi xảy ra khi tạo đề xuất: {str(e)}")
                    finally:
                        progress_bar.empty()
                        status_text.empty()
                        
        except Exception as e:
            st.error(f"Lỗi khi đọc file: {str(e)}")
