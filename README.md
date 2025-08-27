# RAG Chatbot with Mistral AI

A simple Retrieval-Augmented Generation chatbot that allows users to upload PDF documents and ask intelligent questions about their content using Mistral AI.

## Features

- PDF document upload and text extraction
- Intelligent document chunking and retrieval
- Question answering powered by Mistral AI
- Interactive web interface with Streamlit
- Analytical responses for data-heavy documents

## Tech Stack

- **Framework**: Streamlit (Web Interface)
- **PDF Processing**: PyPDF (Document Loading)
- **LLM**: Mistral AI (mistral-small model)
- **Retrieval**: Keyword-based text search
- **API**: Direct Mistral API integration

## Setup Instructions

1. **Clone/Download the project**
   ```bash
   cd rag-chatbot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   - Create a `.env` file
   - Add your Mistral API key:
   ```
   MISTRAL_API_KEY=your_mistral_api_key_here
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

## Usage

1. Upload a PDF document using the sidebar
2. Wait for processing to complete
3. Ask questions about your document in the chat interface
4. Get intelligent, context-aware responses

## Example Queries

- "What is this document about?"
- "List the main topics covered"
- "Which course has the highest cost?" (for course catalogs)
- "Summarize the key findings"
- "What are the requirements mentioned?"

## Project Structure

```
rag-chatbot/
├── app.py               # Main Streamlit application
├── requirements.txt     # Python dependencies
├── .env                # Environment variables (API keys)
└── README.md           # This file
```

## How It Works

1. **Document Processing**: Extracts text from uploaded PDF
2. **Text Chunking**: Splits document into manageable chunks
3. **Query Processing**: Finds relevant chunks based on keyword matching
4. **Answer Generation**: Uses Mistral AI to generate contextual responses
5. **Interactive Interface**: Streamlit provides chat-like experience


## Limitations

- Currently supports PDF files only
- Retrieval based on keyword matching 
- Requires internet connection for Mistral API calls

## License

This project is for educational purposes.