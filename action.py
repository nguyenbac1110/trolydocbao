import requests
from bs4 import BeautifulSoup
import random
import webbrowser
import openai
openai.api_key = "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"
class XuLyTinTuc:
    def __init__(self):
        self.danh_sach_bao = [
            "https://vnexpress.net/", "https://baomoi.com/", "https://dantri.com.vn/", 
            "https://www.24h.com.vn/", "https://vietnamnet.vn/", "https://tuoitre.vn/", 
            "https://kenh14.vn/", "https://thanhnien.vn/", "https://znews.vn/", "https://soha.vn/"
        ]
        self.luu_tru_tin_tuc = []
    
    def lay_tin_moi_nhat(self, so_luong=5, bao_cu_the=None):
        if bao_cu_the and bao_cu_the in self.danh_sach_bao:
            url = bao_cu_the
        else:
            url = random.choice(self.danh_sach_bao)
        
        try:
            phan_hoi = requests.get(url)
            phan_hoi.raise_for_status()
            
            soup = BeautifulSoup(phan_hoi.content, 'html.parser')
            danh_sach_tin = soup.find_all('article', limit=so_luong)
            
            self.luu_tru_tin_tuc = []
            danh_sach_tieu_de = []
            
            for bai_bao in danh_sach_tin:
                tieu_de = bai_bao.find('h3')
                link = bai_bao.find('a', href=True)
                
                if tieu_de and link:
                    tieu_de_text = tieu_de.text.strip()
                    link_url = link['href']
                    if not link_url.startswith('http'):
                        link_url = url + link_url
                    
                    self.luu_tru_tin_tuc.append({
                        'tieu_de': tieu_de_text,
                        'link': link_url
                    })
                    danh_sach_tieu_de.append(f"{tieu_de_text}")
            
            return danh_sach_tieu_de if danh_sach_tieu_de else ["Không tìm thấy tin tức."]
        except requests.RequestException:
            return ["Không thể kết nối đến trang báo. Vui lòng thử lại sau."]

    def mo_bai_bao(self, tieu_de):
        for tin in self.luu_tru_tin_tuc:
            if tieu_de.lower() in tin['tieu_de'].lower():
                webbrowser.open(tin['link'])
                return "Đang mở bài báo trong trình duyệt."
        return "Không tìm thấy bài báo này."
    
    def tom_tat_bai_bao(self, tieu_de):
        for tin in self.luu_tru_tin_tuc:
            if tieu_de.lower() in tin['tieu_de'].lower():
                try:
                    phan_hoi = requests.get(tin['link'])
                    phan_hoi.raise_for_status()
                    soup = BeautifulSoup(phan_hoi.content, 'html.parser')
                    
                    noi_dung_bai = ' '.join([p.text.strip() for p in soup.find_all('p')])
                    
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "system", "content": "Tóm tắt bài báo:"},
                                  {"role": "user", "content": noi_dung_bai}]
                    )
                    return response['choices'][0]['message']['content']
                except Exception:
                    return "Không thể tóm tắt bài báo này."
        return "Không tìm thấy bài báo để tóm tắt."
    
    def xu_ly_yeu_cau(self, loai_yeu_cau, noi_dung=None):
        if loai_yeu_cau == 'latest_news':
            return self.lay_tin_moi_nhat()
        elif loai_yeu_cau == 'search_news':
            return self.mo_bai_bao(noi_dung)
        elif loai_yeu_cau == 'summarize_news':
            return self.tom_tat_bai_bao(noi_dung)
        elif loai_yeu_cau == 'intro_bot':
            return "Xin chào! Tôi là chatbot trợ lý đọc báo. Tôi có thể cung cấp tin tức mới nhất từ nhiều nguồn, mở bài báo trực tiếp trên trình duyệt và tóm tắt nội dung bài viết. Bạn cần giúp gì?"
        else:
            return "Tôi không hiểu yêu cầu của bạn."
