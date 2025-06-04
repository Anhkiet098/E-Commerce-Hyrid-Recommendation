import os

# Model paths
MODEL_PATHS = {
    'hybrid_model': 'models/Final_hybrid_model_components.joblib',
    'english_sentiment': 'models/english_sentiment',
    'vietnamese_sentiment': 'models/vietnamese_sentiment',
    'vietnamese_tokenizer': 'vinai/phobert-base'
}

# UI Settings
UI_SETTINGS = {
    'page_title': 'Hệ thống đề xuất sản phẩm',
    'layout': 'wide',
    'products_per_row': 2
}
không
# Sentiment Analysis Settings
SENTIMENT_LABELS = {
    0: 'Tiêu cực',
    1: 'Tích cực'
}

# Hybrid Recommendation Settings
# hybrid_score = 0.2 * pred.est + 0.3 * content_similarity + 0.3 * price_similarity + 0.2 * user_sentiment
HYBRID_SCORE_WEIGHTS = {
    'svd_score': 0.2,          # Weight for SVD model prediction
    'content_similarity': 0.3,  # Weight for content-based similarity
    'price_similarity': 0.3,    # Weight for price similarity
    'user_sentiment': 0.2       # Weight for user sentiment
}

# Application Settings
APP_CONFIG = {
    'cache_expiry': 3600,  # Thời gian hết hạn cache (giây)
    'max_upload_size': 50 * 1024 * 1024,  # Kích thước tối đa file upload (50MB)
    'supported_file_types': ['csv']  # Các định dạng file được hỗ trợ
}

# Đường dẫn thư mục
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
MODEL_DIR = os.path.join(BASE_DIR, 'models')

# Tạo các thư mục nếu chưa tồn tại
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)
