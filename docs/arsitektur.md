# Arsitektur Sistem CACO RAG 🎓

Sistem ini terdiri dari dua pipeline utama: Indexing (Offline) dan Query (Online).

## 1. Pipeline Indexing (Offline)
Pipeline ini bertanggung jawab untuk memproses dokumen sumber dan menyimpannya ke dalam Vector Database.

```mermaid
graph TD
    A[Dokumen: PDF/TXT] --> B[Document Loader]
    B --> C[Text Splitter: 2000 Chunks]
    C --> D[Embedding Model: gemini-embedding-001]
    D --> E[(Vector Store: ChromaDB)]
```

## 2. Pipeline Query (Online)
Pipeline ini menangani pertanyaan pengguna dengan menggabungkan konteks dokumen dan kemampuan LLM.

```mermaid
graph LR
    User[User Query] --> Embed[Embedding]
    Embed --> Search[Similarity Search]
    Search --> Store[(ChromaDB)]
    Store --> Context[Context Retrieval]
    Context --> Prompt[Augmented Prompt]
    Prompt --> LLM[LLM: Gemini 1.5 Flash]
    LLM --> Answer[Bot Answer]
    
    subgraph "Hybrid Feature"
    LLM -.-> Web[Web Search Retrieval]
    Web -.-> LLM
    end
```

## Komponen Utama
- **Framework**: LangChain
- **LLM**: Google Gemini 1.5 Flash
- **Vector DB**: ChromaDB
- **Embedding**: Google Generative AI Embeddings
- **Interface**: Streamlit
