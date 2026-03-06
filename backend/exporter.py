# backend/exporter.py

import csv
import os

class DataExporter:
    @staticmethod
    def _clean_text(value):
        """Ubah nilai jadi string satu baris agar sel CSV lebih rapi di Excel."""
        if value is None:
            return ""

        text = str(value)
        return " ".join(text.replace("\r", " ").replace("\n", " ").split())

    @staticmethod
    def export_to_csv(data_list, filename="hasil_scraping.csv"):
        """
        Fungsi untuk menyimpan list of dictionaries ke dalam file CSV.
        Mengembalikan True jika berhasil, False jika gagal.
        """
        # Kontrak data backend (lihat scraper.py dan processor.py)
        expected_headers = ["judul", "tanggal", "isi", "url"]

        # Cek apakah datanya kosong
        if not data_list:
            return False, "Data kosong, tidak ada yang bisa diekspor."

        if not isinstance(data_list, list):
            return False, "Format data tidak valid. Data harus berupa list of dict."
        
        try:
            # Normalisasi agar semua row punya key yang sama dan urutan stabil
            normalized_rows = []
            for item in data_list:
                if not isinstance(item, dict):
                    continue

                normalized_rows.append({
                    "judul": DataExporter._clean_text(item.get("judul", "")),
                    "tanggal": DataExporter._clean_text(item.get("tanggal", "")),
                    "isi": DataExporter._clean_text(item.get("isi", "")),
                    "url": DataExporter._clean_text(item.get("url", ""))
                })

            if not normalized_rows:
                return False, "Tidak ada data valid untuk diekspor."

            # Membuka/membuat file CSV baru
            with open(filename, mode='w', newline='', encoding='utf-8-sig') as csv_file:
                # Delimiter ';' lebih kompatibel untuk Excel dengan regional Indonesia.
                writer = csv.DictWriter(csv_file, fieldnames=expected_headers, delimiter=';')
                
                # Tulis baris pertama (Judul Kolom)
                writer.writeheader()
                
                # Tulis seluruh isi berita sekaligus
                writer.writerows(normalized_rows)
            
            # Ambil lokasi file absolut agar mudah dicari jika sukses
            file_path = os.path.abspath(filename)
            return True, f"Data berhasil disimpan di: {file_path}"
            
        except Exception as e:
            return False, f"Terjadi kesalahan saat menyimpan file: {str(e)}"