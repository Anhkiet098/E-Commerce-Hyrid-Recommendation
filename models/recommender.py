import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from surprise import SVD

class ProductRecommender:
    def __init__(self, svd_model, items_df, user_features, tfidf_vectorizer, price_scaler):
        """
        Khởi tạo hệ thống đề xuất sản phẩm
        
        Args:
            svd_model: Mô hình SVD đã được huấn luyện
            items_df: DataFrame chứa thông tin sản phẩm
            user_features: DataFrame chứa đặc trưng người dùng
            tfidf_vectorizer: Bộ vector hóa TF-IDF đã được huấn luyện
            price_scaler: Bộ chuẩn hóa giá
        """
        self.svd_model = svd_model
        self.items_df = items_df
        self.user_features = user_features
        self.tfidf = tfidf_vectorizer
        self.scaler = price_scaler
    
    def get_content_based_similarity(self, item_id):
        """Tính độ tương đồng dựa trên nội dung"""
        item_vector = self.items_df[self.items_df['asin'] == item_id]['title_vector'].values[0]
        similarities = cosine_similarity([item_vector], list(self.items_df['title_vector']))
        return similarities[0]
    
    def get_hybrid_recommendations(self, user_id, n=5):
        """
        Lấy các khuyến nghị dựa trên mô hình hybrid
        
        Args:
            user_id: ID của người dùng
            n: S lượng khuyến nghị
            
        Returns:
            list: Danh sách các sản phẩm được đề xuất
        """
        all_items = set(self.items_df['asin'])
        user_items = set(self.user_features[self.user_features['user_id'] == user_id]['asin'])
        items_to_predict = list(all_items - user_items)
        
        # Lấy các dự đoán từ mô hình SVD
        svd_predictions = [self.svd_model.predict(user_id, item) for item in items_to_predict]
        
        # Lấy các đặc trưng của người dùng
        user_data = self.user_features[self.user_features['user_id'] == user_id]
        user_sentiment = user_data['sentiment'].values[0] if not user_data.empty else 0.5
        user_price_pref = user_data['normalized_price'].values[0] if not user_data.empty else 0.5
        
        # Kết hợp các dự đoán với lọc dựa trên nội dung và đặc trưng của người dùng
        hybrid_predictions = []
        for pred in svd_predictions:
            item_details = self.items_df[self.items_df['asin'] == pred.iid].iloc[0]
            content_similarity = self.get_content_based_similarity(pred.iid)[0]
            price_similarity = 1 - abs(user_price_pref - item_details['normalized_price'])
            
            # Kết hợp các điểm số
            hybrid_score = 0.2 * pred.est + 0.3 * content_similarity + 0.3 * price_similarity + 0.2 * user_sentiment
            
            hybrid_predictions.append((pred.iid, hybrid_score))
        
        # Sắp xếp và lấy N khuyến nghị hàng đầu
        top_n = sorted(hybrid_predictions, key=lambda x: x[1], reverse=True)[:n]
        
        recommendations = []
        for item_id, score in top_n:
            item_details = self.items_df[self.items_df['asin'] == item_id].iloc[0]
            recommendations.append({
                'asin': item_details['asin'],
                'brand': item_details['brand'],
                'title': item_details['title'],
                'url': item_details['url'],
                'image': item_details['image'],
                'rating': item_details['rating'],
                'reviewUrl': item_details['reviewUrl'],
                'totalReviews': item_details['totalReviews'],
                'price': item_details['price'],
                'originalPrice': item_details['originalPrice'],
                'hybrid_score': score
            })
                
        return recommendations
    
    def update_user_features(self, new_review, sentiment_analyzer):
        """
        Cập nhật đặc trưng của người dùng dựa trên đánh giá mới
        
        Args:
            new_review: DataFrame chứa đánh giá mới
            sentiment_analyzer: Đối tượng SentimentAnalyzer
            
        Returns:
            DataFrame: user_features đã được cập nhật
        """
        user_id = new_review['user_id'].values[0]
        
        # Phát hiện ngôn ngữ và dự đoán cảm xúc
        review_text = new_review['title'].values[0] + " " + new_review['body'].values[0]
        sentiment = sentiment_analyzer.predict_sentiment(review_text)
        
        if user_id in self.user_features['user_id'].values:
            # Cập nhật người dùng hiện có
            user_data = self.user_features[self.user_features['user_id'] == user_id]
            updated_sentiment = (user_data['sentiment'].values[0] + sentiment) / 2
            updated_price = (user_data['price'].values[0] + new_review['price'].values[0]) / 2
            updated_rating = (user_data['user_rating'].values[0] + new_review['rating'].values[0]) / 2
            
            self.user_features.loc[self.user_features['user_id'] == user_id, 'sentiment'] = updated_sentiment
            self.user_features.loc[self.user_features['user_id'] == user_id, 'price'] = updated_price
            self.user_features.loc[self.user_features['user_id'] == user_id, 'user_rating'] = updated_rating
            self.user_features.loc[self.user_features['user_id'] == user_id, 'asin'] = new_review['asin'].values[0]
        else:
            # Thêm người dùng mới
            new_user = pd.DataFrame({
                'user_id': [user_id],
                'sentiment': [sentiment],
                'price': [new_review['price'].values[0]],
                'user_rating': [new_review['rating'].values[0]],
                'asin': [new_review['asin'].values[0]]
            })
            self.user_features = pd.concat([self.user_features, new_user], ignore_index=True)
        
        # Cập nhật các đặc trưng được chuẩn hóa
        self.user_features['normalized_price'] = self.scaler.fit_transform(self.user_features[['price']])
        self.user_features['normalized_rating'] = self.user_features['user_rating'] / 5.0
        
        return self.user_features
