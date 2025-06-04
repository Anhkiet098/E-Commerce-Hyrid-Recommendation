import streamlit as st
import pandas as pd

# Import cấu hình từ file settings
from settings import UI_SETTINGS, APP_CONFIG

def render_multi_user_tab(recommender):
    """
    Hiển thị giao diện cho tab đề xuất nhiều người dùng
    
    Args:
        recommender: Đối tượng ProductRecommender
    """
    st.header("Đề xuất nhiều người dùng")
    
    # Sử dụng cấu hình từ settings
    max_upload_size = APP_CONFIG['max_upload_size']
    supported_file_types = APP_CONFIG['supported_file_types']
    
    uploaded_file = st.file_uploader(
        "Chọn file dữ liệu người dùng",
        type=supported_file_types,
        key="tab2_uploader",
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
            
            if st.button("Nhận đề xuất", key="recommend_tab2"):
                with st.spinner('Đang xử lý...'):
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # Hiển thị tiến trình
                    status_text.text("Đang xử lý...")
                    progress_bar.progress(25)
                    
                    try:
                        # TODO: Thêm logic xử lý cho nhiều người dùng
                        # Đây là phần xử lý chính cần được thêm sau
                        
                        # Giả lập quá trình xử lý
                        import time
                        time.sleep(1)
                        progress_bar.progress(50)
                        
                        # Hiển thị kết quả mẫu
                        st.success("Đã xử lý xong dữ liệu của {} người dùng".format(len(df['user_id'].unique())))
                        
                        # Cập nhật giao diện
                        progress_bar.progress(100)
                        status_text.text("Hoàn thành!")
                        
                    except Exception as e:
                        st.error(f"Có lỗi xảy ra khi xử lý: {str(e)}")
                    finally:
                        progress_bar.empty()
                        status_text.empty()
                        
        except Exception as e:
            st.error(f"Lỗi khi đọc file: {str(e)}")
    else:
        st.info("Vui lòng tải lên file dữ liệu người dùng để bắt đầu")

# Thêm dòng này để có thể chạy thử component độc lập (tùy chọn)
if __name__ == "__main__":
    render_multi_user_tab(None)
