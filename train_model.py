from intent_classification import IntentClassifier
import os

def train():
    # Tạo thư mục model nếu chưa tồn tại
    if not os.path.exists('model'):
        os.makedirs('model')

    # Khởi tạo và huấn luyện model
    intent_classifier = IntentClassifier()
    intent_classifier.train('intent_data.csv')
    
    # Lưu model
    intent_classifier.save_model('model/intent_model.joblib')
    print("Đã huấn luyện và lưu model thành công!")

if __name__ == "__main__":
    train() 