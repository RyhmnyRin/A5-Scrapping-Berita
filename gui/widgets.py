import os
import sys
from datetime import datetime, time

from PyQt5 import uic
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import (
    QApplication,
    QFrame,
    QFileDialog,
    QMainWindow,
    QMessageBox,
    QScrollArea,
    QTableWidgetItem,
)

from backend.exporter import DataExporter
from backend.processor import ScraperProcessor

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ui_path = os.path.join(base_dir, "gui", "layout.ui")
        uic.loadUi(ui_path, self)

        # Allow scrolling when window height is smaller than UI content.
        self._enable_vertical_scroll()

        self.scraped_data = []
        self.processor = None

        self._set_default_date_range()

        self.btnScrape.clicked.connect(self.start_scraping)
        self.btnExportCSV.clicked.connect(self.export_csv)

        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(["Judul Berita", "Tanggal", "Isi Berita", "URL"])
        self.progressBar.setValue(0)
        self.progressBar.setMaximum(100)
        self.logBox.setReadOnly(True)
        self.statusScraping.setText("Status: Menunggu scraping...")

    def _enable_vertical_scroll(self):
        content_widget = self.takeCentralWidget()
        if content_widget is None:
            return

        # layout.ui uses absolute geometry, so infer the full content size
        # from children bounds to make scrollbars appear reliably.
        content_rect = content_widget.childrenRect()
        content_widget.setMinimumSize(content_rect.right() + 20, content_rect.bottom() + 20)

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(False)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setWidget(content_widget)
        self.setCentralWidget(scroll_area)

    def _set_default_date_range(self):
        today = QDate.currentDate()
        self.StarDateEdit.setDate(today)
        self.EndDateEdit.setDate(today)

    def _log(self, message):
        self.logBox.appendPlainText(message)

    def start_scraping(self):
        url = self.inputLink.text().strip()
        if not url:
            QMessageBox.warning(self, "Input Tidak Valid", "Masukkan link website berita terlebih dahulu.")
            return

        max_artikel = self.limitNews.value()

        start_qdate = self.StarDateEdit.date().toPyDate()
        end_qdate = self.EndDateEdit.date().toPyDate()
        start_date = datetime.combine(start_qdate, time.min)
        end_date = datetime.combine(end_qdate, time.max)

        if start_date > end_date:
            QMessageBox.warning(self, "Filter Tanggal", "Start Date tidak boleh lebih besar dari End Date.")
            return

        self.scraped_data = []
        self.tableWidget.setRowCount(0)
        self.progressBar.setValue(0)
        self.statusScraping.setText("Status: Sedang scraping...")
        self.btnScrape.setEnabled(False)
        self.btnExportCSV.setEnabled(False)

        self._log(f"Memulai scraping: {url} (limit {max_artikel})")

        self.processor = ScraperProcessor(
            url=url,
            max_artikel=max_artikel,
            start_date=start_date,
            end_date=end_date,
        )
        self.processor.data_found.connect(self.on_data_found)
        self.processor.progress.connect(self.on_progress)
        self.processor.error.connect(self.on_error)
        self.processor.finished.connect(self.on_finished)
        self.processor.start()

    def on_data_found(self, article):
        self.scraped_data.append(article)

        row = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row)
        self.tableWidget.setItem(row, 0, QTableWidgetItem(article.get("judul", "")))
        self.tableWidget.setItem(row, 1, QTableWidgetItem(article.get("tanggal", "")))
        self.tableWidget.setItem(row, 2, QTableWidgetItem(article.get("isi", "")))
        self.tableWidget.setItem(row, 3, QTableWidgetItem(article.get("url", "")))

    def on_progress(self, current, total):
        if total > 0:
            percent = int((current / total) * 100)
            self.progressBar.setValue(percent)
        self.statusScraping.setText(f"Status: Proses {current}/{total}")

    def on_error(self, message):
        self._log(f"Error: {message}")
        self.statusScraping.setText("Status: Gagal")
        QMessageBox.critical(self, "Scraping Gagal", message)

    def on_finished(self):
        self.btnScrape.setEnabled(True)
        self.btnExportCSV.setEnabled(True)
        self.progressBar.setValue(100)
        self.statusScraping.setText(
            f"Status: Selesai ({len(self.scraped_data)} artikel lolos filter)"
        )
        self._log(f"Scraping selesai. Data terkumpul: {len(self.scraped_data)} artikel.")

    def export_csv(self):
        default_name = "hasil_scraping.csv"
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Simpan CSV",
            default_name,
            "CSV Files (*.csv)",
        )

        if not filename:
            return

        success, message = DataExporter.export_to_csv(self.scraped_data, filename)
        if success:
            self._log(message)
            QMessageBox.information(self, "Export Berhasil", message)
        else:
            self._log(message)
            QMessageBox.warning(self, "Export Gagal", message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())