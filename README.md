# CAreer-COnsultant (CACO) RAG System 🎓

A Retrieval-Augmented Generation (RAG) system specialized for **Career Counseling in Education**. This system uses Google Gemini as the core Large Language Model and ChromaDB for local vector storage, providing accurate answers based on career guidance handbooks and documents.

---

## 🏗️ Architecture

The system is built on two primary pipelines:

### 1. Indexing Pipeline (`src/indexing.py`)
- **Document Loading**: Loads PDF and CSV documents from the `data/` directory using LangChain's `PyPDFLoader` and `CSVLoader`.
- **Text Splitting**: Breaks documents into manageable chunks (800-1000 characters with 100-200 overlap) to preserve context.
- **Embedding Generation**: Converts text chunks into high-dimensional vectors using Google's `embedding-001` model.
- **Vector Storage**: Persists these embeddings in a local **ChromaDB** instance for efficient similarity searching.

### 2. Query Pipeline (`src/query.py`)
- **Input Transformation**: User queries are embedded using the same embedding model.
- **Similarity Search**: Retrieves the top 5 most relevant document chunks from ChromaDB.
- **Chat History**: Supports multi-turn conversation by passing previous messages to the LLM.
- **Generation**: Uses **Gemini 1.5 Flash** with optional **Google Search Grounding** for real-time data.

---

## 🛠️ Tech Stack Justification

| Technology | Reason for Choice |
| :--- | :--- |
| **Python** | Industry standard for AI/ML and RAG orchestration. |
| **LangChain** | Provides a robust framework for chaining LLM components and document loaders. |
| **ChromaDB** | A lightweight, local vector database that allows persistence without external infrastructure. |
| **Google Gemini API** | Offers high-performance language modeling and efficient embedding at a competitive speed. |
| **Streamlit** | Enables rapid development of a clean, interactive user interface. |

---

## 🚀 Installation & Setup

### 1. Pre-requisites
- Python 3.9+
- [Google Gemini API Key](https://aistudio.google.com/app/apikey)

### 2. Clone and Setup
```bash
# Clone the repository
git clone https://github.com/Irham-Najib-Azimul-Qowi/rag-uts-kelompok_2-CAreer_COnsultant.git
cd rag-uts-kelompok_2-CAreer_COnsultant

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_actual_api_key_here
```

---

## 🏃 How to Run

### Step 1: Run Indexing
Sebelum bertanya, sistem harus memproses dokumen ke dalam Vector DB.
```bash
python src/indexing.py
```

### Step 2: Launch the App
Akses Chatbot UI berbasis Streamlit.
```bash
streamlit run ui/app.py
```

### Step 3: Run Evaluation (Automated)
Melakukan pengujian otomatis terhadap 10 pertanyaan inti.
```bash
python src/evaluate.py
```

---

## 🧪 Evaluation Format

The system's performance can be evaluated using the following 10 questions. Results are stored in `evaluation/hasil_evaluasi.xlsx` (placeholder).

| No | Question | Ideal Answer |
| :-- | :--- | :--- |
| 1 | Karir apa yang cocok untuk mahasiswa IT? | Mahasiswa IT cocok untuk Software Engineer, Data Scientist, atau Network Architect. |
| 2 | Bagaimana menentukan minat karir? | Menggunakan tes minat, introspeksi passion, dan observasi aktivitas yang disukai. |
| 3 | Apa langkah dalam konseling karir? | Identifikasi masalah, asesmen diri, eksplorasi karir, dan pengambilan keputusan. |
| 4 | Apa itu RIASEC dalam konseling? | Model Holland yang membagi minat ke tipe Realistic, Investigative, Artistic, Social, Enterprising, dan Conventional. |
| 5 | Mengapa penting memiliki tujuan karir? | Sebagai panduan arah hidup dan motivasi dalam pengembangan diri secara profesional. |
| 6 | Apa peran konselor dalam pendidikan? | Membantu siswa memahami potensi diri dan memberikan opsi jalur pendidikan yang relevan. |
| 7 | Bagaimana cara mengatasi keraguan karir? | Konsultasi dengan ahli, melakukan magang, dan riset mendalam tentang industri terkait. |
| 8 | Apa bedanya minat dan bakat? | Minat adalah kecenderungan menyukai sesuatu, bakat adalah kemampuan alami yang menonjol. |
| 9 | Apa tantangan utama karir di era digital? | Perubahan teknologi yang cepat dan kebutuhan untuk terus belajar (lifelong learning). |
| 10 | Bagaimana cara menyusun CV yang baik? | Fokus pada pencapaian, gunakan kata kerja aksi, dan sesuaikan dengan deskripsi pekerjaan. |

---

## 📄 Project Structure
*   `data/`: Source documents (PDF/CSV).
*   `src/`: Core logic (Indexing, Query, Embeddings, Utils).
*   `ui/`: User Interface (Streamlit).
*   `docs/`: Documentation and architecture diagrams.
*   `evaluation/`: Evaluation metrics and results.
*   `chroma_db/`: Vector database storage (auto-generated).

---

## ⚠️ Constraints
- The system will only answer based on documents in the `data/` folder.
- Does not answer out-of-scope general knowledge queries.
- Requires internet connection for Gemini API.
