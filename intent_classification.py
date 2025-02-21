import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib

class IntentClassifier:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.classifier = MultinomialNB()
        
    def train(self, data_path):
        # Đọc dữ liệu từ file CSV
        df = pd.read_csv(data_path)
        X = df['text']
        y = df['intent']
        
        # Vectorize văn bản và huấn luyện mô hình
        X_vectorized = self.vectorizer.fit_transform(X)
        self.classifier.fit(X_vectorized, y)
        
    def predict(self, text):
        # Chuyển đổi văn bản và dự đoán intent
        text_vectorized = self.vectorizer.transform([text])
        intent = self.classifier.predict(text_vectorized)[0]
        return intent
    
    def save_model(self, model_path):
        joblib.dump((self.vectorizer, self.classifier), model_path)
        
    def load_model(self, model_path):
        self.vectorizer, self.classifier = joblib.load(model_path) 