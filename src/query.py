import os
import json
from google import genai
from google.genai import types
from langchain_chroma import Chroma
from src.embeddings import get_embedding_model
from src.utils import format_prompt
from dotenv import load_dotenv

load_dotenv()
CHROMA_PATH = "chroma_db"

def get_rag_context(query_text):
    """
    Retrieve context from ChromaDB.
    """
    embeddings = get_embedding_model()
    
    if not os.path.exists(CHROMA_PATH):
        raise FileNotFoundError(f"Vector store not found at {CHROMA_PATH}.")

    vector_store = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings
    )
    
    # Similarity Search
    results = vector_store.similarity_search_with_relevance_scores(query_text, k=5)
    context_text = "\n\n---\n\n".join([doc.page_content for doc, score in results])
    sources = list(set([doc.metadata.get("source", "Unknown") for doc, score in results]))
    
    return context_text, sources

def query_rag(query_text, chat_history=None):
    """
    Main query pipeline using the latest google-genai SDK.
    Supports chat history for context-aware responses.
    """
    try:
        # 1. Get Context (R)
        context_text, sources = get_rag_context(query_text)
        
        # 2. Construct Prompt (A)
        prompt_template = format_prompt()
        prompt = prompt_template.format(context=context_text, question=query_text)
        
        # 3. Load Web Config
        config_path = os.path.join("data", "web_config.json")
        web_tools = []
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                web_config = json.load(f)
                if web_config.get("use_web_search"):
                    web_tools.append(types.Tool(google_search_retrieval=types.GoogleSearchRetrieval()))
        
        # 4. Generate Answer (G)
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
        
        # Format history for Gemini API if provided
        contents = []
        if chat_history:
            for msg in chat_history:
                role = "user" if msg["role"] == "user" else "model"
                contents.append(types.Content(role=role, parts=[types.Part.from_text(text=msg["content"])]))
        
        # Add the current prompt
        contents.append(types.Content(role="user", parts=[types.Part.from_text(text=prompt)]))
        
        response = client.models.generate_content(
            model=model_name,
            contents=contents,
            config=types.GenerateContentConfig(
                tools=web_tools if web_tools else None
            )
        )
        
        return {
            "answer": response.text,
            "context": context_text,
            "sources": sources
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Test query
    test_query = "Bagaimana menentukan minat karir?"
    print(f"Query: {test_query}")
    result = query_rag(test_query)
    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print(f"Answer: {result['answer']}")
        print(f"Sources: {result['sources']}")
