import os
import glob
import pandas as pd
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document

def load_all_documents(data_dir="data"):
    """
    Load PDF and TXT documents for theoretical knowledge.
    Excel/CSV logic is removed in favor of real-time Web Search.
    """
    from langchain_community.document_loaders import TextLoader
    documents = []
    
    # Load PDFs
    pdf_files = glob.glob(os.path.join(data_dir, "*.pdf"))
    for pdf in pdf_files:
        try:
            loader = PyPDFLoader(pdf)
            documents.extend(loader.load())
            print(f"Loaded PDF: {pdf}")
        except Exception as e:
            print(f"Error loading {pdf}: {e}")

    # Load TXTs
    txt_files = glob.glob(os.path.join(data_dir, "*.txt"))
    for txt in txt_files:
        try:
            loader = TextLoader(txt, encoding='utf-8')
            documents.extend(loader.load())
            print(f"Loaded TXT: {txt}")
        except Exception as e:
            print(f"Error loading {txt}: {e}")

    return documents

def format_prompt():
    """
    Returns a prompt template for the CACO Career Counseling RAG system in Indonesian.
    """
    template = """
    Anda adalah "CACO" (Career Consultant), asisten virtual cerdas yang ahli dalam bimbingan karir untuk mahasiswa, fresh graduate, dan masyarakat umum.
    Tugas Anda adalah memberikan saran karir yang profesional, empatik, dan aplikatif.

    Gunakan konteks di bawah ini untuk menjawab pertanyaan. Konteks ini mencakup:
    1. Panduan dan strategi karir dari dokumen PDF (untuk teknik dan cara).
    2. Hasil pencarian web terkini (untuk rekomendasi tempat, perusahaan, atau info pasar kerja Indonesia).

    Konteks:
    {context}

    Pertanyaan Pengguna: {question}

    Instruksi Jawaban (PENTING):
    1. Jawablah dalam Bahasa Indonesia yang santun namun profesional.
    2. Jika pengguna bertanya tentang rekomendasi tempat, lowongan kerja, atau perusahaan, gunakan fitur pencarian web untuk memberikan jawaban yang up-to-date di Indonesia.
    3. Jika pengguna bertanya tentang cara (misal: "bagaimana cara interview"), gunakan teknik dari dokumen PDF di konteks.
    4. Berikan langkah-langkah konkret (actionable steps) yang relevan untuk mahasiswa atau fresh graduate.
    5. Sebutkan sumber jika informasi berasal dari dokumen PDF atau hasil pencarian web.

    Jawaban CACO (Career Consultant):
    """
    return PromptTemplate(template=template, input_variables=["context", "question"])
