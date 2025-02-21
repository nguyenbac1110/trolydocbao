from gtts import gTTS
import os
import playsound

class TextToSpeech:
    def __init__(self):
        self.language = 'vi'
        
    def speak(self, text):
        try:
            print("Bot:", text)
            tts = gTTS(text=text, lang=self.language)
            filename = "temp_audio.mp3"
            tts.save(filename)
            playsound.playsound(filename)
            os.remove(filename)
        except Exception as e:
            print(f"Lỗi chuyển đổi text to speech: {str(e)}") 