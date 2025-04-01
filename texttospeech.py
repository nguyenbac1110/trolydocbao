from gtts import gTTS
import os
import playsound
import re

class TextToSpeech:
    def __init__(self):
        self.language = 'vi'
        
    def split_into_sentences(self, text):
        """Chia văn bản thành các câu nhỏ hơn, đảm bảo không cắt giữa từ."""
        # Đầu tiên tách theo dòng mới
        lines = text.split('\n')
        result = []
        
        for line in lines:
            if not line.strip():  # Bỏ qua dòng trống
                continue
            
            # Tách theo dấu câu hoặc khoảng trắng
            sentences = re.split('([.!?])', line)
            current = ""
            
            for i in range(0, len(sentences)-1, 2):
                if len(sentences[i].strip()) == 0:
                    continue
                
                # Ghép câu với dấu câu
                current = sentences[i].strip() + (sentences[i+1] if i+1 < len(sentences) else "")
                
                # Nếu câu quá dài, chia theo dấu phẩy
                if len(current) > 100:
                    comma_parts = current.split(',')
                    temp = ""
                    for part in comma_parts:
                        if len(temp + part) > 100:
                            if temp:
                                result.append(temp.strip())
                            temp = part
                        else:
                            temp = temp + "," + part if temp else part
                    if temp:
                        result.append(temp.strip())
                else:
                    result.append(current.strip())
                
            # Nếu dòng không có dấu câu, thêm trực tiếp vào kết quả
            if not any(punct in line for punct in '.!?'):
                result.append(line.strip())
                
        return result
        
    def speak(self, text):
        try:
            print("Bot:", text)
            # Chia văn bản thành các câu nhỏ
            chunks = self.split_into_sentences(text)
            
            for i, chunk in enumerate(chunks):
                if not chunk.strip():  # Bỏ qua chunk rỗng
                    continue
                    
                filename = f"temp_audio_{i}.mp3"
                tts = gTTS(text=chunk, lang=self.language)
                tts.save(filename)
                playsound.playsound(filename)
                os.remove(filename)
                
        except Exception as e:
            print(f"Lỗi chuyển đổi text to speech: {str(e)}")