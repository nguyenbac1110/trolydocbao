import requests
from bs4 import BeautifulSoup
import random
import webbrowser
class XuLyTinTuc:
    def __init__(self):
        self.duongdan = "https://vnexpress.net/"
        self.luutrutintuc = []
        self.baibao_hientai = None
        self.trangbao_hientai = "VnExpress"
        
        # Định nghĩa các chuyên mục chung cơ bản
        self.danhmuc_chung = {
            'thời sự': 'thoi-su',
            'thế giới': 'the-gioi',
            'kinh doanh': 'kinh-doanh',
            'thể thao': 'the-thao',
            'giải trí': 'giai-tri',
            'giáo dục': 'giao-duc',
            'pháp luật': 'phap-luat',
            'sức khỏe': 'suc-khoe',
            'đời sống': 'doi-song',
            'du lịch': 'du-lich',
            'khoa học': 'khoa-hoc',
            'văn hóa': 'van-hoa'
        }
        
        # Cấu hình chi tiết cho từng trang báo
        self.danhsach_trangbao = {
            "vnexpress": {
                "ten": "VnExpress",
                "url": "https://vnexpress.net/",
                "mota": "Báo điện tử hàng đầu Việt Nam",
                "danhmuc": {
                    **self.danhmuc_chung,
                    'xe': 'oto-xe-may',
                    'công nghệ': 'so-hoa',
                    'góc nhìn': 'goc-nhin',
                    'podcasts': 'podcast',
                    'video': 'video',
                    'bất động sản': 'bat-dong-san'
                },
                "prefix": "/",
                "suffix": ""
            },
         
            "tienphong": {
                "ten": "Tiền Phong",
                "url": "https://tienphong.vn",
                "mota": "Cơ quan của Trung ương Đoàn TNCS Hồ Chí Minh",
                "danhmuc": {
                    **self.danhmuc_chung,
                    'xã hội': 'xa-hoi',
                    'kinh tế': 'kinh-te',
                    'giới trẻ': 'gioi-tre',
                    'bạn đọc': 'ban-doc',
                    'xe': 'xe',
                    'địa ốc': 'dia-oc',
                    'bóng đá': 'the-thao-bong-da',
                    'video': 'video-clip',
                    'hoa hậu': 'hoa-hau'
                },
                "prefix": "/",
                "suffix": "/"
            },
            "vietnamnet": {
                "ten": "VietnamNet",
                "url": "https://vietnamnet.vn/",
                "mota": "Báo điện tử thuộc Bộ Thông tin và Truyền thông",
                "danhmuc": {
                    **self.danhmuc_chung,
                    'chính trị': 'chinh-tri',
                    'thông tin truyền thông': 'thong-tin-truyen-thong',
                    'bất động sản': 'bat-dong-san',
                    'bạn đọc': 'ban-doc',
                    'bóng đá việt nam': 'the-thao/bong-da-viet-nam',
                    'bóng đá quốc tế': 'the-thao/bong-da-quoc-te'
                },
                "prefix": "/",
                "suffix": ""
            }
        }

        
        self.trangbao_selectors = {
            "vnexpress": {
              
                "category": {
                    "article": ['article.item-news', 'article.item-news-common'],
                    "title": ['h3.title-news', 'h2.title-news'],
                    "description": ['p.description'],
                    "link": 'a[href]'
                }
            },
            "tienphong": {
            
                "category": {
                    "article": ['article.story', 'div.story--primary', 'div.story--secondary'],
                    "title": ['h3.story__title', 'h2.story__title'],
                    "description": ['div.story__summary'],
                    "link": 'a[href]'
                }
            },
            "vietnamnet": {
             
                "category": {
                    "article": ['div.box-news-container', 'article.item-news'],
                    "title": ['h3.title', 'h2.title'],
                    "description": ['p.lead', 'div.lead'],
                    "link": 'a[href]'
                }
            },
            "baomoi": {
             
                "category": {
                    "article": ['div.story', 'div.story--primary'],
                    "title": ['h3.story__heading'],
                    "description": ['div.story__summary'],
                    "link": 'a[href]'
                }
            }
        }

    def laytin_moinhat(self):
        """Lấy tin mới nhất từ trang báo hiện tại"""
        try:
            response = requests.get(self.duongdan)
            soup = BeautifulSoup(response.content, 'html.parser')
            danhsachtin = []
            ketqua = []
            
            # Set để lưu trữ URL đã thu thập để tránh trùng lặp
            url_dadanhsach = set()

            # Xử lý theo từng trang báo
            if self.trangbao_hientai == "VnExpress":
                articles = soup.find_all(['article'], {
                    'class': ['item-news', 'item-news-common', 'article-item']
                })
                
                for article in articles:
                    title_tag = article.find(['h2', 'h3'], class_='title-news')
                    if title_tag:
                        link = title_tag.find('a')
                        if link:
                            tieude = link.get('title', '').strip()
                            url = link.get('href', '')
                            if tieude and url:
                                danhsachtin.append({
                                    'tieude': tieude,
                                    'url': url
                                })
                                ketqua.append(f"Tiêu đề: {tieude}")

            elif self.trangbao_hientai == "Tiền Phong":
                # Xác định xem URL hiện tại có phải là trang chủ hay không
                is_homepage = self.duongdan.rstrip('/') == self.danhsach_trangbao["tienphong"]["url"].rstrip('/')
                
                # Dựa vào URL hiện tại để xác định cách quét bài viết
                if is_homepage:
                    # Nếu là trang chủ, quét cả các phần rank và bài viết nổi bật
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
                                        ketqua.append(f"Tiêu đề: {tieude}")
                
                    # 2. Quét các bài viết chính khác
                    main_articles = soup.find_all('article', class_='story')
                    for article in main_articles:
                        # Bỏ qua các bài viết đã nằm trong phần rank
                        if article.parent and article.parent.get('class') and any(cls in ['rank-1', 'rank-2', 'rank-3'] for cls in article.parent.get('class')):
                            continue
                            
                        heading = article.find('h3', class_='story__heading')
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
                                    ketqua.append(f"Tiêu đề: {tieude}")
                else:
                    # Nếu là trang chuyên mục, tìm container chính chứa các bài viết
                    main_content = soup.find('div', class_='box-content content-list')
                    
                    if main_content:
                        # Lấy các bài viết trong chuyên mục
                        articles = main_content.find_all('article', class_='story')
                        
                        for article in articles:
                            heading = article.find('h3', class_='story__heading')
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
                                        ketqua.append(f"Tiêu đề: {tieude}")
                
                    # Nếu không tìm thấy bài viết nào trong container chính
                    # Tìm kiếm theo cách thay thế để đảm bảo lấy được bài viết
                    if not danhsachtin:
                        # Tìm các bài viết có thể nằm trong cấu trúc khác
                        all_articles = soup.find_all('article', class_='story')
                        for article in all_articles:
                            heading = article.find(['h2', 'h3'], class_='story__heading')
                            if heading:
                                link = heading.find('a', class_='cms-link')
                                if link:
                                    tieude = link.get('title', '') or link.text.strip()
                                    url = link.get('href', '')
                                    # Kiểm tra xem URL có thuộc về chuyên mục hiện tại hay không
                                    if tieude and url and url not in url_dadanhsach:
                                        # Kiểm tra URL có chứa tên chuyên mục trong đường dẫn không
                                        # Đây là kiểm tra bổ sung để đảm bảo bài viết thuộc về chuyên mục đã chọn
                                        chuyenmuc = self.duongdan.split('/')[-2] if self.duongdan.endswith('/') else self.duongdan.split('/')[-1]
                                        if chuyenmuc in url:
                                            url_dadanhsach.add(url)
                                            danhsachtin.append({
                                                'tieude': tieude,
                                                'url': url
                                            })
                                            ketqua.append(f"Tiêu đề: {tieude}")

            elif self.trangbao_hientai == "VietnamNet":
                articles = soup.find_all(['div', 'article'], {
                    'class': ['horizontalPost', 'verticalPost']
                })
                
                for article in articles:
                    title_tag = article.find(['h2', 'h3'], class_=['horizontalPost__main-title', 'verticalPost__main-title'])
                    if title_tag:
                        link = title_tag.find('a')
                        if link:
                            tieude = link.get('title', '').strip()
                            url = 'https://vietnamnet.vn' + link.get('href', '')
                            if tieude and url:
                                danhsachtin.append({
                                    'tieude': tieude,
                                    'url': url
                                })
                                ketqua.append(f"Tiêu đề: {tieude}")

            self.luutrutintuc = danhsachtin[:10]  # Lưu 10 tin đầu tiên
            return "\n".join(ketqua[:10])  # Trả về 10 tin đầu tiên, mỗi tin một dòng

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
                
                # Xử lý theo từng trang báo
                if self.trangbao_hientai == "VnExpress":
                    # Lấy description
                    description = soup.find('p', class_='description')
                    if description:
                        noidung_parts.append(description.text.strip())
                    
                    # Lấy nội dung chính
                    article_content = soup.find('article', class_='fck_detail')
                    if article_content:
                        paragraphs = article_content.find_all(['p', 'h2', 'h3'], class_=['Normal', 'title_news'])
                        noidung_parts.extend([p.text.strip() for p in paragraphs if p.text.strip()])
                    
                elif self.trangbao_hientai == "Tiền Phong":
                    # Lấy sapo (tóm tắt)
                    sapo = soup.find('div', class_='article__sapo')
                    if sapo:
                        noidung_parts.append(sapo.text.strip())
                    
                    # Lấy nội dung chính
                    article_content = soup.find('div', class_=['article-content', 'article-body'])
                    if article_content:
                        paragraphs = article_content.find_all(['p', 'h2', 'h3'])
                        noidung_parts.extend([p.text.strip() for p in paragraphs if p.text.strip()])
                    
                elif self.trangbao_hientai == "VietnamNet":
                    # Lấy sapo
                    sapo = soup.find('h2', class_='content-detail-sapo')
                    if sapo:
                        noidung_parts.append(sapo.text.strip())
                    
                    # Lấy nội dung chính
                    article_content = soup.find('div', class_='maincontent')
                    if article_content:
                        paragraphs = article_content.find_all(['p', 'h2', 'h3'])
                        noidung_parts.extend([p.text.strip() for p in paragraphs if p.text.strip() and not p.find('figure')])
                
                # Loại bỏ các đoạn trùng lặp và nối nội dung
                noidung_parts = list(dict.fromkeys(noidung_parts))
                noidung_daydu = ' '.join(noidung_parts)
                
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
            "Xin chào! Tôi là trợ lý đọc báo thông minh.",
            "Tôi có thể giúp bạn:",
            "- Đọc tin tức từ nhiều trang báo khác nhau",
            "- Đọc tin tức theo chuyên mục bạn quan tâm", 
            "- Đọc chi tiết nội dung bài báo",
            "- Tóm tắt nội dung bài báo",
            "",
            "Bạn muốn đọc tin tức từ trang báo nào?",
            "Tôi có thể đọc từ VnExpress, Tiền Phong và VietnamNet."
        ]
        return "\n".join(gioi_thieu)

    def chao_hoi(self):
        chao = [
            "Xin chào! Tôi là trợ lý đọc báo thông minh.",
            "Bạn muốn đọc tin tức từ trang báo nào?", 
            "Tôi có thể đọc từ VnExpress, Tiền Phong và VietnamNet."
        ]
        return "\n".join(chao)

    def chon_trangbao(self, text):
        text_lower = text.lower()
        
        for key, trang in self.danhsach_trangbao.items():
            if key in text_lower or trang["ten"].lower() in text_lower:
                self.duongdan = trang["url"]
                self.trangbao_hientai = trang["ten"]
                
                # Mở trang báo trong trình duyệt
                try:
                    webbrowser.open(self.duongdan)
                except:
                    pass  # Bỏ qua lỗi khi mở trình duyệt
                    
                return f"Bạn đã chọn {trang['ten']} - {trang['mota']}. Tôi đã mở trang báo trong trình duyệt. Bạn muốn đọc tin về lĩnh vực nào? Ví dụ: thời sự, thể thao, giải trí, kinh doanh..."
        
        return "Tôi không nhận ra trang báo này. Hiện tại tôi hỗ trợ đọc từ: VnExpress, Tiền Phong và VietnamNet. Vui lòng chọn lại."

    def xuly_yeucau(self, intent, text):
        # Danh sách từ khóa để nhận diện yêu cầu giới thiệu
        gioi_thieu_keywords = [
            "giới thiệu", "bạn là ai", "bạn có thể làm gì", "chức năng", 
            "khả năng", "làm được gì", "giúp được gì", "hỗ trợ gì", 
            "có thể làm", "bạn làm được gì", "bạn giúp được gì"
        ]
        
        # Kiểm tra intent và từ khóa giới thiệu trước
        if (intent == 'intro_bot' or 
            any(keyword in text.lower() for keyword in gioi_thieu_keywords)):
            return self.gioi_thieu_bot()
        
        elif intent == 'greeting':
            return self.chao_hoi()
        
        elif intent == 'select_newspaper':
            return self.chon_trangbao(text)
        
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
            return result
        
        elif intent == 'category_news' and text:
            return self.lay_tin_theloai(text)
        
        else:
            # Thông báo lỗi rõ ràng hơn
            return ("Xin lỗi, tôi không hiểu yêu cầu của bạn. "
                    "Bạn có thể:\n"
                    "- Chọn trang báo để đọc (VnExpress, Tiền Phong, VietnamNet)\n"
                    "- Đọc tin theo chuyên mục (thể thao, kinh doanh, giải trí...)\n"
                    "- Đọc chi tiết một bài báo\n"
                    "- Hoặc hỏi tôi 'bạn có thể làm gì?' để biết thêm chi tiết")

    def lay_tin_theloai(self, text):
        noidung_timkiem = text.lower()
        chuyenmuc_duocchon = None
        
        # Lấy thông tin trang báo hiện tại
        trangbao = None
        for key, trang in self.danhsach_trangbao.items():
            if trang["ten"] == self.trangbao_hientai:
                trangbao = trang
                break
        
        if not trangbao:
            return "Không thể xác định trang báo hiện tại"
        
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
            return f"Chuyên mục này không có trên {self.trangbao_hientai} hoặc chưa được hỗ trợ. Vui lòng thử chuyên mục khác như: {', '.join(list(trangbao['danhmuc'].keys())[:5])}..."
        
        try:
            # Tạo URL đầy đủ cho chuyên mục
            duongdan_url = f"{trangbao['url'].rstrip('/')}{trangbao['prefix']}{chuyenmuc_duocchon}"
            # Đặc biệt xử lý cho Tiền Phong - đảm bảo luôn có dấu / ở cuối
            if self.trangbao_hientai == "Tiền Phong" and not duongdan_url.endswith('/'):
                duongdan_url += '/'
            else:
                duongdan_url += trangbao['suffix']
            
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
                return f"Trang {self.trangbao_hientai} đã chặn truy cập đến chuyên mục này. Tôi đã mở trang trong trình duyệt để bạn xem trực tiếp."
            elif phanhoi.status_code != 200:
                return f"Không thể tải tin tức cho chuyên mục này. Tôi đã mở trang trong trình duyệt để bạn xem trực tiếp."
            
            phanhoi.raise_for_status()
            
            # Kiểm tra nội dung có chứa thông báo lỗi hoặc từ chối truy cập
            if "access denied" in phanhoi.text.lower() or "blocked" in phanhoi.text.lower() or "403 forbidden" in phanhoi.text.lower():
                return f"Trang {self.trangbao_hientai} đã chặn truy cập đến chuyên mục này. Tôi đã mở trang trong trình duyệt để bạn xem trực tiếp."
            
            # Lưu URL hiện tại để truy cập bài viết
            self.duongdan = duongdan_url
            
            # Thông báo về việc mở trình duyệt
            return f"Đã mở chuyên mục {chuyenmuc} của {self.trangbao_hientai} trong trình duyệt. Đang tải tin tức...\n\n" + self.laytin_moinhat()
            
        except requests.Timeout:
            return f"Không thể tải tin tức cho chuyên mục này do quá thời gian chờ. Tôi đã mở trang trong trình duyệt để bạn xem trực tiếp."
        except requests.RequestException as e:
            return f"Không thể kết nối đến chuyên mục này. Tôi đã mở trang trong trình duyệt để bạn xem trực tiếp."
        except Exception as e:
            return f"Đã xảy ra lỗi khi tải tin tức cho chuyên mục này. Tôi đã mở trang trong trình duyệt để bạn xem trực tiếp."