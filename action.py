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
        self.tu_khoa_loai_bo = [
            'đọc bài', 'đọc chi tiết', 'xem bài', 'bài', 'đọc', 
            'xem', 'nội dung', 'chi tiết', 'cho tôi xem'
        ]
    
    def lay_tin_moi_nhat(self, so_luong=5, bao_cu_the=None):
        if bao_cu_the and bao_cu_the in self.danh_sach_bao:
            url = bao_cu_the
            thong_bao = f"Đang lấy {so_luong} tin từ {bao_cu_the}"
        else:
            url = random.choice(self.danh_sach_bao)
            thong_bao = f"Đang lấy {so_luong} tin mới nhất từ {url}"
        
        try:
            print(thong_bao)
            phan_hoi = requests.get(url)
            phan_hoi.raise_for_status()
            
            soup = BeautifulSoup(phan_hoi.content, 'html.parser')
            self.luu_tru_tin_tuc = []
            danh_sach_tieu_de = []
            
            # Different selectors for different news sites
            if 'vnexpress.net' in url:
                danh_sach_tin = soup.select('.title-news a, .item-news a', limit=so_luong)
                for tin in danh_sach_tin:
                    tieu_de_text = tin.text.strip()
                    link_url = tin.get('href')
                    if link_url and tieu_de_text:
                        if not link_url.startswith('http'):
                            link_url = url + link_url
                        self.luu_tru_tin_tuc.append({
                            'tieu_de': tieu_de_text,
                            'link': link_url
                        })
                        danh_sach_tieu_de.append(tieu_de_text)
            elif 'kenh14.vn' in url:
                danh_sach_tin = soup.select('.knswli-title a, .klwfn-title a', limit=so_luong)
                for tin in danh_sach_tin:
                    tieu_de_text = tin.text.strip()
                    link_url = tin.get('href')
                    if link_url and tieu_de_text:
                        if not link_url.startswith('http'):
                            link_url = 'https://kenh14.vn' + link_url
                        self.luu_tru_tin_tuc.append({
                            'tieu_de': tieu_de_text,
                            'link': link_url
                        })
                        danh_sach_tieu_de.append(tieu_de_text)
            
            else:
                # Generic approach for other news sites
                selectors = ['article a', '.title a', '.headline a', '.news-item a', 'h3 a']
                for selector in selectors:
                    danh_sach_tin = soup.select(selector, limit=so_luong)
                    if danh_sach_tin:
                        for tin in danh_sach_tin:
                            tieu_de_text = tin.text.strip()
                            link_url = tin.get('href')
                            if link_url and tieu_de_text:
                                if not link_url.startswith('http'):
                                    link_url = url + link_url
                                self.luu_tru_tin_tuc.append({
                                    'tieu_de': tieu_de_text,
                                    'link': link_url
                                })
                                danh_sach_tieu_de.append(tieu_de_text)
                        break
                    
                    self.luu_tru_tin_tuc.append({
                        'tieu_de': tieu_de_text,
                        'link': link_url
                    })
                    danh_sach_tieu_de.append(f"{tieu_de_text}")
            
            # Add numbering to titles for better readability
            danh_sach_tieu_de_format = []
            for i, tieu_de in enumerate(danh_sach_tieu_de, 1):
                # Remove common category/section names
                for category in ['Sports', 'News', 'Entertainment', 'Business', 'Technology', 'Thể thao', 'Tin tức', 'Giải trí', 'Kinh doanh', 'Công nghệ']:
                    if tieu_de == category:
                        continue
                    tieu_de = tieu_de.replace(f"{category}: ", "")
                    tieu_de = tieu_de.replace(f"{category} - ", "")
                if tieu_de.strip():
                    danh_sach_tieu_de_format.append(f"{i}. {tieu_de}")
            
            return danh_sach_tieu_de_format if danh_sach_tieu_de_format else ["Không tìm thấy tin tức."]
        except requests.RequestException:
            return ["Không thể kết nối đến trang báo. Vui lòng thử lại sau."]

    def mo_bai_bao(self, tieu_de):
        if not self.luu_tru_tin_tuc:
            return "Vui lòng xem tin tức mới nhất trước khi đọc chi tiết"
        
        tu_timkiem = tieu_de.lower()
        for tu in self.tu_khoa_loai_bo:
            tu_timkiem = tu_timkiem.replace(tu, '').strip()
        
        if not tu_timkiem:
            return "Vui lòng nói rõ tiêu đề bài báo bạn muốn đọc"
        
        tin_phuhop = None
        tile_phuhop_max = 0
        
        for tin in self.luu_tru_tin_tuc:
            tieude = tin['tieu_de'].lower()
            
            danhsach_tu_tim = [tu for tu in tu_timkiem.split() if len(tu) > 1]
            danhsach_tu_tieude = tieude.split()
            
            so_tu_trung = sum(1 for tu in danhsach_tu_tim if any(tu in tu_tieude for tu_tieude in danhsach_tu_tieude))
            
            if so_tu_trung > 0:
                tile_phuhop = so_tu_trung / len(danhsach_tu_tim)
                if tile_phuhop > tile_phuhop_max:
                    tile_phuhop_max = tile_phuhop
                    tin_phuhop = tin
        
        if tin_phuhop and tile_phuhop_max >= 0.3:
            try:
                webbrowser.open(tin_phuhop['link'])
                return "Đang mở bài báo trong trình duyệt."
            except Exception as e:
                return "Không thể mở bài báo. Vui lòng thử lại sau."
            
        return "Không tìm thấy bài báo với tiêu đề này. Vui lòng nói rõ tiêu đề bài báo bạn muốn đọc."
    
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
                        messages=[
                            {"role": "system", "content": "Bạn là một trợ lý AI chuyên tóm tắt nội dung bài báo. Hãy tóm tắt bài báo sau một cách ngắn gọn, súc tích nhưng đầy đủ ý chính:"},
                            {"role": "user", "content": noi_dung_bai}
                        ],
                        temperature=0.7,
                        max_tokens=500
                    )
                    return response['choices'][0]['message']['content']
                except Exception as e:
                    print(f"Lỗi khi tóm tắt bài báo: {str(e)}")
                    return "Không thể tóm tắt bài báo này."
        return "Không tìm thấy bài báo để tóm tắt."
    
    def xu_ly_yeu_cau(self, loai_yeu_cau, noi_dung=None):
        if loai_yeu_cau == 'latest_news':
            return self.lay_tin_moi_nhat()
        elif loai_yeu_cau == 'search_news':
            return self.mo_bai_bao(noi_dung)
        elif loai_yeu_cau == 'summarize_news':
            return self.tom_tat_bai_bao(noi_dung)
        elif loai_yeu_cau == 'open_article':
            return self.mo_bai_bao(noi_dung)
        elif loai_yeu_cau == 'intro_bot':
            return "Xin chào! Tôi là chatbot trợ lý đọc báo. Tôi có thể cung cấp tin tức mới nhất từ nhiều nguồn, mở bài báo trực tiếp trên trình duyệt và tóm tắt nội dung bài viết. Bạn cần giúp gì?"
        else:
            return "Tôi không hiểu yêu cầu của bạn."
