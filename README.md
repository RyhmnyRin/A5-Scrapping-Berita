# Aplikasi Scraping Berita dengan GUI (PyQt + Selenium)

Aplikasi ini merupakan aplikasi desktop berbasis Python yang digunakan untuk melakukan web scraping berita dari sebuah halaman website. Pengguna dapat memasukkan link halaman berita (homepage atau halaman kategori), kemudian sistem akan mengambil seluruh link artikel yang tersedia pada halaman tersebut dan mengekstrak informasi penting dari setiap artikel.

Data yang diambil meliputi judul berita, tanggal berita (jika tersedia), dan isi berita. Seluruh hasil scraping kemudian akan ditampilkan dalam bentuk tabel pada GUI sehingga pengguna dapat melihat data secara langsung dengan tampilan yang terstruktur.

Aplikasi ini dibuat menggunakan PyQt untuk antarmuka pengguna (GUI) dan Selenium untuk melakukan proses web scraping. Dengan adanya GUI, proses scraping menjadi lebih mudah digunakan tanpa perlu menjalankan script melalui terminal.

## Fitur Utama
Aplikasi memiliki beberapa fitur utama sebagai berikut:

- Pengguna dapat memasukkan link halaman berita yang ingin di-scrape.
- Sistem akan mengambil seluruh link artikel dari halaman tersebut.
- Setiap artikel akan dibuka secara otomatis oleh sistem.
- Sistem akan mengambil data penting dari artikel yaitu:
  - Judul berita
  - Tanggal berita (jika tersedia)
  - Isi berita
- Hasil scraping akan ditampilkan dalam tabel pada aplikasi GUI.

## Fitur Tambahan
Untuk meningkatkan fungsi aplikasi, beberapa fitur tambahan juga diimplementasikan, yaitu:

- Limit jumlah berita yang ingin diambil agar proses scraping lebih cepat saat testing.
- Filter berita berdasarkan rentang tanggal (Start Date – End Date).
- Export hasil scraping ke dalam file CSV.
- Progress bar untuk menunjukkan perkembangan proses scraping.
- Status scraping yang menampilkan kondisi program.
- Log aktivitas yang menampilkan proses scraping yang sedang berjalan.
- Error handling agar aplikasi tidak mudah crash ketika terjadi kesalahan.

## Tampilan Aplikasi
Tampilan aplikasi dibagi menjadi beberapa bagian utama agar mudah digunakan oleh pengguna:

### 1. Pengaturan Scraping
Bagian ini digunakan untuk mengatur proses scraping, yang terdiri dari:
- Input Link Berita
- Limit jumlah berita
- Filter tanggal (Start Date dan End Date)
- Tombol Mulai Scraping
- Progress Bar Scraping 

### 2. Hasil Scraping
Bagian ini menampilkan data hasil scraping dalam bentuk tabel yang berisi:
- Judul berita
- Tanggal berita
- Isi berita
- URL berita

### 3. Export Data
Bagian ini menyediakan tombol untuk mengekspor hasil scraping ke file CSV.

### 4. Log Aktivitas
Bagian ini menampilkan aktivitas program selama proses scraping berlangsung, sehingga pengguna dapat mengetahui status yang sedang berjalan.

## Teknologi yang Digunakan
Beberapa teknologi yang digunakan dalam pembuatan aplikasi ini antara lain:

- Python sebagai bahasa pemrograman utama
- PyQt5 untuk membuat Graphical User Interface (GUI)
- Selenium untuk melakukan proses web scraping
- CSV untuk mengekspor data hasil scraping
- Threading untuk memastikan GUI tidak freeze saat proses scraping berlangsung

## Struktur Project
Struktur folder dalam project ini adalah sebagai berikut:

project-scraping/
├── main.py
├── gui/
│ ├── layout.ui
│ └── widgets.py
└── backend/
├── scraper.py
├── processor.py
└── exporter.py

Penjelasan struktur project:
- **main.py**  
  File utama yang digunakan untuk menjalankan aplikasi.

- **layout.ui**  
  File desain tampilan GUI yang dibuat menggunakan Qt Designer.

- **widgets.py**  
  File yang menghubungkan komponen GUI dengan logika program.

- **scraper.py**  
  File yang berisi fungsi untuk mengambil data dari website menggunakan Selenium.

- **processor.py**  
  File yang digunakan untuk memproses data hasil scraping sebelum ditampilkan.

- **exporter.py**  
  File yang digunakan untuk mengekspor data ke dalam file CSV.

## Pembagian Tugas Tim
Project ini dikerjakan secara berkelompok dengan pembagian tugas sebagai berikut:

### Frontend
- Tania Putri Ramadhani
- Jocelyn Christina Simamora
  
Tugas:
- Mendesain tampilan GUI menggunakan PyQt
- Membuat layout aplikasi menggunakan Qt Designer (`layout.ui`)
- Menata posisi dan struktur widget pada antarmuka
- Memberikan styling warna pada tampilan aplikasi
- Menghubungkan komponen GUI dengan fungsi program melalui `widgets.py`
  
### Web Scraper
- Muhammad Salman Al Farisi
- Muhammad Rafi Al Bani
  
Tugas:
- Mengembangkan sistem scraping menggunakan Selenium
- Mengambil data berita dari website
- Memproses data hasil scraping

### Backend
- Arsel Fahri Khadafi
  
Tugas:
- Menghubungkan backend dengan GUI
- Membuat fitur export data ke CSV
- Menjalankan sistem utama aplikasi

## Cara Menjalankan Program
Untuk menjalankan aplikasi ini, ikuti langkah-langkah berikut:

### 1. Install Python
Pastikan Python sudah terinstall di komputer.

### 2. Install Library yang Dibutuhkan
Jalankan perintah berikut pada terminal atau command prompt:
- pip install pyqt5
- pip install pyqt5-tools
- pip install selenium

### 3. Jalankan Program
Setelah semua library terinstall, jalankan program dengan perintah:
                      python main.py

Aplikasi GUI akan terbuka dan siap digunakan.

## Deadline Tugas
Sabtu, 7 Maret 2026  
Pukul 23.59 WIB

## Catatan
Aplikasi ini dibuat sebagai bagian dari tugas mata kuliah Web Scraping. Melalui project ini, mahasiswa dapat mempelajari konsep pengambilan data dari website, pembuatan GUI menggunakan PyQt, serta integrasi antara frontend dan backend dalam sebuah aplikasi Python.
