import os
import shutil
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from src.utils import load_all_documents
from src.embeddings import get_embedding_model

CHROMA_PATH = "chroma_db"

def run_indexing():
    """
    Executes the full indexing pipeline:
    1. Load documents
    2. Split documents into chunks
    3. Generate embeddings and store in ChromaDB
    """
    print("--- Starting Indexing Pipeline ---")
    
    # 0. Clean old database
    if os.path.exists(CHROMA_PATH):
        print(f"Cleaning existing database at {CHROMA_PATH}...")
        shutil.rmtree(CHROMA_PATH)

    # 1. Load Documents
    documents = load_all_documents("data")
    if not documents:
        print("No documents found to index.")
        return

    # 2. Text Splitting
    # Requirements: chunk_size 2000 (optimized to reduce daily API quota usage)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=200,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

    # 3. Create Vector Store (ChromaDB)
    embeddings = get_embedding_model()
    
    print(f"Saving {len(chunks)} chunks to {CHROMA_PATH} in batches...")
    
    # Process in batches to avoid RateLimit (429)
    # Gemini Free Tier limit is 100 requests per minute
    batch_size = 20
    import time
    
    # Initialize the vector store with the first batch
    vector_store = Chroma.from_documents(
        documents=chunks[:batch_size],
        embedding=embeddings,
        persist_directory=CHROMA_PATH
    )
    
    # Add subsequent batches
    for i in range(batch_size, len(chunks), batch_size):
        print(f"Adding batch {i} to {i+batch_size}...")
        batch = chunks[i:i+batch_size]
        vector_store.add_documents(batch)
        print(f"Added {i+len(batch)} chunks total...")
        time.sleep(15) # Pause to stay below 100 RPM limit
    
    print("--- Indexing Completed Successfully ---")

if __name__ == "__main__":
    run_indexing()
