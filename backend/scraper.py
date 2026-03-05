# scraper.py

import time
import urllib.parse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

class GeneralNewsScraper:
    def __init__(self, headless=True):
        self.options = Options()
        if headless:
            self.options.add_argument("--headless")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--log-level=3")
        
        # 1. TOPENG ANTI-BOT LEVEL DEWA (Bypass 403 Tribun/Cloudflare)
        self.options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option('useAutomationExtension', False)
        
        self.driver = None

    def start_engine(self):
        if not self.driver:
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)
            # Trik tambahan agar Cloudflare tertipu
            self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'})
            
            # 2. ALARM LOADING MAKSIMAL 15 DETIK (Jurus Paksa Stop buat web berat/iklan)
            self.driver.set_page_load_timeout(15)

    def stop_engine(self):
        if self.driver:
            self.driver.quit()
            self.driver = None

    def get_article_links(self, main_url, limit=5):
        print(f"[!] Mencari link berita di: {main_url}")
        
        # Jurus paksa stop loading
        try:
            self.driver.get(main_url)
        except:
            print("[!] Loading web terlalu lama! Memaksa robot untuk lanjut...")
            self.driver.execute_script("window.stop();")
            
        time.sleep(3) 
        
        base_domain = urllib.parse.urlparse(main_url).netloc.replace("www.", "")
        elements = self.driver.find_elements(By.TAG_NAME, 'a')
        links = []
        
        blacklist = ['login', 'register', 'tag', 'kategori', 'search', 'author', 'video', 'foto', 'indeks', 'redirect', 'delivery', 'newrevive', 'oauth', 'signout', 'livestreaming', 'digital']
        
        for el in elements:
            try:
                href = el.get_attribute('href')
                if href and 'http' in href:
                    href_lower = href.lower()
                    
                    if base_domain not in href_lower: continue
                    if any(bad_word in href_lower for bad_word in blacklist): continue
                    
                    parts = [p for p in href.split('/') if p]
                    if not parts: continue
                    last_part = parts[-1]
                    
                    # THE HYPHEN RULE: Link artikel asli biasanya punya >= 3 strip
                    if last_part.count('-') >= 3: 
                        if href not in links:
                            links.append(href)
            except:
                continue 
                
        print(f"[+] Ditemukan {len(links)} link ARTIKEL ASLI. Mengambil {limit} link...")
        return links[:limit]

    def scrape_single_article(self, url):
        # Jurus paksa stop loading di halaman artikel
        try:
            self.driver.get(url)
        except:
            self.driver.execute_script("window.stop();")
            
        time.sleep(2) 
        
        # Ambil Judul
        try:
            title = self.driver.find_element(By.TAG_NAME, 'h1').text
        except:
            title = self.driver.title 

        # Ambil Tanggal (TEKS MENTAH SAJA, Nanti Rafi yang olah di processor.py)
        raw_date_str = "Tanggal tidak ditemukan"
        try:
            # JURUS 1: Sadap Meta Data SEO (Ini yang dipakai Google, 99% Akurat!)
            meta_tags = self.driver.find_elements(By.XPATH, "//meta[@property='article:published_time' or @name='pubdate' or @name='publishdate' or @itemprop='datePublished']")
            if meta_tags:
                # Output meta tag biasanya ISO format: "2026-03-05T16:44:00+07:00"
                raw_date_str = meta_tags[0].get_attribute('content')
            
            # JURUS 2: Kalau ga ada meta tag, cari tag <time> standar
            if raw_date_str == "Tanggal tidak ditemukan":
                times = self.driver.find_elements(By.TAG_NAME, 'time')
                if times:
                    raw_date_str = times[0].text
            
            # JURUS 3: Deteksi Manual teks Indonesia (Cari yang ada WIB/WITA/WIT)
            if raw_date_str == "Tanggal tidak ditemukan":
                zona_waktu = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'WIB') or contains(text(), 'WITA') or contains(text(), 'WIT')]")
                for el in zona_waktu:
                    # Kalau panjang teksnya wajar (10-60 huruf), berarti itu tanggalnya!
                    if 10 < len(el.text) < 60: 
                        raw_date_str = el.text
                        break
        except:
            pass

        # Ambil Isi Berita
        content_paragraphs = []
        try:
            paragraphs = self.driver.find_elements(By.TAG_NAME, 'p')
            for p in paragraphs:
                if len(p.text.split()) > 10: # Minimal 10 kata biar gak ngambil footer
                    content_paragraphs.append(p.text)
        except:
            pass
            
        content = "\n\n".join(content_paragraphs)
        if not content.strip():
            content = "Gagal mengekstrak teks. Website mungkin memblokir bot."

        # KONTRAK DATA: Mengirim data ke Rafi (processor.py)
        return {
            'judul': title,
            'tanggal': raw_date_str, 
            'isi': content,
            'url': url
        }

# ==========================================
# BLOK TESTING KHUSUS SALMAN (Terminal Only)
# ==========================================
if __name__ == "__main__":
    # Ubah jadi headless=False kalau Salman mau lihat wujud browsernya
    scraper = GeneralNewsScraper(headless=True) 
    scraper.start_engine()
    
    url_tes = "https://www.cnnindonesia.com/nasional"
    links = scraper.get_article_links(url_tes, limit=5)
    
    for link in links:
        print(f"\n[>] Mengekstrak: {link}")
        data = scraper.scrape_single_article(link)
        print(f"Judul   : {data['judul']}")
        print(f"Tanggal : {data['tanggal']} (Teks Mentah)")
        print(f"Isi     : {data['isi']}...\n")
        
    scraper.stop_engine()