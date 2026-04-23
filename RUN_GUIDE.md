# 🚀 Panduan Menjalankan Proyek CACO (Career Consultant)

Ikuti langkah-langkah di bawah ini untuk menyiapkan lingkungan pengembangan (setup) dan menjalankan aplikasi RAG ini di komputer lokal Anda.

## 📋 Prasyarat
- **Python 3.9** atau versi yang lebih baru.
- **Google Gemini API Key** (Dapatkan di [Google AI Studio](https://aistudio.google.com/app/apikey)).

---

## 🛠️ Langkah-Langkah Instalasi

### 1. Clone Repositori
Buka terminal/command prompt dan clone proyek ini:
```bash
git clone https://github.com/Irham-Najib-Azimul-Qowi/rag-uts-kelompok_2-CAreer_COnsultant.git
cd rag-uts-kelompok_2-CAreer_COnsultant
```

### 2. Siapkan Virtual Environment
Gunakan virtual environment agar library proyek tidak mengganggu library sistem Anda.

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instal Dependencies
Instal semua library yang dibutuhkan dengan perintah berikut:
```bash
pip install -r requirements.txt
```

### 4. Konfigurasi API Key (.env)
1. Buat file baru bernama `.env` di folder root proyek (atau salin dari `.env.example`).
2. Tambahkan API Key Gemini Anda ke dalam file tersebut:
   ```env
   GEMINI_API_KEY=MASUKKAN_API_KEY_ANDA_DI_SINI
   GEMINI_MODEL=gemini-flash-latest
   ```

---

## 🏃 Cara Menjalankan

### Tahap 1: Indexing Data
Sebelum menggunakan chatbot, sistem perlu memproses dokumen (PDF, TXT, CSV) yang ada di folder `data/` ke dalam database vektor.
```bash
python -m src.indexing
```
*Tunggu hingga muncul pesan "Indexing Completed Successfully".*

### Tahap 2: Menjalankan UI Chatbot
Setelah indexing selesai, jalankan antarmuka chatbot menggunakan Streamlit:
```bash
streamlit run ui/app.py
```
Aplikasi akan secara otomatis terbuka di browser Anda (biasanya pada alamat `http://localhost:8501`).

---

## 📂 Struktur Folder Utama
- `data/`: Tempat menyimpan dokumen sumber (PDF, CSV, TXT).
- `src/`: Inti logika RAG (Indexing, Query, Utils).
- `ui/`: File tampilan antarmuka Streamlit.
- `chroma_db/`: Folder penyimpanan database vektor (terbuat otomatis setelah indexing).

## ⚠️ Tips Tambahan
- **Update Data**: Jika Anda menambahkan file baru ke folder `data/`, Anda harus menjalankan ulang perintah **Indexing Data** (Tahap 1).
- **Internet**: Pastikan koneksi internet aktif karena aplikasi ini menggunakan API Cloud dari Google Gemini.
