import streamlit as st
import requests
import json
from pypdf import PdfReader
import re
import os
from dotenv import load_dotenv

load_dotenv()

st.title("📚 RAG-Powered PDF Chatbot")

# Sidebar for file upload
st.sidebar.header("Upload Document")
uploaded_file = st.sidebar.file_uploader("Choose a PDF file", type="pdf")

# Initialize session state
if "document_text" not in st.session_state:
    st.session_state.document_text = ""
if "messages" not in st.session_state:
    st.session_state.messages = []

def extract_text_from_pdf(pdf_file):
    """Extract text from PDF"""
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def find_relevant_chunks(text, query, chunk_size=1000):
    """Simple text search to find relevant chunks"""
    # Split text into chunks
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size//5):  # Overlap
        chunk = " ".join(words[i:i+chunk_size//5])
        chunks.append(chunk)
    
    # Find chunks containing query words
    query_words = query.lower().split()
    relevant_chunks = []
    
    for chunk in chunks:
        chunk_lower = chunk.lower()
        score = sum(1 for word in query_words if word in chunk_lower)
        if score > 0:
            relevant_chunks.append((chunk, score))
    
    # Sort by relevance and return top 3
    relevant_chunks.sort(key=lambda x: x[1], reverse=True)
    return [chunk[0] for chunk in relevant_chunks[:3]]

def call_mistral_api(context, question):
    """Call Mistral API for answer generation"""
    api_key = os.getenv("MISTRAL_API_KEY")
    
    prompt = f"""Answer the question based on the context below. Be specific and analytical.

Context: {context}

Question: {question}

Answer:"""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "mistral-small",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1,
        "max_tokens": 500
    }
    
    try:
        response = requests.post(
            "https://api.mistral.ai/v1/chat/completions",
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error calling Mistral API: {str(e)}"

# Process uploaded file
if uploaded_file:
    with st.spinner("Processing document..."):
        st.session_state.document_text = extract_text_from_pdf(uploaded_file)
        st.success(f"Document '{uploaded_file.name}' processed!")

# Chat interface
if st.session_state.document_text:
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask a question about your document"):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # Find relevant chunks
                relevant_chunks = find_relevant_chunks(st.session_state.document_text, prompt)
                context = "\n\n".join(relevant_chunks)
                
                # Get answer from Mistral
                response = call_mistral_api(context, prompt)
                st.markdown(response)
        
        # Add assistant message
        st.session_state.messages.append({"role": "assistant", "content": response})
else:
    st.info("Please upload a PDF document to start chatting!")

    