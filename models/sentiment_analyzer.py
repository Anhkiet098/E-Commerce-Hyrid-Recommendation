import torch
from transformers import BertTokenizer, BertForSequenceClassification, AutoTokenizer, AutoModelForSequenceClassification
from pathlib import Path

# Import cấu hình từ file settings
from settings import MODEL_PATHS

class SentimentAnalyzer:
    def __init__(self, device='cuda' if torch.cuda.is_available() else 'cpu'):
        """
        Khởi tạo bộ phân tích cảm xúc với các mô hình tiếng Anh và tiếng Việt
        """
        self.device = device
        self.english_model, self.english_tokenizer = self._load_english_model()
        self.vietnamese_model, self.vietnamese_tokenizer = self._load_vietnamese_model()
        
    def _load_english_model(self):
        """Tải mô hình phân tích cảm xúc tiếng Anh"""
        model_path = MODEL_PATHS['english_sentiment']
        model = BertForSequenceClassification.from_pretrained(model_path)
        tokenizer = BertTokenizer.from_pretrained(model_path)
        model.to(self.device)
        return model, tokenizer
    
    def _load_vietnamese_model(self):
        """Tải mô hình phân tích cảm xúc tiếng Việt"""
        model_path = MODEL_PATHS['vietnamese_sentiment']
        model = AutoModelForSequenceClassification.from_pretrained(model_path)
        tokenizer = AutoTokenizer.from_pretrained(MODEL_PATHS['vietnamese_tokenizer'])
        model.to(self.device)
        return model, tokenizer
    
    def detect_language(self, text):
        """Phát hiện ngôn ngữ của văn bản"""
        if any('\u4e00' <= char <= '\u9fff' for char in text):
            return 'vi'  # Tiếng Việt
        return 'en'  # Tiếng Anh
    
    def predict_sentiment(self, text, language=None):
        """
        Dự đoán cảm xúc của văn bản
        
        Args:
            text (str): Văn bản cần phân tích
            language (str, optional): 'en' hoặc 'vi'. Nếu None, sẽ tự động phát hiện
            
        Returns:
            int: 1 cho cảm xúc tích cực, 0 cho tiêu cực
        """
        if language is None:
            language = self.detect_language(text)
            
        if language == 'en':
            model, tokenizer = self.english_model, self.english_tokenizer
        else:
            model, tokenizer = self.vietnamese_model, self.vietnamese_tokenizer
        
        model.eval()
        encoded_input = tokenizer(text, padding=True, truncation=True, max_length=128, return_tensors='pt')
        encoded_input = {k: v.to(self.device) for k, v in encoded_input.items()}
        
        with torch.no_grad():
            output = model(**encoded_input)
        
        probabilities = torch.softmax(output.logits, dim=1)
        return torch.argmax(probabilities, dim=1).item()
