import streamlit as st
import sys
import os

# Add the root directory to sys.path so we can import from src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.query import query_rag

# Page config
st.set_page_config(
    page_title="CACO - Konsultan Karir Pintar",
    page_icon="🎓",
    layout="wide"
)

# Sidebar
with st.sidebar:
    st.title("Pengaturan")
    st.info("CACO adalah asisten virtual berbasis RAG yang memberikan bimbingan karir berdasarkan dokumen panduan dan data pasar kerja.")
    if st.button("Hapus Riwayat Chat"):
        st.session_state.messages = []
        st.rerun()

# Main UI
st.title("🎓 CACO: Career Consultant Intelligence")
st.subheader("Konsultasi karir untuk mahasiswa, fresh graduate, dan umum.")
st.markdown("---")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message:
            with st.expander("Lihat Sumber"):
                for source in message["sources"]:
                    st.write(f"- {source}")

# React to user input
if prompt := st.chat_input("Tanyakan sesuatu tentang rencana karir Anda..."):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Sedang berpikir..."):
            result = query_rag(prompt, chat_history=st.session_state.messages[:-1]) # Don't include the current prompt yet
            
            if "error" in result:
                st.error(f"Error: {result['error']}")
                response_content = f"Mohon maaf, terjadi kesalahan: {result['error']}"
            else:
                response_content = result["answer"]
                st.markdown(response_content)
                
                # Display sources
                if result.get("sources"):
                    with st.expander("Lihat Sumber Referensi"):
                        for src in result["sources"]:
                            st.write(f"- {os.path.basename(src)}")

    # Add assistant message to chat history
    message_data = {"role": "assistant", "content": response_content}
    if not result.get("error") and result.get("sources"):
        message_data["sources"] = [os.path.basename(s) for s in result["sources"]]
    st.session_state.messages.append(message_data)
