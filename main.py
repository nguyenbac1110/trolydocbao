from speechtotext import SpeechToText
from intent_classification import IntentClassifier
from action import XuLyTinTuc
from texttospeech import TextToSpeech
import signal
import sys
import os
import webbrowser

def cleanup(signal_number=None, frame=None):
    print('\nĐang dọn dẹp và thoát...')
    # Xóa file temp_audio.mp3 nếu tồn tại
    if os.path.exists("temp_audio.mp3"):
        try:
            os.remove("temp_audio.mp3")
        except:
            pass
    if signal_number is not None:
        sys.exit(0)

def main():
    
    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)
    
    stt = SpeechToText()
    intent_classifier = IntentClassifier()
    news_action = XuLyTinTuc()
    tts = TextToSpeech()
    
    try:
        
        intent_classifier.load_model('model/intent_model.joblib')
        #print("Bot: Xin chào, tôi giúp được gì cho bạn?")
        tts.speak("Xin chào, tôi giúp được gì cho bạn?")
        
        while True:
            
            text = stt.convert_speech_to_text()
            if text:
                
                intent = intent_classifier.predict(text)
                
                
                result = news_action.xuly_yeucau(intent, text)
                
                
                if isinstance(result, list):
                    if not result:
                        #print("Bot: Không tìm thấy tin tức nào.")
                        tts.speak("Không tìm thấy tin tức nào.")
                    else:
                        for news in result:
                            tts.speak(news)
                elif isinstance(result, dict):
                    tts.speak(f"Tiêu đề: {result['tieude']}")
                    tts.speak(f"Nội dung: {result['noidung']}")
                else:
                    #print(f"Bot: {str(result)}")
                    tts.speak(result)
    finally:
        cleanup()

def handle_latest_news(text):
    webbrowser.open('https://vnexpress.net')
    # Existing code for displaying titles
    titles = get_latest_news()
    for title in titles:
        print(title)
    
    # Open VnExpress homepage

def handle_search_news(text, titles):
    # Get the article content and URL
    article_url = get_article_url(titles[0])  # Assuming first match
    content = get_article_content(article_url)
    
    # Display content in terminal
    print(content)
    
    # Open article in browser
    webbrowser.open(article_url)

def handle_category_news(category):
    # Existing code for displaying category titles
    titles = get_category_news(category)
    for title in titles:
        print(title)
    
    # Open category page in browser
    category_url = f'https://vnexpress.net/{category}'
    webbrowser.open(category_url)

if __name__ == "__main__":
    main()