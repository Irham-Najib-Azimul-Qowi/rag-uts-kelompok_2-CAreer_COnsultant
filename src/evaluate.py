import os
import sys
import pandas as pd
import time

# Add the root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.query import query_rag
from dotenv import load_dotenv

load_dotenv()

def run_evaluation():
    """
    Automated evaluation of 10 core questions for the UTS project.
    Saves results to evaluation/hasil_evaluasi.xlsx
    """
    questions = [
        {"q": "Karir apa yang cocok untuk mahasiswa IT?", "ideal": "Mahasiswa IT cocok untuk Software Engineer, Data Scientist, atau Network Architect."},
        {"q": "Bagaimana menentukan minat karir?", "ideal": "Menggunakan tes minat, introspeksi passion, dan observasi aktivitas yang disukai."},
        {"q": "Apa langkah dalam konseling karir?", "ideal": "Identifikasi masalah, asesmen diri, eksplorasi karir, dan pengambilan keputusan."},
        {"q": "Apa itu RIASEC dalam konseling?", "ideal": "Model Holland yang membagi minat ke tipe Realistic, Investigative, Artistic, Social, Enterprising, dan Conventional."},
        {"q": "Mengapa penting memiliki tujuan karir?", "ideal": "Sebagai panduan arah hidup dan motivasi dalam pengembangan diri secara profesional."},
        {"q": "Apa peran konselor dalam pendidikan?", "ideal": "Membantu siswa memahami potensi diri dan memberikan opsi jalur pendidikan yang relevan."},
        {"q": "Bagaimana cara mengatasi keraguan karir?", "ideal": "Konsultasi dengan ahli, melakukan magang, dan riset mendalam tentang industri terkait."},
        {"q": "Apa bedanya minat dan bakat?", "ideal": "Minat adalah kecenderungan menyukai sesuatu, bakat adalah kemampuan alami yang menonjol."},
        {"q": "Apa tantangan utama karir di era digital?", "ideal": "Perubahan teknologi yang cepat dan kebutuhan untuk terus belajar (lifelong learning)."},
        {"q": "Bagaimana cara menyusun CV yang baik?", "ideal": "Fokus pada pencapaian, gunakan kata kerja aksi, dan sesuaikan dengan deskripsi pekerjaan."}
    ]

    results = []
    print(f"--- Starting Automated Evaluation (10 Questions) ---")
    
    for i, item in enumerate(questions):
        print(f"Processing Q{i+1}: {item['q']}")
        start_time = time.time()
        
        # Query the RAG system
        response = query_rag(item['q'])
        
        end_time = time.time()
        latency = round(end_time - start_time, 2)
        
        if "error" in response:
            answer = f"ERROR: {response['error']}"
            sources = ""
        else:
            answer = response['answer']
            sources = ", ".join([os.path.basename(s) for s in response.get('sources', [])])
        
        results.append({
            "No": i + 1,
            "Pertanyaan": item['q'],
            "Jawaban Ideal": item['ideal'],
            "Jawaban Sistem": answer,
            "Sumber": sources,
            "Latency (s)": latency,
            "Status": "Success" if "error" not in response else "Failed"
        })
        
        # Sleep to avoid rate limits
        time.sleep(2)

    # Save to Excel
    df = pd.DataFrame(results)
    output_path = os.path.join("evaluation", "hasil_evaluasi.xlsx")
    
    # Ensure directory exists
    os.makedirs("evaluation", exist_ok=True)
    
    try:
        df.to_excel(output_path, index=False)
        print(f"--- Evaluation Completed! Results saved to {output_path} ---")
    except Exception as e:
        # Fallback to CSV if Excel fails
        csv_path = output_path.replace(".xlsx", ".csv")
        df.to_csv(csv_path, index=False)
        print(f"--- Evaluation Completed! Results saved to {csv_path} (Excel write failed) ---")

if __name__ == "__main__":
    run_evaluation()
