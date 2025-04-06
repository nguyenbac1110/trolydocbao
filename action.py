import requests
from bs4 import BeautifulSoup
import random
import webbrowser
class XuLyTinTuc:
    def __init__(self):
        self.duongdan = "https://nhandan.vn/"
        self.luutrutintuc = []
        self.baibao_hientai = None
        self.trangbao_hientai = "Nhân Dân"
        
        # Định nghĩa các chuyên mục cơ bản của báo Nhân Dân
        self.danhmuc_chung = {
            'chính trị': 'chinhtri',
            'kinh tế': 'kinhte',
            'văn hóa': 'vanhoa',
            'xã hội': 'xahoi',
            'pháp luật': 'phapluat',
            'du lịch': 'du-lich',
            'thế giới': 'thegioi',
            'thể thao': 'thethao',
            'giáo dục': 'giaoduc',
            'y tế': 'y-te',
            'khoa học công nghệ': 'khoahoc-congnghe',
            'môi trường': 'moi-truong',
            'bạn đọc': 'bandoc'
        }
        
        # Cấu hình chi tiết cho Báo Nhân Dân
        self.danhsach_trangbao = {
            "nhandan": {
                "ten": "Nhân Dân",
                "url": "https://nhandan.vn/",
                "mota": "Cơ quan Trung ương của Đảng Cộng sản Việt Nam",
                "danhmuc": {
                    **self.danhmuc_chung,
                    'xã luận': 'xa-luan',
                    'bình luận phê phán': 'binh-luan-phe-phan',
                    'xây dựng đảng': 'xay-dung-dang',
                    'tài chính chứng khoán': 'chungkhoan',
                    'thông tin hàng hóa': 'thong-tin-hang-hoa',
                    'bhxh và cuộc sống': 'bhxh-va-cuoc-song',
                    'người tốt việc tốt': 'nguoi-tot-viec-tot',
                    'bình luận quốc tế': 'binh-luan-quoc-te',
                    'asean': 'asean',
                    'châu phi': 'chau-phi',
                    'châu mỹ': 'chau-my',
                    'châu âu': 'chau-au',
                    'trung đông': 'trung-dong',
                    'châu á-tbd': 'chau-a-tbd',
                    'góc tư vấn': 'goc-tu-van',
                    'đường dây nóng': 'duong-day-nong',
                    'kiểm chứng thông tin': 'factcheck'
                },
                "prefix": "/",
                "suffix": "/"
            }
        }

        # Cấu hình các bộ chọn (selectors) HTML cho Báo Nhân Dân
        self.trangbao_selectors = {
            "nhandan": {
                "category": {
                    "article": ['article.story', 'div.rank-1', 'div.rank-2', 'div.rank-3'],
                    "title": ['h2.story__heading', 'h3.story__heading'],
                    "description": ['div.story__summary'],
                    "link": 'a.cms-link'
                }
            }
        }
    
    def la_bai_video(self, tieude):
        """Kiểm tra xem tiêu đề có bắt đầu bằng [Video] hay không"""
        return tieude.startswith('[Video]')
    
    def loc_bai_video(self, danhsach_bai):
        """Lọc bỏ tất cả bài viết có tiêu đề bắt đầu bằng [Video]"""
        return [bai for bai in danhsach_bai if not self.la_bai_video(bai['tieude'])]

    def laytin_moinhat(self):
        """Lấy tin mới nhất từ trang báo Nhân Dân"""
        try:
            response = requests.get(self.duongdan)
            soup = BeautifulSoup(response.content, 'html.parser')
            danhsachtin = []
            ketqua = []
            
            # Set để lưu trữ URL đã thu thập để tránh trùng lặp
            url_dadanhsach = set()
            
            # Xác định xem URL hiện tại có phải là trang chủ hay không
            is_homepage = self.duongdan.rstrip('/') == self.danhsach_trangbao["nhandan"]["url"].rstrip('/')
            
            # Nếu là trang chủ, quét cả các phần rank và bài viết nổi bật
            if is_homepage:
                # 1. Quét các phần rank trước (vì đây là các bài viết nổi bật nhất)
                rank_divs = soup.find_all('div', class_=['rank-1', 'rank-2', 'rank-3'])
                for div in rank_divs:
                    rank_articles = div.find_all('article', class_='story')
                    for article in rank_articles:
                        heading = article.find(['h2', 'h3'], class_='story__heading')
                        if heading:
                            link = heading.find('a', class_='cms-link')
                            if link:
                                tieude = link.get('title', '') or link.text.strip()
                                url = link.get('href', '')
                                if tieude and url and url not in url_dadanhsach:
                                    url_dadanhsach.add(url)
                                    danhsachtin.append({
                                        'tieude': tieude,
                                        'url': url
                                    })
            
                # 2. Quét các bài viết chính khác
                main_articles = soup.find_all('article', class_='story')
                for article in main_articles:
                    # Bỏ qua các bài viết đã nằm trong phần rank
                    if article.parent and article.parent.get('class') and any(cls in ['rank-1', 'rank-2', 'rank-3'] for cls in article.parent.get('class')):
                        continue
                        
                    heading = article.find(['h2', 'h3'], class_='story__heading')
                    if heading:
                        link = heading.find('a', class_='cms-link')
                        if link:
                            tieude = link.get('title', '') or link.text.strip()
                            url = link.get('href', '')
                            if tieude and url and url not in url_dadanhsach:
                                url_dadanhsach.add(url)
                                danhsachtin.append({
                                    'tieude': tieude,
                                    'url': url
                                })
            else:
                # Nếu là trang chuyên mục, tìm tất cả bài viết
                articles = soup.find_all('article', class_='story')
                
                for article in articles:
                    heading = article.find(['h2', 'h3'], class_='story__heading')
                    if heading:
                        link = heading.find('a', class_='cms-link')
                        if link:
                            tieude = link.get('title', '') or link.text.strip()
                            url = link.get('href', '')
                            if tieude and url and url not in url_dadanhsach:
                                url_dadanhsach.add(url)
                                danhsachtin.append({
                                    'tieude': tieude,
                                    'url': url
                                })

            # Lọc bỏ tất cả bài viết video
            danhsachtin_loc = self.loc_bai_video(danhsachtin)
            
            # Tạo danh sách kết quả hiển thị
            ketqua = [f"Tiêu đề: {tin['tieude']}" for tin in danhsachtin_loc[:10]]
            
            # Lưu danh sách tin đã lọc bỏ video
            self.luutrutintuc = danhsachtin_loc[:10]
            
            # Trả về 10 tin đầu tiên đã lọc, mỗi tin một dòng
            return "\n".join(ketqua)

        except Exception as e:
            print(f"Lỗi khi lấy tin mới nhất: {str(e)}")
            return "Đã xảy ra lỗi khi tải tin tức. Vui lòng thử lại sau."

    def lay_chitiet_baibao(self, tieude_timkiem):
        if not self.luutrutintuc:
            return "Vui lòng xem tin tức mới nhất trước khi đọc chi tiết bài báo"
        
        tukhoa_loaibo = [
            'đọc bài', 'đọc chi tiết', 'xem bài', 'bài', 'đọc', 
            'xem', 'nội dung', 'chi tiết', 'cho tôi xem'
        ]
        
        tu_timkiem = tieude_timkiem.lower()
        for tu in tukhoa_loaibo:
            tu_timkiem = tu_timkiem.replace(tu, '').strip()
        
        if not tu_timkiem:
            return "Vui lòng nói rõ tiêu đề bài báo bạn muốn đọc"
        
        tin_phuhop = None
        tile_phuhop_max = 0
        
        for tin in self.luutrutintuc:
            tieude = tin['tieude'].lower()
            
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
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5'
                }
                
                phanhoi = requests.get(tin_phuhop['url'], headers=headers, timeout=10)
                phanhoi.raise_for_status()
                soup = BeautifulSoup(phanhoi.content, 'html.parser')
                
                noidung_parts = []
                
                # Xử lý cho Báo Nhân Dân
                # Lấy tiêu đề
                article_title = soup.find('h1', class_='article__title')
                if article_title:
                    noidung_parts.append(article_title.text.strip())
                
                # Lấy tóm tắt (sapo)
                article_sapo = soup.find('div', class_='article__sapo')
                if article_sapo:
                    noidung_parts.append(article_sapo.text.strip())
                
                # Lấy nội dung chính - tìm tất cả thẻ p trong bài viết
                article_content = soup.find_all('p')
                if article_content:
                    for p in article_content:
                        # Loại bỏ các caption ảnh và thành phần không phải nội dung chính
                        if not p.find('figure') and p.text.strip():
                            noidung_parts.append(p.text.strip())
                
                # Nếu không tìm thấy nội dung, thử phương pháp khác
                if len(noidung_parts) <= 2:  # Nếu chỉ có tiêu đề và sapo
                    article_body = soup.find('div', class_='article-body')
                    if article_body:
                        paragraphs = article_body.find_all(['p', 'h2', 'h3'])
                        for p in paragraphs:
                            if p.text.strip() and not p.find('figure'):
                                noidung_parts.append(p.text.strip())
                
                # Loại bỏ các đoạn trùng lặp và nối nội dung
                noidung_parts = list(dict.fromkeys(noidung_parts))
                noidung_daydu = '\n\n'.join(noidung_parts)
                
                if not noidung_daydu:
                    return f"Không thể đọc nội dung bài viết này. Tôi đã mở bài viết trong trình duyệt để bạn đọc."
                
                self.baibao_hientai = {
                    'tieude': tin_phuhop['tieude'],
                    'noidung': noidung_daydu
                }
                
                return self.baibao_hientai
                
            except Exception as e:
                return f"Không thể tải nội dung chi tiết. Tôi đã mở bài viết trong trình duyệt để bạn đọc."
        
        return "Không tìm thấy bài báo với tiêu đề này. Vui lòng nói rõ tiêu đề bài báo bạn muốn đọc."

    def gioi_thieu_bot(self):
        gioi_thieu = [
            "Xin chào! Tôi là trợ lý đọc báo Nhân Dân.",
            "Tôi có thể giúp bạn:",
            "- Đọc tin tức mới nhất từ báo Nhân Dân",
            "- Đọc tin tức theo chuyên mục bạn quan tâm", 
            "- Đọc chi tiết nội dung bài báo",
            "",
            "Bạn muốn đọc tin tức về chủ đề nào? Ví dụ: chính trị, kinh tế, văn hóa, xã hội..."
        ]
        return "\n".join(gioi_thieu)

    def chao_hoi(self):
        chao = [
            "Xin chào! Tôi là trợ lý đọc báo Nhân Dân.",
            "Bạn muốn đọc tin tức về chủ đề nào? Ví dụ: chính trị, kinh tế, văn hóa, xã hội..."
        ]
        return "\n".join(chao)

    def xuly_yeucau(self, intent, text):
        # Danh sách từ khóa để nhận diện yêu cầu giới thiệu
        gioi_thieu_keywords = [
            "giới thiệu", "bạn là ai", "bạn có thể làm gì", "chức năng", 
            "khả năng", "làm được gì", "giúp được gì", "hỗ trợ gì", 
            "có thể làm", "bạn làm được gì", "bạn giúp được gì"
        ]
        
        text_lower = text.lower()
        
        # Kiểm tra intent và từ khóa giới thiệu trước
        if (intent == 'intro_bot' or 
            any(keyword in text_lower for keyword in gioi_thieu_keywords)):
            return self.gioi_thieu_bot()
        
        elif intent == 'greeting':
            return self.chao_hoi()
        
        elif intent == 'latest_news':
            try:
                webbrowser.open(self.duongdan)
            except:
                pass
            return self.laytin_moinhat()
        
        elif intent == 'search_news':
            result = self.lay_chitiet_baibao(text)
            if isinstance(result, dict):
                for tin in self.luutrutintuc:
                    if tin['tieude'] == result['tieude']:
                        try:
                            webbrowser.open(tin['url'])
                        except:
                            pass
                        break
                return result['noidung']  # Trả về nội dung bài báo
            return result
        
        elif intent == 'category_news' and text:
            return self.lay_tin_theloai(text)
        
        else:
            # Thông báo lỗi rõ ràng hơn
            return ("Xin lỗi, tôi không hiểu yêu cầu của bạn. "
                    "Bạn có thể:\n"
                    "- Đọc tin mới nhất từ báo Nhân Dân\n"
                    "- Đọc tin theo chuyên mục (chính trị, kinh tế, văn hóa...)\n"
                    "- Đọc chi tiết một bài báo\n"
                    "- Hoặc hỏi tôi 'bạn có thể làm gì?' để biết thêm chi tiết")

    def lay_tin_theloai(self, text):
        noidung_timkiem = text.lower()
        chuyenmuc_duocchon = None
        
        # Lấy thông tin trang báo hiện tại (Nhân Dân)
        trangbao = self.danhsach_trangbao["nhandan"]
        
        # Xử lý đặc biệt cho "trang chủ"
        if "trang chủ" in noidung_timkiem:
            self.duongdan = trangbao["url"]
            try:
                webbrowser.open(self.duongdan)
            except:
                pass
            return self.laytin_moinhat()
        
        # Tìm chuyên mục phù hợp
        for chuyenmuc, duongdan in trangbao["danhmuc"].items():
            if chuyenmuc in noidung_timkiem:
                chuyenmuc_duocchon = duongdan
                break
        
        if not chuyenmuc_duocchon:
            return f"Chuyên mục này không có trên báo Nhân Dân hoặc chưa được hỗ trợ. Vui lòng thử chuyên mục khác như: {', '.join(list(trangbao['danhmuc'].keys())[:5])}..."
        
        try:
            # Tạo URL đầy đủ cho chuyên mục
            duongdan_url = f"{trangbao['url'].rstrip('/')}{trangbao['prefix']}{chuyenmuc_duocchon}{trangbao['suffix']}"
            
            # Mở chuyên mục trong trình duyệt
            try:
                webbrowser.open(duongdan_url)
            except:
                pass
            
            # Thêm header để tránh bị chặn như một bot
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
                'Referer': self.duongdan
            }
            
            phanhoi = requests.get(duongdan_url, headers=headers, timeout=10)
            
            # Kiểm tra mã trạng thái HTTP
            if phanhoi.status_code == 403:
                return f"Trang báo Nhân Dân đã chặn truy cập đến chuyên mục này. Tôi đã mở trang trong trình duyệt để bạn xem trực tiếp."
            elif phanhoi.status_code != 200:
                return f"Không thể tải tin tức cho chuyên mục này. Tôi đã mở trang trong trình duyệt để bạn xem trực tiếp."
            
            phanhoi.raise_for_status()
            
            # Kiểm tra nội dung có chứa thông báo lỗi hoặc từ chối truy cập
            if "access denied" in phanhoi.text.lower() or "blocked" in phanhoi.text.lower() or "403 forbidden" in phanhoi.text.lower():
                return f"Trang báo Nhân Dân đã chặn truy cập đến chuyên mục này. Tôi đã mở trang trong trình duyệt để bạn xem trực tiếp."
            
            # Lưu URL hiện tại để truy cập bài viết
            self.duongdan = duongdan_url
            
            # Thông báo về việc mở trình duyệt
            return f"Đã mở chuyên mục {chuyenmuc} của báo Nhân Dân trong trình duyệt. Đang tải tin tức...\n\n" + self.laytin_moinhat()
            
        except requests.Timeout:
            return f"Không thể tải tin tức cho chuyên mục này do quá thời gian chờ. Tôi đã mở trang trong trình duyệt để bạn xem trực tiếp."
        except requests.RequestException as e:
            return f"Không thể kết nối đến chuyên mục này. Tôi đã mở trang trong trình duyệt để bạn xem trực tiếp."
        except Exception as e:
            return f"Đã xảy ra lỗi khi tải tin tức cho chuyên mục này. Tôi đã mở trang trong trình duyệt để bạn xem trực tiếp."