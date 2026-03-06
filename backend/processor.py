# processor.py

import dateparser
from datetime import datetime
from PyQt5.QtCore import QThread, pyqtSignal
from backend.scraper import GeneralNewsScraper

class ScraperProcessor(QThread):
    # ==============================
    # SIGNALS (Jembatan ke UI/Arsel)
    # ==============================
    data_found = pyqtSignal(dict)       # kirim 1 artikel bersih ke UI
    progress   = pyqtSignal(int, int)   # kirim (artikel ke-x, total) ke progress bar
    finished   = pyqtSignal()
    error      = pyqtSignal(str)

    def __init__(self, url, max_artikel=10, start_date=None, end_date=None):
        super().__init__()
        self.url         = url
        self.max_artikel = max_artikel
        self.start_date  = start_date
        self.end_date    = end_date

    # ==============================
    # FUNGSI CUCI TANGGAL
    # ==============================
    def bersihkan_tanggal(self, teks_tanggal):
        if not teks_tanggal or teks_tanggal == "Tanggal tidak ditemukan":
            return None

        teks_bersih = teks_tanggal.strip()

        # Format ISO dengan strip: "2026-03-05T08:32:43+07:00"
        if len(teks_bersih) >= 10 and teks_bersih[4] == '-':
            try:
                return teks_bersih[:10]
            except Exception:
                pass

        # Format dengan garis miring: "2026/03/05 08:32:43"
        if len(teks_bersih) >= 10 and teks_bersih[4] == '/':
            try:
                return teks_bersih[:10].replace('/', '-')
            except Exception:
                pass

        # Fallback: pakai dateparser untuk format lain
        # Contoh: "Kamis, 05 Mar 2026 08:32 WIB"
        try:
            hasil = dateparser.parse(
                teks_bersih,
                settings={
                    'PREFER_DAY_OF_MONTH': 'first',
                    'RETURN_AS_TIMEZONE_AWARE': False,
                    'LANGUAGES': ['id', 'en']
                }
            )
            if hasil:
                return hasil.strftime("%Y-%m-%d")
        except Exception:
            pass

        return None

    # ==============================
    # FUNGSI FILTER TANGGAL
    # ==============================
    def lolos_filter(self, tanggal_str):
        if not self.start_date and not self.end_date:
            return True

        if not tanggal_str:
            return False

        try:
            tgl = datetime.strptime(tanggal_str, "%Y-%m-%d")
            if self.start_date and tgl < self.start_date:
                return False
            if self.end_date and tgl > self.end_date:
                return False
            return True
        except Exception:
            return False

    # ==============================
    # FUNGSI UTAMA (dipanggil QThread)
    # ==============================
    def run(self):
        scraper = GeneralNewsScraper(headless=True)
        try:
            scraper.start_engine()

            links = scraper.get_article_links(self.url, limit=self.max_artikel)
            total = len(links)

            if total == 0:
                self.error.emit("Tidak ada link artikel yang ditemukan.")
                return

            for i, link in enumerate(links):
                try:
                    data_mentah = scraper.scrape_single_article(link)

                    tanggal_bersih = self.bersihkan_tanggal(data_mentah['tanggal'])

                    if not self.lolos_filter(tanggal_bersih):
                        self.progress.emit(i + 1, total)
                        continue

                    data_bersih = {
                        "judul"   : data_mentah['judul'],
                        "tanggal" : tanggal_bersih or "",
                        "isi"     : data_mentah['isi'],
                        "url"     : data_mentah['url']
                    }

                    self.data_found.emit(data_bersih)

                except Exception as e:
                    print(f"[!] Gagal proses artikel: {e}")

                finally:
                    self.progress.emit(i + 1, total)

        except Exception as e:
            self.error.emit(str(e))

        finally:
            scraper.stop_engine()
            self.finished.emit()


# ==============================
# BLOK TESTING
# ==============================
if __name__ == "__main__":
    import sys
    from PyQt5.QtCore import QCoreApplication

    app = QCoreApplication(sys.argv)

    def tampilkan(data):
        print("\n✅ Data Bersih:")
        print(f"  Judul   : {data['judul']}")
        print(f"  Tanggal : {data['tanggal']}")
        print(f"  Isi     : {data['isi'][:150]}...")
        print(f"  URL     : {data['url']}")

    def progress(x, total):
        print(f"⏳ Progress: {x}/{total}")

    def selesai():
        print("\n🎉 Test selesai! Data siap dikirim ke Arsel & UI.")
        app.quit()

    def on_error(msg):
        print(f"❌ Error: {msg}")
        app.quit()

    processor = ScraperProcessor(
        url="https://news.detik.com",
        max_artikel=3
    )
    processor.data_found.connect(tampilkan)
    processor.progress.connect(progress)
    processor.finished.connect(selesai)
    processor.error.connect(on_error)
    processor.start()

    sys.exit(app.exec_())