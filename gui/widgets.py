import sys
import csv
from PyQt5 import uic
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableWidgetItem,
    QFileDialog,
    QMessageBox
)


dummy_data = [
    {
        "judul": "Berita Ekonomi Indonesia",
        "tanggal": "2026-03-07",
        "isi": "Perekonomian Indonesia menunjukkan pertumbuhan positif.",
        "url": "https://contoh.com/berita-ekonomi"
    },
    {
        "judul": "Teknologi AI Semakin Berkembang",
        "tanggal": "2026-03-06",
        "isi": "Banyak perusahaan mulai menggunakan AI untuk meningkatkan produktivitas.",
        "url": "https://contoh.com/teknologi-ai"
    },
    {
        "judul": "Cuaca Ekstrem di Beberapa Wilayah",
        "tanggal": "2026-03-05",
        "isi": "BMKG mengingatkan masyarakat untuk waspada terhadap cuaca ekstrem.",
        "url": "https://contoh.com/cuaca-ekstrem"
    }
]


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("gui/layout.ui", self)

        self.hasil_scraping = []

        self.btnScrape.clicked.connect(self.start_scraping)
        self.btnExportCSV.clicked.connect(self.export_csv)

        self.progressBar.setValue(0)
        self.set_status("Menunggu scraping...")

    def set_status(self, text):
        self.statusScraping.setText(f"Status : {text}")

    def add_log(self, message):
        self.logBox.appendPlainText(message)

    def reset_ui(self):
        self.tableWidget.setRowCount(0)
        self.progressBar.setValue(0)
        self.logBox.setPlainText("")
        self.hasil_scraping = []

    def update_progress(self, current, total):
        if total > 0:
            persen = int((current / total) * 100)
        else:
            persen = 0
        self.progressBar.setValue(persen)

    def tambah_ke_tabel(self, berita):
        row_position = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_position)

        self.tableWidget.setItem(row_position, 0, QTableWidgetItem(berita["judul"]))
        self.tableWidget.setItem(row_position, 1, QTableWidgetItem(berita["tanggal"]))
        self.tableWidget.setItem(row_position, 2, QTableWidgetItem(berita["isi"]))

    def start_scraping(self):
        link = self.inputLink.text().strip()
        limit = self.limitNews.value()
        start_date = self.StarDateEdit.date().toString("yyyy-MM-dd")
        end_date = self.EndDateEdit.date().toString("yyyy-MM-dd")

        if not link:
            QMessageBox.warning(self, "Peringatan", "Link berita harus diisi dulu ya.")
            return

        self.reset_ui()
        self.set_status("Scraping berjalan...")

        self.add_log("Memulai proses scraping...")
        self.add_log(f"Link: {link}")
        self.add_log(f"Limit berita: {limit}")
        self.add_log(f"Start date: {start_date}")
        self.add_log(f"End date: {end_date}")

        data_aktif = dummy_data[:limit]
        total = len(data_aktif)

        if total == 0:
            self.add_log("Tidak ada data yang bisa ditampilkan.")
            self.set_status("Tidak ada data")
            return

        for i, berita in enumerate(data_aktif, start=1):
            self.hasil_scraping.append(berita)
            self.tambah_ke_tabel(berita)
            self.update_progress(i, total)
            self.add_log(f"Berita ke-{i} berhasil dimasukkan")

        self.add_log("Proses selesai.")
        self.set_status("Scraping selesai")

    def export_csv(self):
        if not self.hasil_scraping:
            QMessageBox.information(self, "Info", "Belum ada data untuk diexport.")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Simpan Hasil Scraping",
            "hasil_scraping.csv",
            "CSV Files (*.csv)"
        )

        if not file_path:
            return

        try:
            with open(file_path, mode="w", newline="", encoding="utf-8-sig") as file:
                writer = csv.DictWriter(file, fieldnames=["judul", "tanggal", "isi", "url"])
                writer.writeheader()
                writer.writerows(self.hasil_scraping)

            self.add_log(f"Data berhasil diexport ke: {file_path}")
            QMessageBox.information(self, "Berhasil", "File CSV berhasil disimpan.")
            self.set_status("Export CSV berhasil")

        except Exception as e:
            self.add_log(f"Error export CSV: {str(e)}")
            QMessageBox.critical(self, "Error", f"Gagal export CSV:\n{str(e)}")
            self.set_status("Export CSV gagal")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())